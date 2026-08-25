import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Aggregate pruning recall/speedup evaluation across complexity buckets — multistart version.
"""
import ast
import pickle
import time
import random
import itertools
import gurobipy as gp

from pruning import (
    load_lp_files, parse_scenario_x_tuples, write_reduced_lp,
    load_scoring_net, score_x, DEVICE,
)
from blo.data_preprocessor.watwa import WatwaDataPreprocessor

CKPT_PATH = "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7_FULLDECAY_VERIFIED_20260813_1245.pt"
EVAL_PATH = "data/watwa/results/batch_eval_watwa_v7.pkl"
KEEP_VALUES = [1, 2]
N_INSTANCES_PER_BUCKET = 25
N_RESTARTS = 5

BUCKETS = [(100, 1000), (1000, 10000), (10000, float("inf"))]


def greedy_prune_multistart(net, pml_feats, s, keep_per_switch_point, n_restarts=5, refine_iters=2, seed=0):
    rng = random.Random(seed)
    all_kept_per_sp = [set() for _ in range(s)]

    starts = [[1] * s]
    starts += [[rng.randint(0, 2) for _ in range(s)] for _ in range(n_restarts - 1)]

    for x_start in starts:
        x_ref = list(x_start)
        for _ in range(refine_iters):
            for sp in range(s):
                scores = [score_x(net, pml_feats, [*x_ref[:sp], alt, *x_ref[sp+1:]], s) for alt in range(3)]
                x_ref[sp] = int(min(range(3), key=lambda a: scores[a]))
        for sp in range(s):
            scored = [(alt, score_x(net, pml_feats, [*x_ref[:sp], alt, *x_ref[sp+1:]], s)) for alt in range(3)]
            scored.sort(key=lambda t: t[1])
            for alt, _ in scored[:keep_per_switch_point]:
                all_kept_per_sp[sp].add(alt)

    kept_per_sp = [sorted(x) for x in all_kept_per_sp]
    return list(itertools.product(*kept_per_sp))


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

            for keep in KEEP_VALUES:
                kept = greedy_prune_multistart(net, pml_feats, s, keep, n_restarts=N_RESTARTS)
                recall = true_x in kept
                keep_ids = [x_to_id[x] for x in kept if x in x_to_id]

                out_path = f"/tmp/{pdir.split('/')[-1]}_ms_k{keep}.lp"
                write_reduced_lp(preamble, scenario_blocks, keep_ids, out_path)

                t0 = time.time()
                best_obj, _ = solve_multi_scenario(out_path)
                t_pruned = time.time() - t0
                gap = (best_obj - opt_energy) / opt_energy * 100

                per_instance_rows.append({
                    "program_dir": pdir, "bucket": (lo, hi), "num_scenarios": r["num_scenarios"],
                    "s": s, "keep": keep, "kept_n": len(keep_ids), "recall": recall,
                    "gap_pct": gap, "t_pruned": t_pruned, "t_full": r["watwaos_time"],
                })

    with open("pruning_recall_multistart_results.pkl", "wb") as f:
        pickle.dump(per_instance_rows, f)

    print(f"{'bucket':<16}{'keep':>6}{'n':>5}{'recall%':>10}{'mean_kept_n':>14}{'mean_speedup':>14}{'median_speedup':>16}")
    for lo, hi in BUCKETS:
        for keep in KEEP_VALUES:
            rows = [r for r in per_instance_rows if r["bucket"] == (lo, hi) and r["keep"] == keep]
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
            print(f"{label:<16}{keep:>6}{n:>5}{recall_pct:>10.1f}{mean_kept_n:>14.1f}{mean_sp:>14.1f}x{median_sp:>16.1f}x")


if __name__ == "__main__":
    main()