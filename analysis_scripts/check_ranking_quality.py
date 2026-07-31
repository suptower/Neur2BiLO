import pickle
import argparse
import torch
from collections import defaultdict
from scipy.stats import kendalltau

import blo.params as blo_params
from blo.data_preprocessor import factory_dp

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

val_data_full = dataset["val_data"]

# Gezielt die ersten N unterschiedlichen inst_id vollstaendig einsammeln
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

print(f"Ausgewaehlte Instanzen: {len(seen_ids)}, davon Zeilen gesamt: {len(selected)}")

small_tr = dataset["tr_data"][:100]  # Platzhalter, wird nicht wirklich fuer diesen Check gebraucht
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

print("Anzahl Zeilen pro Instanz (erste 10):",
      [len(v) for v in list(by_inst_true.values())[:10]])

taus = []
for iid in by_inst_true:
    t = by_inst_true[iid]
    p = by_inst_pred[iid]
    if len(t) >= 3 and len(set(t)) > 1:
        tau, _ = kendalltau(t, p)
        if tau == tau:
            taus.append(tau)

print(f"n instances with Kendall tau: {len(taus)}")
if taus:
    print(f"mean Kendall tau: {sum(taus)/len(taus):.4f}")
    print(f"median Kendall tau: {sorted(taus)[len(taus)//2]:.4f}")
    print(f"fraction with tau > 0.3: {sum(1 for t in taus if t > 0.3)/len(taus):.4f}")
    print(f"fraction with tau < 0: {sum(1 for t in taus if t < 0)/len(taus):.4f}")
else:
    print("Immer noch keine brauchbaren Instanzen gefunden.")
