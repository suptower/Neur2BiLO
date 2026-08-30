"""
Break down solver and ML model execution times across scenario count buckets.

Usage:
    python bucket_timing_breakdown.py --pkl data/watwa/results/batch_eval_no_gurobi_watwa_v7.pkl
"""
import argparse
import pickle
import numpy as np


def main(args):
    with open(args.pkl, "rb") as f:
        metrics = pickle.load(f)

    print(f"Loaded {len(metrics)} instances from {args.pkl}\n")

    bins = [
        (1, 10),
        (10, 100),
        (100, 1000),
        (1000, 10000),
        (10000, float("inf")),
    ]

    header = (
        f"  {'Bucket':>16}  {'n':>4}  {'ML avg':>10}  {'ML median':>10}  "
        f"{'WatwaOS avg':>12}  {'WatwaOS med':>12}  {'Speedup avg':>12}  "
        f"{'Speedup med':>12}"
    )
    print(header)
    print("  " + "-" * (len(header) - 2))

    for lower, upper in bins:
        subset = [m for m in metrics if lower <= m["num_scenarios"] < upper]
        if not subset:
            continue

        ml_times = np.array([m["ml_time"] for m in subset]) * 1000  # convert to ms
        watwaos_times = np.array([m["watwaos_time"] for m in subset]) * 1000
        speedups = np.array([m["speedup"] for m in subset])

        upper_str = str(upper) if upper < float("inf") else "inf"
        bucket_str = f"[{lower}-{upper_str}]"

        print(
            f"  {bucket_str:>16}  {len(subset):>4}  "
            f"{np.mean(ml_times):>8.2f}ms  {np.median(ml_times):>8.2f}ms  "
            f"{np.mean(watwaos_times):>10.1f}ms  {np.median(watwaos_times):>10.1f}ms  "
            f"{np.mean(speedups):>10.2f}x  {np.median(speedups):>10.2f}x"
        )

    print(
        "\nNote: Speedup is calculated per instance (WatwaOS time / ML time) "
        "and then averaged, rather than computed from the ratio of average runtimes."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compute execution time and speedup breakdown by scenario buckets."
    )
    parser.add_argument(
        "--pkl",
        type=str,
        required=True,
        help="Path to the evaluation results pickle file.",
    )
    args = parser.parse_args()
    main(args)