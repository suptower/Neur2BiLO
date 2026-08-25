"""
Usage:
    python -m blo.scripts.check_dead_at_init --problem watwa_v7
"""

import argparse
import ast
import collections
import json
import os

import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import FeedForwardBase


DEVICE = "cpu"


def build_inst_tensor(pml_feats, s):
    features = [
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

    return torch.tensor(features, dtype=torch.float32).unsqueeze(0)


def main(args):
    import blo.params as params

    problem_config = getattr(params, args.problem)

    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )

    seed_results = []

    for seed in range(args.n_seeds):
        torch.manual_seed(seed)

        instance_decision_embedder = FeedForwardBase(
            input_dim=15,
            hidden_dims=[128],
            output_dim=64,
            name="instance_decision_embedder",
        )
        final_instance_embedder = FeedForwardBase(
            input_dim=64,
            hidden_dims=[128],
            output_dim=32,
            name="final_instance_embedder",
        )

        instance_decision_embedder.eval()
        final_instance_embedder.eval()

        final_input_layer = final_instance_embedder.net[0]
        dead_by_s = collections.defaultdict(list)

        n_checked = 0

        for program_dir in problem_config.program_dirs:
            result_path = os.path.join(
                program_dir, "build", "optimize-result.json"
            )
            if not os.path.exists(result_path):
                continue

            with open(result_path) as f:
                result = json.load(f)

            s = len(ast.literal_eval(result["ideal_scenario"]))

            pml_feats = preproc._parse_pml_features(
                {"program_dir": program_dir}
            )
            inst_t = build_inst_tensor(pml_feats, s)

            with torch.no_grad():
                emb = instance_decision_embedder(inst_t)
                agg = torch.sum(emb, dim=1)
                logits = final_input_layer(agg)

            dead_frac = (logits <= 0).float().mean().item()
            dead_by_s[s].append(dead_frac)

            n_checked += 1
            if args.limit is not None and n_checked >= args.limit:
                break

        seed_result = {
            s: np.mean(values) * 100
            for s, values in dead_by_s.items()
        }
        seed_results.append(seed_result)

        values = ", ".join(
            f"s={s}: {value:.1f}%"
            for s, value in sorted(seed_result.items())
        )
        print(f"Seed {seed}: {values}")

    print(
        f"\nMittelwert ueber {args.n_seeds} zufaellige Initialisierungen "
        "(Tot-Anteil am final_instance_embedder-Eingang):"
    )

    all_s = sorted({s for result in seed_results for s in result})

    for s in all_s:
        values = [result[s] for result in seed_results if s in result]
        print(
            f"  s={s:2d}: {np.mean(values):5.1f}% "
            f"(min={np.min(values):.1f}%, max={np.max(values):.1f}%)"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem", type=str, default="watwa_v7")
    parser.add_argument("--n-seeds", type=int, default=5)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Nur die ersten N Instanzen pruefen",
    )

    args = parser.parse_args()
    main(args)
