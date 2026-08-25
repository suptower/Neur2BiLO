import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
Batch recall/speedup evaluation of neural pruning.
Restricted to instances where pruning is expected to help (>=100 scenarios).
"""
import ast
import pickle
import time
import itertools
import gurobipy as gp

from pruning import (
    load_lp_files, parse_scenario_x_tuples, write_reduced_lp,
    load_scoring_net, score_x, DEVICE,
)
from blo.data_preprocessor.watwa import WatwaDataPreprocessor

CKPT_PATH = "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7_FULLDECAY_VERIFIED_20260813_1245.pt"
MIN_SCENARIOS_FOR_PRUNING = 100
KEEP_VALUES = [1, 2]  # keep=3 == no pruning at all (all 3 alts kept), skip — same as full search
N_INSTANCES_PER_BUCKET = 5

BUCKETS = [(100, 1000), (1000, 10000), (10000, float("inf"))]


def parse_x(val):
    """opt_scenario may already be a tuple, or a string like '(2, 0)'."""
    if isinstance(val, str):
        return ast.literal_eval(val)
    return tuple(val)


def greedy_prune(net, pml_feats, s, keep_per_switch_point, refine_iters=2):
    x_ref = [1] * s
    for _ in range(refine_iters):
        for sp in range(s):
            scores = [score_x(net, pml_feats, [*x_ref[:sp], alt, *x_ref[sp+1:]], s) for alt in range(3)]
            x_ref[sp] = int(min(range(3), key=lambda a: scores[a]))
    kept_per_sp = []
    for sp in range(s):
        scored = [(alt, score_x(net, pml_feats, [*x_ref[:sp], alt, *x_ref[sp+1:]], s)) for alt in range(3)]
        scored.sort(key=lambda t: t[1])
        kept_per_sp.append([a for a, _ in scored[:keep_per_switch_point]])
    return list(itertools.product(*kept_per_sp))


def solve_multi_scenario(lp_path):
    model = gp.read(lp_path)
    model.setParam("OutputFlag", 0)
    model.optimize()
    n = model.NumScenarios
    best_obj, best_idx = None, None
    for i in range(n):
        model.Params.ScenarioNumber = i
        obj = model.ScenNObjVal
        if best_obj is None or obj < best_obj:
            best_obj, best_idx = obj, i
    return best_obj, model.Runtime


def main():
    with open("data/watwa/results/batch_eval_watwa_v7.pkl", "rb") as f:
        eval_results = pickle.load(f)

    net = load_scoring_net(CKPT_PATH)
    dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both", device=DEVICE)

    sample = []
    for lo, hi in BUCKETS:
        in_bucket = [r for r in eval_results if lo <= r["num_scenarios"] < hi]
        in_bucket.sort(key=lambda r: r["num_scenarios"])
        step = max(1, len(in_bucket) // N_INSTANCES_PER_BUCKET)
        sample += in_bucket[::step][:N_INSTANCES_PER_BUCKET]

    print(f"{'instance':<32}{'n_scen':>8}{'s':>4}{'keep':>6}{'kept_n':>8}{'recall':>8}{'gap%':>10}{'t_pruned':>10}{'t_full':>10}")

    for r in sample:
        pdir = r["program_dir"]
        s = r["s"]
        true_x = parse_x(r["opt_scenario"])
        opt_energy = r["opt_energy"]

        try:
            preamble, scenario_blocks = load_lp_files(pdir)
        except FileNotFoundError as e:
            print(pdir, "SKIP:", e)
            continue

        x_tuples = parse_scenario_x_tuples(scenario_blocks, s)
        pml_feats = dp._parse_pml_features({"program_dir": pdir})
        x_to_id = {v: k for k, v in x_tuples.items()}

        for keep in KEEP_VALUES:
            kept = greedy_prune(net, pml_feats, s, keep)
            recall = true_x in kept

            keep_ids = [x_to_id[x] for x in kept if x in x_to_id]
            out_path = f"/tmp/{pdir.split('/')[-1]}_pruned_k{keep}.lp"
            write_reduced_lp(preamble, scenario_blocks, keep_ids, out_path)

            t0 = time.time()
            best_obj, gurobi_runtime = solve_multi_scenario(out_path)
            t_pruned = time.time() - t0

            gap = (best_obj - opt_energy) / opt_energy * 100
            print(f"{pdir:<32}{r['num_scenarios']:>8}{s:>4}{keep:>6}{len(keep_ids):>8}"
                  f"{str(recall):>8}{gap:>10.4f}{t_pruned:>10.4f}{r['watwaos_time']:>10.2f}")


if __name__ == "__main__":
    main()