"""
Usage:
    python plot_rank_histogram.py results/rank_histogram.csv
"""

import csv
import sys

import matplotlib.pyplot as plt
import numpy as np


path = sys.argv[1] if len(sys.argv) > 1 else "rank_histogram.csv"

rows = []

with open(path, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        rows.append({
            "num_scenarios": int(row["num_scenarios"]),
            "percentile": float(row["percentile_rank_of_true_optimum"]),
        })

percentiles = np.array([row["percentile"] for row in rows])

bins = [0, 1, 2, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

scenario_ranges = [
    (1, 10, "1-10"),
    (10, 100, "10-100"),
    (100, 1000, "100-1,000"),
    (1000, 10000, "1,000-10,000"),
    (10000, float("inf"), "10,000+"),
]


fig, axes = plt.subplots(2, 3, figsize=(13, 7))
axes = axes.ravel()

# All instances
axes[0].hist(
    percentiles,
    bins=bins,
    edgecolor="white",
)
axes[0].set_title(f"All instances (n={len(percentiles)})")
axes[0].set_xlabel(
    "Percentile rank of true optimum\n"
    "in the network's ranking (%)"
)
axes[0].set_ylabel("# Instances")


# Individual scenario ranges
for ax, (lower, upper, label) in zip(axes[1:], scenario_ranges):
    values = np.array([
        row["percentile"]
        for row in rows
        if lower <= row["num_scenarios"] < upper
    ])

    if len(values) == 0:
        ax.set_visible(False)
        continue

    ax.hist(
        values,
        bins=bins,
        edgecolor="white",
    )
    ax.set_title(f"{label} scenarios (n={len(values)})")
    ax.set_xlabel("Percentile rank (%)")
    ax.set_ylabel("# Instances")


for ax in axes:
    ax.grid(True, alpha=0.3)


fig.suptitle(
    "Distribution of the network's rank of the true optimum\n"
    "(0% = network ranks the true optimum first)"
)

fig.tight_layout()
fig.savefig("rank_histogram.pdf", bbox_inches="tight")
fig.savefig("rank_histogram.png", dpi=200, bbox_inches="tight")

print("Saved rank_histogram.pdf / .png")


# Summary statistics
low = np.mean(percentiles <= 5) * 100
high = np.mean(percentiles >= 50) * 100
middle = 100 - low - high

print(f"\nShare <=5th percentile:  {low:.1f}%")
print(f"Share in 5-50 range:     {middle:.1f}%")
print(f"Share >=50th percentile: {high:.1f}%")