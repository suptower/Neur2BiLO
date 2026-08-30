"""
Multi-scenario LP domain reduction and candidate pruning.
Parses pregenerated gurobi-model-*.lp files, applies surrogate model scoring,
and generates reduced LP models for accelerated Gurobi MILP solving.
"""

import glob
import itertools
import os
import re

import gurobipy as gp
import numpy as np
import torch

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from blo.models.models import SetInstanceEncodingNetwork

DEVICE = torch.device("cpu")


# ---------------------------------------------------------------------------
# 1. LP Parsing and Multi-File Scenario Extraction
# ---------------------------------------------------------------------------

def load_lp_files(program_dir):
    """
    Parses and concatenates scenario blocks across split gurobi-model-*.lp files.
    Returns the shared preamble lines and a mapping from unique global indices to scenario blocks.
    """
    lp_files = sorted(
        glob.glob(os.path.join(program_dir, "gurobi-model-*.lp")),
        key=lambda p: int(re.search(r"gurobi-model-(\d+)\.lp", p).group(1)),
    )
    if not lp_files:
        raise FileNotFoundError(f"No gurobi-model-*.lp files found in {program_dir}")

    preamble = None
    scenario_blocks = {}
    global_idx = 0

    for fp in lp_files:
        with open(fp) as f:
            lines = f.readlines()

        first_scenario_idx = next(
            (i for i, l in enumerate(lines) if l.strip().startswith("Scenario ")),
            len(lines),
        )
        if preamble is None:
            preamble = lines[:first_scenario_idx]

        i = first_scenario_idx
        while i < len(lines):
            m = re.match(r"Scenario (\d+)", lines[i].strip())
            if not m:
                i += 1
                continue

            start = i
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("Scenario "):
                i += 1

            scenario_blocks[global_idx] = lines[start:i]
            global_idx += 1

    return preamble, scenario_blocks


def parse_scenario_x_tuples(scenario_blocks, s):
    """Extracts the s-dimensional decision vector corresponding to each scenario block."""
    result = {}
    for idx, lines in scenario_blocks.items():
        fixed = set()
        for l in lines:
            m = re.match(r"\s*cc_alt_vars_(\d+)\s*<=\s*0", l)
            if m:
                fixed.add(int(m.group(1)))

        x = []
        for sp in range(s):
            free = [a for a in range(3) if (sp * 3 + a) not in fixed]
            assert len(free) == 1, f"Scenario {idx}, switch point {sp}: expected 1 free choice, got {free}"
            x.append(free[0])

        result[idx] = tuple(x)
    return result


def write_reduced_lp(preamble, scenario_blocks, keep_scenario_ids, out_path):
    """Writes a new LP file containing only the selected scenario blocks."""
    with open(out_path, "w") as f:
        f.writelines(preamble)
        for new_idx, old_idx in enumerate(sorted(keep_scenario_ids)):
            block = scenario_blocks[old_idx]
            body = block[1:]
            if body and body[-1].strip() == "End":
                body = body[:-1]
            f.write(f"Scenario {new_idx}\n")
            f.writelines(body)
        f.write("End\n")


# ---------------------------------------------------------------------------
# 2. Network Loading
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# 3. Feature Construction and Scoring
# ---------------------------------------------------------------------------

def build_feature_tensors(pml_feats, x, s):
    """Constructs input feature tensors for a single candidate decision vector."""
    inst_feats = []
    dec_feats = []

    for i in range(s):
        pf = pml_feats[i]
        inst_feats.append([
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
        xi = int(x[i])
        tc = pf["transition_costs"][xi]
        dec_feats.append([
            float(xi == 0),
            float(xi == 1),
            float(xi == 2),
            tc["time_ns"] / 1e6,
            tc["power_nw"] / 1e9,
        ])

    inst_t = torch.tensor([inst_feats], dtype=torch.float32, device=DEVICE)
    dec_t = torch.tensor([dec_feats], dtype=torch.float32, device=DEVICE)
    return inst_t, dec_t


def score_x(net, pml_feats, x, s):
    """Computes the surrogate model predicted objective value for decision vector x."""
    inst_t, dec_t = build_feature_tensors(pml_feats, x, s)
    x_dummy = torch.zeros((1, s), dtype=torch.float32, device=DEVICE)
    p_dummy = torch.zeros((1, 1), dtype=torch.float32, device=DEVICE)

    with torch.no_grad():
        pred = net(inst_t, dec_t, x_dummy, p_dummy, None)
    return pred.item()


# ---------------------------------------------------------------------------
# 4. Coordinate-Wise Greedy Pruning
# ---------------------------------------------------------------------------

def greedy_prune(net, pml_feats, s, keep_per_switch_point=1, refine_iters=2):
    """Performs coordinate descent refinement and returns the Cartesian product of top choices."""
    x_ref = [1] * s

    for _ in range(refine_iters):
        for sp in range(s):
            scores = []
            for alt in range(3):
                x_try = list(x_ref)
                x_try[sp] = alt
                scores.append(score_x(net, pml_feats, x_try, s))
            x_ref[sp] = int(np.argmin(scores))

    kept_per_sp = []
    for sp in range(s):
        scored = []
        for alt in range(3):
            x_try = list(x_ref)
            x_try[sp] = alt
            scored.append((alt, score_x(net, pml_feats, x_try, s)))
        scored.sort(key=lambda t: t[1])
        kept_per_sp.append([a for a, _ in scored[:keep_per_switch_point]])

    return list(itertools.product(*kept_per_sp))


# ---------------------------------------------------------------------------
# 5. Standalone Smoke Test
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    program_dir = "programs/generated/gen_0000"
    ckpt_path = "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt"
    s = 2

    preamble, scenario_blocks = load_lp_files(program_dir)
    x_tuples = parse_scenario_x_tuples(scenario_blocks, s)
    print(f"Scenarios parsed: {len(x_tuples)}")

    net = load_scoring_net(ckpt_path)
    dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both", device=DEVICE)
    pml_feats = dp._parse_pml_features({"program_dir": program_dir})

    kept = greedy_prune(net, pml_feats, s, keep_per_switch_point=1)
    print(f"Kept candidate decisions: {kept}")

    true_optimum = (2, 0)
    print(f"True optimum retained: {true_optimum in kept}")

    x_to_id = {v: k for k, v in x_tuples.items()}
    for x, idx in x_to_id.items():
        print(f"  x={x} -> score={score_x(net, pml_feats, x, s):.6f}")

    keep_ids = [x_to_id[x] for x in kept if x in x_to_id]
    out_lp = "gen_0000_pruned.lp"
    write_reduced_lp(preamble, scenario_blocks, keep_ids, out_lp)
    print(f"Wrote {out_lp} with {len(keep_ids)} scenarios.")

    model = gp.read(out_lp)
    model.setParam("OutputFlag", 0)
    model.optimize()
    print(f"Pruned solve objective: {model.ObjVal:.6f} | Solve time: {model.Runtime:.4f} s")
    model.dispose()