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

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 13,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})

box_data, labels, colors, ns = [], [], [], []
for lo, hi, label, color in bins:
    mask = (num_scenarios_arr >= lo) & (num_scenarios_arr < hi)
    if mask.sum() == 0:
        continue
    box_data.append(percentiles[mask] * 100)
    labels.append(label)
    colors.append(color)
    ns.append(mask.sum())

fig, ax = plt.subplots(figsize=(7, 4.5))

bp = ax.boxplot(
    box_data,
    patch_artist=True,
    widths=0.6,
    medianprops=dict(color="black", linewidth=1.4),
    flierprops=dict(marker="o", markersize=3, markerfacecolor="none",
                     markeredgewidth=0.6, alpha=0.4),
    whiskerprops=dict(linewidth=0.9),
    capprops=dict(linewidth=0.9),
    boxprops=dict(linewidth=0.9),
)
for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.55)
    patch.set_edgecolor(color)

ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels)
ax.set_xlabel("Scenarios")
ax.set_ylabel("Percentile rank of model's choice\n(0% = optimum, 100% = worst)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, pos: f"{x:g}%"))

# data-driven y-range instead of fixed 0-100, with headroom for n= labels
ymax = max(np.concatenate(box_data).max(), 5)
ax.set_ylim(-ymax * 0.05, ymax * 1.22)

for i, n in enumerate(ns):
    ax.text(i + 1, ymax * 1.13, f"n={n}", ha="center", va="center",
             fontsize=9, color="dimgray")

ax.grid(True, which="major", axis="y", linestyle=":", linewidth=0.5, alpha=0.4)
ax.set_axisbelow(True)

plt.tight_layout()
plt.savefig("percentile_rank_boxplot.pdf", bbox_inches="tight")
plt.savefig("percentile_rank_boxplot.png", dpi=200, bbox_inches="tight")
print("Gespeichert: percentile_rank_boxplot.pdf / .png")