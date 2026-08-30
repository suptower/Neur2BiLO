"""
Full-enumeration candidate pruning: scores all 3^s candidates using the surrogate
model, retains the top-k fraction, and evaluates recall and speedup against full
multi-scenario MILP solves across complexity buckets.
"""

import ast
import itertools
import os
import pickle
import sys
import tempfile
import time

import gurobipy as gp
import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from pruning.pruning import (
    DEVICE,
    load_lp_files,
    load_scoring_net,
    parse_scenario_x_tuples,
    write_reduced_lp,
)

# Configuration and Paths
CKPT_PATH = (
    "data/watwa/checkpoints_archive/20260824_relu/"
    "nn_inst_encoder_bs128_lr00025_layernorm1_besttop1-0.130_"
    "finalep213_hitrate19.1pct_20260824_0923.pt"
)
EVAL_PATH = "data/watwa/results/batch_eval_no_gurobi_watwa_v7.pkl"
RESULTS_OUT_PATH = "pruning_fullenum_results.pkl"

BUCKETS = [
    (1, 10),
    (10, 100),
    (100, 1000),
    (1000, 10000),
    (10000, float("inf")),
]

# Keep fractions per bucket: the largest complexity bucket is evaluated on smaller
# fractions (1%, 5%, 10%) where multi-scenario pruning remains runtime-effective.
KEEP_FRACTIONS_BY_BUCKET = {
    (1, 10): [0.01, 0.05, 0.10, 0.15, 0.20, 0.25],
    (10, 100): [0.01, 0.05, 0.10, 0.15, 0.20, 0.25],
    (100, 1000): [0.01, 0.05, 0.10, 0.15, 0.20, 0.25],
    (1000, 10000): [0.01, 0.05, 0.10, 0.15, 0.20, 0.25],
    (10000, float("inf")): [0.01, 0.05, 0.10],
}

N_INSTANCES_PER_BUCKET = None  # None evaluates all instances in each bucket
BATCH_SIZE = 4096
VERBOSE = False


def build_feature_tensors_batch(pml_feats, x_list, s):
    """Constructs batched instance and decision tensors for candidate evaluation."""
    inst_row = [
        [
            pf["time_ns_high"] / 1e6,
            pf["time_ns_low"] / 1e6,
            pf["power_nw_high"] / 1e9,
            pf["power_nw_low"] / 1e9,
            pf["energy_high"] / 1e15,
            pf["energy_low"] / 1e15,
            pf["energy_ratio"],
            pf["time_ratio"] / 100.0,
            pf["is_uart"],
            pf["loop_bound"] / 2500,
            pf["position_norm"],
            pf["position_abs"] / 20,
            pf["tc_ratio_x1"],
            pf["tc_ratio_x2"],
            s / 20,
        ]
        for pf in pml_feats
    ]
    inst_row = np.array(inst_row, dtype=np.float32)

    batch_size = len(x_list)
    inst_batch = np.broadcast_to(inst_row, (batch_size, s, 15)).copy()
    dec_batch = np.zeros((batch_size, s, 5), dtype=np.float32)

    for b, x in enumerate(x_list):
        for i in range(s):
            xi = int(x[i])
            tc = pml_feats[i]["transition_costs"][xi]
            dec_batch[b, i, xi] = 1.0
            dec_batch[b, i, 3] = tc["time_ns"] / 1e6
            dec_batch[b, i, 4] = tc["power_nw"] / 1e9

    return torch.from_numpy(inst_batch).to(DEVICE), torch.from_numpy(dec_batch).to(DEVICE)


def score_all_candidates_batched(net, pml_feats, s, batch_size=BATCH_SIZE):
    """Scores all 3^s candidate decision scenarios in mini-batches."""
    all_x = list(itertools.product(range(3), repeat=s))
    results = []

    for i in range(0, len(all_x), batch_size):
        chunk = all_x[i : i + batch_size]
        inst_t, dec_t = build_feature_tensors_batch(pml_feats, chunk, s)
        x_dummy = torch.zeros((len(chunk), s), dtype=torch.float32, device=DEVICE)
        p_dummy = torch.zeros((len(chunk), 1), dtype=torch.float32, device=DEVICE)

        with torch.no_grad():
            preds = net(inst_t, dec_t, x_dummy, p_dummy, None)

        results.extend(zip(chunk, preds.squeeze(-1).tolist()))

    return results


def prune_top_k_percent(net, pml_feats, s, keep_fraction):
    """Returns top-k candidate configurations based on surrogate model scores."""
    scored = score_all_candidates_batched(net, pml_feats, s)
    scored.sort(key=lambda t: t[1])
    n_keep = max(1, int(len(scored) * keep_fraction))
    return [x for x, _ in scored[:n_keep]]


def solve_multi_scenario_timed(lp_path):
    """Solves a multi-scenario LP file and records stage breakdown and solve runtime."""
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

    if VERBOSE:
        print(
            f"    [timing] read={t1-t0:.3f}s optimize={t2-t1:.3f}s "
            f"readback={t3-t2:.3f}s (n_scenarios={n})"
        )

    runtime = model.Runtime
    model.dispose()
    return best_obj, runtime


def main():
    with open(EVAL_PATH, "rb") as f:
        eval_results = pickle.load(f)

    net = load_scoring_net(CKPT_PATH)
    dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both", device=DEVICE)

    per_instance_rows = []
    temp_dir = tempfile.gettempdir()

    for lo, hi in BUCKETS:
        in_bucket = [r for r in eval_results if lo <= r["num_scenarios"] < hi]
        in_bucket.sort(key=lambda r: r["num_scenarios"])

        if N_INSTANCES_PER_BUCKET is None:
            sample = in_bucket
        else:
            step = max(1, len(in_bucket) // N_INSTANCES_PER_BUCKET)
            sample = in_bucket[::step][:N_INSTANCES_PER_BUCKET]

        keep_fractions_here = KEEP_FRACTIONS_BY_BUCKET[(lo, hi)]
        bucket_label = f"[{lo}-{hi if hi < float('inf') else 'inf'}]"
        print(
            f"  Bucket {bucket_label}: {len(sample)} instances x "
            f"{len(keep_fractions_here)} keep fractions "
            f"({[f'{kf * 100:.0f}%' for kf in keep_fractions_here]})"
        )
        n_done_in_bucket = 0

        for r in sample:
            pdir = r["program_dir"]
            s = r["s"]
            true_x = (
                ast.literal_eval(r["opt_scenario"])
                if isinstance(r["opt_scenario"], str)
                else tuple(r["opt_scenario"])
            )
            opt_energy = r["opt_energy"]

            try:
                preamble, scenario_blocks = load_lp_files(pdir)
            except FileNotFoundError:
                continue

            x_tuples = parse_scenario_x_tuples(scenario_blocks, s)
            pml_feats = dp._parse_pml_features({"program_dir": pdir})
            x_to_id = {v: k for k, v in x_tuples.items()}

            for kf in keep_fractions_here:
                kept = prune_top_k_percent(net, pml_feats, s, kf)
                recall = true_x in kept
                keep_ids = [x_to_id[x] for x in kept if x in x_to_id]

                prog_name = os.path.basename(os.path.normpath(pdir))
                out_path = os.path.join(temp_dir, f"{prog_name}_fe_{kf}.lp")
                write_reduced_lp(preamble, scenario_blocks, keep_ids, out_path)

                if VERBOSE:
                    print(f"    [debug] out_path={out_path!r} kept_n={len(keep_ids)}")

                t0 = time.time()
                best_obj, _ = solve_multi_scenario_timed(out_path)
                t_pruned = time.time() - t0
                gap = (best_obj - opt_energy) / opt_energy * 100

                per_instance_rows.append({
                    "program_dir": pdir,
                    "bucket": (lo, hi),
                    "num_scenarios": r["num_scenarios"],
                    "s": s,
                    "keep_fraction": kf,
                    "kept_n": len(keep_ids),
                    "recall": recall,
                    "gap_pct": gap,
                    "t_pruned": t_pruned,
                    "t_full": r["watwaos_time"],
                })

            n_done_in_bucket += 1
            if n_done_in_bucket % 25 == 0:
                print(f"    {n_done_in_bucket}/{len(sample)} instances completed in bucket {bucket_label}")

    with open(RESULTS_OUT_PATH, "wb") as f:
        pickle.dump(per_instance_rows, f)

    print(f"\nSaved evaluation metrics to: {RESULTS_OUT_PATH}\n")

    header = (
        f"{'Bucket':<16}{'Keep%':>7}{'n':>5}{'Recall%':>10}"
        f"{'Mean Kept':>14}{'Mean Speedup':>14}{'Median Speedup':>16}"
    )
    print(header)
    print("-" * len(header))

    for lo, hi in BUCKETS:
        for kf in KEEP_FRACTIONS_BY_BUCKET[(lo, hi)]:
            rows = [
                r
                for r in per_instance_rows
                if r["bucket"] == (lo, hi) and r["keep_fraction"] == kf
            ]
            if not rows:
                continue

            n = len(rows)
            recall_pct = sum(r["recall"] for r in rows) / n * 100
            mean_kept_n = sum(r["kept_n"] for r in rows) / n
            speedups = [
                r["t_full"] / r["t_pruned"] if r["t_pruned"] > 0 else float("inf")
                for r in rows
            ]
            speedups_sorted = sorted(speedups)
            mean_sp = sum(speedups) / n
            median_sp = speedups_sorted[n // 2]
            label = f"[{lo}-{hi if hi < float('inf') else 'inf'}]"

            print(
                f"{label:<16}{kf * 100:>6.0f}%{n:>5}{recall_pct:>10.1f}"
                f"{mean_kept_n:>14.1f}{mean_sp:>13.1f}x{median_sp:>15.1f}x"
            )


if __name__ == "__main__":
    main()