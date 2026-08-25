"""
Usage:
    python -m blo.scripts.pruning_rank_histogram \
        --problem watwa_v7 \
        --ckpt data/watwa/<checkpoint>.pt \
        --out results/rank_histogram.csv
"""

import argparse
import ast
import csv
import itertools
import json
import os

import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = torch.device("cpu")
BATCH_SIZE = 4096


def load_scoring_net(ckpt_path):
    ckpt = torch.load(
        ckpt_path,
        map_location=DEVICE,
        weights_only=False,
    )

    net = SetInstanceEncodingNetwork(
        instance_decision_embedder=ckpt["instance_decision_embedder"],
        final_instance_embedder=ckpt["final_instance_embedder"],
        value_predictor=ckpt["value_predictor"],
        agg_type=ckpt["params"].get("inst_agg_type", "sum"),
        use_coef=ckpt["use_coef"],
        problem="watwa_v7",
        approx_type="both",
        use_context="context_proj" in ckpt,
        context_proj=ckpt.get("context_proj"),
        use_inst_embedding_norm=ckpt.get(
            "use_inst_embedding_norm",
            False,
        ),
    )

    if ckpt.get("use_inst_embedding_norm", False):
        net.inst_embedding_norm = ckpt["inst_embedding_norm"]

    net.to(DEVICE)
    net.eval()

    return net


def build_feature_tensors_batch(pml_feats, candidates, s):
    inst_features = []

    for pf in pml_feats:
        inst_features.append([
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
        ])

    inst_features = np.asarray(inst_features, dtype=np.float32)

    batch_size = len(candidates)
    inst_batch = np.broadcast_to(
        inst_features,
        (batch_size, s, 15),
    ).copy()

    decision_batch = np.zeros(
        (batch_size, s, 5),
        dtype=np.float32,
    )

    for batch_idx, candidate in enumerate(candidates):
        for i in range(s):
            decision = int(candidate[i])
            transition_cost = pml_feats[i]["transition_costs"][decision]

            decision_batch[batch_idx, i, decision] = 1.0
            decision_batch[batch_idx, i, 3] = (
                transition_cost["time_ns"] / 1e6
            )
            decision_batch[batch_idx, i, 4] = (
                transition_cost["power_nw"] / 1e9
            )

    return (
        torch.from_numpy(inst_batch).to(DEVICE),
        torch.from_numpy(decision_batch).to(DEVICE),
    )


def score_all_candidates(net, pml_feats, s, batch_size=BATCH_SIZE):
    candidates = list(itertools.product(range(3), repeat=s))
    scores = np.empty(len(candidates), dtype=np.float64)

    for start in range(0, len(candidates), batch_size):
        batch = candidates[start:start + batch_size]

        inst_tensor, decision_tensor = build_feature_tensors_batch(
            pml_feats,
            batch,
            s,
        )

        x_dummy = torch.zeros(
            (len(batch), s),
            dtype=torch.float32,
            device=DEVICE,
        )
        p_dummy = torch.zeros(
            (len(batch), 1),
            dtype=torch.float32,
            device=DEVICE,
        )

        with torch.no_grad():
            predictions = net(
                inst_tensor,
                decision_tensor,
                x_dummy,
                p_dummy,
                None,
            ).squeeze(-1)

        scores[start:start + len(batch)] = (
            predictions.cpu().numpy()
        )

    return candidates, scores


def rank_of_true_optimum(net, dp, program_dir):
    result_path = os.path.join(
        program_dir,
        "build",
        "optimize-result.json",
    )

    if not os.path.exists(result_path):
        return None

    with open(result_path) as f:
        data = json.load(f)

    optimum = data["ideal_scenario"]
    num_scenarios = data["num_scenarios"]
    s = len(ast.literal_eval(optimum))

    pml_feats = dp._parse_pml_features(
        {"program_dir": program_dir}
    )

    candidates, scores = score_all_candidates(
        net,
        pml_feats,
        s,
    )

    order = np.argsort(scores, kind="stable")

    ranked_candidates = [
        str(tuple(candidates[i]))
        for i in order
    ]

    try:
        rank = ranked_candidates.index(optimum)
    except ValueError:
        return None

    denominator = max(1, len(candidates) - 1)
    percentile = 100.0 * rank / denominator

    return {
        "program_dir": program_dir,
        "s": s,
        "num_scenarios": num_scenarios,
        "rank_of_true_optimum": rank,
        "percentile_rank_of_true_optimum": percentile,
    }


def main(args):
    import blo.params as params

    cfg = getattr(params, args.problem)
    program_dirs = cfg.program_dirs

    if args.limit is not None:
        program_dirs = program_dirs[:args.limit]

    net = load_scoring_net(args.ckpt)

    dp = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )

    print(
        f"Berechne den Netz-Rang des wahren Optimums "
        f"für {len(program_dirs)} Instanzen..."
    )

    rows = []

    for idx, program_dir in enumerate(program_dirs):
        result = rank_of_true_optimum(
            net,
            dp,
            program_dir,
        )

        if result is not None:
            result["inst_idx"] = idx
            rows.append(result)

        if (idx + 1) % 50 == 0:
            print(f"  {idx + 1}/{len(program_dirs)}")

    print(
        f"Fertig: {len(rows)}/{len(program_dirs)} Instanzen."
    )

    output_dir = os.path.dirname(args.out)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    fieldnames = [
        "inst_idx",
        "program_dir",
        "s",
        "num_scenarios",
        "rank_of_true_optimum",
        "percentile_rank_of_true_optimum",
    ]

    with open(args.out, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV gespeichert: {args.out}")

    scenario_ranges = [
        (1, 10),
        (10, 100),
        (100, 1000),
        (1000, 10000),
        (10000, float("inf")),
    ]

    print(
        "\nBucket-Zusammenfassung "
        "(Median/Mean des Perzentilrangs):"
    )

    for lower, upper in scenario_ranges:
        values = [
            row["percentile_rank_of_true_optimum"]
            for row in rows
            if lower <= row["num_scenarios"] < upper
        ]

        if not values:
            continue

        values = np.asarray(values)

        print(
            f"  [{lower:6} - "
            f"{upper if upper < float('inf') else 'inf':>6}] "
            f"n={len(values):3d}  "
            f"median={np.median(values):.2f}%  "
            f"mean={np.mean(values):.2f}%  "
            f"share<=1%={np.mean(values <= 1) * 100:.1f}%  "
            f"share<=10%={np.mean(values <= 10) * 100:.1f}%"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=str, default="watwa_v7")
    parser.add_argument("--ckpt", type=str, required=True)
    parser.add_argument(
        "--out",
        type=str,
        default="results/rank_histogram.csv",
    )
    parser.add_argument("--limit", type=int, default=None)

    args = parser.parse_args()
    main(args)