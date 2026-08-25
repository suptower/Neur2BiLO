"""
Usage:
    python -m blo.scripts.sensitivity_loop_bound \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt \
        --problem watwa_v7 \
        --program-dir programs/generated/gen_0019 \
        --s 2
"""

import argparse
import itertools

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


def build_feature_tensors_batch(pml_feats_variants, x, s):
    """Build input tensors for a fixed candidate across several instances."""
    batch_size = len(pml_feats_variants)
    inst_batch = np.zeros((batch_size, s, 15), dtype=np.float32)
    dec_batch = np.zeros((batch_size, s, 5), dtype=np.float32)

    for b, pml_feats in enumerate(pml_feats_variants):
        for i, pf in enumerate(pml_feats):
            inst_batch[b, i] = [
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

            xi = int(x[i])
            tc = pf["transition_costs"][xi]

            dec_batch[b, i, xi] = 1.0
            dec_batch[b, i, 3] = tc["time_ns"] / 1e6
            dec_batch[b, i, 4] = tc["power_nw"] / 1e9

    return (
        torch.from_numpy(inst_batch).to(DEVICE),
        torch.from_numpy(dec_batch).to(DEVICE),
    )


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

    print(f"Basis-Instanz: {args.program_dir}")
    print(
        "Original loop_bound je switch point: "
        f"{[pf['loop_bound'] for pf in base_pml_feats]}\n"
    )

    loop_bound_grid = np.linspace(10, 2500, args.n_steps)
    all_x = list(itertools.product(range(3), repeat=args.s))

    print(
        f"Variiere loop_bound an SWITCH POINT 0 von 10 bis 2500 "
        f"({args.n_steps} Schritte),"
    )
    print(
        "alle anderen Features (inkl. loop_bound an anderen switch points) "
        "bleiben fix.\n"
    )

    print(
        f"{'loop_bound':>12}"
        + "".join(f"  score[x={x}]" for x in all_x)
    )

    score_matrix = []

    for loop_bound in loop_bound_grid:
        variant = [dict(pf) for pf in base_pml_feats]
        variant[0] = dict(variant[0])
        variant[0]["loop_bound"] = loop_bound

        row_scores = []

        for x in all_x:
            inst_t, dec_t = build_feature_tensors_batch(
                [variant], x, args.s
            )

            x_dummy = torch.zeros(
                (1, args.s),
                dtype=torch.float32,
                device=DEVICE,
            )
            p_dummy = torch.zeros(
                (1, 1),
                dtype=torch.float32,
                device=DEVICE,
            )

            with torch.no_grad():
                pred = net(
                    inst_t,
                    dec_t,
                    x_dummy,
                    p_dummy,
                    None,
                ).squeeze().item()

            row_scores.append(pred)

        score_matrix.append(row_scores)

        print(
            f"{loop_bound:12.1f}"
            + "".join(f"{score:14.6f}" for score in row_scores)
        )

    score_matrix = np.array(score_matrix)

    print("\nVarianz jedes Kandidaten-Scores UEBER DEN loop_bound-GRID:")

    for i, x in enumerate(all_x):
        variance = np.var(score_matrix[:, i])
        score_range = score_matrix[:, i].max() - score_matrix[:, i].min()

        flag = ""
        if score_range < 1e-4:
            flag = " <-- praktisch konstant (Netz ignoriert loop_bound hier)"

        print(
            f"  x={x}: var={variance:.8f} "
            f"range={score_range:.8f}{flag}"
        )

    argmins = [all_x[np.argmin(row)] for row in score_matrix]
    unique_argmins = set(argmins)

    print(
        "\nArgmin-Kandidat aendert sich ueber den loop_bound-Grid: "
        f"{len(unique_argmins)} verschiedene(r) Gewinner: {unique_argmins}"
    )

    if len(unique_argmins) == 1:
        print(
            "  -> Das Netz waehlt UNABHAENGIG von loop_bound "
            "immer denselben Kandidaten."
        )
    else:
        print(
            "  -> Das Netz reagiert zumindest in der finalen "
            "Entscheidung auf loop_bound."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True)
    parser.add_argument("--problem", type=str, default="watwa_v7")
    parser.add_argument("--program-dir", type=str, required=True)
    parser.add_argument("--s", type=int, default=2)
    parser.add_argument("--n-steps", type=int, default=10)
    args = parser.parse_args()
    main(args)