import pickle
import argparse
import numpy as np
import torch

import blo.params as blo_params
from blo.data_preprocessor import factory_dp

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

# Nur einen kleinen Ausschnitt nehmen, genug um mehrere inst_id abzudecken
small_tr = dataset["tr_data"][:5000]
small_val = dataset["val_data"][:2000]
del dataset

args = argparse.Namespace(
    problem="watwa_v7",
    model_type="inst_encoder",
    approx_type="both",
    use_context=1,
    scale_labels=0,
)
device = torch.device("cpu")
dp = factory_dp(args, args.model_type, args.approx_type, args.problem, device)

tr_dataset, val_dataset = dp.preprocess_data(small_tr, small_val)

print("Anzahl Tensoren im Dataset:", len(tr_dataset.tensors))
for i, t in enumerate(tr_dataset.tensors):
    print(f"  tensor[{i}]: shape={tuple(t.shape)} dtype={t.dtype}")

inst_features = tr_dataset.tensors[0]
decisions_features = tr_dataset.tensors[1]

print()
print("=== inst_features (geht in instance_decision_embedder) ===")
flat = inst_features.reshape(-1, inst_features.shape[-1]).float()
print("shape:", inst_features.shape)
print("global min/max/mean/std:", flat.min().item(), flat.max().item(), flat.mean().item(), flat.std().item())
print("fraction exactly zero:", (flat == 0).float().mean().item())
print("per-feature std:", flat.std(dim=0))
print("per-feature mean:", flat.mean(dim=0))

print()
print("=== decisions_features (pro Switch-Point) ===")
flat_d = decisions_features.reshape(-1, decisions_features.shape[-1]).float()
print("shape:", decisions_features.shape)
print("per-feature std:", flat_d.std(dim=0))
