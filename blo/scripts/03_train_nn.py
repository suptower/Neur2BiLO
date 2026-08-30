import argparse
import collections
import copy
import datetime
import hashlib
import os
import pickle as pkl
import time

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

import blo.params as blo_params
from blo.data_preprocessor import factory_dp
from blo.models import (
    FeedForwardBase,
    FeedForwardNetwork,
    SetBasedNetwork,
    SetInstanceEncodingNetwork,
)
from blo.utils import factory_get_path


# ---------------------------------------------------------------------------
# Evaluation Helpers
# ---------------------------------------------------------------------------

def forward_pass_all_data(net, loader, model_type):
    """Runs a complete forward pass over the data loader and returns flat lists."""
    labels_all, preds_all, inst_ids_all = [], [], []

    with torch.no_grad():
        for batch_data in loader:
            if "set" in model_type:
                features, n_decisions, p, labels = batch_data
                preds = net(features, p, n_decisions)
                inst_ids = torch.zeros(labels.shape[0])
            elif "ff" in model_type:
                features, p, labels = batch_data
                preds = net(features, p)
                inst_ids = torch.zeros(labels.shape[0])
            elif "inst" in model_type:
                inst_features, decisions_features, x, n_decisions, labels, inst_ids = batch_data
                p = torch.zeros(inst_features.shape[0], 1, device=inst_features.device)
                preds = net(inst_features, decisions_features, x, p, n_decisions)

            labels_all.extend(labels.cpu().numpy().reshape(-1).tolist())
            preds_all.extend(preds.detach().cpu().numpy().reshape(-1).tolist())
            inst_ids_all.extend(inst_ids.cpu().numpy().reshape(-1).tolist())

    return labels_all, preds_all, inst_ids_all


def test_model_predictions(
    cfg,
    net,
    loader,
    model_type,
    print_predictions=False,
    get_ranking=False,
    verbose=True,
):
    """Evaluates model performance and returns error and ranking statistics."""
    labels_all, preds_all, inst_ids_all = forward_pass_all_data(net, loader, model_type)

    labels_arr = np.array(labels_all)
    preds_arr = np.array(preds_all)

    abs_diff = np.abs(labels_arr - preds_arr)
    rel_err = abs_diff / (labels_arr + 1e-8)
    diff = preds_arr - labels_arr

    mae = float(np.mean(abs_diff))
    mape = float(np.mean(rel_err))

    over_estimates = rel_err[diff > 0]
    under_estimates = rel_err[diff < 0]
    err_max_over = float(np.max(over_estimates)) if len(over_estimates) > 0 else -1.0
    err_max_under = float(np.max(under_estimates)) if len(under_estimates) > 0 else -1.0

    # Top-1 accuracy grouped by instance ID
    inst_labels = collections.defaultdict(list)
    inst_preds = collections.defaultdict(list)
    for label, pred, iid in zip(labels_all, preds_all, inst_ids_all):
        inst_labels[iid].append(label)
        inst_preds[iid].append(pred)

    top1_correct = sum(
        np.argmin(inst_labels[iid]) == np.argmin(inst_preds[iid])
        for iid in inst_labels
    )
    top1_total = len(inst_labels)
    top1_acc = top1_correct / top1_total if top1_total > 0 else 0.0

    res_kendall_all = []

    if verbose:
        print(f"Mean Percentage Error = {mape:.6f}")
        print(f"Max over/underestimate: {err_max_over:.6f}, {err_max_under:.6f}")
        if get_ranking:
            print(f"Top-1 Accuracy: {top1_acc:.6f}")

    return {
        "mae": mae,
        "mape": mape,
        "top1_acc": top1_acc,
        "err_max_over": err_max_over,
        "err_max_under": err_max_under,
        "kendall_all": res_kendall_all,
        "kendall_min": float(np.min(res_kendall_all)) if res_kendall_all else 0.0,
        "kendall_max": float(np.max(res_kendall_all)) if res_kendall_all else 0.0,
        "kendall_median": float(np.median(res_kendall_all)) if res_kendall_all else 0.0,
        "kendall_mean": float(np.mean(res_kendall_all)) if res_kendall_all else 0.0,
    }


def get_nn_param_str(args, params):
    """Generates a unique, bounded parameter string for checkpoint filenames."""

    def lst_to_str(lst):
        return "-".join(str(x) for x in lst)

    tokens = [
        f"bs-{params['batch_size']}",
        f"lr-{params['lr']}",
        f"o-{params['optimizer']}",
        f"ep-{params['n_epochs']}",
        f"do-{params['dropout']}",
    ]

    if "ff" in args.model_type:
        tokens.append(f"ff-h-{lst_to_str(params['ff_hidden_dim'])}")
        tokens.append(f"ff-ro-{params['ff_relu_output']}")

    elif "set" in args.model_type:
        tokens.extend([
            f"set-eh-{lst_to_str(params['set_embed_hidden_dim'])}",
            f"set-eo-{params['set_embed_output_dim']}",
            f"set-vh-{lst_to_str(params['set_value_hidden_dim'])}",
            f"set-ero-{params['set_embed_relu_output']}",
            f"set-vro-{params['set_value_relu_output']}",
            f"set-a-{params['set_agg_type']}",
        ])

    elif "inst" in args.model_type:
        tokens.extend([
            f"in-eh-{lst_to_str(params['inst_embed_hidden_dim'])}",
            f"in-eo-{params['inst_embed_output_dim']}",
            f"in-ph-{lst_to_str(params['inst_post_agg_hidden_dim'])}",
            f"in-po-{params['inst_post_agg_output_dim']}",
            f"in-vh-{lst_to_str(params['inst_value_hidden_dim'])}",
            f"in-ero-{params['inst_embed_relu_output']}",
            f"in-pro-{params['inst_post_agg_relu_output']}",
            f"in-vro-{params['inst_value_relu_output']}",
            f"in-a-{params['inst_agg_type']}",
            f"in-ctx-{int(bool(params.get('use_context', False)))}",
            f"in-ln-{int(bool(params.get('use_inst_embedding_norm', False)))}",
            f"in-act-{params.get('activation', 'relu')}",
            f"rank-{int(bool(params.get('use_rank_labels', False)))}",
            f"edm-{params.get('embedder_decay_mult', 1.0)}",
            f"attn-{int(bool(params.get('use_attention', False)))}",
        ])
        if params.get("use_attention", False):
            tokens.append(f"attnheads-{params.get('attention_num_heads', 4)}")
            tokens.append(f"attndim-{params.get('attention_hidden_dim', 32)}")

    nn_param_str = "_".join(tokens)

    # Prevent exceeding filesystem filename limits (e.g. 255 bytes on ext4)
    max_param_str_len = 100
    if len(nn_param_str) > max_param_str_len:
        full_hash = hashlib.sha256(nn_param_str.encode()).hexdigest()[:10]
        keep_prefix = nn_param_str[: max_param_str_len - 15]
        truncated = f"{keep_prefix}_h{full_hash}"
        print(
            f"  [get_nn_param_str] Warning: Param string length ({len(nn_param_str)}) "
            f"exceeded {max_param_str_len} chars. Truncated to: {truncated!r}"
        )
        nn_param_str = truncated

    return nn_param_str


# ---------------------------------------------------------------------------
# Training Pipeline
# ---------------------------------------------------------------------------

def main(args):
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print(f"Loading configuration for problem: {args.problem} ...")
    cfg = getattr(blo_params, args.problem)

    get_path = factory_get_path(args)
    fp_data = get_path(cfg.data_path, cfg, "ml_data")

    # Check for cached compact dataset format
    label_suffix = "_ranklabels" if args.use_rank_labels else ""
    fp_compact = str(fp_data).replace(".pkl", f"_compact{label_suffix}.npz")
    data_preprocessor = factory_dp(args, args.model_type, args.approx_type, args.problem, device)

    if os.path.exists(fp_compact) and args.model_type == "inst_encoder":
        print(f"Loading precomputed compact dataset from {fp_compact} ...")
        npz = np.load(fp_compact)

        def _make_dataset(prefix):
            tensors = [
                torch.from_numpy(npz[f"{prefix}_inst_features"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_decision_features"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_decisions"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_n_decisions"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_labels"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_inst_ids"]).float().to(device),
            ]
            return TensorDataset(*tensors)

        tr_dataset = _make_dataset("tr")
        val_dataset = _make_dataset("val")
        if args.scale_labels:
            raise NotImplementedError("--scale_labels requires the raw .pkl dataset; remove compact .npz cache.")
    else:
        print("Loading raw pickle dataset ...")
        with open(fp_data, "rb") as pf:
            dataset = pkl.load(pf)

        print("Preprocessing data ...")
        if args.scale_labels and args.problem in ["watwa"]:
            data_preprocessor.get_label_scalers(dataset["tr_data"] + dataset["val_data"])
        elif args.scale_labels:
            data_preprocessor.get_label_scalers(dataset["tr_data"])

        tr_dataset, val_dataset = data_preprocessor.preprocess_data(
            dataset["tr_data"], dataset["val_data"]
        )

    # Configure data loaders (instance-grouped batch sampler for ranking loss)
    if "inst" in args.model_type and args.ranking_loss_weight > 0:
        all_inst_ids = tr_dataset.tensors[-1].long().tolist()
        id_to_indices = collections.defaultdict(list)
        for idx, iid in enumerate(all_inst_ids):
            id_to_indices[int(iid)].append(idx)

        samples_per_inst = args.samples_per_inst
        insts_per_batch = max(1, args.batch_size // samples_per_inst)
        inst_keys = list(id_to_indices.keys())
        np.random.shuffle(inst_keys)

        grouped_batches = []
        for i in range(0, len(inst_keys), insts_per_batch):
            batch = []
            for iid in inst_keys[i : i + insts_per_batch]:
                idxs = id_to_indices[iid]
                chosen = np.random.choice(
                    idxs, min(samples_per_inst, len(idxs)), replace=False
                ).tolist()
                batch.extend(chosen)
            grouped_batches.append(batch)

        tr_loader = DataLoader(tr_dataset, batch_sampler=grouped_batches)
        val_loader = DataLoader(val_dataset, shuffle=False, batch_size=args.batch_size_eval)
    else:
        tr_loader = DataLoader(tr_dataset, shuffle=True, batch_size=args.batch_size)
        val_loader = DataLoader(val_dataset, shuffle=False, batch_size=args.batch_size_eval)

    # Initialize neural network architectures
    print("Initializing model architecture ...")

    if "set" in args.model_type:
        value_output_dim = cfg.n[0] if "kp" in args.problem and args.use_coef else 1
        feat_size = tr_dataset[0][0].shape[-1]

        decision_embedder = FeedForwardBase(
            input_dim=feat_size,
            hidden_dims=args.set_embed_hidden_dim,
            output_dim=args.set_embed_output_dim,
            output_relu=args.set_embed_relu_output,
            dropout=args.dropout,
            bias=False,
            name="decision_embedder",
        ).to(device)

        value_predictor = FeedForwardBase(
            input_dim=args.set_embed_output_dim,
            hidden_dims=args.set_value_hidden_dim,
            output_dim=value_output_dim,
            output_relu=args.set_value_relu_output,
            dropout=args.dropout,
            bias=True,
            name="value",
        ).to(device)

        net = SetBasedNetwork(
            decision_embedder=decision_embedder,
            value_predictor=value_predictor,
            agg_type=args.set_agg_type,
            use_coef=args.use_coef,
        )

    elif "ff" in args.model_type:
        if "fixed" in args.model_type:
            assert len(cfg.n) == 1, "ff_fixed only supports a single fixed dimension n"

        input_size = len(tr_dataset[0][0])
        value_output_dim = cfg.n[0] if "kp" in args.problem and args.use_coef else 1

        ff_net = FeedForwardBase(
            input_dim=input_size,
            hidden_dims=args.ff_hidden_dim,
            output_dim=value_output_dim,
            output_relu=args.ff_relu_output,
            dropout=args.dropout,
            bias=True,
            name="ff",
        ).to(device)

        net = FeedForwardNetwork(ff_net, use_coef=args.use_coef)

    elif "inst" in args.model_type:
        inst_feat_size = tr_dataset[0][0].shape[-1]
        decision_feat_size = tr_dataset[0][1].shape[-1]

        instance_decision_embedder = FeedForwardBase(
            input_dim=inst_feat_size,
            hidden_dims=args.inst_embed_hidden_dim,
            output_dim=args.inst_embed_output_dim,
            output_relu=args.inst_embed_relu_output,
            dropout=args.dropout,
            bias=False,
            activation=args.activation,
            leaky_relu_slope=args.leaky_relu_slope,
            name="instance_decision_embedder",
        ).to(device)

        final_instance_embedder = FeedForwardBase(
            input_dim=args.inst_embed_output_dim,
            hidden_dims=args.inst_post_agg_hidden_dim,
            output_dim=args.inst_post_agg_output_dim,
            output_relu=args.inst_post_agg_relu_output,
            dropout=args.dropout,
            bias=True,
            activation=args.activation,
            leaky_relu_slope=args.leaky_relu_slope,
            name="final_instance_embedder",
        ).to(device)

        own_feat_dim = decision_feat_size + args.inst_post_agg_output_dim
        value_input_dim = own_feat_dim

        context_proj = None
        if args.use_context:
            context_proj = FeedForwardBase(
                input_dim=own_feat_dim,
                hidden_dims=[args.context_hidden_dim],
                output_dim=args.context_hidden_dim,
                output_relu=args.context_relu_output,
                dropout=args.dropout,
                bias=True,
                activation=args.activation,
                leaky_relu_slope=args.leaky_relu_slope,
                name="context_proj",
            ).to(device)
            value_input_dim += args.context_hidden_dim

        attention_proj = None
        attention = None
        if args.use_attention:
            if args.attention_hidden_dim % args.attention_num_heads != 0:
                raise ValueError(
                    f"--attention_hidden_dim ({args.attention_hidden_dim}) must be "
                    f"divisible by --attention_num_heads ({args.attention_num_heads})."
                )
            attention_proj = FeedForwardBase(
                input_dim=own_feat_dim,
                hidden_dims=[args.attention_hidden_dim],
                output_dim=args.attention_hidden_dim,
                output_relu=False,
                dropout=args.dropout,
                bias=True,
                activation=args.activation,
                leaky_relu_slope=args.leaky_relu_slope,
                name="attention_proj",
            ).to(device)

            attention = nn.MultiheadAttention(
                embed_dim=args.attention_hidden_dim,
                num_heads=args.attention_num_heads,
                batch_first=True,
            ).to(device)
            value_input_dim += args.attention_hidden_dim

        value_predictor = FeedForwardBase(
            input_dim=value_input_dim,
            hidden_dims=args.inst_value_hidden_dim,
            output_dim=1,
            output_relu=args.inst_value_relu_output,
            dropout=args.dropout,
            bias=True,
            activation=args.activation,
            leaky_relu_slope=args.leaky_relu_slope,
            name="value",
        ).to(device)

        net = SetInstanceEncodingNetwork(
            instance_decision_embedder=instance_decision_embedder,
            final_instance_embedder=final_instance_embedder,
            value_predictor=value_predictor,
            agg_type=args.set_agg_type,
            use_coef=args.use_coef,
            problem=args.problem,
            approx_type=args.approx_type,
            use_context=bool(args.use_context),
            context_proj=context_proj,
            use_inst_embedding_norm=bool(args.use_inst_embedding_norm),
            use_attention=bool(args.use_attention),
            attention_proj=attention_proj,
            attention=attention,
            attention_num_heads=args.attention_num_heads,
        )
    else:
        raise ValueError(f"Unsupported model_type: {args.model_type}")

    criterion = nn.MSELoss()
    Opt = getattr(torch.optim, args.optimizer)
    embedder_decay_mult = getattr(args, "embedder_decay_mult", 1.0)

    if "inst" in args.model_type and args.weight_decay > 0:
        value_param_names = [n for n, _ in net.named_parameters() if "value_predictor" in n]
        embedder_param_names = [
            n for n, _ in net.named_parameters()
            if "instance_decision_embedder" in n or "final_instance_embedder" in n
        ]
        base_param_names = [
            n for n, _ in net.named_parameters()
            if n not in value_param_names and n not in embedder_param_names
        ]

        param_groups = [
            {
                "params": [p for n, p in net.named_parameters() if n in base_param_names],
                "weight_decay": args.weight_decay,
            },
            {
                "params": [p for n, p in net.named_parameters() if n in value_param_names],
                "weight_decay": args.weight_decay * 1000,
            },
            {
                "params": [p for n, p in net.named_parameters() if n in embedder_param_names],
                "weight_decay": args.weight_decay * embedder_decay_mult,
            },
        ]
        optimizer = Opt(param_groups, lr=args.lr)
    else:
        optimizer = Opt(net.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, "min", factor=0.9, cooldown=100
    )

    print("Training model ...")
    val_results = []
    loss_epoch = []
    val_metric_best = -float("inf") if args.metric == "top1_acc" else float("inf")
    loss_epoch_min_idx = 0
    best_model = None

    train_start_time = time.time()

    for epoch in range(args.n_epochs):
        loss_epoch.append(0.0)

        for batch_data in tr_loader:
            if "set" in args.model_type:
                features, n_decisions, p, labels = batch_data
                preds = net(features, p, n_decisions)
            elif "ff" in args.model_type:
                features, p, labels = batch_data
                preds = net(features, p)
            elif "inst" in args.model_type:
                inst_features, decisions_features, x, n_decisions, labels, inst_ids = batch_data
                p = torch.zeros(inst_features.shape[0], 1, device=inst_features.device)
                preds = net(inst_features, decisions_features, x, p, n_decisions)

            mse_loss = criterion(preds, labels)
            ranking_loss = torch.tensor(0.0, device=preds.device)

            if "inst" in args.model_type and args.ranking_loss_weight > 0:
                preds_flat = preds.squeeze(-1)
                labels_flat = labels.squeeze(-1)
                k = args.ranking_loss_k
                for uid in inst_ids.unique():
                    mask = inst_ids == uid
                    if mask.sum() < 2 * k:
                        continue
                    p_lab = labels_flat[mask]
                    p_pre = preds_flat[mask]
                    _, bot_idx = torch.topk(p_lab, k, largest=False)
                    _, top_idx = torch.topk(p_lab, k, largest=True)
                    margin_violations = torch.relu(
                        p_pre[bot_idx].unsqueeze(1) - p_pre[top_idx].unsqueeze(0) + args.ranking_margin
                    )
                    ranking_loss = ranking_loss + margin_violations.mean()

            loss = mse_loss + args.ranking_loss_weight * ranking_loss
            loss_epoch[-1] += loss.item() / len(tr_loader)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        val_res = test_model_predictions(
            cfg=cfg,
            net=net,
            loader=val_loader,
            model_type=args.model_type,
            get_ranking=True,
            verbose=False,
        )
        val_results.append(val_res)
        scheduler.step(loss_epoch[-1])

        print(f"  Epoch: {epoch}:")
        print(f"          val_mae:        {val_res['mae']:.6f}")
        print(f"          val_mape:       {val_res['mape']:.6f}")
        print(f"          tr_loss:        {loss_epoch[-1]:.6f}")
        print(f"          err_max_over:   {val_res['err_max_over']:.6f}")
        print(f"          err_max_under:  {val_res['err_max_under']:.6f}")
        print(f"          val_top1_acc:   {val_res['top1_acc']:.6f}")

        if "inst" in args.model_type and epoch % 5 == 0:
            for mod_name in ["instance_decision_embedder", "final_instance_embedder"]:
                mod = getattr(net, mod_name, None)
                if mod is not None:
                    total_norm = sum(p.norm().item() for p in mod.parameters())
                    print(f"          {mod_name}_norm: {total_norm:.6f}")

        val_metric = val_res[args.metric]
        is_better = (
            val_metric > val_metric_best
            if args.metric == "top1_acc"
            else val_metric < val_metric_best
        )

        if is_better:
            print("    New best model found.")
            val_metric_best = val_metric
            loss_epoch_min_idx = epoch
            best_model = copy.deepcopy(net)

            emergency_data = {
                "model_type": args.model_type,
                "use_coef": args.use_coef,
                "epoch": epoch,
                "val_metric_best": val_metric_best,
                "args": vars(args),
                "params": {
                    "set_agg_type": args.set_agg_type,
                    "inst_agg_type": args.set_agg_type,
                    "use_context": bool(args.use_context),
                    "use_inst_embedding_norm": bool(args.use_inst_embedding_norm),
                },
            }
            if "inst" in args.model_type:
                emergency_data["instance_decision_embedder"] = net.instance_decision_embedder
                emergency_data["final_instance_embedder"] = net.final_instance_embedder
                emergency_data["value_predictor"] = net.value_predictor
                if net.use_context:
                    emergency_data["context_proj"] = net.context_proj
                if net.use_inst_embedding_norm:
                    emergency_data["inst_embedding_norm"] = net.inst_embedding_norm
                    emergency_data["use_inst_embedding_norm"] = True
                if net.use_attention:
                    emergency_data["attention_proj"] = net.attention_proj
                    emergency_data["attention"] = net.attention
                    emergency_data["params"]["attention_num_heads"] = net.attention_num_heads
            elif "set" in args.model_type:
                emergency_data["decision_embedder"] = net.decision_embedder
                emergency_data["value_predictor"] = net.value_predictor
            elif "ff" in args.model_type:
                emergency_data["feedforward_net"] = net.feedforward_net

            os.makedirs("data", exist_ok=True)
            torch.save(emergency_data, "data/EMERGENCY_v7_checkpoint.pt")

            if args.n_epochs - epoch < 200:
                print("    Extending training budget.")
                args.n_epochs *= 2

        if epoch - loss_epoch_min_idx >= 200:
            print(f"  Early stopping triggered at epoch {epoch}.")
            break

    print("Training finished.")
    total_train_time = time.time() - train_start_time

    if best_model is None:
        best_model = net

    best_model.eval()
    eval_res = test_model_predictions(
        cfg=cfg,
        net=best_model,
        loader=val_loader,
        model_type=args.model_type,
        get_ranking=True,
        verbose=False,
    )

    print(f"\n  Final model validation results:")
    print(f"          val_mape:       {eval_res['mape']:.6f}")
    print(f"          val_mae:        {eval_res['mae']:.6f}")
    print(f"          err_max_over:   {eval_res['err_max_over']:.6f}")
    print(f"          err_max_under:  {eval_res['err_max_under']:.6f}\n")

    params = {
        "batch_size": args.batch_size,
        "lr": args.lr,
        "optimizer": args.optimizer,
        "n_epochs": args.n_epochs,
        "dropout": args.dropout,
        "use_coef": args.use_coef,
    }

    if "set" in args.model_type:
        params.update({
            "set_embed_hidden_dim": args.set_embed_hidden_dim,
            "set_embed_output_dim": args.set_embed_output_dim,
            "set_value_hidden_dim": args.set_value_hidden_dim,
            "set_embed_relu_output": args.set_embed_relu_output,
            "set_value_relu_output": args.set_value_relu_output,
            "set_agg_type": args.set_agg_type,
        })
    elif "ff" in args.model_type:
        params.update({
            "ff_hidden_dim": args.ff_hidden_dim,
            "ff_relu_output": args.ff_relu_output,
        })
    elif "inst" in args.model_type:
        params.update({
            "inst_embed_hidden_dim": args.inst_embed_hidden_dim,
            "inst_embed_output_dim": args.inst_embed_output_dim,
            "inst_post_agg_hidden_dim": args.inst_post_agg_hidden_dim,
            "inst_post_agg_output_dim": args.inst_post_agg_output_dim,
            "inst_value_hidden_dim": args.inst_value_hidden_dim,
            "inst_embed_relu_output": args.inst_embed_relu_output,
            "inst_post_agg_relu_output": args.inst_post_agg_relu_output,
            "inst_value_relu_output": args.inst_value_relu_output,
            "inst_agg_type": args.inst_agg_type,
            "use_context": bool(args.use_context),
            "use_rank_labels": bool(args.use_rank_labels),
            "context_hidden_dim": args.context_hidden_dim,
            "use_inst_embedding_norm": bool(args.use_inst_embedding_norm),
            "use_attention": bool(args.use_attention),
            "attention_num_heads": args.attention_num_heads,
            "attention_hidden_dim": args.attention_hidden_dim,
            "activation": args.activation,
            "leaky_relu_slope": args.leaky_relu_slope,
            "embedder_decay_mult": embedder_decay_mult,
            "ranking_loss_weight": args.ranking_loss_weight,
            "ranking_loss_k": args.ranking_loss_k,
            "ranking_margin": args.ranking_margin,
        })

    if "kp" in args.problem:
        params["kp_use_greedy"] = args.kp_use_greedy

    results = {
        "val_metric": args.metric,
        "val_metric_min": val_metric_best,
        "val_results": val_results,
        "eval_res": eval_res,
        "term_epoch": epoch,
        "tr_losses": loss_epoch,
        "params": params,
        "train_time": total_train_time,
    }

    # Append timestamp to archive filenames
    param_str = get_nn_param_str(args, params)
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    param_str = f"{param_str}__ts-{run_timestamp}"

    # Save timestamped results and weights
    fp_res = get_path(cfg.data_path, cfg, f"random_search/nn_res_{args.model_type}_{args.approx_type}")
    fp_res = str(fp_res).replace(".pkl", f"__{param_str}__.pkl")
    with open(fp_res, "wb") as p:
        pkl.dump(results, p)
    print("  Saved training results to:", fp_res)

    fp_net = get_path(cfg.data_path, cfg, f"random_search/nn_{args.model_type}_{args.approx_type}", suffix="pt")
    fp_net = str(fp_net).replace(".pt", f"__{param_str}__.pt")

    save_data = {
        "model_type": args.model_type,
        "use_coef": args.use_coef,
        "err_max_over": eval_res["err_max_over"],
        "err_max_under": eval_res["err_max_under"],
        "label_scaler": data_preprocessor.label_scaler,
        "params": params,
        "train_time": total_train_time,
    }
    if "kp" in args.problem:
        save_data["kp_use_greedy"] = args.kp_use_greedy

    if "set" in args.model_type:
        save_data["decision_embedder"] = net.decision_embedder
        save_data["value_predictor"] = net.value_predictor
    elif "ff" in args.model_type:
        save_data["feedforward_net"] = net.feedforward_net
    elif "inst" in args.model_type:
        save_data["instance_decision_embedder"] = net.instance_decision_embedder
        save_data["final_instance_embedder"] = net.final_instance_embedder
        save_data["value_predictor"] = net.value_predictor
        if net.use_context:
            save_data["context_proj"] = net.context_proj
        if net.use_inst_embedding_norm:
            save_data["inst_embedding_norm"] = net.inst_embedding_norm
            save_data["use_inst_embedding_norm"] = True
        if net.use_attention:
            save_data["attention_proj"] = net.attention_proj
            save_data["attention"] = net.attention

    torch.save(save_data, fp_net)
    print("  Saved model to:", fp_net)

    # Save to short path for downstream evaluation scripts
    fp_net_short = get_path(cfg.data_path, cfg, f"nn_{args.model_type}_both", suffix="pt")
    torch.save(save_data, fp_net_short)
    print("  Saved model (short path):", fp_net_short)

    fp_res_short = get_path(cfg.data_path, cfg, f"nn_res_{args.model_type}_both")
    with open(fp_res_short, "wb") as p:
        pkl.dump(results, p)
    print("  Saved training results (short path):", fp_res_short)


# ---------------------------------------------------------------------------
# CLI Argument Parser
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Train neural networks for bi-level optimization lower/upper level approximation."
    )

    parser.add_argument("--problem", type=str, default="kp")
    parser.add_argument(
        "--model_type",
        type=str,
        default="inst_encoder",
        choices=["ff_fixed", "ff_invariant", "set_invariant", "inst_encoder"],
    )
    parser.add_argument(
        "--approx_type",
        type=str,
        default="both",
        choices=["lower", "upper", "both"],
    )
    parser.add_argument(
        "--metric",
        type=str,
        default="mae",
        choices=["mape", "mae", "top1_acc"],
    )

    # Problem-specific and data preprocessing arguments
    parser.add_argument("--kp_use_greedy", type=int, default=0, help="Use greedy knapsack features.")
    parser.add_argument("--scale_labels", type=int, default=0, help="Scale objective targets.")

    # General optimization hyperparameters
    parser.add_argument("--batch_size", type=int, default=32, help="Training batch size.")
    parser.add_argument("--batch_size_eval", type=int, default=32, help="Evaluation batch size.")
    parser.add_argument("--lr", type=float, default=1e-2, help="Learning rate.")
    parser.add_argument("--optimizer", type=str, default="Adam", help="Optimizer name from torch.optim.")
    parser.add_argument("--weight_decay", type=float, default=0.0, help="L2 regularization weight decay.")
    parser.add_argument(
        "--embedder_decay_mult",
        type=float,
        default=1.0,
        help="Weight decay multiplier for instance decision embedder modules.",
    )
    parser.add_argument("--n_epochs", type=int, default=1000, help="Number of training epochs.")
    parser.add_argument("--dropout", type=float, default=0.0, help="Dropout probability.")
    parser.add_argument("--use_coef", type=int, default=1, help="Multiply predictions by objective coefficients.")

    # FeedForwardNetwork parameters
    parser.add_argument("--ff_hidden_dim", nargs="+", type=int, default=[64], help="Hidden dimensions for feed-forward net.")
    parser.add_argument("--ff_relu_output", type=int, default=0, help="Apply ReLU to feed-forward network output.")

    # SetBasedNetwork parameters
    parser.add_argument("--set_embed_hidden_dim", type=int, nargs="+", default=[64], help="Hidden dims for decision embedder.")
    parser.add_argument("--set_embed_output_dim", type=int, default=16, help="Output dim for decision embedder.")
    parser.add_argument("--set_value_hidden_dim", type=int, nargs="+", default=[64], help="Hidden dims for value predictor.")
    parser.add_argument("--set_embed_relu_output", type=int, default=0, help="Apply ReLU to decision embedder output.")
    parser.add_argument("--set_value_relu_output", type=int, default=0, help="Apply ReLU to value predictor output.")
    parser.add_argument("--set_agg_type", type=str, default="sum", choices=["sum", "mean"], help="Set aggregation method.")

    # SetInstanceEncodingNetwork parameters
    parser.add_argument("--inst_embed_hidden_dim", type=int, nargs="+", default=[128], help="Hidden dims for instance embedder.")
    parser.add_argument("--inst_embed_output_dim", type=int, default=64, help="Output dim for instance embedder.")
    parser.add_argument("--inst_post_agg_hidden_dim", type=int, nargs="+", default=[128], help="Hidden dims for post-aggregation net.")
    parser.add_argument("--inst_post_agg_output_dim", type=int, default=32, help="Output dim for post-aggregation net.")
    parser.add_argument("--inst_value_hidden_dim", type=int, nargs="+", default=[128], help="Hidden dims for value predictor.")
    parser.add_argument("--inst_embed_relu_output", type=int, default=0, help="Apply ReLU to instance embedder output.")
    parser.add_argument("--inst_post_agg_relu_output", type=int, default=0, help="Apply ReLU to post-aggregation net output.")
    parser.add_argument("--inst_value_relu_output", type=int, default=0, help="Apply ReLU to value predictor output.")
    parser.add_argument("--inst_agg_type", type=str, default="sum", choices=["sum", "mean"], help="Instance aggregation method.")

    # Context and attention interaction arguments
    parser.add_argument("--use_context", type=int, default=0, help="Enable leave-one-out context sum across switch points.")
    parser.add_argument("--context_hidden_dim", type=int, default=32, help="Hidden dim for context projection.")
    parser.add_argument("--context_relu_output", type=int, default=1, help="Apply ReLU to context projection output.")
    parser.add_argument("--use_attention", type=int, default=0, help="Enable multi-head self-attention.")
    parser.add_argument("--attention_num_heads", type=int, default=4, help="Number of attention heads.")
    parser.add_argument("--attention_hidden_dim", type=int, default=32, help="Embedding dimension for attention block.")
    parser.add_argument("--use_inst_embedding_norm", type=int, default=0, help="Apply LayerNorm to aggregated instance embeddings.")
    parser.add_argument(
        "--activation",
        type=str,
        default="relu",
        choices=["relu", "leaky_relu", "gelu", "silu"],
        help="Activation function for FeedForwardBase modules.",
    )
    parser.add_argument("--leaky_relu_slope", type=float, default=0.01, help="Negative slope for LeakyReLU.")

    # Ranking loss parameters
    parser.add_argument("--ranking_loss_weight", type=float, default=0.0, help="Weight for pairwise ranking loss.")
    parser.add_argument("--ranking_loss_k", type=int, default=5, help="Number of top/bottom pairs for ranking loss.")
    parser.add_argument("--ranking_margin", type=float, default=0.0, help="Margin for ranking loss penalty.")
    parser.add_argument("--use_rank_labels", type=int, default=0, help="Use rank-based labels instead of raw objective values.")
    parser.add_argument("--samples_per_inst", type=int, default=50, help="Samples per instance for grouped ranking batch sampler.")

    parser.add_argument("--seed", type=int, default=12345, help="Random seed for reproducibility.")

    args = parser.parse_args()
    main(args)