import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Pruning prototype v2 — corrected against actual model/data-pipeline code.
Works directly on the pregenerated gen_xxxx/gurobi-model-*.lp files,
no WatwaOS/make invocation needed.
"""
import os
import re
import glob
import itertools
import torch
import gurobipy as gp
from blo.models.models import SetInstanceEncodingNetwork
from blo.data_preprocessor.watwa import WatwaDataPreprocessor

DEVICE = torch.device("cpu")

# ------------------------------------------------------------------
# 1. .lp parsing (multi-file aware)
# ------------------------------------------------------------------

def load_lp_files(program_dir):
    lp_files = sorted(
        glob.glob(os.path.join(program_dir, "gurobi-model-*.lp")),
        key=lambda p: int(re.search(r"gurobi-model-(\d+)\.lp", p).group(1)),
    )
    if not lp_files:
        raise FileNotFoundError(f"No gurobi-model-*.lp found in {program_dir}")

    preamble = None
    scenario_blocks = {}
    global_idx = 0  # each split file restarts its own "Scenario N" label at 0,
                     # so we assign our own globally unique keys instead
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
            assert len(free) == 1, f"scenario {idx}, sp {sp}: expected 1 free alt, got {free}"
            x.append(free[0])
        result[idx] = tuple(x)
    return result


def write_reduced_lp(preamble, scenario_blocks, keep_scenario_ids, out_path):
    with open(out_path, "w") as f:
        f.writelines(preamble)
        for new_idx, old_idx in enumerate(sorted(keep_scenario_ids)):
            block = scenario_blocks[old_idx]
            body = block[1:]
            # strip a trailing 'End' if this happened to be the original last scenario
            if body and body[-1].strip() == "End":
                body = body[:-1]
            f.write(f"Scenario {new_idx}\n")
            f.writelines(body)
        f.write("End\n")  # always write exactly one, at the very end


# ------------------------------------------------------------------
# 2. Network loading — submodules are saved as full nn.Module objects
# ------------------------------------------------------------------

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
    )
    net.to(DEVICE)
    net.eval()
    return net


# ------------------------------------------------------------------
# 3. Feature extraction — mirrors get_inst_encoder_dataset exactly
# ------------------------------------------------------------------

def build_feature_tensors(pml_feats, x, s):
    inst_feats, dec_feats = [], []
    for i in range(s):
        pf = pml_feats[i]
        inst_feats.append([
            pf["time_ns_high"] / 1e6, pf["time_ns_low"] / 1e6,
            pf["power_nw_high"] / 1e9, pf["power_nw_low"] / 1e9,
            pf["energy_high"] / 1e15, pf["energy_low"] / 1e15,
            pf["energy_ratio"], pf["time_ratio"] / 100.0,
            pf["is_uart"], pf["loop_bound"] / 2500,
            pf["position_norm"], pf["position_abs"] / 20,
            pf["tc_ratio_x1"], pf["tc_ratio_x2"], s / 20,
        ])
        xi = int(x[i])
        tc = pf["transition_costs"][xi]
        dec_feats.append([
            float(xi == 0), float(xi == 1), float(xi == 2),
            tc["time_ns"] / 1e6, tc["power_nw"] / 1e9,
        ])
    inst_t = torch.tensor([inst_feats], dtype=torch.float32, device=DEVICE)
    dec_t = torch.tensor([dec_feats], dtype=torch.float32, device=DEVICE)
    return inst_t, dec_t


def score_x(net, pml_feats, x, s):
    inst_t, dec_t = build_feature_tensors(pml_feats, x, s)
    x_dummy = torch.zeros((1, s), dtype=torch.float32, device=DEVICE)
    p_dummy = torch.zeros((1, 1), dtype=torch.float32, device=DEVICE)
    with torch.no_grad():
        pred = net(inst_t, dec_t, x_dummy, p_dummy, None)
    return pred.item()


# ------------------------------------------------------------------
# 4. Greedy pruning
# ------------------------------------------------------------------

def greedy_prune(net, pml_feats, s, keep_per_switch_point=1, refine_iters=2):
    x_ref = [1] * s
    for _ in range(refine_iters):
        for sp in range(s):
            scores = []
            for alt in range(3):
                x_try = list(x_ref); x_try[sp] = alt
                scores.append(score_x(net, pml_feats, x_try, s))
            x_ref[sp] = int(min(range(3), key=lambda a: scores[a]))

    kept_per_sp = []
    for sp in range(s):
        scored = []
        for alt in range(3):
            x_try = list(x_ref); x_try[sp] = alt
            scored.append((alt, score_x(net, pml_feats, x_try, s)))
        scored.sort(key=lambda t: t[1])
        kept_per_sp.append([a for a, _ in scored[:keep_per_switch_point]])

    return list(itertools.product(*kept_per_sp))


# ------------------------------------------------------------------
# 5. End-to-end test on gen_0000, solving the reduced .lp directly
# ------------------------------------------------------------------

if __name__ == "__main__":
    program_dir = "programs/generated/gen_0000"
    ckpt_path = "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt"  # swap to _FULLDECAY_VERIFIED_ once ready
    s = 2

    preamble, scenario_blocks = load_lp_files(program_dir)
    x_tuples = parse_scenario_x_tuples(scenario_blocks, s)
    print("scenarios found:", len(x_tuples))

    net = load_scoring_net(ckpt_path)
    dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both", device=DEVICE)
    pml_feats = dp._parse_pml_features({"program_dir": program_dir})

    kept = greedy_prune(net, pml_feats, s, keep_per_switch_point=1)
    print("kept x tuples:", kept)

    true_optimum = (2, 0)  # documented ground truth for gen_0000
    print("true optimum survives pruning:", true_optimum in kept)

    x_to_id = {v: k for k, v in x_tuples.items()}
    for x, idx in x_to_id.items():
        print(x, "-> score:", score_x(net, pml_feats, x, s))
    keep_ids = [x_to_id[x] for x in kept if x in x_to_id]
    write_reduced_lp(preamble, scenario_blocks, keep_ids, "gen_0000_pruned.lp")
    print("wrote gen_0000_pruned.lp with", len(keep_ids), "scenarios")

    # solve the reduced model directly with gurobipy — no WatwaOS needed
    model = gp.read("gen_0000_pruned.lp")
    model.optimize()
    print("pruned solve objective:", model.ObjVal, "| solve time:", model.Runtime, "s")
    model.dispose()