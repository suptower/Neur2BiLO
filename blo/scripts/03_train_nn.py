# general
import math
import time
import copy
import argparse
import collections
import datetime
import numpy as np
import pandas as pd
import pickle as pkl
from scipy import stats 
import os

# gurobi
import gurobipy as gp
from gurobi_ml import add_predictor_constr
import matplotlib.pyplot as plt

# torch
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader

# sklearn
from sklearn.metrics import mean_absolute_error as MAE
from sklearn.metrics import mean_squared_error as MSE

# blo
import blo.params as blo_params
from blo.utils import load_problem, factory_get_path
from blo.data_preprocessor import factory_dp

from blo.models import *




#-----------------------------------------------------------------------#
#                                                                       #
#           File to train nn to approximation lower-level obj           # 
#                                                                       #
#-----------------------------------------------------------------------#


#------------------------------------------------#
#           Functions for evaluation             #
#------------------------------------------------#

def forward_pass_all_data(net, loader, model_type):
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

            labels = labels.cpu().numpy().reshape(-1)
            preds = preds.detach().cpu().numpy().reshape(-1)
            inst_ids = inst_ids.cpu().numpy().reshape(-1)

            labels_all += labels.tolist()
            preds_all += preds.tolist()
            inst_ids_all += inst_ids.tolist()

    return labels_all, preds_all, inst_ids_all




def test_model_predictions(cfg, net, loader, model_type, print_predictions=False, get_ranking=False, verbose=True):
    """ Evaluations model. """
    err = 0
    err_max_over = -1
    err_max_under = -1
    counter = 0
    labels_instance = []
    outputs_instance = []
    res_kendall_all = []
    top1_correct = 0
    top1_total = 0

    labels_all, preds_all, inst_ids_all = forward_pass_all_data(net, loader, model_type)

    # MAPE/MAE berechnen
    for i in range(len(labels_all)):
        pred = preds_all[i]
        label = labels_all[i]
        mae_cur = np.abs(label - pred)
        err_cur = np.abs(label - pred) / (label + 1e-8)
        err += err_cur
        err_max_over = np.max([err_cur, err_max_over]) if pred - label > 0 else err_max_over
        err_max_under = np.max([err_cur, err_max_under]) if pred - label < 0 else err_max_under
        counter += 1

    mae = mae_cur / counter
    mape = err / counter

    # Top-1 accuracy: gruppiere nach inst_id
    from collections import defaultdict
    inst_labels = defaultdict(list)
    inst_preds  = defaultdict(list)
    for label, pred, iid in zip(labels_all, preds_all, inst_ids_all):
        inst_labels[iid].append(label)
        inst_preds[iid].append(pred)
    top1_correct = sum(
        np.argmin(inst_labels[iid]) == np.argmin(inst_preds[iid])
        for iid in inst_labels
    )
    top1_total = len(inst_labels)
    top1_acc = top1_correct / top1_total if top1_total > 0 else 0.0

    if verbose:
        print("Mean Percentage Error =", mape)
        print("max over/underestimate :", err_max_over, err_max_under)
        if get_ranking:
            print("Kendall:", np.min(res_kendall_all), np.median(res_kendall_all), np.max(res_kendall_all))
            print("Top-1 Accuracy:", top1_acc)

    res = {
        "mae"            : mae,
        "mape"           : mape,
        "top1_acc"       : top1_acc,
        "err_max_over"   : err_max_over,
        "err_max_under"  : err_max_under,
        "kendall_all"    : res_kendall_all,
        "kendall_min"    : np.min(res_kendall_all) if res_kendall_all else 0,
        "kendall_max"    : np.max(res_kendall_all) if res_kendall_all else 0,
        "kendall_median" : np.median(res_kendall_all) if res_kendall_all else 0,
        "kendall_mean"   : np.mean(res_kendall_all) if res_kendall_all else 0,
    }
    
    return res


def get_nn_param_str(args, params):
    """ Gets parameter string for use in random search. Will need to be changed as more params are added. """

    def lst_to_str(lst):
        """ Converts list of str/int to single string """
        lst_str = list(map(lambda x: str(x), lst))
        return "-".join(lst_str)

    nn_param_str = ""

    nn_param_str += f"bs-{params['batch_size']}_"
    nn_param_str += f"lr-{params['lr']}_"
    nn_param_str += f"o-{params['optimizer']}_"
    nn_param_str += f"ep-{params['n_epochs']}_"
    nn_param_str += f"do-{params['dropout']}_"

    if "ff" in args.model_type:
        nn_param_str += f"ff-h-{lst_to_str(params['ff_hidden_dim'])}_"
        nn_param_str += f"ff-ro-{params['ff_relu_output']}"

    elif "set" in args.model_type:
        nn_param_str += f"set-eh-{lst_to_str(params['set_embed_hidden_dim'])}_"
        nn_param_str += f"set-eo-{params['set_embed_output_dim']}_"
        nn_param_str += f"set-vh-{lst_to_str(params['set_value_hidden_dim'])}_"
        nn_param_str += f"set-ero-{params['set_embed_relu_output']}_"
        nn_param_str += f"set-vro-{params['set_value_relu_output']}_"
        nn_param_str += f"set-a-{params['set_agg_type']}"

    elif "inst" in args.model_type:
        nn_param_str += f"in-eh-{lst_to_str(params['inst_embed_hidden_dim'])}_"
        nn_param_str += f"in-eo-{params['inst_embed_output_dim']}_"
        nn_param_str += f"in-ph-{lst_to_str(params['inst_post_agg_hidden_dim'])}_"
        nn_param_str += f"in-po-{params['inst_post_agg_output_dim']}_"
        nn_param_str += f"in-vh-{lst_to_str(params['inst_value_hidden_dim'])}_"
        nn_param_str += f"in-ero-{params['inst_embed_relu_output']}_"
        nn_param_str += f"in-pro-{params['inst_post_agg_relu_output']}_"
        nn_param_str += f"in-vro-{params['inst_value_relu_output']}_"
        nn_param_str += f"in-a-{params['inst_agg_type']}_"
        # Diese beiden Flags fehlten bisher komplett im Dateinamen, obwohl sie
        # das Verhalten des Netzes grundlegend aendern (siehe LayerNorm-Fix
        # gegen das Dying-ReLU-Problem in final_instance_embedder) -- ohne sie
        # erzeugten zwei architektonisch verschiedene Laeufe denselben
        # Dateinamen und ueberschrieben sich gegenseitig stillschweigend.
        nn_param_str += f"in-ctx-{int(bool(params.get('use_context', False)))}_"
        nn_param_str += f"in-ln-{int(bool(params.get('use_inst_embedding_norm', False)))}_"
        nn_param_str += f"in-act-{params.get('activation', 'relu')}"

    return nn_param_str



#------------------------------------------------#
#                     Main                       #
#------------------------------------------------#

def main(args):
    
    torch.manual_seed(args.seed)
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")

    print(f"Getting instance/path info for {args.problem} ...")
    
    # Get cfg, paths, functions
    cfg = getattr(blo_params, args.problem)

    # get all paths
    get_path = factory_get_path(args)
    fp_data = get_path(cfg.data_path, cfg, "ml_data")

    # load data — use precomputed compact .npz if available (avoids the
    # RAM-heavy raw-pickle load + get_inst_encoder_dataset pass, see
    # convert_ml_data.py). Falls back to the original path otherwise.
    fp_compact = str(fp_data).replace(".pkl", "_compact.npz")
    data_preprocessor = factory_dp(args, args.model_type, args.approx_type, args.problem, device)

    if os.path.exists(fp_compact) and args.model_type == "inst_encoder":
        print(f"Loading precomputed compact dataset from {fp_compact} ... ")
        npz = np.load(fp_compact)

        def _mk_dataset(prefix):
            tensors = [
                torch.from_numpy(npz[f"{prefix}_inst_features"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_decision_features"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_decisions"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_n_decisions"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_labels"]).float().to(device),
                torch.from_numpy(npz[f"{prefix}_inst_ids"]).float().to(device),
            ]
            return TensorDataset(*tensors)

        tr_dataset = _mk_dataset("tr")
        val_dataset = _mk_dataset("val")
        dataset = None  # raw dataset not loaded — only used below for scale_labels, unsupported in this fast path
        if args.scale_labels:
            raise NotImplementedError("--scale_labels requires the raw .pkl dataset; delete the _compact.npz or disable scale_labels")
    else:
        print("Loading data for machine learning ... ")
        with open(fp_data, 'rb') as pf:
            dataset = pkl.load(pf)

        print("Preprocessing data  ... ")
        if args.scale_labels and args.problem in ["watwa"]:
            print("  Scaling labels for watwa ...")
            data_preprocessor.get_label_scalers(dataset['tr_data'] + dataset['val_data'])
        elif args.scale_labels:
            print("  Scaling labels ...")
            data_preprocessor.get_label_scalers(dataset['tr_data'])

        tr_dataset, val_dataset = data_preprocessor.preprocess_data(dataset['tr_data'], dataset['val_data'])

    # create train/validation loaders
    # Instanz-gruppierter Sampler für Ranking-Loss
    if "inst" in args.model_type and args.ranking_loss_weight > 0:
        from torch.utils.data import BatchSampler, SequentialSampler
        # inst_ids sind der letzte Tensor im Dataset
        all_inst_ids = tr_dataset.tensors[-1].long().tolist()
        # Gruppiere Indices nach inst_id
        from collections import defaultdict
        id_to_indices = defaultdict(list)
        for idx, iid in enumerate(all_inst_ids):
            id_to_indices[int(iid)].append(idx)
        # Baue Batches: pro Batch samples_per_inst Samples aus batch_size//samples_per_inst Instanzen
        samples_per_inst = args.samples_per_inst
        insts_per_batch = max(1, args.batch_size // samples_per_inst)
        inst_keys = list(id_to_indices.keys())
        grouped_batches = []
        np.random.shuffle(inst_keys)
        for i in range(0, len(inst_keys), insts_per_batch):
            batch = []
            for iid in inst_keys[i:i+insts_per_batch]:
                idxs = id_to_indices[iid]
                chosen = np.random.choice(idxs, min(samples_per_inst, len(idxs)), replace=False).tolist()
                batch.extend(chosen)
            grouped_batches.append(batch)
        tr_loader = DataLoader(tr_dataset, batch_sampler=grouped_batches)
        val_loader = DataLoader(val_dataset, shuffle=False, batch_size=args.batch_size_eval)
    else:
        tr_loader = DataLoader(tr_dataset, shuffle=True, batch_size=args.batch_size)
        val_loader = DataLoader(val_dataset, shuffle=False, batch_size=args.batch_size_eval)

    # initializing model
    print("Initializing Model  ... ")

    if "set" in args.model_type:

        # get output dimension (may need to be done case-by-case)
        if "kp" in args.problem:
            value_output_dim = cfg.n[0]

        feat_size = tr_dataset[0][0].shape[-1]
        
        # decision embedding network
        decision_embedder = FeedForwardBase(
            input_dim = feat_size, 
            hidden_dims = args.set_embed_hidden_dim, 
            output_dim = args.set_embed_output_dim, 
            output_relu = args.set_embed_relu_output, 
            dropout = args.dropout, 
            bias = False,
            name="decision_embedder")

        # force value dimension to be 1 if not prediction second-stage coef dimension
        if not args.use_coef:
            value_output_dim = 1

        # value predictor
        value_predictor = FeedForwardBase(
            input_dim = args.set_embed_output_dim,  
            hidden_dims = args.set_value_hidden_dim, 
            output_dim = value_output_dim, 
            output_relu = args.set_value_relu_output, 
            dropout = args.dropout, 
            bias = True,
            name = "value")

        decision_embedder.to(device)
        value_predictor.to(device)

        net = SetBasedNetwork(
            decision_embedder = decision_embedder, 
            value_predictor = value_predictor, 
            agg_type = args.set_agg_type,
            use_coef = args.use_coef)

    elif "ff" in args.model_type:

        if "fixed" in args.model_type:
            assert(len(cfg.n) == 1) # ff_fixed   only works for fixed n

        input_size = len(tr_dataset[0][0])

        # get output dimension (may need to be done case-by-case)
        if "kp" in args.problem:
            value_output_dim = cfg.n[0]

        # force value dimension to be 1 if not prediction second-stage coef dimension
        if not args.use_coef:
            value_output_dim = 1
        
        # initialize ff_net
        ff_net = FeedForwardBase(
            input_dim = input_size,  
            hidden_dims = args.ff_hidden_dim, 
            output_dim = value_output_dim, 
            output_relu = args.ff_relu_output, 
            dropout = args.dropout, 
            bias = True,
            name = "ff")

        ff_net.to(device)

        net = FeedForwardNetwork(ff_net, use_coef = args.use_coef)

    elif "inst" in args.model_type:
 
        inst_feat_size = tr_dataset[0][0].shape[-1]
        decision_feat_size = tr_dataset[0][1].shape[-1]
 
        # instance embedding networks
        instance_decision_embedder = FeedForwardBase(
            input_dim = inst_feat_size,
            hidden_dims = args.inst_embed_hidden_dim,
            output_dim = args.inst_embed_output_dim,
            output_relu = args.inst_embed_relu_output,
            dropout = args.dropout,
            bias = False,
            activation = args.activation,
            leaky_relu_slope = args.leaky_relu_slope,
            name="instance_decision_embedder")
 
        final_instance_embedder = FeedForwardBase(
            input_dim = args.inst_embed_output_dim,
            hidden_dims = args.inst_post_agg_hidden_dim,
            output_dim = args.inst_post_agg_output_dim,
            output_relu = args.inst_post_agg_relu_output,
            dropout = args.dropout,
            bias = True,
            activation = args.activation,
            leaky_relu_slope = args.leaky_relu_slope,
            name="final_instance_embedder")
 
        # raw per-switch-point feature dim BEFORE context concat
        # (decision features + broadcast instance embedding)
        own_feat_dim = decision_feat_size + args.inst_post_agg_output_dim
 
        # --- NEW: context projection (MIP-compatible cross-switch-point interaction) ---
        context_proj = None
        value_input_dim = own_feat_dim
        if args.use_context:
            context_proj = FeedForwardBase(
                input_dim = own_feat_dim,
                hidden_dims = [args.context_hidden_dim],  # mindestens 1 Hidden-Layer nötig
                output_dim = args.context_hidden_dim,
                output_relu = args.context_relu_output,
                dropout = args.dropout,
                bias = True,
                activation = args.activation,
                leaky_relu_slope = args.leaky_relu_slope,
                name = "context_proj")
            context_proj.to(device)
 
            # value_predictor must accept the concatenated [own_feats, context] vector
            value_input_dim = own_feat_dim + args.context_hidden_dim
 
        # value predictor
        value_predictor = FeedForwardBase(
            input_dim = value_input_dim,
            hidden_dims = args.inst_value_hidden_dim,
            output_dim = 1,
            output_relu = args.inst_value_relu_output,
            dropout = args.dropout,
            bias = True,
            activation = args.activation,
            leaky_relu_slope = args.leaky_relu_slope,
            name = "value")
 
        instance_decision_embedder.to(device)
        final_instance_embedder.to(device)
        value_predictor.to(device)
 
        net = SetInstanceEncodingNetwork(
            instance_decision_embedder = instance_decision_embedder,
            final_instance_embedder = final_instance_embedder,
            value_predictor = value_predictor,
            agg_type = args.set_agg_type,
            use_coef = args.use_coef,
            problem = args.problem,
            approx_type = args.approx_type,
            use_context = bool(args.use_context),
            context_proj = context_proj,
            use_inst_embedding_norm = bool(args.use_inst_embedding_norm))

    else:
        raise Exception("No other model_types implemented")

    # loss
    weighted_loss = False
    criterion = nn.MSELoss()

    # optimizer
    Opt = getattr(torch.optim, args.optimizer)
    optimizer = Opt(net.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # Staerkere Regularisierung auf value_predictor UND context_proj, da beide
    # Submodule direkt in die Big-M-Bound-Propagation der Surrogate-MIP eingehen.
    # context_proj wird pro Switch-Point einmal ausgewertet (Leave-one-out-Summe),
    # sein Beitrag zu den Bounds waechst also mit s -- bei grossen Instanzen war
    # das bisher der dominante, unregulierte Anteil.
    if "inst" in args.model_type and args.weight_decay > 0:
        value_param_names = [n for n, p in net.named_parameters() if 'value_predictor' in n]
        print(f"  [param_groups] {len(value_param_names)} params in strong-decay group:")
        for n in value_param_names:
            print(f"    {n}")
        param_groups = [
            {'params': [p for n, p in net.named_parameters()
                        if 'value_predictor' not in n],
            'weight_decay': args.weight_decay},
            {'params': [p for n, p in net.named_parameters()
                        if 'value_predictor' in n],
            'weight_decay': args.weight_decay * 1000},
        ]
        optimizer = Opt(param_groups, lr=args.lr)
    else:
        optimizer = Opt(net.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    # scdheuler
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, 'min', factor=0.9, cooldown=100)

    # training model
    print("Training Model  ... ")

    val_mapes = []
    val_results = []

    loss_epoch = []
    # val_mape_min = math.inf
    val_metric_best = -math.inf if args.metric == "top1_acc" else math.inf
    loss_epoch_min_idx = 0

    total_size = len(tr_loader)
    train_time = time.time()

    for epoch in range(args.n_epochs):
        
        loss_epoch += [0]
        for i, batch_data in enumerate(tr_loader, 0):

            # forward pass for invariant models
            if "set" in args.model_type:
                features, n_decisions, p, labels = batch_data
                preds = net(features, p, n_decisions)

            # forward pass for feed-forward models
            elif "ff" in args.model_type:
                features, p, labels = batch_data
                preds = net(features, p)

            elif "inst" in args.model_type:
                inst_features, decisions_features, x, n_decisions, labels, inst_ids = batch_data
                p = torch.zeros(inst_features.shape[0], 1, device=inst_features.device)  # dummy p tensor
                preds = net(inst_features, decisions_features, x, p, n_decisions)

            # compute loss
            mse_loss = criterion(preds, labels)
            ranking_loss = torch.tensor(0.0, device=preds.device)
            if "inst" in args.model_type and args.ranking_loss_weight > 0:
                preds_flat  = preds.squeeze(-1)
                labels_flat = labels.squeeze(-1)
                k = args.ranking_loss_k
                for uid in inst_ids.unique():
                    mask = (inst_ids == uid)
                    if mask.sum() < 2 * k:
                        continue
                    p_lab = labels_flat[mask]
                    p_pre = preds_flat[mask]
                    _, bot_idx = torch.topk(p_lab, k, largest=False)
                    _, top_idx = torch.topk(p_lab, k, largest=True)
                    best_preds  = p_pre[bot_idx]
                    worst_preds = p_pre[top_idx]
                    margin_violations = torch.relu(
                        best_preds.unsqueeze(1) - worst_preds.unsqueeze(0) + args.ranking_margin
                    )
                    ranking_loss = ranking_loss + margin_violations.mean()

            loss = mse_loss + args.ranking_loss_weight * ranking_loss
            loss_epoch[-1] += loss.item() / len(tr_loader)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        # get validation results
        val_res = test_model_predictions(
            cfg = cfg,
            net = net,
            loader = val_loader,
            model_type = args.model_type, 
            get_ranking = True, 
            verbose = False)

        # add results from iteration
        val_results.append(val_res)

        # update learning-rate scheduler
        scheduler.step(loss_epoch[-1])

        # print/update best model
        print(f'  Epoch: {epoch}: ')
        print(f'          val_mae:        {val_res["mae"]:.6f}')
        print(f'          val_mape:       {val_res["mape"]:.6f}')
        print(f'          tr_loss:        {loss_epoch[-1]:.6f}')
        print(f'          err_max_over:   {val_res["err_max_over"]:.6f}')
        print(f'          err_max_under:  {val_res["err_max_under"]:.6f}')
        print(f'          val_top1_acc:   {val_res["top1_acc"]:.6f}')
        if "inst" in args.model_type and epoch % 5 == 0:
            for mod_name in ["instance_decision_embedder", "final_instance_embedder"]:
                mod = getattr(net, mod_name, None)
                if mod is not None:
                    total_norm = sum(p.norm().item() for p in mod.parameters())
                    print(f'          {mod_name}_norm: {total_norm:.6f}')

        val_metric = val_res[args.metric]
        is_better = val_metric > val_metric_best if args.metric == "top1_acc" else val_metric < val_metric_best
        loss_epoch_min_idx = epoch if is_better else loss_epoch_min_idx
        if loss_epoch_min_idx == epoch:
            print("    new best model")
            val_metric_best = val_metric
            best_model = copy.deepcopy(net) # copy.deepcopy(net.state_dict())

            # Emergency-Checkpoint im GLEICHEN Format wie der finale save_data-Block
            # weiter unten (Submodul-Objekte statt flachem state_dict), damit
            # load_scoring_net() (eval_no_gurobi.py, pruning_rank_histogram.py,
            # check_scale_mismatch.py, etc.) den Zwischenstand ohne Sonderfall
            # laden kann. 'params' existiert an dieser Stelle noch nicht (wird
            # erst nach der Trainingsschleife gebaut) -- deshalb hier ein
            # minimales, aber fuer load_scoring_net ausreichendes Params-Dict.
            emergency_data = {
                'model_type': args.model_type,
                'use_coef': args.use_coef,
                'epoch': epoch,
                'val_metric_best': val_metric_best,
                'args': vars(args),
                'params': {
                    'set_agg_type': args.set_agg_type,
                    'inst_agg_type': args.set_agg_type,  # net wird mit set_agg_type gebaut (s.o.)
                    'use_context': bool(args.use_context),
                    'use_inst_embedding_norm': bool(args.use_inst_embedding_norm),
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
            elif "set" in args.model_type:
                emergency_data["decision_embedder"] = net.decision_embedder
                emergency_data["value_predictor"] = net.value_predictor
            elif "ff" in args.model_type:
                emergency_data["feedforward_net"] = net.feedforward_net

            torch.save(emergency_data, 'data/EMERGENCY_v7_checkpoint.pt')
            print("    [emergency checkpoint saved: data/EMERGENCY_v7_checkpoint.pt]")

            # if model found within last 200 epochs, then increase # of epochs
            if args.n_epochs - epoch < 200:
                print('    doubling epochs!!!')
                args.n_epochs *= 2

        # if True and epoch >= 10 and np.abs(loss_epoch[-1]-np.mean(loss_epoch[-11:-1]))/np.mean(loss_epoch[-11:-1]) <= 1e-3:
        if True and epoch - loss_epoch_min_idx >= 200:
            print('  Early termination!', loss_epoch[-1], loss_epoch[-6])
            break

        if (epoch+1) % 10 == 0:
            print("    Epoch {}/{} Step {}/{} : Epoch {} {:.6f}, Loss {:.6f}".format(epoch+1, args.n_epochs,i+1, total_size, args.metric, val_metric, loss_epoch[-1]))
            print("    Best Epoch {} : Best {}, {:.6f}, Best Loss {:.6f}".format(loss_epoch_min_idx+1, args.metric, val_metric_best, loss_epoch[loss_epoch_min_idx]))

    print("Done training")

    best_model.eval()
    eval_res = test_model_predictions(
        cfg = cfg,
        net = best_model,
        loader = val_loader,
        model_type = args.model_type, 
        get_ranking = True,
        verbose = False)

    print(f'\n  Final model validation results: ')
    print(f'          val_mape:       {eval_res["mape"]:.6f}')
    print(f'          val_mae:       {eval_res["mae"]:.6f}')
    print(f'          err_max_over:   {eval_res["err_max_over"]:.6f}')
    print(f'          err_max_under:  {eval_res["err_max_under"]:.6f}\n')

    # collect parameters and results
    params = {
        "batch_size" : args.batch_size,
        "lr" : args.lr,
        "optimizer" : args.optimizer,
        "n_epochs" : args.n_epochs,
        "dropout" : args.dropout,
        "use_coef" : args.use_coef,
    }

    if "set" in args.model_type:
        params["set_embed_hidden_dim"] = args.set_embed_hidden_dim
        params["set_embed_output_dim"] = args.set_embed_output_dim
        params["set_value_hidden_dim"] = args.set_value_hidden_dim

        params["set_embed_relu_output"] = args.set_embed_relu_output
        params["set_value_relu_output"] = args.set_value_relu_output

        params["set_agg_type"] = args.set_agg_type

    elif "ff" in args.model_type:
        params["ff_hidden_dim"] = args.ff_hidden_dim
        params["ff_relu_output"] = args.ff_relu_output

    elif "inst" in args.model_type:
        params["inst_embed_hidden_dim"] = args.inst_embed_hidden_dim
        params["inst_embed_output_dim"] = args.inst_embed_output_dim
        params["inst_post_agg_hidden_dim"] = args.inst_post_agg_hidden_dim
        params["inst_post_agg_output_dim"] = args.inst_post_agg_output_dim
        params["inst_value_hidden_dim"] = args.inst_value_hidden_dim

        params["inst_embed_relu_output"] = args.inst_embed_relu_output
        params["inst_post_agg_relu_output"] = args.inst_post_agg_relu_output
        params["inst_value_relu_output"] = args.inst_value_relu_output

        params["inst_agg_type"] = args.inst_agg_type

        params["use_context"] = bool(args.use_context)
        params["use_rank_labels"] = bool(args.use_rank_labels)
        params["context_hidden_dim"] = args.context_hidden_dim
        params["use_inst_embedding_norm"] = bool(args.use_inst_embedding_norm)
        params["activation"] = args.activation
        params["leaky_relu_slope"] = args.leaky_relu_slope
        params["ranking_loss_weight"] = args.ranking_loss_weight

        params["ranking_loss_k"] = args.ranking_loss_k
        params["ranking_margin"] = args.ranking_margin

    if "kp" in args.problem:
        params["kp_use_greedy"] = args.kp_use_greedy

    train_time = time.time() - train_time
    
    # collect results
    results = {
        'val_metric' : args.metric,
        'val_metric_min' : val_metric_best,
        'val_results' : val_results,
        'eval_res' : eval_res,
        'term_epoch' : epoch,
        'tr_losses' : loss_epoch,
        'params' : params,
        'train_time' : train_time,
    }
    
    # get parameter string
    param_str = get_nn_param_str(args, params)

    # Timestamp anhaengen, damit zwei Laeufe mit identischen Hyperparametern
    # (z.B. gleicher bs/lr/architecture, nur ein neues Flag wie
    # use_inst_embedding_norm dazugeschaltet, das noch nicht in
    # get_nn_param_str beruecksichtigt wurde -- oder schlicht ein Re-Run mit
    # anderem Seed) NIE mehr denselben random_search-Dateinamen erzeugen und
    # sich damit stillschweigend gegenseitig ueberschreiben. Betrifft NUR die
    # random_search/-Archivkopien unten, NICHT die kurzen Pfade
    # (nn_..._both_..._s-7.pt), die 05_run_ml_blo.py und die
    # Evaluations-/Diagnose-Skripte absichtlich unter festem Namen erwarten.
    run_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    param_str = f"{param_str}__ts-{run_timestamp}"

    # save results
    fp_res = get_path(cfg.data_path, cfg, f"random_search/nn_res_{args.model_type}_{args.approx_type}")
    fp_res = str(fp_res).replace(".pkl", f"__{param_str}__.pkl")

    with open(fp_res, 'wb') as p:
        pkl.dump(results, p)

    print('  Saved training results to:', fp_res)

    # save model
    fp_net = get_path(cfg.data_path, cfg, f"random_search/nn_{args.model_type}_{args.approx_type}", suffix="pt")
    fp_net = str(fp_net).replace(".pt", f"__{param_str}__.pt")

    
    # model data
    save_data = {
        'model_type' : args.model_type,
        'use_coef' : args.use_coef,
        'err_max_over' : eval_res['err_max_over'],
        'err_max_under' : eval_res['err_max_under'],
        'label_scaler' : data_preprocessor.label_scaler,
        # 'feat_scaler' : data_preprocessor.feat_scaler, # Not implemented
        'params': params,
        'train_time' : train_time,
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

    torch.save(save_data, fp_net)

    print('  Saved model to:', fp_net)

    # Zusätzlich unter dem kurzen "both"-Pfad speichern, den 05_run_ml_blo.py
    # standardmäßig sucht (ohne Hyperparameter-Suffix im Dateinamen).
    # Das ersetzt das bisherige manuelle Symlink-Setzen und verhindert, dass
    # Batch-Eval-Läufe versehentlich ein altes/falsches Modell laden.
    fp_net_short = get_path(cfg.data_path, cfg, f"nn_{args.model_type}_both", suffix="pt")
    torch.save(save_data, fp_net_short)
    print('  Saved model (short path, used by 05_run_ml_blo.py):', fp_net_short)
    
    # Gleiches für die Trainings-Ergebnisse (.pkl), falls 05_run_ml_blo.py oder
    # andere Scripts diese ebenfalls über den kurzen Pfad referenzieren.
    fp_res_short = get_path(cfg.data_path, cfg, f"nn_res_{args.model_type}_both")
    with open(fp_res_short, 'wb') as p:
        pkl.dump(results, p)
    print('  Saved training results (short path):', fp_res_short)

    return
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Trains network for predicting lower/upper level decisions.')

    parser.add_argument('--problem', type=str, default="kp")

    # data/model type, these may not need to be separate
    parser.add_argument('--model_type', type=str, default='inst_encoder', choices=['ff_fixed', 'ff_invariant', 'set_invariant', 'inst_encoder'])

    # approximation type (lower, upper, both [for interdiction])
    parser.add_argument('--approx_type', type=str, default='both', choices=['lower', 'upper', 'both'])

    # metric to track best model over
    parser.add_argument('--metric', type=str, default='mae', choices=['mape', 'mae', 'top1_acc'])

    # Knapsack specific
    parser.add_argument('--kp_use_greedy', type=int, default=0, help='Use greedy features.')

    # Scaling arguments
    # parser.add_argument('--scale_features', type=int, default=0, help='Boolean to scale features. ') 
    parser.add_argument('--scale_labels', type=int, default=0, help='Boolean to scale labels. Must be implemented for each problem in data_preprocessor.')

    # General NN parameters
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size.')
    parser.add_argument('--batch_size_eval', type=int, default=32, help='Batch size.')
    parser.add_argument('--lr', type=float, default=1e-2, help='Learning rate.')
    parser.add_argument('--optimizer', type=str, default='Adam')
    parser.add_argument('--weight_decay', type=float, default=0.0, help='L2 regularization weight decay.')
    parser.add_argument('--n_epochs', type=int, default=1000, help='Number of training epochs.')
    parser.add_argument('--dropout', type=float, default=0, help='Dropout rate.')

    # general BLO model specific params
    parser.add_argument('--use_coef', type=int, default=1, help='Use dot product with coefficients of objectives (if 1, predicts dot prod with n-dimensional output.)')

    # FeedForwardNetwork parameters
    parser.add_argument('--ff_hidden_dim', nargs="+", type=int, default=[64], help='Hidden dimensions for feed-forward network')
    parser.add_argument('--ff_relu_output',  type=int, default=0, help='Indicator for using ReLU on output for feed-forward network.')

    # SetBasedNetwork parameters
    parser.add_argument('--set_embed_hidden_dim', type=int, nargs="+", default=[64], help='Hidden dimensions for decision embedder.')
    parser.add_argument('--set_embed_output_dim', type=int, default=16, help='Output dimension for decision embedder.')
    parser.add_argument('--set_value_hidden_dim', type=int, nargs="+", default=[64], help='Hidden dimensions for value network.')
    parser.add_argument('--set_embed_relu_output', type=int, default=0, help='Indicator for using ReLU on output of decision embedder.')
    parser.add_argument('--set_value_relu_output', type=int, default=0, help='Indicator for using ReLU on output of value network.')
    parser.add_argument('--set_agg_type', type=str, default="sum", help='Type of aggregation (sum, mean).')

    # SetInstanceEncodingNetwork parameters
    parser.add_argument('--inst_embed_hidden_dim', type=int, nargs="+", default=[128], help='Hidden dimensions for decision embedder.')
    parser.add_argument('--inst_embed_output_dim', type=int, default=64, help='Output dimension for decision embedder.')
    parser.add_argument('--inst_post_agg_hidden_dim', type=int, nargs="+", default=[128], help='Hidden dimensions for decision embedder.')
    parser.add_argument('--inst_post_agg_output_dim', type=int, default=32, help='Output dimension for decision embedder.')
    parser.add_argument('--inst_value_hidden_dim', type=int, nargs="+", default=[128], help='Hidden dimensions for value network.')

    parser.add_argument('--inst_embed_relu_output', type=int, default=0, help='Indicator for using ReLU on output of decision embedder.')
    parser.add_argument('--inst_post_agg_relu_output', type=int, default=0, help='Indicator for using ReLU on output of decision embedder.')
    parser.add_argument('--inst_value_relu_output', type=int, default=0, help='Indicator for using ReLU on output of value network.')

    parser.add_argument('--inst_agg_type', type=str, default="sum", help='Type of aggregation (sum, mean).')


    # Attention parameters -- IGNORE for now, no improvements seen
    parser.add_argument('--use_attention', type=int, default=0, help='Whether to use attention in instance encoder model.')
    parser.add_argument('--attention_num_heads', type=int, default=4, help='Number of heads for attention in instance encoder model.')

    parser.add_argument('--use_context', type=int, default=0, help='Whether to use leave-one-out context sum across switch points.')
    parser.add_argument('--context_hidden_dim', type=int, default=32, help='Hidden dimension for context projection (if use_context=1).')

    parser.add_argument('--use_inst_embedding_norm', type=int, default=0,
                         help='Whether to apply LayerNorm to the aggregated instance embedding '
                              'before final_instance_embedder. Mitigates a dying-ReLU collapse '
                              'observed at that bottleneck across all s during training '
                              '(diagnosed via check_dead_at_init.py / check_scale_mismatch.py: '
                              '~48-53%% dead at random init, but ~100%% dead after training, '
                              'for every s bucket tested).')

    parser.add_argument('--activation', type=str, default='relu', choices=['relu', 'leaky_relu', 'gelu', 'silu'],
                         help="Activation used throughout FeedForwardBase (instance_decision_embedder, "
                              "final_instance_embedder, context_proj, value_predictor). 'relu' is the "
                              "historical default. 'leaky_relu' is a candidate fix for the dying-ReLU "
                              "collapse observed even WITH use_inst_embedding_norm=1 (that fix alone "
                              "reduced but did not eliminate the collapse, ~97-98%% dead neurons "
                              "remaining at final_instance_embedder after training).")
    parser.add_argument('--leaky_relu_slope', type=float, default=0.01,
                         help='Negative-side slope for LeakyReLU (only used if --activation leaky_relu).')
    parser.add_argument('--context_relu_output', type=int, default=1, help='Indicator for using ReLU on output of context projection.')

    parser.add_argument('--ranking_loss_weight', type=float, default=0.0, help='Weight for ranking loss (only used for instance encoder model).')

    parser.add_argument('--ranking_loss_k', type=int, default=5,
        help='Top-k/Bottom-k pairs for ranking loss.')
    parser.add_argument('--use_rank_labels', type=int, default=0, help='Use rank-based labels instead of normalized energy.')
    parser.add_argument('--ranking_margin', type=float, default=0.0,
        help='Margin for ranking loss violations.')

    parser.add_argument('--samples_per_inst', type=int, default=50, help='Number of samples per instance for ranking loss batch sampling (only used for instance encoder model).')

    # random seed
    parser.add_argument('--seed', type=int, default=12345, help='Seed.')

    args = parser.parse_args()

    main(args)