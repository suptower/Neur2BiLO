import pickle
from collections import defaultdict

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

val_data_full = dataset["val_data"]

N_INSTANCES = 30
seen_ids = []
by_inst_true = defaultdict(list)
for row in val_data_full:
    iid = row["inst_id"]
    if iid not in seen_ids:
        if len(seen_ids) >= N_INSTANCES:
            break
        seen_ids.append(iid)
    if iid in seen_ids:
        by_inst_true[iid].append(row["solve_res"]["leader_obj"])

print(f"{'inst_id':>10} {'n_scen':>8} {'opt':>12} {'rank1':>12} {'rank1_gap':>12} {'top1pct_avg_gap':>16}")
for iid, vals in by_inst_true.items():
    vals_sorted = sorted(vals)
    opt = vals_sorted[0]
    rank1 = vals_sorted[1] if len(vals_sorted) > 1 else opt
    rank1_gap = (rank1 - opt) / opt if opt != 0 else float("nan")
    top1pct_n = max(1, len(vals_sorted) // 100)
    top1pct_avg = sum(vals_sorted[:top1pct_n]) / top1pct_n
    top1pct_gap = (top1pct_avg - opt) / opt if opt != 0 else float("nan")
    print(f"{iid:>10} {len(vals):>8} {opt:>12.4f} {rank1:>12.4f} {rank1_gap:>12.4f} {top1pct_gap:>16.4f}")
