"""
Evaluation script for Neur2BiLO WatwaOS adapter.
Compares ML-based decisions against WatwaOS optimal solutions.

Metrics:
  - Quality Gap:  (energy_ml - energy_opt) / energy_opt  [%]
  - Optimal Hit Rate: fraction of instances where ML finds the optimal scenario
  - Speedup: watwaos_solve_time / ml_inference_time
"""

import json
import os
import pickle
import time
import ast
import numpy as np
from argparse import ArgumentParser
import blo.params as params


# ── helpers ──────────────────────────────────────────────────────────────────

def load_json(path):
    with open(path) as f:
        return json.load(f)


def x_to_scenario_key(x):
    """Convert ML decision list [2, 0] → '(2, 0)' to match JSON keys."""
    return str(tuple(x))


def evaluate_instance(program_dir, ml_x, ml_time):
    """
    Compare ML decision against WatwaOS optimum for one instance.
    Returns a dict with all relevant metrics.
    """
    result_path = os.path.join(program_dir, "build", "optimize-result.json")
    if not os.path.exists(result_path):
        return None

    data = load_json(result_path)

    opt_scenario   = data["ideal_scenario"]          # e.g. "(2, 0)"
    opt_energy     = data["ideal_energy"]
    watwaos_time   = data["total_time"]
    num_scenarios  = data["num_scenarios"]
    solutions      = data["solutions"]

    ml_key = x_to_scenario_key(ml_x)

    # Energy at ML decision (None if scenario not in JSON)
    if ml_key in solutions:
        ml_energy = solutions[ml_key]["energy"]
    else:
        # ML chose a scenario that wasn't evaluated — treat as worst case
        worst_energy = max(v["energy"] for v in solutions.values())
        ml_energy = worst_energy

    # Metrics
    quality_gap  = (ml_energy - opt_energy) / opt_energy  # relative gap
    optimal_hit  = (ml_key == opt_scenario)
    speedup      = watwaos_time / ml_time if ml_time > 0 else float("inf")

    return {
        "program_dir":    program_dir,
        "opt_scenario":   opt_scenario,
        "ml_scenario":    ml_key,
        "opt_energy":     opt_energy,
        "ml_energy":      ml_energy,
        "quality_gap":    quality_gap,
        "optimal_hit":    optimal_hit,
        "watwaos_time":   watwaos_time,
        "ml_time":        ml_time,
        "speedup":        speedup,
        "num_scenarios":  num_scenarios,
    }


# ── main ─────────────────────────────────────────────────────────────────────

def main(args):
    # Load ML results
    results_dir = args.results_dir
    if not os.path.isdir(results_dir):
        raise FileNotFoundError(f"Results dir not found: {results_dir}")

    result_files = sorted(f for f in os.listdir(results_dir) if f.endswith(".pkl"))
    if not result_files:
        raise FileNotFoundError(f"No .pkl result files found in {results_dir}")

    print(f"Found {len(result_files)} ML result file(s) in {results_dir}\n")

    # Load program dirs from params
    cfg = getattr(params, args.problem)
    program_dirs = cfg.program_dirs

    all_metrics = []

    for result_file in result_files:
        res = pickle.load(open(os.path.join(results_dir, result_file), "rb"))
        ml_x    = res["x"]
        ml_time = res["time"]

        # Find matching program dir — use instance index 0 for single-instance runs,
        # or iterate all dirs when running batch evaluation
        print(f"Result file: {result_file}")
        print(f"  ML decision: x = {ml_x}  (inference time: {ml_time*1000:.2f} ms)")

        # For single-file results, evaluate against the first instance as a demo
        # For full batch evaluation, we iterate all program_dirs below
        break

    # ── Batch evaluation over all instances ──────────────────────────────────
    print("\nRunning batch evaluation over all program directories...\n")

    # We need to run the ML model on each instance individually.
    # Since 05_run_ml_blo only saves one result file, we instead
    # evaluate by reading each instance's JSON and comparing against
    # the stored ML result (which corresponds to instance index 0).
    #
    # For a proper per-instance evaluation, we read all JSONs and
    # compute what a RANDOM and GREEDY baseline would achieve,
    # then compare against the single ML result as a proof-of-concept.

    opt_energies   = []
    worst_energies = []
    greedy_energies = []  # always pick (2, 2, ..., 2) — all HighFreq
    random_gaps    = []
    watwaos_times  = []
    num_scenarios_list = []

    for program_dir in program_dirs:
        result_path = os.path.join(program_dir, "build", "optimize-result.json")
        if not os.path.exists(result_path):
            continue

        data = load_json(result_path)
        solutions     = data["solutions"]
        opt_energy    = data["ideal_energy"]
        watwaos_time  = data["total_time"]
        num_scenarios = data["num_scenarios"]

        energies = [v["energy"] for v in solutions.values()]
        worst_e  = max(energies)
        mean_e   = np.mean(energies)

        # Greedy: pick scenario with all HighFreq (2s)
        s = len(ast.literal_eval(data["ideal_scenario"]))
        greedy_key = str(tuple([2] * s))
        greedy_e = solutions[greedy_key]["energy"] if greedy_key in solutions else worst_e

        opt_energies.append(opt_energy)
        worst_energies.append(worst_e)
        greedy_energies.append(greedy_e)
        random_gaps.append((mean_e - opt_energy) / opt_energy)
        watwaos_times.append(watwaos_time)
        num_scenarios_list.append(num_scenarios)

    n = len(opt_energies)
    print(f"Evaluated {n} instances\n")

    print("=" * 60)
    print("WatwaOS Solver Statistics")
    print("=" * 60)
    print(f"  Avg solve time:        {np.mean(watwaos_times)*1000:.1f} ms")
    print(f"  Median solve time:     {np.median(watwaos_times)*1000:.1f} ms")
    print(f"  Max solve time:        {np.max(watwaos_times)*1000:.1f} ms")
    print(f"  Avg num scenarios:     {np.mean(num_scenarios_list):.0f}")
    print(f"  Max num scenarios:     {np.max(num_scenarios_list)}")

    greedy_gaps = [(g - o) / o for g, o in zip(greedy_energies, opt_energies)]
    print("\n" + "=" * 60)
    print("Baseline: All-HighFreq (greedy x=[2,2,...,2])")
    print("=" * 60)
    print(f"  Mean quality gap:      {np.mean(greedy_gaps)*100:.2f}%")
    print(f"  Median quality gap:    {np.median(greedy_gaps)*100:.2f}%")
    print(f"  Max quality gap:       {np.max(greedy_gaps)*100:.2f}%")
    print(f"  Optimal hit rate:      {sum(g==0 for g in greedy_gaps)/n*100:.1f}%")

    print("\n" + "=" * 60)
    print("Baseline: Random scenario selection")
    print("=" * 60)
    print(f"  Mean quality gap:      {np.mean(random_gaps)*100:.2f}%")
    print(f"  Median quality gap:    {np.median(random_gaps)*100:.2f}%")

    # ── Single ML result evaluation ───────────────────────────────────────────
    print("\n" + "=" * 60)
    print("ML Model (Neur2BiLO) — single instance result")
    print("=" * 60)

    result_file = sorted(f for f in os.listdir(results_dir) if f.endswith(".pkl"))[0]
    res = pickle.load(open(os.path.join(results_dir, result_file), "rb"))
    ml_x    = res["x"]
    ml_time = res["time"]

    # Evaluate on first instance (index 0)
    first_dir = program_dirs[0]
    m = evaluate_instance(first_dir, ml_x, ml_time)
    if m:
        print(f"  Instance:              {first_dir}")
        print(f"  Optimal scenario:      {m['opt_scenario']}")
        print(f"  ML scenario:           {m['ml_scenario']}")
        print(f"  Optimal energy:        {m['opt_energy']:.0f}")
        print(f"  ML energy:             {m['ml_energy']:.0f}")
        print(f"  Quality gap:           {m['quality_gap']*100:.4f}%")
        print(f"  Optimal hit:           {m['optimal_hit']}")
        print(f"  WatwaOS solve time:    {m['watwaos_time']*1000:.1f} ms")
        print(f"  ML inference time:     {m['ml_time']*1000:.2f} ms")
        print(f"  Speedup:               {m['speedup']:.1f}x")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Dataset size:          {n} instances")
    print(f"  Avg WatwaOS time:      {np.mean(watwaos_times)*1000:.1f} ms")
    print(f"  ML inference time:     {ml_time*1000:.2f} ms")
    print(f"  Theoretical speedup:   {np.mean(watwaos_times)/ml_time:.1f}x")
    print(f"  Greedy gap (baseline): {np.mean(greedy_gaps)*100:.2f}%")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--problem",     type=str, default="watwa_v1")
    parser.add_argument("--results_dir", type=str, default="data/watwa/results/")
    args = parser.parse_args()
    main(args)