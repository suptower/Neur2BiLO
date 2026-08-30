"""
Evaluation script for the Neur2BiLO WatwaOS adapter.
Compares ML predictions against WatwaOS optimal solutions and baseline heuristics.

Metrics evaluated:
  - Quality Gap: (energy_ml - energy_opt) / energy_opt [%]
  - Optimal Hit Rate: Fraction of instances where the model finds the global optimum
  - Speedup: watwaos_solve_time / ml_inference_time
"""

import argparse
import ast
import json
import os
import pickle

import numpy as np

import blo.params as blo_params


def load_json(path):
    """Loads a JSON file from disk."""
    with open(path) as f:
        return json.load(f)


def x_to_scenario_key(x):
    """Converts a decision vector into a scenario tuple string key, e.g. [2, 0] -> '(2, 0)'."""
    return str(tuple(x))


def evaluate_instance(program_dir, ml_x, ml_time):
    """
    Compares an ML decision vector against WatwaOS ground truth for a single program instance.
    Returns a dictionary of quality gap and runtime metrics.
    """
    result_path = os.path.join(program_dir, "build", "optimize-result.json")
    if not os.path.exists(result_path):
        return None

    data = load_json(result_path)
    opt_scenario = data["ideal_scenario"]
    opt_energy = data["ideal_energy"]
    watwaos_time = data["total_time"]
    num_scenarios = data["num_scenarios"]
    solutions = data["solutions"]

    ml_key = x_to_scenario_key(ml_x)

    if ml_key in solutions:
        ml_energy = solutions[ml_key]["energy"]
    else:
        # Fallback to worst-case energy if configuration was not in precomputed solution pool
        ml_energy = max(v["energy"] for v in solutions.values())

    quality_gap = (ml_energy - opt_energy) / opt_energy
    optimal_hit = ml_key == opt_scenario
    speedup = watwaos_time / ml_time if ml_time > 0 else float("inf")

    return {
        "program_dir": program_dir,
        "opt_scenario": opt_scenario,
        "ml_scenario": ml_key,
        "opt_energy": opt_energy,
        "ml_energy": ml_energy,
        "quality_gap": quality_gap,
        "optimal_hit": optimal_hit,
        "watwaos_time": watwaos_time,
        "ml_time": ml_time,
        "speedup": speedup,
        "num_scenarios": num_scenarios,
    }


def main(args):
    results_dir = args.results_dir
    if not os.path.isdir(results_dir):
        raise FileNotFoundError(f"Results directory not found: {results_dir}")

    result_files = sorted(f for f in os.listdir(results_dir) if f.endswith(".pkl"))
    if not result_files:
        raise FileNotFoundError(f"No .pkl result files found in {results_dir}")

    print(f"Found {len(result_files)} result file(s) in {results_dir}\n")

    cfg = getattr(blo_params, args.problem)
    program_dirs = cfg.program_dirs

    # Display first result summary
    first_file = result_files[0]
    with open(os.path.join(results_dir, first_file), "rb") as f:
        res = pickle.load(f)

    ml_x = res["x"]
    ml_time = res["time"]
    print(f"Sample Result ({first_file}):")
    print(f"  Decision vector: x = {ml_x}")
    print(f"  Inference time:  {ml_time * 1000:.2f} ms\n")

    # Aggregate dataset baseline metrics across all program directories
    print("Evaluating baseline distributions across all program directories...\n")

    opt_energies = []
    worst_energies = []
    greedy_energies = []
    random_gaps = []
    watwaos_times = []
    num_scenarios_list = []

    for program_dir in program_dirs:
        result_path = os.path.join(program_dir, "build", "optimize-result.json")
        if not os.path.exists(result_path):
            continue

        data = load_json(result_path)
        solutions = data["solutions"]
        opt_energy = data["ideal_energy"]
        watwaos_time = data["total_time"]
        num_scenarios = data["num_scenarios"]

        energies = [v["energy"] for v in solutions.values()]
        worst_e = max(energies)
        mean_e = float(np.mean(energies))

        # Greedy baseline: select all-HighFreq (alternative 2)
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
    print(f"Evaluated {n} valid program instances\n")

    print("=" * 60)
    print("WatwaOS Solver Statistics")
    print("=" * 60)
    print(f"  Avg solve time:        {np.mean(watwaos_times) * 1000:.1f} ms")
    print(f"  Median solve time:     {np.median(watwaos_times) * 1000:.1f} ms")
    print(f"  Max solve time:        {np.max(watwaos_times) * 1000:.1f} ms")
    print(f"  Avg num scenarios:     {np.mean(num_scenarios_list):.0f}")
    print(f"  Max num scenarios:     {np.max(num_scenarios_list)}")

    greedy_gaps = [(g - o) / o for g, o in zip(greedy_energies, opt_energies)]
    print("\n" + "=" * 60)
    print("Baseline: All-HighFreq Heuristic (x=[2, 2, ..., 2])")
    print("=" * 60)
    print(f"  Mean quality gap:      {np.mean(greedy_gaps) * 100:.2f}%")
    print(f"  Median quality gap:    {np.median(greedy_gaps) * 100:.2f}%")
    print(f"  Max quality gap:       {np.max(greedy_gaps) * 100:.2f}%")
    print(f"  Optimal hit rate:      {sum(g == 0 for g in greedy_gaps) / n * 100:.1f}%")

    print("\n" + "=" * 60)
    print("Baseline: Random Scenario Selection")
    print("=" * 60)
    print(f"  Mean quality gap:      {np.mean(random_gaps) * 100:.2f}%")
    print(f"  Median quality gap:    {np.median(random_gaps) * 100:.2f}%")

    # Sample Instance ML Evaluation
    print("\n" + "=" * 60)
    print("Surrogate Model (Neur2BiLO): Single Instance Demo")
    print("=" * 60)

    first_dir = program_dirs[0]
    m = evaluate_instance(first_dir, ml_x, ml_time)
    if m:
        print(f"  Instance:              {first_dir}")
        print(f"  Optimal scenario:      {m['opt_scenario']}")
        print(f"  Predicted scenario:    {m['ml_scenario']}")
        print(f"  Optimal energy:        {m['opt_energy']:.0f}")
        print(f"  Predicted energy:      {m['ml_energy']:.0f}")
        print(f"  Quality gap:           {m['quality_gap'] * 100:.4f}%")
        print(f"  Optimal hit:           {m['optimal_hit']}")
        print(f"  WatwaOS solve time:    {m['watwaos_time'] * 1000:.1f} ms")
        print(f"  ML inference time:     {m['ml_time'] * 1000:.2f} ms")
        print(f"  Speedup:               {m['speedup']:.1f}x")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"  Dataset size:          {n} instances")
    print(f"  Avg WatwaOS solve:     {np.mean(watwaos_times) * 1000:.1f} ms")
    print(f"  ML inference time:     {ml_time * 1000:.2f} ms")
    print(f"  Theoretical speedup:   {np.mean(watwaos_times) / ml_time:.1f}x")
    print(f"  Greedy gap:            {np.mean(greedy_gaps) * 100:.2f}%")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate WatwaOS surrogate model outputs against exact solver solutions."
    )
    parser.add_argument("--problem", type=str, default="watwa_v1", help="Problem configuration name.")
    parser.add_argument(
        "--results_dir",
        type=str,
        default="data/watwa/results/",
        help="Path to results directory containing .pkl files.",
    )

    args = parser.parse_args()
    main(args)