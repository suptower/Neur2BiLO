"""
Usage:
    python -m blo.scripts.inspect_dead_relu \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt \
        --program-dir programs/generated/gen_0019 \
        --s 2
"""

import argparse

import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork


DEVICE = torch.device("cpu")


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


def build_inst_tensor(pml_feats, s):
    rows = []

    for pf in pml_feats:
        rows.append([
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

    features = np.asarray(rows, dtype=np.float32)

    return torch.from_numpy(features).unsqueeze(0).to(DEVICE)


def find_input_layer(net):
    for name, module in net.instance_decision_embedder.named_modules():
        if isinstance(module, torch.nn.Linear) and module.in_features == 15:
            return name, module

    raise RuntimeError(
        "Keine Linear-Schicht mit 15 Eingangsfeatures "
        "in instance_decision_embedder gefunden."
    )


def main(args):
    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )
    net = load_scoring_net(args.ckpt)

    pml_feats = preproc._parse_pml_features(
        {"program_dir": args.program_dir}
    )

    if len(pml_feats) != args.s:
        raise ValueError(
            f"{args.program_dir} hat {len(pml_feats)} Switch Points, "
            f"erwartet werden {args.s}."
        )

    layer_name, first_linear = find_input_layer(net)

    print(
        f"Analysierte Schicht: "
        f"instance_decision_embedder.{layer_name} "
        f"(in={first_linear.in_features}, "
        f"out={first_linear.out_features})\n"
    )

    captured = {}

    def capture_activation(_, __, output):
        captured["pre_activation"] = output.detach()

    hook = first_linear.register_forward_hook(capture_activation)

    loop_bounds = np.linspace(
        10,
        2500,
        args.n_steps,
    )

    n_hidden = first_linear.out_features
    pre_activations = np.empty(
        (args.n_steps, args.s, n_hidden),
        dtype=np.float32,
    )

    try:
        for step, loop_bound in enumerate(loop_bounds):
            current_feats = [dict(pf) for pf in pml_feats]
            current_feats[0] = dict(current_feats[0])
            current_feats[0]["loop_bound"] = loop_bound

            inst_tensor = build_inst_tensor(
                current_feats,
                args.s,
            )

            with torch.no_grad():
                net.instance_decision_embedder(inst_tensor)

            pre_activations[step] = (
                captured["pre_activation"]
                .squeeze(0)
                .cpu()
                .numpy()
            )
    finally:
        hook.remove()

    # Nur Switch Point 0 wird variiert.
    sp0 = pre_activations[:, 0, :]

    always_off = np.all(sp0 <= 0, axis=0)
    always_on = np.all(sp0 > 0, axis=0)
    sign_changes = ~(always_off | always_on)

    n_dead = always_off.sum()
    n_always_on = always_on.sum()
    n_variable = sign_changes.sum()

    print(
        f"Von {n_hidden} Neuronen der ersten Schicht "
        f"(Switch Point 0, {args.n_steps} loop_bound-Werte):"
    )
    print(
        f"  Immer <= 0:              "
        f"{n_dead:4d} ({100 * n_dead / n_hidden:.1f}%)"
    )
    print(
        f"  Immer > 0:               "
        f"{n_always_on:4d} ({100 * n_always_on / n_hidden:.1f}%)"
    )
    print(
        f"  Vorzeichenwechsel:       "
        f"{n_variable:4d} ({100 * n_variable / n_hidden:.1f}%)"
    )

    activation_ranges = sp0.max(axis=0) - sp0.min(axis=0)

    n_flat = np.sum(activation_ranges < 1e-4)

    print(
        f"\nAktivierungs-Spannweite < 1e-4: "
        f"{n_flat}/{n_hidden} "
        f"({100 * n_flat / n_hidden:.1f}%)"
    )
    print(
        f"Maximale Spannweite:   "
        f"{activation_ranges.max():.6f}"
    )
    print(
        f"Median der Spannweiten: "
        f"{np.median(activation_ranges):.6f}"
    )

    if (
        n_dead / n_hidden > 0.9
        or activation_ranges.max() < 1e-3
    ):
        print(
            "\n-> Die erste Schicht ist in diesem "
            "Eingabebereich weitgehend inaktiv bzw. "
            "reagiert kaum auf loop_bound."
        )
    else:
        print(
            "\n-> Die erste Schicht reagiert zumindest teilweise "
            "auf loop_bound. Die beobachtete Insensitivität "
            "entsteht daher vermutlich in einer späteren Schicht."
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ckpt", type=str, required=True)
    parser.add_argument("--program-dir", type=str, required=True)
    parser.add_argument("--s", type=int, default=2)
    parser.add_argument("--n-steps", type=int, default=20)

    args = parser.parse_args()
    main(args)