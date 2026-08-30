"""
Diagnoses rank-distribution collapses and feature sensitivities for target switch-point counts (s).

Usage:
    python -m blo.scripts.diagnose_s2_collapse \
        --problem watwa_v7 \
        --rank-csv rank_histogram_bs128_lr00025.csv
"""

import argparse
import csv
import itertools
from collections import defaultdict

import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = "cpu"

FEATURE_NAMES = [
    "time_ns_high",
    "time_ns_low",
    "power_nw_high",
    "power_nw_low",
    "energy_high",
    "energy_low",
    "energy_ratio",
    "time_ratio",
    "is_uart",
    "loop_bound",
    "position_norm",
    "position_abs",
    "tc_ratio_x1",
    "tc_ratio_x2",
]


def load_scoring_net(ckpt_path, problem):
    """Loads and initializes a trained SetInstanceEncodingNetwork from checkpoint."""
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
    """Constructs batched instance and decision tensors for a list of candidate decisions."""
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

    decision_batch = np.zeros((batch_size, s, 5), dtype=np.float32)

    for batch_idx, x in enumerate(x_list):
        for i in range(s):
            decision = int(x[i])
            transition_cost = pml_feats[i]["transition_costs"][decision]

            decision_batch[batch_idx, i, decision] = 1.0
            decision_batch[batch_idx, i, 3] = transition_cost["time_ns"] / 1e6
            decision_batch[batch_idx, i, 4] = transition_cost["power_nw"] / 1e9

    return (
        torch.from_numpy(inst_batch).to(DEVICE),
        torch.from_numpy(decision_batch).to(DEVICE),
    )


def score_all_candidates(net, pml_feats, s):
    """Scores all 3^s candidate decision combinations for a given instance."""
    candidates = list(itertools.product(range(3), repeat=s))
    inst_t, dec_t = build_feature_tensors_batch(pml_feats, candidates, s)

    x_dummy = torch.zeros((len(candidates), s), dtype=torch.float32, device=DEVICE)
    p_dummy = torch.zeros((len(candidates), 1), dtype=torch.float32, device=DEVICE)

    with torch.no_grad():
        scores = net(inst_t, dec_t, x_dummy, p_dummy, None).squeeze(-1)

    return candidates, scores.cpu().numpy()


def load_rank_csv(path, target_s):
    """Loads evaluation instances matching the target switch-point count."""
    rows = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            if int(row["s"]) == target_s:
                rows.append({
                    "program_dir": row["program_dir"],
                    "rank": int(row["rank_of_true_optimum"]),
                })
    return rows


def collect_features(rank_rows, preproc, s):
    """Parses and groups instance features by their true optimum rank."""
    by_rank = defaultdict(list)

    for row in rank_rows:
        pml_feats = preproc._parse_pml_features({"program_dir": row["program_dir"]})

        if len(pml_feats) != s:
            print(
                f"  Warning: {row['program_dir']} has {len(pml_feats)} "
                f"switch points, expected {s} (skipping)."
            )
            continue

        by_rank[row["rank"]].append(pml_feats)

    return by_rank


def print_network_scores(rank_rows, preproc, net, s, examples_per_group):
    """Displays predicted candidate rankings for sample programs in each rank group."""
    ranks = sorted({row["rank"] for row in rank_rows})

    print(f"\n{'=' * 70}")
    print(f"Raw Network Scores ({examples_per_group} examples per group)")
    print(f"{'=' * 70}")

    for rank in ranks:
        print(f"\n-- Group rank={rank} --")

        examples = [row["program_dir"] for row in rank_rows if row["rank"] == rank][:examples_per_group]

        for program_dir in examples:
            pml_feats = preproc._parse_pml_features({"program_dir": program_dir})
            candidates, scores = score_all_candidates(net, pml_feats, s)
            order = np.argsort(scores)

            print(f"  {program_dir}")
            print("    Candidate scores (sorted ascending):")
            for rank_pos, idx in enumerate(order):
                print(f"      rank {rank_pos}: x={candidates[idx]}  score={scores[idx]:.6f}")

            score_range = scores.max() - scores.min()
            print(f"    Score range across all {len(candidates)} candidates: {score_range:.6f}")


def print_feature_statistics(by_rank, s):
    """Prints feature variance and per-group means for each switch point."""
    ranks = sorted(by_rank)

    for sp_idx in range(s):
        print(f"\n{'=' * 70}")
        print(f"Switch Point {sp_idx}")
        print(f"{'=' * 70}")

        header = (
            f"{'feature':<16}"
            f"{'var (all)':>12}"
            + "".join(f"{'mean (rank=' + str(rank) + ')':>20}" for rank in ranks)
        )
        print(header)

        for feature_name in FEATURE_NAMES:
            all_values = []
            group_means = {}

            for rank in ranks:
                values = [pml_feats[sp_idx][feature_name] for pml_feats in by_rank[rank]]
                group_means[rank] = float(np.mean(values))
                all_values.extend(values)

            variance = float(np.var(all_values))
            line = f"{feature_name:<16}{variance:12.6f}"
            for rank in ranks:
                line += f"{group_means[rank]:20.6f}"

            print(line)


def print_feature_differences(by_rank, s):
    """Highlights features that show notable separation or uniformity across rank groups."""
    ranks = sorted(by_rank)

    print(f"\n{'=' * 70}")
    print("Feature Comparison Across Rank Groups")
    print(f"{'=' * 70}")

    for sp_idx in range(s):
        for feature_name in FEATURE_NAMES:
            all_values = []
            group_means = {}

            for rank in ranks:
                values = [pml_feats[sp_idx][feature_name] for pml_feats in by_rank[rank]]
                group_means[rank] = float(np.mean(values))
                all_values.extend(values)

            variance = float(np.var(all_values))
            group_spread = (max(group_means.values()) - min(group_means.values())) if len(ranks) >= 2 else 0.0
            std = np.sqrt(variance + 1e-12)

            if variance < 1e-9:
                continue

            if group_spread > 0.5 * std:
                print(
                    f"  sp{sp_idx}.{feature_name}: Group means differ significantly "
                    f"(var={variance:.4f}, spread={group_spread:.4f})"
                )
            elif variance > 1e-4 and group_spread < 0.1 * std:
                print(
                    f"  sp{sp_idx}.{feature_name}: High variance within data, but low spread across groups "
                    f"(var={variance:.4f}, spread={group_spread:.4f})"
                )


def main(args):
    rank_rows = load_rank_csv(args.rank_csv, target_s=args.s)
    print(f"Loaded {len(rank_rows)} instances with s={args.s} from {args.rank_csv}.")

    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )

    net = load_scoring_net(args.ckpt, args.problem) if args.ckpt else None
    by_rank = collect_features(rank_rows, preproc, args.s)

    ranks = sorted(by_rank)
    counts = [len(by_rank[rank]) for rank in ranks]
    print(f"\nObserved rank groups: {ranks} (counts: {counts})")

    if net is not None:
        print_network_scores(rank_rows, preproc, net, args.s, args.examples_per_group)

    print_feature_statistics(by_rank, args.s)
    print_feature_differences(by_rank, args.s)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Diagnose performance and feature distributions for specific switch-point counts."
    )
    parser.add_argument("--problem", type=str, default="watwa_v7", help="Problem configuration name.")
    parser.add_argument("--rank-csv", type=str, required=True, help="Path to ranking CSV results file.")
    parser.add_argument("--s", type=int, default=2, help="Switch-point count to analyze.")
    parser.add_argument("--ckpt", type=str, default=None, help="Optional path to model checkpoint for scoring.")
    parser.add_argument(
        "--examples-per-group",
        type=int,
        default=3,
        help="Number of example instances to score per rank group.",
    )

    args = parser.parse_args()
    main(args)