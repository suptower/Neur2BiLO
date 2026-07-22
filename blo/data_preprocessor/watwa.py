import numpy as np
import yaml

import torch
from torch.utils.data import TensorDataset

from .data_preprocessor import DataPreprocessor


# Physical constants from PML / devices config
POWER_HIGH_NW  = 105_648_000   # CpuHighFreq power in nW
POWER_LOW_NW   =  28_483_000   # CpuLowFreq  power in nW


class WatwaDataPreprocessor(DataPreprocessor):

    def __init__(self, model_type, approx_type, device, cfg=None, use_rank_labels=False):
        self.model_type      = model_type
        self.approx_type     = approx_type
        self.device          = device
        self.cfg             = cfg
        self.label_scaler    = None
        self.use_rank_labels = use_rank_labels


    # ------------------------------------------------------------------
    # Label scaling
    # ------------------------------------------------------------------

    def get_label_scalers(self, data):
        """Scale labels per-instance: each instance's energies normalized to [0,1] independently."""
        from collections import defaultdict
        inst_labels = defaultdict(list)
        for s in data:
            inst_labels[s["instance"]["program_dir"]].append(s["follower_obj"])
    
        # Dict: program_dir -> (min, max) für diese Instanz
        self.label_scaler = {
            prog: (min(vals), max(vals))
            for prog, vals in inst_labels.items()
        }

    # def get_label_scalers(self, data):
    #     """Scale labels (energy) globally across all samples."""
    #     labels = [s["follower_obj"] for s in data]
    #     self.label_scaler = (np.min(labels), np.max(labels))

    # def get_label_scalers(self, data):
    #     # Gruppiere nach Instanz, skaliere pro Instanz
    #     from collections import defaultdict
    #     inst_labels = defaultdict(list)
    #     for s in data:
    #         inst_labels[s["instance"]["program_dir"]].append(s["follower_obj"])

    #     # evt
    #     # label_norm = (energy - min_energy_this_instance) / (max_energy_this_instance - min_energy_this_instance)
        
    #     # Globale Skalierung aber relativ zur optimalen Energie pro Instanz
    #     labels = [s["follower_obj"] for s in data]
    #     self.label_scaler = (np.min(labels), np.max(labels))


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

        inst_features, decision_features, decisions, n_decisions, labels, inst_ids = \
            [], [], [], [], [], []

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
                    pf["time_ns_high"]  / 1e6,
                    pf["time_ns_low"]   / 1e6,
                    pf["power_nw_high"] / 1e9,
                    pf["power_nw_low"]  / 1e9,
                    pf["energy_high"]   / 1e15,
                    pf["energy_low"]    / 1e15,
                    pf["energy_ratio"],
                    pf["time_ratio"]    / 100.0,
                    pf["is_uart"],
                    pf["loop_bound"]    / 2500,
                    pf["position_norm"],
                    pf["position_abs"]  / 20,
                    pf["tc_ratio_x1"],
                    pf["tc_ratio_x2"],
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
                prog = sample["instance"]["program_dir"]
                lo, hi = self.label_scaler.get(prog, (label, label))
                label = (label - lo) / (hi - lo) if hi > lo else 0.0

            inst_features.append(inst_feats)
            decision_features.append(dec_feats)
            decisions.append(x_padded)
            n_decisions.append(s)
            labels.append(label)
            inst_ids.append(sample["inst_id"])

        # Rang-basierte Labels (0=beste, 1=schlechteste) statt normalisierter Energie
        if self.use_rank_labels:
            from collections import defaultdict
            inst_energy_map = defaultdict(dict)
            for iid, label in zip(inst_ids, labels):
                if label not in inst_energy_map[iid]:
                    inst_energy_map[iid][label] = None
            # Ränge berechnen
            inst_rank_maps = {}
            for iid, energy_dict in inst_energy_map.items():
                sorted_energies = sorted(energy_dict.keys())
                n = len(sorted_energies)
                inst_rank_maps[iid] = {
                    e: i / (n - 1) if n > 1 else 0.0
                    for i, e in enumerate(sorted_energies)
                }
            labels = [inst_rank_maps[iid][label]
                      for iid, label in zip(inst_ids, labels)]
        inst_features     = self.to_tensor(np.array(inst_features)).to(self.device)
        decision_features = self.to_tensor(np.array(decision_features)).to(self.device)
        decisions         = self.to_tensor(np.array(decisions)).to(self.device)
        n_decisions       = self.to_tensor(np.array(n_decisions)).to(self.device)
        labels            = self.to_tensor(np.array(labels)).to(self.device)
        
        inst_ids_t = self.to_tensor(np.array(inst_ids, dtype=np.float32)).to(self.device)
        return TensorDataset(inst_features, decision_features, decisions, 
                            n_decisions, labels, inst_ids_t)


    # ------------------------------------------------------------------
    # PML feature extraction
    # ------------------------------------------------------------------

    def _parse_pml_features(self, instance):
        """
        Parse the PML file and extract per-switch-point features.
        """
        if "_pml_features" in instance:
            return instance["_pml_features"]

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

            # Kosten direkt aus transition_costs (Edge-Daten, korrekt)
            tc0 = transition_costs[0] if len(transition_costs) > 0 else {"time_ns": 0.0, "power_nw": 0.0}
            tc1 = transition_costs[1] if len(transition_costs) > 1 else {"time_ns": 0.0, "power_nw": 0.0}
            tc2 = transition_costs[2] if len(transition_costs) > 2 else {"time_ns": 0.0, "power_nw": 0.0}

            time_x1 = tc1["time_ns"]   # HighFreq-Transition
            time_x2 = tc2["time_ns"]   # LowFreq-Transition
            pwr_x1  = tc1["power_nw"]
            pwr_x2  = tc2["power_nw"]

            energy_x1 = time_x1 * pwr_x1
            energy_x2 = time_x2 * pwr_x2

            # Verhältnisse: zeigen direkt ob LowFreq lohnt
            time_ratio   = time_x2  / time_x1  if time_x1  > 0 else 1.0
            energy_ratio = energy_x2 / energy_x1 if energy_x1 > 0 else 1.0
            is_uart      = float(time_ratio > 10.0)

            # Transition cost ratio: Wechselkosten relativ zur Ausführungszeit
            tc_ratio_x1 = time_x1 / time_x2 if time_x2 > 0 else 0.0
            tc_ratio_x2 = time_x2 / time_x1 if time_x1 > 0 else 0.0

            loop_bound = self._get_loop_bound(flowfacts, cc_node_indices, nodes)

            feats.append({
                "time_ns_high"   : time_x1,
                "time_ns_low"    : time_x2,
                "power_nw_high"  : pwr_x1,
                "power_nw_low"   : pwr_x2,
                "energy_high"    : energy_x1,
                "energy_low"     : energy_x2,
                "energy_ratio"   : energy_ratio,
                "time_ratio"     : time_ratio,
                "is_uart"        : is_uart,
                "loop_bound"     : loop_bound,
                "position_norm"  : pos / max(s - 1, 1),
                "position_abs"   : float(pos),
                "tc_ratio_x1"    : tc_ratio_x1,
                "tc_ratio_x2"    : tc_ratio_x2,
                "transition_costs": transition_costs,
            })

        instance["_pml_features"] = feats
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