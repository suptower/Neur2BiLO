"""
For every instance, computes the percentile rank of the model's chosen
scenario within the TRUE energy ranking of all scenarios for that instance
(0.0 = true optimum, 1.0 = worst possible scenario). Aggregates by the same
complexity buckets used throughout the evaluation chapter, and reports
top-K% coverage (share of instances whose chosen scenario falls within the
best K% of all true scenario values).

Run this wherever ml_data + batch_eval_watwa_v7.pkl live (i4watwa/cipslurm).
"""

import pickle
import numpy as np

EVAL_RESULTS_PATH = "data/watwa/results/batch_eval_watwa_v7.pkl"
ML_DATA_PATH = "ml_data_v7_full.pkl"  # adjust to whichever ml_data file matches this eval run

BUCKETS = [(1, 10), (10, 100), (100, 1000), (1000, 10000), (10000, float("inf"))]
TOP_K_THRESHOLDS = [0.01, 0.05, 0.10]  # top 1%, top 5%, top 10%


def main():
    with open(EVAL_RESULTS_PATH, "rb") as f:
        eval_results = pickle.load(f)

    with open(ML_DATA_PATH, "rb") as f:
        dataset = pickle.load(f)

    needed_dirs = {r["program_dir"] for r in eval_results}
    scenarios_by_dir = {}
    print(dataset.keys())
    for split in ["tr_data", "val_data", "data", "recovered_data"]:
        for row in dataset[split]:
            pdir = row["instance"]["program_dir"]
            if pdir in needed_dirs and pdir not in scenarios_by_dir:
                scenarios_by_dir[pdir] = row["instance"]["scenarios"]
            if len(scenarios_by_dir) == len(needed_dirs):
                break
        if len(scenarios_by_dir) == len(needed_dirs):
            break
    del dataset

    percentiles = []
    num_scenarios_list = []
    missing = 0

    for r in eval_results:
        pdir = r["program_dir"]
        if pdir not in scenarios_by_dir:
            missing += 1
            continue

        energies = sorted(v["energy"] for v in scenarios_by_dir[pdir].values())
        n = len(energies)

        ml_energy = r["ml_energy"]
        # rank = number of true scenarios strictly better than the model's choice
        rank = sum(1 for e in energies if e < ml_energy)
        percentile = rank / (n - 1) if n > 1 else 0.0

        percentiles.append(percentile)
        num_scenarios_list.append(r["num_scenarios"])

    print(f"Missing (program_dir not found in ml_data): {missing}")
    print(f"Instances analyzed: {len(percentiles)}\n")

    percentiles = np.array(percentiles)
    num_scenarios_arr = np.array(num_scenarios_list)

    print(f"{'Bucket':<20}{'n':>5}{'median pct':>13}{'mean pct':>11}"
          + "".join(f"{'top' + str(int(t*100)) + '%':>10}" for t in TOP_K_THRESHOLDS))

    for lo, hi in BUCKETS:
        mask = (num_scenarios_arr >= lo) & (num_scenarios_arr < hi)
        if mask.sum() == 0:
            continue
        p = percentiles[mask]
        label = f"[{lo}-{hi if hi < float('inf') else 'inf'}]"
        row = f"{label:<20}{mask.sum():>5}{np.median(p)*100:>12.2f}%{p.mean()*100:>10.2f}%"
        for t in TOP_K_THRESHOLDS:
            row += f"{(p <= t).mean()*100:>9.1f}%"
        print(row)

    # save per-instance data for plotting (boxplot script can consume this)
    out = {
        "percentiles": percentiles,
        "num_scenarios": num_scenarios_arr,
    }
    with open("percentile_rank_data.pkl", "wb") as f:
        pickle.dump(out, f)
    print("\nSaved per-instance data to percentile_rank_data.pkl")


if __name__ == "__main__":
    main()