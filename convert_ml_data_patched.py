import argparse
import pickle
import numpy as np
import torch
from blo.data_preprocessor.watwa import WatwaDataPreprocessor

parser = argparse.ArgumentParser()
parser.add_argument('--use_rank_labels', type=int, default=0,
                     help='Bake rank-based labels into the compact cache instead of '
                          'normalized energy. Must match the --use_rank_labels value '
                          'passed to 03_train_nn.py, or that flag has no effect (the '
                          'training script silently prefers this cache when present).')
args = parser.parse_args()

SRC = "data/watwa/ml_data_nsi-498_nspi-100000_s-7.pkl"
label_suffix = "_ranklabels" if args.use_rank_labels else ""
OUT = f"data/watwa/ml_data_nsi-498_nspi-100000_s-7_compact{label_suffix}.npz"

with open(SRC, "rb") as f:
    dataset = pickle.load(f)

dp = WatwaDataPreprocessor(model_type="inst_encoder", approx_type="both",
                            device=torch.device("cpu"),
                            use_rank_labels=bool(args.use_rank_labels))
tr_ds = dp.get_inst_encoder_dataset(dataset["tr_data"])
val_ds = dp.get_inst_encoder_dataset(dataset["val_data"])

np.savez_compressed(
    OUT,
    tr_inst_features=tr_ds.tensors[0].numpy(), tr_decision_features=tr_ds.tensors[1].numpy(),
    tr_decisions=tr_ds.tensors[2].numpy(), tr_n_decisions=tr_ds.tensors[3].numpy(),
    tr_labels=tr_ds.tensors[4].numpy(), tr_inst_ids=tr_ds.tensors[5].numpy(),
    val_inst_features=val_ds.tensors[0].numpy(), val_decision_features=val_ds.tensors[1].numpy(),
    val_decisions=val_ds.tensors[2].numpy(), val_n_decisions=val_ds.tensors[3].numpy(),
    val_labels=val_ds.tensors[4].numpy(), val_inst_ids=val_ds.tensors[5].numpy(),
)
print("saved compact dataset to", OUT)