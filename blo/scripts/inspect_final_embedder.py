"""
Usage:
    python -m blo.scripts.inspect_final_embedder \
        --ckpt data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt \
        --program-dir programs/generated/gen_0019 \
        --s 2 \
        --candidate 2 1
"""

import argparse

import numpy as np
import torch
import torch.nn as nn

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


def build_tensors(pml_feats, x, s):
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
    inst_tensor = torch.from_numpy(inst_features).unsqueeze(0)

    decisions = np.zeros((s, 5), dtype=np.float32)

    for i in range(s):
        decision = int(x[i])
        transition_cost = pml_feats[i]["transition_costs"][decision]

        decisions[i, decision] = 1.0
        decisions[i, 3] = transition_cost["time_ns"] / 1e6
        decisions[i, 4] = transition_cost["power_nw"] / 1e9

    decision_tensor = torch.from_numpy(decisions).unsqueeze(0)

    return (
        inst_tensor.to(DEVICE),
        decision_tensor.to(DEVICE),
    )


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
    preproc = WatwaDataPreprocessor(
        model_type="inst_encoder",
        approx_type="both",
        device=DEVICE,
    )
    net = load_scoring_net(args.ckpt)

    print("=" * 78)
    print("CHECK A: Gewichtsnormen im final_instance_embedder")
    print("=" * 78)

    linear_layers = find_linear_layers(
        net.final_instance_embedder,
        prefix="final_instance_embedder",
    )

    for layer_name, layer in linear_layers:
        weights = layer.weight.detach()

        column_norms = weights.norm(dim=0)
        row_norms = weights.norm(dim=1)

        print(
            f"\n{layer_name} "
            f"(in={layer.in_features}, out={layer.out_features})"
        )
        print(
            f"  Input-Spalten: "
            f"min={column_norms.min():.6f}  "
            f"median={column_norms.median():.6f}  "
            f"max={column_norms.max():.6f}"
        )

        n_dead_in = (column_norms < 1e-4).sum().item()
        print(
            f"  Spalten mit Norm < 1e-4: "
            f"{n_dead_in}/{layer.in_features}"
        )

        print(
            f"  Output-Neuronen: "
            f"min={row_norms.min():.6f}  "
            f"median={row_norms.median():.6f}  "
            f"max={row_norms.max():.6f}"
        )

        n_dead_out = (row_norms < 1e-4).sum().item()
        print(
            f"  Output-Neuronen mit Norm < 1e-4: "
            f"{n_dead_out}/{layer.out_features}"
        )

        if layer.bias is not None:
            bias = layer.bias.detach()
            print(
                f"  Bias: "
                f"min={bias.min():.6f}  "
                f"median={bias.median():.6f}  "
                f"max={bias.max():.6f}"
            )

    print(f"\n{'=' * 78}")
    print("CHECK B: Bottleneck-Aktivierungen über loop_bound-Sweep")
    print("=" * 78)

    linear_layers = find_linear_layers(
        net.final_instance_embedder,
        prefix="final_instance_embedder",
    )

    if not linear_layers:
        print("Keine Linear-Schicht in final_instance_embedder gefunden.")
        return

    first_linear_name, first_linear = linear_layers[0]

    print(
        f"\nAnalysierte Schicht: {first_linear_name} "
        f"(in={first_linear.in_features}, "
        f"out={first_linear.out_features})"
    )

    captured = {}

    def capture_activation(_, __, output):
        captured["pre_activation"] = output.detach()

    hook = first_linear.register_forward_hook(capture_activation)

    base_pml_feats = preproc._parse_pml_features(
        {"program_dir": args.program_dir}
    )

    if len(base_pml_feats) != args.s:
        hook.remove()
        raise ValueError(
            f"{args.program_dir} hat {len(base_pml_feats)} Switch Points, "
            f"erwartet werden {args.s}."
        )

    candidate = tuple(args.candidate)

    if len(candidate) != args.s:
        hook.remove()
        raise ValueError(
            f"Der Kandidat muss genau {args.s} Entscheidungen enthalten."
        )

    loop_bounds = np.linspace(
        10,
        2500,
        args.n_steps,
    )

    n_hidden = first_linear.out_features
    pre_activations = np.empty(
        (args.n_steps, n_hidden),
        dtype=np.float32,
    )

    try:
        for step, loop_bound in enumerate(loop_bounds):
            current_feats = [dict(pf) for pf in base_pml_feats]
            current_feats[0] = dict(current_feats[0])
            current_feats[0]["loop_bound"] = loop_bound

            inst_tensor, decision_tensor = build_tensors(
                current_feats,
                candidate,
                args.s,
            )

            with torch.no_grad():
                h1 = net.instance_decision_embedder(inst_tensor)
                h1_agg = net.aggregate(
                    h1,
                    net.agg_type,
                    None,
                )
                net.final_instance_embedder(h1_agg)

            pre_activations[step] = (
                captured["pre_activation"]
                .squeeze(0)
                .cpu()
                .numpy()
            )
    finally:
        hook.remove()

    always_off = np.all(pre_activations <= 0, axis=0)
    always_on = np.all(pre_activations > 0, axis=0)
    sign_changes = ~(always_off | always_on)

    n_dead = always_off.sum()
    n_always_on = always_on.sum()
    n_variable = sign_changes.sum()

    print(
        f"\nVon {n_hidden} Bottleneck-Neuronen "
        f"über {args.n_steps} loop_bound-Werte:"
    )
    print(
        f"  Immer <= 0: "
        f"{n_dead:4d} ({100 * n_dead / n_hidden:.1f}%)"
    )
    print(
        f"  Immer > 0:  "
        f"{n_always_on:4d} ({100 * n_always_on / n_hidden:.1f}%)"
    )
    print(
        f"  Vorzeichenwechsel: "
        f"{n_variable:4d} ({100 * n_variable / n_hidden:.1f}%)"
    )

    activation_ranges = (
        pre_activations.max(axis=0)
        - pre_activations.min(axis=0)
    )

    n_flat = (activation_ranges < 1e-4).sum()

    print(
        f"\nAktivierungs-Spannweite < 1e-4: "
        f"{n_flat}/{n_hidden} "
        f"({100 * n_flat / n_hidden:.1f}%)"
    )
    print(
        f"Maximale Spannweite: "
        f"{activation_ranges.max():.8f}"
    )

    if n_flat == n_hidden:
        print(
            "\n-> Alle Bottleneck-Neuronen bleiben für diesen "
            "Input praktisch konstant."
        )
    elif n_dead / n_hidden > 0.9:
        print(
            "\n-> Der Großteil der Bottleneck-Neuronen ist "
            "durch die ReLU dauerhaft deaktiviert."
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
    )
    parser.add_argument("--n-steps", type=int, default=20)

    args = parser.parse_args()
    main(args)