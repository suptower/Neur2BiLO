import gurobipy as gp
import numpy as np
import torch
from gurobi_ml import add_predictor_constr

from blo.data_preprocessor.watwa import WatwaDataPreprocessor
from .approximator import Approximator


class WatwaApproximator(Approximator):
    """
    Approximator for the WatwaOS bilevel optimization problem.
    The leader selects a ternary frequency choice per switch point (0, 1, or 2).
    The follower response represents the optimal energy consumption for that selection.
    """

    def __init__(self, args, cfg, blo, net, instance):
        super().__init__(args, cfg, blo, net, instance)
        self.s = instance["k"]

    # ------------------------------------------------------------------
    # Solution Recovery & Model Construction
    # ------------------------------------------------------------------

    def recover_sol(self, grb_model):
        """Extracts leader decision vector x and predicted energy from solved Gurobi model."""
        all_vars = grb_model.getVars()
        var_names = grb_model.getAttr("VarName", all_vars)
        var_values = grb_model.getAttr("X", all_vars)

        x_values = [None] * self.s
        y_vf = None

        for name, val in zip(var_names, var_values):
            if name.startswith("x_oh["):
                idx_str = name[5:-1]
                i, c = map(int, idx_str.split(","))
                if val > 0.5:
                    x_values[i] = c
            elif name == "y_vf[0]":
                y_vf = val

        x_values = [v if v is not None else 0 for v in x_values]

        return {
            "x": x_values,
            "y": [],
            "y_vf": y_vf,
        }

    def do_warmstart(self, grb_model):
        """Warmstarts are not implemented for WatwaOS."""
        pass

    def get_approx_model_upper_level(self):
        """
        Constructs Gurobi surrogate model using Upper-Level Approximation (NN_u).
        Minimizes total predicted energy over binary one-hot decision variables x_oh.
        """
        grb_model = gp.Model()
        s = self.s

        # One-hot leader decision variables per switch point
        x_oh = grb_model.addVars(s, 3, vtype=gp.GRB.BINARY, name="x_oh")
        for i in range(s):
            grb_model.addConstr(
                gp.quicksum(x_oh[i, c] for c in range(3)) == 1,
                name=f"one_hot_{i}",
            )
        grb_model._x_oh = x_oh

        y_valuefun = grb_model.addMVar((1,), lb=-gp.GRB.INFINITY, name="y_vf")
        self.embed_inst_encoder(y_valuefun, grb_model)

        grb_model.setObjective(y_valuefun[0], gp.GRB.MINIMIZE)
        return grb_model

    def get_approx_model_lower_level(self):
        """Lower-level approximation is not supported for WatwaOS."""
        raise NotImplementedError(
            "Lower-level approximation is not implemented for WatwaOS. Use approx_type='upper'."
        )

    def get_grb_features_with_x(self, x_oh, grb_model):
        """
        Constructs feature matrix as a Gurobi MVar.
        Features per switch point: 15 static instance features + 5 decision features.
        """
        s = self.s
        n_inst = 15
        n_dec = 5
        n_feats = n_inst + n_dec

        inst_feats = self._get_instance_features_np()
        trans_costs = self._get_transition_costs_np()

        x_wf = grb_model.addMVar(
            (s, n_feats),
            vtype=gp.GRB.CONTINUOUS,
            lb=-gp.GRB.INFINITY,
            name="x_wf",
        )

        for i in range(s):
            for j in range(n_inst):
                grb_model.addConstr(
                    x_wf[i, j] == inst_feats[i, j],
                    name=f"inst_feat_{i}_{j}",
                )

            for c in range(3):
                grb_model.addConstr(
                    x_wf[i, n_inst + c] == x_oh[i, c],
                    name=f"dec_oh_{i}_{c}",
                )

            grb_model.addConstr(
                x_wf[i, n_inst + 3] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 0] for c in range(3)
                ),
                name=f"trans_time_{i}",
            )

            grb_model.addConstr(
                x_wf[i, n_inst + 4] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 1] for c in range(3)
                ),
                name=f"trans_power_{i}",
            )

        return x_wf

    # ------------------------------------------------------------------
    # Feature Extraction Helpers
    # ------------------------------------------------------------------

    def _get_instance_features_np(self):
        """Extracts normalized static instance features (s, 15) from parsed PML data."""
        dp = WatwaDataPreprocessor(
            model_type="inst_encoder",
            approx_type=self.args.approx_type,
            device=torch.device("cpu"),
        )
        pml_feats = dp._parse_pml_features(self.instance)

        rows = []
        s = self.s
        for pf in pml_feats:
            row = [
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
            rows.append(row)

        return np.array(rows, dtype=np.float64)

    def _get_transition_costs_np(self):
        """Extracts normalized transition costs per alternative per switch point (s, 3, 2)."""
        dp = WatwaDataPreprocessor(
            model_type="inst_encoder",
            approx_type=self.args.approx_type,
            device=torch.device("cpu"),
        )
        pml_feats = dp._parse_pml_features(self.instance)

        costs = np.zeros((self.s, 3, 2), dtype=np.float64)
        for i, pf in enumerate(pml_feats):
            for c, tc in enumerate(pf["transition_costs"]):
                costs[i, c, 0] = tc["time_ns"] / 1e6
                costs[i, c, 1] = tc["power_nw"] / 1e9

        return costs

    def embed_inst_encoder(self, y_valuefun, grb_model):
        """Embeds instance encoder network into the Gurobi model using gurobi-ml."""
        s = self.s
        n_dec = 5
        x_oh = grb_model._x_oh

        # Precompute static instance embedding
        inst_feats_np = self._get_instance_features_np()
        inst_feats_t = torch.tensor(inst_feats_np, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            emb = self.net.instance_decision_embedder(inst_feats_t)
            emb = self.net.aggregate(emb, self.net.agg_type)
            if getattr(self.net, "use_inst_embedding_norm", False):
                emb = self.net.inst_embedding_norm(emb)
            emb = self.net.final_instance_embedder(emb)

        inst_embedding = emb.detach().cpu().numpy().reshape(-1)
        inst_emb_dim = inst_embedding.shape[0]
        trans_costs = self._get_transition_costs_np()

        own_feat_dim = n_dec + inst_emb_dim
        x_pred = grb_model.addMVar(
            (s, own_feat_dim),
            vtype=gp.GRB.CONTINUOUS,
            lb=-gp.GRB.INFINITY,
            name="x_pred",
        )

        for i in range(s):
            for c in range(3):
                grb_model.addConstr(
                    x_pred[i, c] == x_oh[i, c],
                    name=f"dec_oh_{i}_{c}",
                )
            grb_model.addConstr(
                x_pred[i, 3] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 0] for c in range(3)
                ),
                name=f"trans_t_{i}",
            )
            grb_model.addConstr(
                x_pred[i, 4] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 1] for c in range(3)
                ),
                name=f"trans_p_{i}",
            )
            for j in range(inst_emb_dim):
                grb_model.addConstr(
                    x_pred[i, n_dec + j] == inst_embedding[j],
                    name=f"inst_emb_{i}_{j}",
                )

        # Cross-switch-point leave-one-out context projection
        if getattr(self, "use_context", False) and getattr(self, "context_proj_grb", None) is not None:
            context_hidden_dim = self.context_proj_grb_output_dim
            total_sum = x_pred.sum(axis=0)

            context_raw = grb_model.addMVar(
                (s, own_feat_dim),
                vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY,
                name="context_raw",
            )
            for i in range(s):
                grb_model.addConstr(
                    context_raw[i, :] == total_sum - x_pred[i, :],
                    name=f"context_raw_{i}",
                )

            context_proj_out = grb_model.addMVar(
                (s, context_hidden_dim),
                vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY,
                name="context_proj_out",
            )
            for i in range(s):
                add_predictor_constr(
                    grb_model,
                    self.context_proj_grb,
                    context_raw[i, :],
                    context_proj_out[i, :],
                )

            value_pred_input_dim = own_feat_dim + context_hidden_dim
            x_pred_ext = grb_model.addMVar(
                (s, value_pred_input_dim),
                vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY,
                name="x_pred_ext",
            )
            for i in range(s):
                grb_model.addConstr(
                    x_pred_ext[i, :own_feat_dim] == x_pred[i, :],
                    name=f"concat_own_{i}",
                )
                grb_model.addConstr(
                    x_pred_ext[i, own_feat_dim:] == context_proj_out[i, :],
                    name=f"concat_context_{i}",
                )

            x_pred = x_pred_ext

        y_pred = grb_model.addMVar(
            (s, 1),
            vtype=gp.GRB.CONTINUOUS,
            lb=-gp.GRB.INFINITY,
            name="y_pred",
        )

        for i in range(s):
            add_predictor_constr(
                grb_model,
                self.net.value_predictor,
                x_pred[i, :],
                y_pred[i],
            )

        grb_model.addConstr(y_valuefun[0] == y_pred[:, 0].sum(), name="set_vf")