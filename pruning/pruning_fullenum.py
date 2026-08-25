import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Full-enumeration pruning: score all 3^s candidates via batched forward
passes, keep top keep_fraction, compare recall/speedup against the
same bucket sample as the earlier greedy runs.
"""
import ast
import pickle
import time
import itertools
import torch
import gurobipy as gp

from pruning import (
    load_lp_files, parse_scenario_x_tuples, write_reduced_lp,
    load_scoring_net, build_feature_tensors, DEVICE,
)
from blo.data_preprocessor.watwa import WatwaDataPreprocessor

CKPT_PATH = "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7_FULLDECAY_VERIFIED_20260813_1245.pt"
EVAL_PATH = "data/watwa/results/batch_eval_watwa_v7.pkl"
KEEP_FRACTIONS = [0.01, 0.05, 0.10]
N_INSTANCES_PER_BUCKET = 25
BATCH_SIZE = 4096

BUCKETS = [(100, 1000), (1000, 10000), (10000, float("inf"))]


def build_feature_tensors_batch(pml_feats, x_list, s):
    import numpy as np
    inst_row = []
    for pf in pml_feats:
        inst_row.append([
            pf["time_ns_high"] / 1e6, pf["time_ns_low"] / 1e6,
            pf["power_nw_high"] / 1e9, pf["power_nw_low"] / 1e9,
            pf["energy_high"] / 1e15, pf["energy_low"] / 1e15,
            pf["energy_ratio"], pf["time_ratio"] / 100.0,
            pf["is_uart"], pf["loop_bound"] / 2500,
            pf["position_norm"], pf["position_abs"] / 20,
            pf["tc_ratio_x1"], pf["tc_ratio_x2"], s / 20,
        ])
    inst_row = np.array(inst_row, dtype=np.float32)

    B = len(x_list)
    inst_batch = np.broadcast_to(inst_row, (B, s, 15)).copy()
    dec_batch = np.zeros((B, s, 5), dtype=np.float32)

    for b, x in enumerate(x_list):
        for i in range(s):
            xi = int(x[i])
            tc = pml_feats[i]["transition_costs"][xi]
            dec_batch[b, i, xi] = 1.0
            dec_batch[b, i, 3] = tc["time_ns"] / 1e6
            dec_batch[b, i, 4] = tc["power_nw"] / 1e9

    return torch.from_numpy(inst_batch).to(DEVICE), torch.from_numpy(dec_batch).to(DEVICE)


def score_all_candidates_batched(net, pml_feats, s, batch_size=BATCH_SIZE):
    all_x = list(itertools.product(range(3), repeat=s))
    results = []
    for i in range(0, len(all_x), batch_size):
        chunk = all_x[i:i + batch_size]
        inst_t, dec_t = build_feature_tensors_batch(pml_feats, chunk, s)
        x_dummy = torch.zeros((len(chunk), s), dtype=torch.float32, device=DEVICE)
        p_dummy = torch.zeros((len(chunk), 1), dtype=torch.float32, device=DEVICE)
        with torch.no_grad():
            preds = net(inst_t, dec_t, x_dummy, p_dummy, None)
        results.extend(zip(chunk, preds.squeeze(-1).tolist()))
    return results


def prune_top_k_percent(net, pml_feats, s, keep_fraction):
    scored = score_all_candidates_batched(net, pml_feats, s)
    scored.sort(key=lambda t: t[1])
    n_keep = max(1, int(len(scored) * keep_fraction))
    return [x for x, _ in scored[:n_keep]]


def solve_multi_scenario(lp_path):
    model = gp.read(lp_path)
    model.setParam("OutputFlag", 0)
    model.optimize()
    n = model.NumScenarios
    best_obj = None
    for i in range(n):
        model.Params.ScenarioNumber = i
        obj = model.ScenNObjVal
        if best_obj is None or obj < best_obj:
            best_obj = obj
    return best_obj, model.Runtime

def solve_multi_scenario_timed(lp_path):
    t0 = time.time()
    model = gp.read(lp_path)
    model.setParam("OutputFlag", 0)
    t1 = time.time()
    model.optimize()
    t2 = time.time()
    n = model.NumScenarios
    best_obj = None
    for i in range(n):
        model.Params.ScenarioNumber = i
        obj = model.ScenNObjVal
        if best_obj is None or obj < best_obj:
            best_obj = obj
    t3 = time.time()
    print(f"    [timing] read={t1-t0:.3f}s optimize={t2-t1:.3f}s readback={t3-t2:.3f}s (n_scenarios={n})")
    runtime = model.Runtime
    model.dispose()
    return best_obj, runtime


def main():
    with open(EVAL_PATH, "rb") as f:
        eval_results = pickle.load(f)

    net = load_scoring_net(CKPT_PATH)
    dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both", device=DEVICE)

    per_instance_rows = []

    for lo, hi in BUCKETS:
        in_bucket = [r for r in eval_results if lo <= r["num_scenarios"] < hi]
        in_bucket.sort(key=lambda r: r["num_scenarios"])
        step = max(1, len(in_bucket) // N_INSTANCES_PER_BUCKET)
        sample = in_bucket[::step][:N_INSTANCES_PER_BUCKET]

        for r in sample:
            pdir = r["program_dir"]
            s = r["s"]
            true_x = ast.literal_eval(r["opt_scenario"]) if isinstance(r["opt_scenario"], str) else tuple(r["opt_scenario"])
            opt_energy = r["opt_energy"]

            try:
                preamble, scenario_blocks = load_lp_files(pdir)
            except FileNotFoundError:
                continue

            x_tuples = parse_scenario_x_tuples(scenario_blocks, s)
            pml_feats = dp._parse_pml_features({"program_dir": pdir})
            x_to_id = {v: k for k, v in x_tuples.items()}

            for kf in KEEP_FRACTIONS:
                kept = prune_top_k_percent(net, pml_feats, s, kf)
                recall = true_x in kept
                keep_ids = [x_to_id[x] for x in kept if x in x_to_id]

                out_path = f"/tmp/{pdir.split('/')[-1]}_fe_{kf}.lp"
                write_reduced_lp(preamble, scenario_blocks, keep_ids, out_path)
                print(f"    [debug] out_path={out_path!r} len={len(out_path)} kept_n={len(keep_ids)}")

                t0 = time.time()
                best_obj, _ = solve_multi_scenario_timed(out_path)
                t_pruned = time.time() - t0
                gap = (best_obj - opt_energy) / opt_energy * 100

                per_instance_rows.append({
                    "program_dir": pdir, "bucket": (lo, hi), "num_scenarios": r["num_scenarios"],
                    "s": s, "keep_fraction": kf, "kept_n": len(keep_ids), "recall": recall,
                    "gap_pct": gap, "t_pruned": t_pruned, "t_full": r["watwaos_time"],
                })

    with open("pruning_fullenum_results.pkl", "wb") as f:
        pickle.dump(per_instance_rows, f)

    print(f"{'bucket':<16}{'keep%':>7}{'n':>5}{'recall%':>10}{'mean_kept_n':>14}{'mean_speedup':>14}{'median_speedup':>16}")
    for lo, hi in BUCKETS:
        for kf in KEEP_FRACTIONS:
            rows = [r for r in per_instance_rows if r["bucket"] == (lo, hi) and r["keep_fraction"] == kf]
            if not rows:
                continue
            n = len(rows)
            recall_pct = sum(r["recall"] for r in rows) / n * 100
            mean_kept_n = sum(r["kept_n"] for r in rows) / n
            speedups = [r["t_full"] / r["t_pruned"] if r["t_pruned"] > 0 else float("inf") for r in rows]
            speedups_sorted = sorted(speedups)
            mean_sp = sum(speedups) / n
            median_sp = speedups_sorted[n // 2]
            label = f"[{lo}-{hi if hi < float('inf') else 'inf'}]"
            print(f"{label:<16}{kf*100:>6.0f}%{n:>5}{recall_pct:>10.1f}{mean_kept_n:>14.1f}{mean_sp:>14.1f}x{median_sp:>16.1f}x")


if __name__ == "__main__":
    main()