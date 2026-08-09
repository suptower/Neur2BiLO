import pickle
import argparse
import torch

import blo.params as blo_params
from blo.data_preprocessor import factory_dp

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

small_tr = dataset["tr_data"][:5000]
small_val = dataset["val_data"][:2000]
del dataset

args = argparse.Namespace(
    problem="watwa_v7", model_type="inst_encoder", approx_type="both",
    use_context=1, scale_labels=0,
)
device = torch.device("cpu")
dp = factory_dp(args, args.model_type, args.approx_type, args.problem, device)
tr_dataset, val_dataset = dp.preprocess_data(small_tr, small_val)

n_decisions = tr_dataset.tensors[3]
labels = tr_dataset.tensors[4]
inst_ids = tr_dataset.tensors[5]

print("n_decisions (k) min/max:", n_decisions.min().item(), n_decisions.max().item())
print("labels global min/max/mean/std:", labels.min().item(), labels.max().item(), labels.mean().item(), labels.std().item())

from collections import defaultdict
by_inst = defaultdict(list)
for l, iid in zip(labels.tolist(), inst_ids.tolist()):
    by_inst[iid].append(l)

within_stds = [torch.tensor(v).std().item() for v in by_inst.values() if len(v) > 1]
between_means = [sum(v)/len(v) for v in by_inst.values()]
print("mean within-instance std:", sum(within_stds)/len(within_stds))
print("std of between-instance means:", torch.tensor(between_means).std().item())
