"""
Usage:
    python -m blo.scripts.inspect_dead_features \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt
"""

import argparse

import torch
import torch.nn as nn


FEATURE_NAMES_15 = [
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
    "s_norm",
]

FEATURE_NAMES_20 = FEATURE_NAMES_15 + [
    "decision_onehot_0",
    "decision_onehot_1",
    "decision_onehot_2",
    "tc_time_ns",
    "tc_power_nw",
]


def find_linear_layers(module, prefix=""):
    layers = []

    for name, child in module.named_children():
        layer_name = f"{prefix}.{name}" if prefix else name

        if isinstance(child, nn.Linear):
            layers.append((layer_name, child))
        else:
            layers.extend(
                find_linear_layers(child, layer_name)
            )

    return layers


def main(args):
    ckpt = torch.load(
        args.ckpt,
        map_location="cpu",
        weights_only=False,
    )

    module_names = [
        name
        for name in ckpt
        if hasattr(ckpt[name], "state_dict")
    ]

    print(f"Checkpoint: {args.ckpt}")
    print(f"Enthaltene Submodule: {module_names}\n")

    for module_name in [
        "instance_decision_embedder",
        "final_instance_embedder",
        "value_predictor",
        "context_proj",
    ]:
        module = ckpt.get(module_name)

        if module is None:
            continue

        linear_layers = find_linear_layers(
            module,
            prefix=module_name,
        )

        for layer_name, layer in linear_layers:
            if layer.in_features not in (15, 20):
                continue

            print("=" * 70)
            print(
                f"{layer_name} "
                f"(Linear, in_features={layer.in_features}, "
                f"out_features={layer.out_features})"
            )
            print("=" * 70)

            feature_names = (
                FEATURE_NAMES_15
                if layer.in_features == 15
                else FEATURE_NAMES_20
            )

            weights = layer.weight.detach()
            column_norms = weights.norm(dim=0)
            total_norm = column_norms.sum().item()

            for idx, feature_name in enumerate(feature_names):
                norm = column_norms[idx].item()

                if total_norm > 0:
                    share = 100 * norm / total_norm
                else:
                    share = 0.0

                marker = "  (sehr klein)" if norm < 1e-4 else ""

                print(
                    f"  [{idx:2d}] "
                    f"{feature_name:<18} "
                    f"col_norm={norm:10.6f}  "
                    f"({share:5.1f}%){marker}"
                )

            print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True)

    args = parser.parse_args()
    main(args)
