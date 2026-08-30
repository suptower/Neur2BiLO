"""
Analyzes layer activation scales and dead neuron fractions across switch-point sizes (s).

Usage:
    python -m blo.scripts.check_scale_mismatch \
        --problem watwa_v7 \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt
"""

import argparse
import ast
import json
import os
from collections import defaultdict

import numpy as np
import torch

import blo.params as blo_params
from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = "cpu"


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


def build_inst_tensor(pml_feats, s):
    """Constructs the normalized instance feature tensor for a program instance."""
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


def get_final_embedder_in_layer(net):
    """Extracts the first linear layer from final_instance_embedder."""
    for module in net.final_instance_embedder.modules():
        if isinstance(module, torch.nn.Linear):
            return module
    raise RuntimeError("No Linear layer found in final_instance_embedder.")


def get_inst_embedder_in_layer(net):
    """Extracts the 15-feature input linear layer from instance_decision_embedder."""
    for module in net.instance_decision_embedder.modules():
        if isinstance(module, torch.nn.Linear) and module.in_features == 15:
            return module
    raise RuntimeError("No Linear(in_features=15) layer found in instance_decision_embedder.")


def main(args):
    problem_config = getattr(blo_params, args.problem)

    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )
    net = load_scoring_net(args.ckpt, args.problem)

    has_norm = getattr(net, "use_inst_embedding_norm", False)
    status_str = "enabled" if has_norm else "disabled (legacy checkpoint without LayerNorm)"
    print(f"Checkpoint LayerNorm status: {status_str}\n")

    final_input_layer = get_final_embedder_in_layer(net)
    W = final_input_layer.weight.detach()
    b = (
        final_input_layer.bias.detach()
        if final_input_layer.bias is not None
        else torch.zeros(final_input_layer.out_features)
    )

    inst_input_layer = get_inst_embedder_in_layer(net)
    W0 = inst_input_layer.weight.detach()
    b0 = (
        inst_input_layer.bias.detach()
        if inst_input_layer.bias is not None
        else torch.zeros(inst_input_layer.out_features)
    )

    by_s = defaultdict(
        lambda: {
            "h1_agg_norm": [],
            "dead_frac_layer1": [],
            "dead_frac_sum": [],
            "dead_frac_mean": [],
        }
    )

    n_processed = 0

    for program_dir in problem_config.program_dirs:
        result_path = os.path.join(program_dir, "build", "optimize-result.json")
        if not os.path.exists(result_path):
            continue

        with open(result_path) as f:
            result = json.load(f)

        s = len(ast.literal_eval(result["ideal_scenario"]))
        pml_feats = preproc._parse_pml_features({"program_dir": program_dir})
        inst_t = build_inst_tensor(pml_feats, s)

        with torch.no_grad():
            pre_h1 = inst_t @ W0.T + b0
            h1 = net.instance_decision_embedder(inst_t)

            h1_agg_sum = net.aggregate(h1, "sum", None)
            h1_agg_mean = h1_agg_sum / s

            if getattr(net, "use_inst_embedding_norm", False):
                h1_agg_sum = net.inst_embedding_norm(h1_agg_sum)
                h1_agg_mean = net.inst_embedding_norm(h1_agg_mean)

            pre_sum = h1_agg_sum @ W.T + b
            pre_mean = h1_agg_mean @ W.T + b

        dead_frac_layer1 = (pre_h1 <= 0).float().mean().item()
        dead_frac_sum = (pre_sum <= 0).float().mean().item()
        dead_frac_mean = (pre_mean <= 0).float().mean().item()

        by_s[s]["h1_agg_norm"].append(h1_agg_sum.norm().item())
        by_s[s]["dead_frac_layer1"].append(dead_frac_layer1)
        by_s[s]["dead_frac_sum"].append(dead_frac_sum)
        by_s[s]["dead_frac_mean"].append(dead_frac_mean)

        n_processed += 1

    print(f"Processed {n_processed} instances.\n")
    header = (
        f"{'s':>4}"
        f"{'n':>6}"
        f"{'Dead% Layer1':>16}"
        f"{'||h1_agg||':>14}"
        f"{'Dead% Final (Sum)':>20}"
        f"{'Dead% Final (Mean)':>22}"
    )
    print(header)
    print("-" * len(header))

    for s in sorted(by_s):
        values = by_s[s]
        n = len(values["h1_agg_norm"])

        norm_mean = np.mean(values["h1_agg_norm"])
        dead_l1_mean = np.mean(values["dead_frac_layer1"]) * 100
        dead_sum_mean = np.mean(values["dead_frac_sum"]) * 100
        dead_mean_mean = np.mean(values["dead_frac_mean"]) * 100

        print(
            f"{s:>4}"
            f"{n:>6}"
            f"{dead_l1_mean:>15.1f}%"
            f"{norm_mean:>14.4f}"
            f"{dead_sum_mean:>19.1f}%"
            f"{dead_mean_mean:>21.1f}%"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check activation norm scaling and dead neuron percentages across switch points."
    )
    parser.add_argument("--problem", type=str, default="watwa_v7", help="Problem configuration key.")
    parser.add_argument("--ckpt", type=str, required=True, help="Path to model checkpoint (.pt).")

    args = parser.parse_args()
    main(args)