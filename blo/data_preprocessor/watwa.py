import numpy as np
import yaml

import torch
from torch.utils.data import TensorDataset

from .data_preprocessor import DataPreprocessor


# Physical constants from PML / devices config
POWER_HIGH_NW  = 105_648_000   # CpuHighFreq power in nW
POWER_LOW_NW   =  28_483_000   # CpuLowFreq  power in nW


class WatwaDataPreprocessor(DataPreprocessor):

    def __init__(self, model_type, approx_type, device, cfg=None):
        self.model_type   = model_type
        self.approx_type  = approx_type
        self.device       = device
        self.cfg          = cfg
        self.label_scaler = None


    # ------------------------------------------------------------------
    # Label scaling
    # ------------------------------------------------------------------

    def get_label_scalers(self, data):
        """Scale labels (energy) globally across all samples."""
        labels = [s["follower_obj"] for s in data]
        self.label_scaler = (np.min(labels), np.max(labels))


    # ------------------------------------------------------------------
    # Padding helper
    # ------------------------------------------------------------------

    def get_max_s(self, data):
        """Get maximum number of switch-points across all samples."""
        return max(sample["instance"]["k"] for sample in data)

    def pad_features(self, feats, pad_size, feat_dim):
        """Pad feature list to pad_size with zero vectors."""
        n_to_add = pad_size - len(feats)
        if n_to_add > 0:
            feats += [[0.0] * feat_dim] * n_to_add
        return feats


    # ------------------------------------------------------------------
    # Dataset construction
    # ------------------------------------------------------------------

    def get_inst_encoder_dataset(self, data):
        """
        Build PyTorch dataset for the inst_encoder model.

        All samples are padded to max_s switch-points for batching.
        """
        # Determine padding size across all samples
        pad_size = self.get_max_s(data)
        n_inst   = 10
        n_dec    = 5

        inst_features, decision_features, decisions, n_decisions, labels = \
            [], [], [], [], []

        for sample in data:
            instance = sample["instance"]
            x        = sample["x"]
            s        = instance["k"]

            pml_feats = self._parse_pml_features(instance)

            inst_feats = []
            dec_feats  = []

            for i in range(s):
                pf = pml_feats[i]

                inst_feat = [
                    pf["time_ns_high"]   / 1e6,
                    pf["time_ns_low"]    / 1e6,
                    pf["power_nw_high"]  / 1e9,
                    pf["power_nw_low"]   / 1e9,
                    pf["energy_high"]    / 1e15,
                    pf["energy_low"]     / 1e15,
                    pf["loop_bound"]     / 2500,
                    float(pf["is_uart"]),
                    pf["position_norm"],
                    s / 20,
                ]
                inst_feats.append(inst_feat)

                xi       = int(x[i])
                tc_time  = pf["transition_costs"][xi]["time_ns"]  / 1e6
                tc_power = pf["transition_costs"][xi]["power_nw"] / 1e9

                dec_feat = [
                    float(xi == 0),
                    float(xi == 1),
                    float(xi == 2),
                    tc_time,
                    tc_power,
                ]
                dec_feats.append(dec_feat)

            # Pad to pad_size
            inst_feats = self.pad_features(inst_feats, pad_size, n_inst)
            dec_feats  = self.pad_features(dec_feats,  pad_size, n_dec)

            # Pad x vector
            x_padded = list(x) + [0] * (pad_size - s)

            # Label (scaled)
            label = sample["follower_obj"]
            if self.label_scaler is not None:
                lo, hi = self.label_scaler
                label  = (label - lo) / (hi - lo) if hi > lo else 0.0

            inst_features.append(inst_feats)
            decision_features.append(dec_feats)
            decisions.append(x_padded)
            n_decisions.append(s)
            labels.append(label)

        inst_features     = self.to_tensor(np.array(inst_features)).to(self.device)
        decision_features = self.to_tensor(np.array(decision_features)).to(self.device)
        decisions         = self.to_tensor(np.array(decisions)).to(self.device)
        n_decisions       = self.to_tensor(np.array(n_decisions)).to(self.device)
        labels            = self.to_tensor(np.array(labels)).to(self.device)

        # Dummy p-Tensor (nicht verwendet, aber Trainings-Skript erwartet 6 tensors)
        p = self.to_tensor(np.zeros((len(labels), 1))).to(self.device)

        return TensorDataset(inst_features, decision_features, decisions,
                             n_decisions, p, labels)


    # ------------------------------------------------------------------
    # PML feature extraction
    # ------------------------------------------------------------------

    def _parse_pml_features(self, instance):
        """
        Parse the PML file and extract per-switch-point features.
        """
        import os

        pml_path = os.path.join(instance["program_dir"], "build", "app.c.pml")

        with open(pml_path, "r") as f:
            raw = f.read()

        docs = [d for d in yaml.safe_load_all(raw) if d is not None]

        pstg_doc = None
        for doc in docs:
            if "pstgs" in doc:
                pstg_doc = doc
                break

        if pstg_doc is None:
            raise ValueError(f"No PSTG found in {pml_path}")

        pstg      = pstg_doc["pstgs"][0]
        cc_alts   = pstg.get("cc-alternatives", [])
        edges     = {e["index"]: e for e in pstg["edges"]}
        nodes     = {n["index"]: n for n in pstg["nodes"]}
        flowfacts = self._parse_flowfacts(docs)

        s     = len(cc_alts)
        feats = []

        for pos, alt_group in enumerate(cc_alts):
            alternatives = alt_group["alternatives"]

            transition_costs = []
            for alt in alternatives:
                total_time  = 0.0
                total_power = 0.0
                for edge_idx in alt["edges"]:
                    e = edges.get(edge_idx, {})
                    c = e.get("costs", {})
                    total_time  += c.get("time_ns",  0.0)
                    total_power += c.get("power_nW", 0.0)
                transition_costs.append({
                    "time_ns"  : total_time,
                    "power_nw" : total_power,
                })

            cc_node_indices = alt_group["cc-nodes"]
            time_high, time_low = 0.0, 0.0
            pwr_high, pwr_low   = POWER_HIGH_NW, POWER_LOW_NW
            is_uart = False

            for ni in cc_node_indices:
                n = nodes.get(ni, {})
                c = n.get("costs", {})
                devices = n.get("devices", [])
                if 0 in devices:
                    time_high += c.get("time_ns", 0.0)
                    if c.get("power_nW"):
                        pwr_high = c.get("power_nW", POWER_HIGH_NW)
                    if c.get("time_ns", 0.0) > 0:
                        is_uart = True
                if 1 in devices:
                    time_low += c.get("time_ns", 0.0)
                    if c.get("power_nW"):
                        pwr_low = c.get("power_nW", POWER_LOW_NW)

            energy_high = time_high * pwr_high
            energy_low  = time_low  * pwr_low
            loop_bound  = self._get_loop_bound(flowfacts, cc_node_indices, nodes)

            feats.append({
                "time_ns_high"     : time_high,
                "time_ns_low"      : time_low,
                "power_nw_high"    : pwr_high,
                "power_nw_low"     : pwr_low,
                "energy_high"      : energy_high,
                "energy_low"       : energy_low,
                "loop_bound"       : loop_bound,
                "is_uart"          : is_uart,
                "position_norm"    : pos / max(s - 1, 1),
                "transition_costs" : transition_costs,
            })

        return feats


    def _parse_flowfacts(self, docs):
        """Extract loop bounds from flowfacts section of PML."""
        flowfacts = {}
        for doc in docs:
            for ff in doc.get("flowfacts", []):
                scope = ff.get("scope", {})
                loop  = scope.get("loop", None)
                rhs   = ff.get("rhs", 0)
                if loop:
                    flowfacts[loop] = rhs
        return flowfacts


    def _get_loop_bound(self, flowfacts, cc_node_indices, nodes):
        """Find loop bound for the loop enclosing these cc-nodes."""
        for ni in cc_node_indices:
            n         = nodes.get(ni, {})
            pabb_name = str(n.get("pabb", ""))
            for loop_name, bound in flowfacts.items():
                if loop_name in pabb_name or pabb_name in loop_name:
                    return bound
        return 1


    # ------------------------------------------------------------------
    # Unused abstract method stubs
    # ------------------------------------------------------------------

    def get_ff_fixed_dataset(self, data):
        raise NotImplementedError(
            "ff_fixed not implemented for WatwaOS. Use inst_encoder."
        )

    def get_ff_invariant_dataset(self, data):
        raise NotImplementedError(
            "ff_invariant not implemented for WatwaOS. Use inst_encoder."
        )

    def get_set_invariant_dataset(self, data):
        raise NotImplementedError(
            "set_invariant not implemented for WatwaOS. Use inst_encoder."
        )