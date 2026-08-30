"""
Traces intermediate feature representations through network stages across loop_bound sweeps.

Usage:
    python -m blo.scripts.trace_forward_stages \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt \
        --program-dir programs/generated/gen_0019 \
        --s 2 \
        --candidate 2 1
"""

import argparse

import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = torch.device("cpu")


def load_scoring_net(ckpt_path):
    """Loads and reconstructs a SetInstanceEncodingNetwork from a saved checkpoint."""
    ckpt = torch.load(ckpt_path, map_location=DEVICE, weights_only=False)

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


def build_tensors(pml_feats, x, s):
    """Builds instance and decision tensors for a given candidate configuration."""
    inst_rows = [
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

    inst_t = torch.tensor(np.array(inst_rows, dtype=np.float32)).unsqueeze(0).to(DEVICE)

    dec_row = np.zeros((s, 5), dtype=np.float32)
    for i in range(s):
        xi = int(x[i])
        tc = pml_feats[i]["transition_costs"][xi]
        dec_row[i, xi] = 1.0
        dec_row[i, 3] = tc["time_ns"] / 1e6
        dec_row[i, 4] = tc["power_nw"] / 1e9

    dec_t = torch.tensor(dec_row, dtype=torch.float32).unsqueeze(0).to(DEVICE)
    return inst_t, dec_t


def trace_forward(net, inst_features, decision_features):
    """Executes a forward pass while capturing activations at each intermediate stage."""
    stages = {}

    h1 = net.instance_decision_embedder(inst_features)
    stages["h1_per_switchpoint_embedding"] = h1.detach().clone()

    h1_agg = net.aggregate(h1, net.agg_type, None)
    stages["h1_agg_summed_over_switchpoints"] = h1_agg.detach().clone()

    if getattr(net, "use_inst_embedding_norm", False):
        h1_agg = net.inst_embedding_norm(h1_agg)
        stages["h1_agg_after_layernorm"] = h1_agg.detach().clone()

    h2 = net.final_instance_embedder(h1_agg)
    stages["h2_final_instance_embedding"] = h2.detach().clone()

    h2 = h2.reshape(h2.shape[0], h2.shape[1])
    h2_repeated = h2[:, None, :].repeat(1, inst_features.shape[1], 1)

    combined = torch.cat([decision_features, h2_repeated], dim=2)
    stages["combined_decision_plus_instctx"] = combined.detach().clone()

    extra_features = []

    if net.use_context:
        total_sum = torch.sum(combined, dim=1, keepdim=True)
        context_raw = total_sum - combined
        stages["context_raw_leaveoneout"] = context_raw.detach().clone()

        context = net.context_proj(context_raw)
        stages["context_projected"] = context.detach().clone()
        extra_features.append(context)

    if getattr(net, "use_attention", False):
        attn_input = net.attention_proj(combined)
        attn_out, _ = net.attention(attn_input, attn_input, attn_input, need_weights=False)
        stages["attention_output"] = attn_out.detach().clone()
        extra_features.append(attn_out)

    if extra_features:
        combined = torch.cat([combined] + extra_features, dim=2)
        stages["combined_plus_interactions"] = combined.detach().clone()

    pred_per_decision = net.value_predictor(combined)
    stages["pred_per_decision"] = pred_per_decision.detach().clone()

    pred_per_decision = pred_per_decision.reshape(
        pred_per_decision.shape[0],
        pred_per_decision.shape[1],
    )

    out = torch.sum(pred_per_decision, dim=1)
    stages["out_final_score"] = out.detach().clone()

    return stages


def main(args):
    dp = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )
    net = load_scoring_net(args.ckpt)

    base_pml_feats = dp._parse_pml_features({"program_dir": args.program_dir})
    if len(base_pml_feats) != args.s:
        raise ValueError(
            f"{args.program_dir} has {len(base_pml_feats)} switch points, expected {args.s}."
        )

    x = tuple(args.candidate)
    print(f"Base instance: {args.program_dir}, Candidate x={x}\n")

    loop_bound_grid = np.linspace(10, 2500, args.n_steps)
    stages_over_grid = None

    for loop_bound in loop_bound_grid:
        variant = [dict(pf) for pf in base_pml_feats]
        variant[0] = dict(variant[0])
        variant[0]["loop_bound"] = loop_bound

        inst_t, dec_t = build_tensors(variant, x, args.s)

        with torch.no_grad():
            stages = trace_forward(net, inst_t, dec_t)

        if stages_over_grid is None:
            stages_over_grid = {name: [] for name in stages}

        for name, value in stages.items():
            stages_over_grid[name].append(value.cpu().numpy())

    header = (
        f"{'Stage':<38}"
        f"{'Shape':<18}"
        f"{'Max-Min (Overall)':>18}"
        f"{'Max-Min (SP0 Only)':>20}"
    )
    print(header)
    print("-" * len(header))

    for stage_name, values in stages_over_grid.items():
        values = np.stack(values, axis=0)
        flat = values.reshape(values.shape[0], -1)
        overall_range = float((flat.max(axis=0) - flat.min(axis=0)).max())

        sp0_range = None
        if values.ndim >= 3 and values.shape[2] == args.s:
            sp0 = values[:, :, 0, ...]
            sp0_flat = sp0.reshape(sp0.shape[0], -1)
            sp0_range = float((sp0_flat.max(axis=0) - sp0_flat.min(axis=0)).max())

        sp0_str = "-".rjust(20) if sp0_range is None else f"{sp0_range:20.8f}"

        print(
            f"{stage_name:<38}"
            f"{str(values.shape[1:]):<18}"
            f"{overall_range:18.8f}"
            f"{sp0_str}"
        )

    print(
        "\nDiagnostic Note: The first stage where the max-min range drops to near-zero "
        "while previous stages exhibit variation indicates where loop_bound signal is lost."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Trace intermediate layer representations across a loop_bound sweep."
    )
    parser.add_argument("--ckpt", type=str, required=True, help="Path to model checkpoint (.pt).")
    parser.add_argument("--program-dir", type=str, required=True, help="Path to program directory.")
    parser.add_argument("--s", type=int, default=2, help="Expected switch-point count.")
    parser.add_argument(
        "--candidate",
        type=int,
        nargs="+",
        required=True,
        help="Candidate decision configuration (e.g. --candidate 2 1 for x=(2,1)).",
    )
    parser.add_argument("--n-steps", type=int, default=20, help="Number of loop_bound sample steps.")

    args = parser.parse_args()
    main(args)