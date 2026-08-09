"""
Batch evaluation script for Neur2BiLO WatwaOS adapter.
Runs 05_run_ml_blo for all instances and aggregates results.

Usage:
    python -u -m blo.scripts.evaluate_watwa_batch --problem watwa_v1 --n_procs 4
"""

import os
import ast
import json
import time
import pickle
import argparse
import subprocess
import numpy as np
from multiprocessing import Pool


# ── helpers ──────────────────────────────────────────────────────────────────

def load_json(path):
    with open(path) as f:
        return json.load(f)


def x_to_scenario_key(x):
    return str(tuple(x))


def evaluate_single(inst_idx, program_dir, result_path):
    """Load ML result and compare against WatwaOS optimum."""
    if not os.path.exists(result_path):
        return None
    if not os.path.exists(os.path.join(program_dir, "build", "optimize-result.json")):
        return None

    res  = pickle.load(open(result_path, "rb"))
    data = load_json(os.path.join(program_dir, "build", "optimize-result.json"))

    ml_x      = res["x"]
    ml_time   = res["time"]
    ml_key    = x_to_scenario_key(ml_x)

    opt_scenario  = data["ideal_scenario"]
    opt_energy    = data["ideal_energy"]
    watwaos_time  = data["total_time"]
    num_scenarios = data["num_scenarios"]
    solutions     = data["solutions"]

    if ml_key in solutions:
        ml_energy = solutions[ml_key]["energy"]
    else:
        ml_energy = max(v["energy"] for v in solutions.values())

    quality_gap = (ml_energy - opt_energy) / opt_energy
    optimal_hit = (ml_key == opt_scenario)
    speedup     = watwaos_time / ml_time if ml_time > 0 else float("inf")

    # Greedy baseline: all HighFreq (2s)
    s = len(ast.literal_eval(opt_scenario))
    greedy_key = str(tuple([2] * s))
    greedy_energy = solutions[greedy_key]["energy"] if greedy_key in solutions else max(v["energy"] for v in solutions.values())
    greedy_gap = (greedy_energy - opt_energy) / opt_energy

    return {
        "inst_idx":      inst_idx,
        "program_dir":   program_dir,
        "opt_scenario":  opt_scenario,
        "ml_scenario":   ml_key,
        "opt_energy":    opt_energy,
        "ml_energy":     ml_energy,
        "quality_gap":   quality_gap,
        "optimal_hit":   optimal_hit,
        "watwaos_time":  watwaos_time,
        "ml_time":       ml_time,
        "speedup":       speedup,
        "num_scenarios": num_scenarios,
        "greedy_gap":    greedy_gap,
        "s":             s,
    }

def run_instance(args_tuple):
    """Run 05_run_ml_blo for a single instance index, skipping if already done."""
    inst_idx, problem, extra_args, results_dir = args_tuple

    # Skip if a result file for this instance already exists (resume support)
    existing = [
        f for f in os.listdir(results_dir)
        if f.endswith(".pkl") and (f"i-{inst_idx}_" in f or f.endswith(f"i-{inst_idx}.pkl") or f"_i-{inst_idx}" in f)
    ]
    if existing:
        return True

    cmd = [
        "python", "-m", "blo.scripts.05_run_ml_blo",
        "--problem", problem,
        "--model_type", "inst_encoder",
        "--inst_idx", str(inst_idx),
        "--approx_type", "upper"
    ] + extra_args

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  [!] inst {inst_idx} failed: {result.stderr[-200:]}")
        return False
    return True

# ── main ─────────────────────────────────────────────────────────────────────

def main(args):
    import blo.params as params
    cfg = getattr(params, args.problem)
    program_dirs = cfg.program_dirs
    n = len(program_dirs)

    print(f"Batch evaluation: {n} instances, problem={args.problem}")
    print(f"Running ML model for each instance...\n")

    # Extra args to pass through to 05_run_ml_blo
    extra_args = [
        "--use_attention", str(args.use_attention),
        "--attention_num_heads", str(args.attention_num_heads),
        "--use_context", str(args.use_context),
        "--context_hidden_dim", str(args.context_hidden_dim)
    ]

    # Run ML model for all instances
    t0 = time.time()
    results_dir = os.path.join(cfg.data_path, "watwa", "results") + "/"
    tasks = [(i, args.problem, extra_args, results_dir) for i in range(n)]

    if args.n_procs > 1:
        with Pool(args.n_procs) as pool:
            results = list(pool.imap(run_instance, tasks))
    else:
        results = []
        for i, task in enumerate(tasks):
            ok = run_instance(task)
            results.append(ok)
            if (i+1) % 10 == 0:
                print(f"  {i+1}/{n} instances done ({time.time()-t0:.0f}s)")

    n_failed = sum(1 for r in results if not r)
    print(f"\nML inference done: {n - n_failed}/{n} succeeded ({time.time()-t0:.1f}s)\n")

    # Collect and evaluate results
    metrics = []

    for inst_idx, program_dir in enumerate(program_dirs):
        # Find result file for this instance
        # 05_run_ml_blo saves with pattern: res_..._i-{inst_idx}_...pkl
        result_files = [
            f for f in os.listdir(results_dir)
            if f.endswith(".pkl") and f"i-{inst_idx}_" in f or f.endswith(f"i-{inst_idx}.pkl")
        ]
        # fallback: find file containing inst_idx
        if not result_files:
            result_files = [
                f for f in os.listdir(results_dir)
                if f.endswith(".pkl") and f"_i-{inst_idx}" in f
            ]
        if not result_files:
            continue

        result_path = os.path.join(results_dir, sorted(result_files)[-1])
        m = evaluate_single(inst_idx, program_dir, result_path)
        if m:
            metrics.append(m)

    if not metrics:
        print("No results found. Check that 05_run_ml_blo ran correctly.")
        return

    n_eval = len(metrics)
    quality_gaps   = [m["quality_gap"]   for m in metrics]
    greedy_gaps    = [m["greedy_gap"]    for m in metrics]
    optimal_hits   = [m["optimal_hit"]   for m in metrics]
    speedups       = [m["speedup"]       for m in metrics]
    watwaos_times  = [m["watwaos_time"]  for m in metrics]
    ml_times       = [m["ml_time"]       for m in metrics]
    num_scenarios  = [m["num_scenarios"] for m in metrics]

    print("=" * 65)
    print(f"Results over {n_eval} instances")
    print("=" * 65)

    print("\nWatwaOS Solver:")
    print(f"  Avg solve time:          {np.mean(watwaos_times)*1000:8.1f} ms")
    print(f"  Median solve time:       {np.median(watwaos_times)*1000:8.1f} ms")
    print(f"  Max solve time:          {np.max(watwaos_times)*1000:8.1f} ms")
    print(f"  Avg num scenarios:       {np.mean(num_scenarios):8.0f}")
    print(f"  Max num scenarios:       {np.max(num_scenarios):8.0f}")

    print("\nML Model (Neur2BiLO):")
    print(f"  Avg inference time:      {np.mean(ml_times)*1000:8.2f} ms")
    print(f"  Mean quality gap:        {np.mean(quality_gaps)*100:8.4f}%")
    print(f"  Median quality gap:      {np.median(quality_gaps)*100:8.4f}%")
    print(f"  Max quality gap:         {np.max(quality_gaps)*100:8.4f}%")
    print(f"  Optimal hit rate:        {np.mean(optimal_hits)*100:8.1f}%")
    print(f"  Mean speedup:            {np.mean(speedups):8.1f}x")
    print(f"  Median speedup:          {np.median(speedups):8.1f}x")
    print(f"  Speedup (avg times):     {np.mean(watwaos_times)/np.mean(ml_times):8.1f}x")

    print("\nGreedy Baseline (all HighFreq):")
    print(f"  Mean quality gap:        {np.mean(greedy_gaps)*100:8.4f}%")
    print(f"  Median quality gap:      {np.median(greedy_gaps)*100:8.4f}%")
    print(f"  Max quality gap:         {np.max(greedy_gaps)*100:8.4f}%")
    print(f"  Optimal hit rate:        {sum(g==0 for g in greedy_gaps)/n_eval*100:8.1f}%")

    print("\nML vs Greedy:")
    ml_better = sum(q < g for q, g in zip(quality_gaps, greedy_gaps))
    print(f"  ML better than greedy:   {ml_better}/{n_eval} instances ({ml_better/n_eval*100:.1f}%)")

    # Per-complexity breakdown
    print("\nBreakdown by problem complexity (num_scenarios):")
    bins = [(1, 10), (10, 100), (100, 1000), (1000, 10000), (10000, float("inf"))]
    for lo, hi in bins:
        subset = [m for m in metrics if lo <= m["num_scenarios"] < hi]
        if not subset:
            continue
        gaps = [m["quality_gap"] for m in subset]
        hits = [m["optimal_hit"] for m in subset]
        print(f"  [{lo:6} – {hi if hi < float('inf') else '∞':>6} scenarios] "
              f"n={len(subset):3d}  "
              f"gap={np.mean(gaps)*100:.3f}%  "
              f"hits={np.mean(hits)*100:.1f}%")

    # Save full results
    out_path = os.path.join(cfg.data_path, "watwa", "results", f"batch_eval_{args.problem}.pkl")
    pickle.dump(metrics, open(out_path, "wb"))
    print(f"\nFull results saved to: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem",  type=str, default="watwa_v1")
    parser.add_argument("--n_procs", type=int, default=1)

    parser.add_argument('--use_attention', type=int, default=0, help='Whether to use attention in instance encoder model.')
    parser.add_argument('--attention_num_heads', type=int, default=4, help='Number of heads for attention in instance encoder model.')

    parser.add_argument('--use_context', type=int, default=0, help='Whether to use additional context features in instance encoder model.')
    parser.add_argument('--context_hidden_dim', type=int, default=32, help='Hidden dimension for context features in instance encoder model.')

    args = parser.parse_args()
    main(args)
