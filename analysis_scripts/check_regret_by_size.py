import pickle
import argparse
import torch
from collections import defaultdict

import blo.params as blo_params
from blo.data_preprocessor import factory_dp

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

val_data_full = dataset["val_data"]

N_INSTANCES = 30
seen_ids = []
selected = []
for row in val_data_full:
    iid = row["inst_id"]
    if iid not in seen_ids:
        if len(seen_ids) >= N_INSTANCES:
            break
        seen_ids.append(iid)
    if iid in seen_ids:
        selected.append(row)

small_tr = dataset["tr_data"][:100]
small_val = selected
del dataset

args = argparse.Namespace(
    problem="watwa_v7", model_type="inst_encoder", approx_type="both",
    use_context=1, scale_labels=0,
)
device = torch.device("cpu")
dp = factory_dp(args, args.model_type, args.approx_type, args.problem, device)
tr_dataset, val_dataset = dp.preprocess_data(small_tr, small_val)

ckpt = torch.load(
    "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt",
    map_location="cpu", weights_only=False,
)

inst_emb = ckpt["instance_decision_embedder"]
final_emb = ckpt["final_instance_embedder"]
value_pred = ckpt["value_predictor"]
ctx_proj = ckpt.get("context_proj", None)

inst_features, decisions_features, x, n_decisions, labels, inst_ids = val_dataset.tensors

with torch.no_grad():
    emb = inst_emb(inst_features)
    emb = torch.sum(emb, dim=1)
    emb = final_emb(emb)
    emb_b = emb[:, None, :].repeat(1, inst_features.shape[1], 1)
    feats = torch.cat([decisions_features, emb_b], dim=2)
    if ctx_proj is not None:
        total = torch.sum(feats, dim=1, keepdim=True)
        context = total - feats
        context = ctx_proj(context)
        feats = torch.cat([feats, context], dim=2)
    pred_per_decision = value_pred(feats).squeeze(-1)
    preds = torch.sum(pred_per_decision, dim=1)

by_inst_true = defaultdict(list)
by_inst_pred = defaultdict(list)
for i in range(labels.shape[0]):
    iid = int(inst_ids[i].item())
    by_inst_true[iid].append(labels[i].item())
    by_inst_pred[iid].append(preds[i].item())

print(f"{'inst_id':>10} {'n_scen':>8} {'true_rank_of_chosen':>20} {'percentile':>12} {'gap_to_true_opt':>16}")
for iid in by_inst_true:
    t = by_inst_true[iid]
    p = by_inst_pred[iid]
    n = len(t)
    chosen_idx = min(range(n), key=lambda i: p[i])  # Modell waehlt das Szenario mit kleinstem predicted V(x)
    true_sorted_idx = sorted(range(n), key=lambda i: t[i])
    true_rank = true_sorted_idx.index(chosen_idx)  # 0 = tatsaechlich bestes Szenario
    percentile = true_rank / (n - 1) if n > 1 else 0.0
    true_opt = min(t)
    gap = (t[chosen_idx] - true_opt) / true_opt if true_opt != 0 else float("nan")
    print(f"{iid:>10} {n:>8} {true_rank:>20} {percentile:>12.4f} {gap:>16.4f}")