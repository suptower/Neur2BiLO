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
        self.model_type  = model_type
        self.approx_type = approx_type
        self.device      = device
        self.cfg         = cfg
        self.label_scaler = None


    # ------------------------------------------------------------------
    # Label scaling
    # ------------------------------------------------------------------

    def get_label_scalers(self, data):
        """Scale labels (energy) globally across all samples."""
        labels = [s["follower_obj"] for s in data]
        self.label_scaler = (np.min(labels), np.max(labels))


    # ------------------------------------------------------------------
    # Dataset construction
    # ------------------------------------------------------------------

    def get_inst_encoder_dataset(self, data):
        """
        Build PyTorch dataset for the inst_encoder model.

        Per sample:
          inst_features    : (s, n_inst_feats)   – instance features per switch-point
          decision_features: (s, n_dec_feats)    – decision-dependent features
          decisions        : (s,)                – x vector (ternary)
          n_decisions      : scalar              – s (number of switch-points)
          labels           : scalar              – follower_obj (energy, scaled)

        where s = instance["k"] = number of switch-points.
        """
        inst_features, decision_features, decisions, n_decisions, labels = \
            [], [], [], [], []

        for sample in data:
            instance = sample["instance"]
            x        = sample["x"]            # ternary vector, length s
            s        = instance["k"]

            # Parse PML features for this instance
            pml_feats = self._parse_pml_features(instance)

            inst_feats = []
            dec_feats  = []

            for i in range(s):
                pf = pml_feats[i]

                # --- Instance features (independent of x) ---
                inst_feat = [
                    pf["time_ns_high"]   / 1e6,    # normalize to ms scale
                    pf["time_ns_low"]    / 1e6,
                    pf["power_nw_high"]  / 1e9,    # normalize to W scale
                    pf["power_nw_low"]   / 1e9,
                    pf["energy_high"]    / 1e15,   # normalize energy
                    pf["energy_low"]     / 1e15,
                    pf["loop_bound"]     / 2500,   # normalize by typical max
                    float(pf["is_uart"]),
                    pf["position_norm"],
                    s / 20,                        # normalize by typical max s
                ]
                inst_feats.append(inst_feat)

                # --- Decision features (depend on x[i]) ---
                xi = int(x[i])
                tc_time  = pf["transition_costs"][xi]["time_ns"]  / 1e6
                tc_power = pf["transition_costs"][xi]["power_nw"] / 1e9

                dec_feat = [
                    float(xi == 0),   # one-hot x=0: no change
                    float(xi == 1),   # one-hot x=1: switch to low freq
                    float(xi == 2),   # one-hot x=2: switch to high freq
                    tc_time,
                    tc_power,
                ]
                dec_feats.append(dec_feat)

            # Label (scaled)
            label = sample["follower_obj"]
            if self.label_scaler is not None:
                lo, hi = self.label_scaler
                label = (label - lo) / (hi - lo) if hi > lo else 0.0

            inst_features.append(inst_feats)
            decision_features.append(dec_feats)
            decisions.append(x)
            n_decisions.append(s)
            labels.append(label)

        inst_features     = self.to_tensor(np.array(inst_features)).to(self.device)
        decision_features = self.to_tensor(np.array(decision_features)).to(self.device)
        decisions         = self.to_tensor(np.array(decisions)).to(self.device)
        n_decisions       = self.to_tensor(np.array(n_decisions)).to(self.device)
        labels            = self.to_tensor(np.array(labels)).to(self.device)

        return TensorDataset(inst_features, decision_features, decisions,
                             n_decisions, labels)


    # ------------------------------------------------------------------
    # PML feature extraction
    # ------------------------------------------------------------------

    def _parse_pml_features(self, instance):
        """
        Parse the PML file for this instance and extract per-switch-point features.

        Returns list of dicts, one per switch-point, with:
          time_ns_high, time_ns_low, power_nw_high, power_nw_low,
          energy_high, energy_low, loop_bound, is_uart,
          position_norm, transition_costs
        """
        import os

        pml_path = os.path.join(instance["program_dir"], "build", "app.c.pml")

        with open(pml_path, "r") as f:
            raw = f.read()

        # PML files contain multiple YAML documents separated by "---"
        docs = [d for d in yaml.safe_load_all(raw) if d is not None]

        # Find the PSTG document
        pstg_doc = None
        for doc in docs:
            if "pstgs" in doc:
                pstg_doc = doc
                break

        if pstg_doc is None:
            raise ValueError(f"No PSTG found in {pml_path}")

        pstg       = pstg_doc["pstgs"][0]
        cc_alts    = pstg.get("cc-alternatives", [])
        edges      = {e["index"]: e for e in pstg["edges"]}
        nodes      = {n["index"]: n for n in pstg["nodes"]}
        flowfacts  = self._parse_flowfacts(docs)

        s = len(cc_alts)
        feats = []

        for pos, alt_group in enumerate(cc_alts):
            alternatives = alt_group["alternatives"]   # list of 3 dicts

            # For each alternative, compute total transition cost
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

            # Get energy costs of the associated PSTG nodes (High and Low freq)
            cc_node_indices = alt_group["cc-nodes"]
            time_high, time_low, pwr_high, pwr_low = 0.0, 0.0, POWER_HIGH_NW, POWER_LOW_NW
            is_uart = False

            for ni in cc_node_indices:
                n = nodes.get(ni, {})
                c = n.get("costs", {})
                devices = n.get("devices", [])
                # 0 = CpuHighFreq, 1 = CpuLowFreq
                if 0 in devices:
                    time_high += c.get("time_ns", 0.0)
                    pwr_high   = c.get("power_nW", POWER_HIGH_NW)
                    # UART nodes have non-zero costs at both freqs
                    if c.get("time_ns", 0.0) > 0:
                        is_uart = True
                if 1 in devices:
                    time_low  += c.get("time_ns", 0.0)
                    pwr_low    = c.get("power_nW", POWER_LOW_NW)

            energy_high = time_high * pwr_high
            energy_low  = time_low  * pwr_low

            # Loop bound: look up flowfact for enclosing loop
            loop_bound = self._get_loop_bound(flowfacts, cc_node_indices, nodes)

            feats.append({
                "time_ns_high"      : time_high,
                "time_ns_low"       : time_low,
                "power_nw_high"     : pwr_high,
                "power_nw_low"      : pwr_low,
                "energy_high"       : energy_high,
                "energy_low"        : energy_low,
                "loop_bound"        : loop_bound,
                "is_uart"           : is_uart,
                "position_norm"     : pos / max(s - 1, 1),
                "transition_costs"  : transition_costs,
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
        """
        Try to find the loop bound for the loop enclosing these cc-nodes.
        Falls back to 1 if not found.
        """
        # cc-nodes often map to cc_loopbegin/cc_loopend blocks
        # which share the loop name with the enclosing loop condition block
        for ni in cc_node_indices:
            n = nodes.get(ni, {})
            pabb_name = str(n.get("pabb", ""))
            # Check each flowfact for a matching loop name
            for loop_name, bound in flowfacts.items():
                if loop_name in pabb_name or pabb_name in loop_name:
                    return bound
        return 1