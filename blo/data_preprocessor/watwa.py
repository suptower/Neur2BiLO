"""
Data preprocessing and feature extraction for the WatwaOS bilevel problem.
"""

import os
from collections import defaultdict

import numpy as np
import torch
from torch.utils.data import TensorDataset
import yaml

from .data_preprocessor import DataPreprocessor


class WatwaDataPreprocessor(DataPreprocessor):
    """
    Extracts PML graph features, scales labels, and constructs PyTorch datasets
    for the WatwaOS instance encoder model.
    """

    def __init__(self, model_type, approx_type, device, cfg=None, use_rank_labels=False):
        super().__init__()
        self.model_type = model_type
        self.approx_type = approx_type
        self.device = device
        self.cfg = cfg
        self.label_scaler = None
        self.use_rank_labels = use_rank_labels

    # ------------------------------------------------------------------
    # Label Scaling
    # ------------------------------------------------------------------

    def get_label_scalers(self, data):
        """Computes min/max energy bounds per program instance for [0, 1] normalization."""
        inst_labels = defaultdict(list)
        for s in data:
            inst_labels[s["instance"]["program_dir"]].append(s["follower_obj"])

        self.label_scaler = {
            prog: (min(vals), max(vals)) for prog, vals in inst_labels.items()
        }

    # ------------------------------------------------------------------
    # Padding Helpers
    # ------------------------------------------------------------------

    def get_max_s(self, data):
        """Returns the maximum number of switch points across all samples."""
        return max(sample["instance"]["k"] for sample in data)

    def pad_features(self, feats, pad_size, feat_dim):
        """Pads feature list to pad_size with zero vectors."""
        n_to_add = pad_size - len(feats)
        if n_to_add > 0:
            feats.extend([[0.0] * feat_dim for _ in range(n_to_add)])
        return feats

    # ------------------------------------------------------------------
    # Dataset Construction
    # ------------------------------------------------------------------

    def get_inst_encoder_dataset(self, data):
        """
        Builds a PyTorch TensorDataset for SetInstanceEncodingNetwork training.
        Pads all instances to max_s switch points for uniform batching.
        """
        pad_size = self.get_max_s(data)
        n_inst = 15
        n_dec = 5

        inst_features = []
        decision_features = []
        decisions = []
        n_decisions = []
        labels = []
        inst_ids = []

        for sample in data:
            instance = sample["instance"]
            x = sample["x"]
            s = instance["k"]

            pml_feats = self._parse_pml_features(instance)
            inst_feats = []
            dec_feats = []

            for i in range(s):
                pf = pml_feats[i]

                inst_feat = [
                    pf["time_ns_high"] / 1e6,
                    pf["time_ns_low"] / 1e6,
                    pf["power_nw_high"] / 1e9,
                    pf["power_nw_low"] / 1e9,
                    pf["energy_high"] / 1e15,
                    pf["energy_low"] / 1e15,
                    pf["energy_ratio"],
                    pf["time_ratio"] / 100.0,
                    pf["is_uart"],
                    pf["loop_bound"] / 2500,
                    pf["position_norm"],
                    pf["position_abs"] / 20,
                    pf["tc_ratio_x1"],
                    pf["tc_ratio_x2"],
                    s / 20,
                ]
                inst_feats.append(inst_feat)

                xi = int(x[i])
                tc_time = pf["transition_costs"][xi]["time_ns"] / 1e6
                tc_power = pf["transition_costs"][xi]["power_nw"] / 1e9

                dec_feat = [
                    float(xi == 0),
                    float(xi == 1),
                    float(xi == 2),
                    tc_time,
                    tc_power,
                ]
                dec_feats.append(dec_feat)

            inst_feats = self.pad_features(inst_feats, pad_size, n_inst)
            dec_feats = self.pad_features(dec_feats, pad_size, n_dec)
            x_padded = list(x) + [0] * (pad_size - s)

            label = sample["follower_obj"]
            if self.label_scaler is not None:
                prog = sample["instance"]["program_dir"]
                lo, hi = self.label_scaler.get(prog, (label, label))
                label = (label - lo) / (hi - lo) if hi > lo else 0.0

            inst_features.append(inst_feats)
            decision_features.append(dec_feats)
            decisions.append(x_padded)
            n_decisions.append(s)
            labels.append(label)
            inst_ids.append(sample["inst_id"])

        if self.use_rank_labels:
            # Map normalized energy targets to relative percentile ranks per instance
            inst_energy_map = defaultdict(set)
            for iid, label in zip(inst_ids, labels):
                inst_energy_map[iid].add(label)

            inst_rank_maps = {}
            for iid, energies in inst_energy_map.items():
                sorted_energies = sorted(energies)
                n = len(sorted_energies)
                inst_rank_maps[iid] = {
                    e: i / (n - 1) if n > 1 else 0.0 for i, e in enumerate(sorted_energies)
                }

            labels = [inst_rank_maps[iid][label] for iid, label in zip(inst_ids, labels)]

        inst_features_t = self.to_tensor(np.array(inst_features, dtype=np.float32)).to(self.device)
        decision_features_t = self.to_tensor(np.array(decision_features, dtype=np.float32)).to(self.device)
        decisions_t = self.to_tensor(np.array(decisions, dtype=np.float32)).to(self.device)
        n_decisions_t = self.to_tensor(np.array(n_decisions, dtype=np.float32)).to(self.device)
        labels_t = self.to_tensor(np.array(labels, dtype=np.float32)).to(self.device)
        inst_ids_t = self.to_tensor(np.array(inst_ids, dtype=np.float32)).to(self.device)

        return TensorDataset(
            inst_features_t,
            decision_features_t,
            decisions_t,
            n_decisions_t,
            labels_t,
            inst_ids_t,
        )

    # ------------------------------------------------------------------
    # PML Feature Parsing
    # ------------------------------------------------------------------

    def _parse_pml_features(self, instance):
        """Extracts static timing, power, energy, and topology features from PML graph descriptions."""
        if "_pml_features" in instance:
            return instance["_pml_features"]

        pml_path = os.path.join(instance["program_dir"], "build", "app.c.pml")
        with open(pml_path, "r") as f:
            raw = f.read()

        docs = [d for d in yaml.safe_load_all(raw) if d is not None]
        pstg_doc = next((doc for doc in docs if "pstgs" in doc), None)
        if pstg_doc is None:
            raise ValueError(f"No PSTG graph definition found in {pml_path}")

        pstg = pstg_doc["pstgs"][0]
        cc_alts = pstg.get("cc-alternatives", [])
        edges = {e["index"]: e for e in pstg["edges"]}
        nodes = {n["index"]: n for n in pstg["nodes"]}
        flowfacts = self._parse_flowfacts(docs)

        s = len(cc_alts)
        feats = []

        for pos, alt_group in enumerate(cc_alts):
            alternatives = alt_group["alternatives"]
            transition_costs = []

            for alt in alternatives:
                total_time = 0.0
                total_power = 0.0
                for edge_idx in alt["edges"]:
                    e = edges.get(edge_idx, {})
                    c = e.get("costs", {})
                    total_time += c.get("time_ns", 0.0)
                    total_power += c.get("power_nW", 0.0)
                transition_costs.append({
                    "time_ns": total_time,
                    "power_nw": total_power,
                })

            cc_node_indices = alt_group["cc-nodes"]

            tc1 = transition_costs[1] if len(transition_costs) > 1 else {"time_ns": 0.0, "power_nw": 0.0}
            tc2 = transition_costs[2] if len(transition_costs) > 2 else {"time_ns": 0.0, "power_nw": 0.0}

            time_x1 = tc1["time_ns"]
            time_x2 = tc2["time_ns"]
            pwr_x1 = tc1["power_nw"]
            pwr_x2 = tc2["power_nw"]

            energy_x1 = time_x1 * pwr_x1
            energy_x2 = time_x2 * pwr_x2

            time_ratio = time_x2 / time_x1 if time_x1 > 0 else 1.0
            energy_ratio = energy_x2 / energy_x1 if energy_x1 > 0 else 1.0
            is_uart = float(time_ratio > 10.0)

            tc_ratio_x1 = time_x1 / time_x2 if time_x2 > 0 else 0.0
            tc_ratio_x2 = time_x2 / time_x1 if time_x1 > 0 else 0.0

            loop_bound = self._get_loop_bound(flowfacts, cc_node_indices, nodes)

            feats.append({
                "time_ns_high": time_x1,
                "time_ns_low": time_x2,
                "power_nw_high": pwr_x1,
                "power_nw_low": pwr_x2,
                "energy_high": energy_x1,
                "energy_low": energy_x2,
                "energy_ratio": energy_ratio,
                "time_ratio": time_ratio,
                "is_uart": is_uart,
                "loop_bound": loop_bound,
                "position_norm": pos / max(s - 1, 1),
                "position_abs": float(pos),
                "tc_ratio_x1": tc_ratio_x1,
                "tc_ratio_x2": tc_ratio_x2,
                "transition_costs": transition_costs,
            })

        instance["_pml_features"] = feats
        return feats

    def _parse_flowfacts(self, docs):
        """Extracts loop bounds from the flowfacts section of PML documents."""
        flowfacts = {}
        for doc in docs:
            for ff in doc.get("flowfacts", []):
                scope = ff.get("scope", {})
                loop = scope.get("loop", None)
                rhs = ff.get("rhs", 0)
                if loop:
                    flowfacts[loop] = rhs
        return flowfacts

    def _get_loop_bound(self, flowfacts, cc_node_indices, nodes):
        """Finds loop bound for the loop enclosing the given choice nodes."""
        for ni in cc_node_indices:
            n = nodes.get(ni, {})
            pabb_name = str(n.get("pabb", ""))
            for loop_name, bound in flowfacts.items():
                if loop_name in pabb_name or pabb_name in loop_name:
                    return bound
        return 1

    # ------------------------------------------------------------------
    # Unused Architecture Stubs
    # ------------------------------------------------------------------

    def get_ff_fixed_dataset(self, data):
        raise NotImplementedError("ff_fixed is not supported for WatwaOS. Use inst_encoder.")

    def get_ff_invariant_dataset(self, data):
        raise NotImplementedError("ff_invariant is not supported for WatwaOS. Use inst_encoder.")

    def get_set_invariant_dataset(self, data):
        raise NotImplementedError("set_invariant is not supported for WatwaOS. Use inst_encoder.")