import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

with open("percentile_rank_data.pkl", "rb") as f:
    data = pickle.load(f)

percentiles = data["percentiles"]
num_scenarios_arr = data["num_scenarios"]

bins = [
    (1, 10,      "1\u201310",        "#4c72b0"),
    (10, 100,     "10\u2013100",      "#55a868"),
    (100, 1000,    "100\u20131,000",   "#c44e52"),
    (1000, 10000,   "1,000\u201310,000", "#8172b2"),
    (10000, float("inf"), "10,000+",  "#ccb974"),
]
top_k = [0.01, 0.05, 0.10]
top_k_labels = ["Top 1%", "Top 5%", "Top 10%"]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 13,
    "axes.labelsize": 13,
    "legend.fontsize": 10,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})

labels, colors, ns, coverage = [], [], [], []
for lo, hi, label, color in bins:
    mask = (num_scenarios_arr >= lo) & (num_scenarios_arr < hi)
    if mask.sum() == 0:
        continue
    p = percentiles[mask]
    labels.append(label)
    colors.append(color)
    ns.append(mask.sum())
    coverage.append([(p <= t).mean() * 100 for t in top_k])

fig, axes = plt.subplots(1, 3, figsize=(11, 4), sharey=True)

for j, (ax, t_label) in enumerate(zip(axes, top_k_labels)):
    heights = [c[j] for c in coverage]
    ax.bar(range(1, len(labels) + 1), heights, width=0.6, color=colors,
           edgecolor=colors, alpha=0.75)
    for i, h in enumerate(heights):
        ax.text(i + 1, h + 2.5, f"{h:.0f}%", ha="center", va="bottom",
                 fontsize=9.5, color="dimgray")
    ax.set_xticks(range(1, len(labels) + 1))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_title(t_label, fontsize=12)
    ax.set_ylim(0, 112)
    ax.grid(True, which="major", axis="y", linestyle=":", linewidth=0.5, alpha=0.4)
    ax.set_axisbelow(True)

axes[0].set_ylabel("Share of instances\nwithin threshold")
axes[0].yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x:g}%"))
fig.supxlabel("Scenarios", fontsize=13, y=-0.02)

plt.tight_layout()
plt.savefig("percentile_rank_coverage.pdf", bbox_inches="tight")
plt.savefig("percentile_rank_coverage.png", dpi=200, bbox_inches="tight")
print("Gespeichert: percentile_rank_coverage.pdf / .png")