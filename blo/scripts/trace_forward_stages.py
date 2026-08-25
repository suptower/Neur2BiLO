"""
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


DEVICE = "cpu"


def load_scoring_net(ckpt_path):
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
    )

    if ckpt.get("use_inst_embedding_norm", False):
        net.inst_embedding_norm = ckpt["inst_embedding_norm"]

    net.to(DEVICE)
    net.eval()

    return net


def build_tensors(pml_feats, x, s):
    inst_rows = []

    for pf in pml_feats:
        inst_rows.append([
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

    inst_t = torch.tensor(
        np.array(inst_rows, dtype=np.float32)
    ).unsqueeze(0)

    dec_row = np.zeros((s, 5), dtype=np.float32)

    for i in range(s):
        xi = int(x[i])
        tc = pml_feats[i]["transition_costs"][xi]

        dec_row[i, xi] = 1.0
        dec_row[i, 3] = tc["time_ns"] / 1e6
        dec_row[i, 4] = tc["power_nw"] / 1e9

    dec_t = torch.tensor(dec_row).unsqueeze(0)

    return inst_t, dec_t


def trace_forward(net, inst_features, decision_features):
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

    if net.use_context:
        total_sum = torch.sum(combined, dim=1, keepdim=True)
        context_raw = total_sum - combined
        stages["context_raw_leaveoneout"] = context_raw.detach().clone()

        context = net.context_proj(context_raw)
        stages["context_projected"] = context.detach().clone()

        combined = torch.cat([combined, context], dim=2)
        stages["combined_plus_context"] = combined.detach().clone()

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

    base_pml_feats = dp._parse_pml_features(
        {"program_dir": args.program_dir}
    )

    if len(base_pml_feats) != args.s:
        raise ValueError(
            f"{args.program_dir} hat {len(base_pml_feats)} switch points, "
            f"erwartet {args.s}"
        )

    x = tuple(args.candidate)

    print(f"Basis-Instanz: {args.program_dir}, Kandidat x={x}\n")

    loop_bound_grid = np.linspace(10, 2500, args.n_steps)

    stages_over_grid = None

    for loop_bound in loop_bound_grid:
        variant = [dict(pf) for pf in base_pml_feats]
        variant[0] = dict(variant[0])
        variant[0]["loop_bound"] = loop_bound

        inst_t, dec_t = build_tensors(
            variant,
            x,
            args.s,
        )

        with torch.no_grad():
            stages = trace_forward(net, inst_t, dec_t)

        if stages_over_grid is None:
            stages_over_grid = {name: [] for name in stages}

        for name, value in stages.items():
            stages_over_grid[name].append(value.numpy())

    print(
        f"{'Stufe':<38}"
        f"{'Shape':<18}"
        f"{'max-min (gesamt)':>18}"
        f"{'max-min (nur SP0)':>20}"
    )
    print("-" * 94)

    for stage_name, values in stages_over_grid.items():
        values = np.stack(values, axis=0)

        flat = values.reshape(values.shape[0], -1)
        overall_range = (flat.max(axis=0) - flat.min(axis=0)).max()

        sp0_range = None
        if values.ndim >= 3 and values.shape[2] == args.s:
            sp0 = values[:, :, 0, ...]
            sp0_flat = sp0.reshape(sp0.shape[0], -1)
            sp0_range = (
                sp0_flat.max(axis=0) - sp0_flat.min(axis=0)
            ).max()

        if sp0_range is None:
            sp0_str = "-".rjust(18)
        else:
            sp0_str = f"{sp0_range:18.8f}"

        print(
            f"{stage_name:<38}"
            f"{str(values.shape[1:]):<18}"
            f"{overall_range:18.8f}"
            f"{sp0_str}"
        )

    print(
        "\nInterpretation: Die erste Stufe, deren max-min-Wert gegen 0 geht, "
        "während die vorherige Stufe noch eine deutliche Variation zeigt, "
        "ist die Stelle, an der die loop_bound-Information verloren geht."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True)
    parser.add_argument("--program-dir", type=str, required=True)
    parser.add_argument("--s", type=int, default=2)
    parser.add_argument(
        "--candidate",
        type=int,
        nargs="+",
        required=True,
        help="z.B. --candidate 2 1 fuer x=(2,1)",
    )
    parser.add_argument("--n-steps", type=int, default=20)

    args = parser.parse_args()
    main(args)