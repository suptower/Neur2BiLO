import pickle
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

with open("data/watwa/results/batch_eval_watwa_v7.pkl", "rb") as f:
    eval_results = pickle.load(f)

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

needed_dirs = {r["program_dir"] for r in eval_results}
scenarios_by_dir = {}
for split in ["tr_data", "val_data"]:
    for row in dataset[split]:
        pdir = row["instance"]["program_dir"]
        if pdir in needed_dirs and pdir not in scenarios_by_dir:
            scenarios_by_dir[pdir] = row["instance"]["scenarios"]
        if len(scenarios_by_dir) == len(needed_dirs):
            break
    if len(scenarios_by_dir) == len(needed_dirs):
        break
del dataset

quality_gaps, rank1_gaps, num_scenarios_list = [], [], []
for r in eval_results:
    pdir = r["program_dir"]
    if pdir not in scenarios_by_dir:
        continue
    energies = sorted(v["energy"] for v in scenarios_by_dir[pdir].values())
    opt = energies[0]
    rank1 = energies[1] if len(energies) > 1 else opt
    rank1_gap = (rank1 - opt) / opt if opt != 0 else np.nan
    quality_gaps.append(r["quality_gap"])
    rank1_gaps.append(rank1_gap)
    num_scenarios_list.append(r["num_scenarios"])

quality_gaps = np.array(quality_gaps)
rank1_gaps = np.array(rank1_gaps)
num_scenarios_arr = np.array(num_scenarios_list)

eps = 1e-6
qg = np.clip(quality_gaps, eps, None)
rg = np.clip(rank1_gaps, eps, None)

bins = [
    (1, 10,    "1\u201310",       "#4c72b0"),
    (10, 100,   "10\u2013100",     "#55a868"),
    (100, 1000,  "100\u20131,000",  "#c44e52"),
    (1000, 10000, "1,000\u201310,000", "#8172b2"),
    (10000, float("inf"), "10,000+", "#ccb974"),
]

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 13,
    "axes.labelsize": 13,
    "legend.fontsize": 10.5,
    "xtick.labelsize": 10.5,
    "ytick.labelsize": 10.5,
})

fig, ax = plt.subplots(figsize=(6.5, 6))

for lo, hi, label, color in bins:
    mask = (num_scenarios_arr >= lo) & (num_scenarios_arr < hi)
    if mask.sum() == 0:
        continue
    ax.scatter(rg[mask], qg[mask], s=26, alpha=0.7, color=color,
               edgecolors="white", linewidths=0.3, label=label)

lims = [min(rg.min(), qg.min()) * 0.7, max(rg.max(), qg.max()) * 1.3]
ax.plot(lims, lims, color="black", linestyle="--", linewidth=1.1, zorder=0)

ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(lims)
ax.set_ylim(lims)

ax.set_xlabel("Gap between best and 2nd-best configuration")
ax.set_ylabel("Model's prediction error")

def pct_formatter(x, pos):
    """Formats log-scale tick as a percentage with just enough
    precision to stay distinguishable across many decades."""
    val = x * 100
    if val == 0:
        return "0%"
    return f"{val:g}%"

major_locator = mticker.LogLocator(base=10.0)
ax.xaxis.set_major_locator(major_locator)
ax.yaxis.set_major_locator(major_locator)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(pct_formatter))
ax.yaxis.set_major_formatter(mticker.FuncFormatter(pct_formatter))
ax.xaxis.set_minor_locator(mticker.NullLocator())
ax.yaxis.set_minor_locator(mticker.NullLocator())

for label in ax.get_xticklabels():
    label.set_rotation(45)
    label.set_ha("right")

ax.legend(title="Scenarios", loc="lower right", frameon=True, framealpha=0.9)
ax.grid(True, which="major", linestyle=":", linewidth=0.5, alpha=0.4)

plt.tight_layout()
plt.savefig("gap_vs_sharpness.pdf")
plt.savefig("gap_vs_sharpness.png", dpi=200)
print("Gespeichert: gap_vs_sharpness.pdf / .png")