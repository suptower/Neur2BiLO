"""
Evaluates neural surrogate model performance via full candidate enumeration without Gurobi.

Usage:
    python -m blo.scripts.evaluate_watwa_no_gurobi \
        --problem watwa_v7 \
        --ckpt data/watwa/nn_inst_encoder_both_....pt
"""

import argparse
import ast
import itertools
import json
import os
import pickle
import time

import numpy as np
import torch

import blo.params as blo_params
from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = torch.device("cpu")
BATCH_SIZE = 4096


def load_scoring_net(ckpt_path, problem):
    """Loads and reconstructs a SetInstanceEncodingNetwork from a saved checkpoint."""
    ckpt = torch.load(ckpt_path, map_location=DEVICE, weights_only=False)

    net = SetInstanceEncodingNetwork(
        instance_decision_embedder=ckpt["instance_decision_embedder"],
        final_instance_embedder=ckpt["final_instance_embedder"],
        value_predictor=ckpt["value_predictor"],
        agg_type=ckpt["params"].get("inst_agg_type", "sum"),
        use_coef=ckpt["use_coef"],
        problem=problem,
        approx_type="both",
        use_context="context_proj" in ckpt,
        context_proj=ckpt.get("context_proj"),
        use_inst_embedding_norm=ckpt.get("use_inst_embedding_norm", False),
        use_attention="attention_proj" in ckpt,
        attention_proj=ckpt.get("attention_proj"),
        attention=ckpt.get("attention"),
        attention_num_heads=ckpt["params"].get("attention_num_heads", 4),
    )

    if ckpt.get("use_inst_embedding_norm", False):
        net.inst_embedding_norm = ckpt["inst_embedding_norm"]

    net.to(DEVICE)
    net.eval()
    return net


def build_feature_tensors_batch(pml_feats, x_list, s):
    """Constructs batched instance and decision feature tensors for candidate scenarios."""
    inst_features = [
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

    inst_features = np.asarray(inst_features, dtype=np.float32)
    batch_size = len(x_list)
    inst_batch = np.broadcast_to(inst_features, (batch_size, s, 15)).copy()

    dec_batch = np.zeros((batch_size, s, 5), dtype=np.float32)

    for batch_idx, x in enumerate(x_list):
        for i in range(s):
            decision = int(x[i])
            transition_cost = pml_feats[i]["transition_costs"][decision]

            dec_batch[batch_idx, i, decision] = 1.0
            dec_batch[batch_idx, i, 3] = transition_cost["time_ns"] / 1e6
            dec_batch[batch_idx, i, 4] = transition_cost["power_nw"] / 1e9

    return (
        torch.from_numpy(inst_batch).to(DEVICE),
        torch.from_numpy(dec_batch).to(DEVICE),
    )


def predict_best_scenario(net, pml_feats, s, batch_size=BATCH_SIZE):
    """Scores all 3^s candidate decision scenarios and returns the argmin configuration."""
    candidates = list(itertools.product(range(3), repeat=s))
    best_x = None
    best_score = None

    for start in range(0, len(candidates), batch_size):
        batch = candidates[start : start + batch_size]
        inst_t, dec_t = build_feature_tensors_batch(pml_feats, batch, s)

        x_dummy = torch.zeros((len(batch), s), dtype=torch.float32, device=DEVICE)
        p_dummy = torch.zeros((len(batch), 1), dtype=torch.float32, device=DEVICE)

        with torch.no_grad():
            scores = net(inst_t, dec_t, x_dummy, p_dummy, None).squeeze(-1)

        idx = int(torch.argmin(scores).item())
        score = scores[idx].item()

        if best_score is None or score < best_score:
            best_score = score
            best_x = batch[idx]

    return best_x


def evaluate_instance(net, preproc, inst_idx, program_dir):
    """Evaluates a single problem instance against solver ground truth and greedy baseline."""
    result_path = os.path.join(program_dir, "build", "optimize-result.json")
    if not os.path.exists(result_path):
        return None

    with open(result_path) as f:
        data = json.load(f)

    opt_scenario = data["ideal_scenario"]
    opt_energy = data["ideal_energy"]
    watwaos_time = data["total_time"]
    num_scenarios = data["num_scenarios"]
    solutions = data["solutions"]

    s = len(ast.literal_eval(opt_scenario))
    pml_feats = preproc._parse_pml_features({"program_dir": program_dir})

    start = time.perf_counter()
    ml_x = predict_best_scenario(net, pml_feats, s)
    ml_time = time.perf_counter() - start

    ml_key = str(tuple(ml_x))
    if ml_key in solutions:
        ml_energy = solutions[ml_key]["energy"]
    else:
        ml_energy = max(sol["energy"] for sol in solutions.values())

    quality_gap = (ml_energy - opt_energy) / opt_energy
    optimal_hit = ml_key == opt_scenario
    speedup = watwaos_time / ml_time if ml_time > 0 else float("inf")

    greedy_key = str((2,) * s)
    if greedy_key in solutions:
        greedy_energy = solutions[greedy_key]["energy"]
    else:
        greedy_energy = max(sol["energy"] for sol in solutions.values())

    greedy_gap = (greedy_energy - opt_energy) / opt_energy

    return {
        "inst_idx": inst_idx,
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
        "greedy_gap": greedy_gap,
        "s": s,
    }


def main(args):
    problem_config = getattr(blo_params, args.problem)
    program_dirs = problem_config.program_dirs

    if args.limit is not None:
        program_dirs = program_dirs[: args.limit]

    print(
        f"Solver-free batch evaluation: {len(program_dirs)} instances, "
        f"problem={args.problem}, ckpt={args.ckpt}"
    )

    net = load_scoring_net(args.ckpt, args.problem)
    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )

    start = time.perf_counter()
    metrics = []

    for inst_idx, program_dir in enumerate(program_dirs):
        result = evaluate_instance(net, preproc, inst_idx, program_dir)
        if result is not None:
            metrics.append(result)

        if (inst_idx + 1) % 25 == 0:
            elapsed = time.perf_counter() - start
            print(f"  {inst_idx + 1}/{len(program_dirs)} instances evaluated ({elapsed:.1f}s)")

    total_elapsed = time.perf_counter() - start
    print(f"\nFinished: {len(metrics)}/{len(program_dirs)} instances evaluated in {total_elapsed:.1f}s\n")

    if not metrics:
        print("No evaluation results. Please verify that optimize-result.json files exist.")
        return

    n_eval = len(metrics)
    quality_gaps = [m["quality_gap"] for m in metrics]
    greedy_gaps = [m["greedy_gap"] for m in metrics]
    optimal_hits = [m["optimal_hit"] for m in metrics]
    speedups = [m["speedup"] for m in metrics]
    watwaos_times = [m["watwaos_time"] for m in metrics]
    ml_times = [m["ml_time"] for m in metrics]
    num_scenarios = [m["num_scenarios"] for m in metrics]

    print("=" * 65)
    print(f"Evaluation Summary ({n_eval} instances)")
    print("=" * 65)

    print("\nWatwaOS Solver:")
    print(f"  Avg solve time:          {np.mean(watwaos_times) * 1000:8.1f} ms")
    print(f"  Median solve time:       {np.median(watwaos_times) * 1000:8.1f} ms")
    print(f"  Avg num scenarios:       {np.mean(num_scenarios):8.0f}")
    print(f"  Max num scenarios:       {np.max(num_scenarios):8.0f}")

    print("\nML Model (Full Enumeration Argmin):")
    print(f"  Avg inference time:      {np.mean(ml_times) * 1000:8.2f} ms")
    print(f"  Median inference time:   {np.median(ml_times) * 1000:8.2f} ms")
    print(f"  Mean quality gap:        {np.mean(quality_gaps) * 100:8.4f}%")
    print(f"  Median quality gap:      {np.median(quality_gaps) * 100:8.4f}%")
    print(f"  Optimal hit rate:        {np.mean(optimal_hits) * 100:8.1f}%")
    print(f"  Mean speedup:            {np.mean(speedups):8.1f}x")
    print(f"  Median speedup:          {np.median(speedups):8.1f}x")

    print("\nGreedy Baseline (all HighFreq):")
    print(f"  Mean quality gap:        {np.mean(greedy_gaps) * 100:8.4f}%")
    print(f"  Optimal hit rate:        {sum(g == 0 for g in greedy_gaps) / n_eval * 100:8.1f}%")

    ml_better = sum(ml_gap < greedy_gap for ml_gap, greedy_gap in zip(quality_gaps, greedy_gaps))
    print(f"\nML outperforms Greedy:     {ml_better}/{n_eval} ({ml_better / n_eval * 100:.1f}%)")

    print("\nPerformance Breakdown by Scenario Complexity:")
    bins = [
        (1, 10),
        (10, 100),
        (100, 1000),
        (1000, 10000),
        (10000, float("inf")),
    ]

    for lower, upper in bins:
        subset = [m for m in metrics if lower <= m["num_scenarios"] < upper]
        if not subset:
            continue

        gaps = [m["quality_gap"] for m in subset]
        hits = [m["optimal_hit"] for m in subset]
        upper_str = str(upper) if upper < float("inf") else "inf"

        print(
            f"  [{lower:6} - {upper_str:>6}] "
            f"n={len(subset):3d}  "
            f"gap={np.mean(gaps) * 100:.3f}%  "
            f"hits={np.mean(hits) * 100:.1f}%"
        )

    out_dir = os.path.join(problem_config.data_path, "watwa", "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"batch_eval_no_gurobi_{args.problem}.pkl")

    with open(out_path, "wb") as f:
        pickle.dump(metrics, f)

    print(f"\nFull evaluation metrics saved to: {out_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Evaluate surrogate network accuracy and inference speed without solver invocation."
    )
    parser.add_argument("--problem", type=str, default="watwa_v7", help="Problem configuration name.")
    parser.add_argument("--ckpt", type=str, required=True, help="Path to .pt model checkpoint.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Optional limit on the number of instances to evaluate.",
    )

    args = parser.parse_args()
    main(args)