import numpy as np
import torch

import gurobipy as gp
from gurobi_ml import add_predictor_constr

from blo.data_preprocessor import factory_dp
from blo.utils.watwa import get_path
from .approximator import Approximator


class WatwaApproximator(Approximator):
    """
    Approximator for the WatwaOS bilevel problem.
    The leader's decision is a ternary choice per switch-point (0, 1, or 2).
    The follower's response is the optimal energy given the leader's choice.
    """

    def __init__(self, args, cfg, blo, net, instance):
        super(WatwaApproximator, self).__init__(args, cfg, blo, net, instance)

        # number of switch-points for this instance
        self.s = instance["k"]


    # ------------------------------------------------------------------
    # Abstract method implementations
    # ------------------------------------------------------------------

    def recover_sol(self, grb_model):
        """Recover x (leader decision) and predicted energy from solved model."""
        all_vars   = grb_model.getVars()
        var_names  = grb_model.getAttr("VarName", all_vars)
        var_values = grb_model.getAttr("X", all_vars)

        x_values  = [None] * self.s
        y_vf      = None

        for name, val in zip(var_names, var_values):
            # Leader decision variables: x_0[i], x_1[i], x_2[i] (one-hot)
            if name.startswith("x_oh["):
                # parse index and class from name "x_oh[i,c]"
                idx_str = name[5:-1]
                i, c = map(int, idx_str.split(","))
                if val > 0.5:
                    x_values[i] = c
            if name == "y_vf[0]":
                y_vf = val

        # Fallback: fill None with 0
        x_values = [v if v is not None else 0 for v in x_values]

        sol = {
            "x"    : x_values,
            "y"    : [],
            "y_vf" : y_vf,
        }

        return sol


    def do_warmstart(self, grb_model):
        """No warmstart implemented for WatwaOS."""
        pass


    def get_approx_model_upper_level(self):
        """
        Build Gurobi surrogate model using Upper-Level Approximation (NN_u).

        The NN predicts F(x, y*(x)) = total energy directly.
        Gurobi minimizes the NN output over x in {0,1,2}^s (one-hot encoded).
        """
        grb_model = gp.Model()
        s = self.s

        # Leader variables: one-hot over {0,1,2} per switch-point
        x_oh = grb_model.addVars(s, 3, vtype=gp.GRB.BINARY, name="x_oh")
        for i in range(s):
            grb_model.addConstr(
                gp.quicksum(x_oh[i, c] for c in range(3)) == 1,
                name=f"one_hot_{i}"
            )
        grb_model._x_oh = x_oh

        # Value function variable
        y_valuefun = grb_model.addMVar((1,), lb=-gp.GRB.INFINITY, name="y_vf")

        # Embed NN directly – no get_grb_features_with_x needed
        self.embed_inst_encoder(y_valuefun, grb_model)

        # Objective: minimize predicted energy
        grb_model.setObjective(y_valuefun[0], gp.GRB.MINIMIZE)

        return grb_model


    def get_approx_model_lower_level(self):
        """
        Lower-Level Approximation not yet implemented for WatwaOS.
        Upper-Level Approximation (NN_u) is the primary approach.
        """
        raise NotImplementedError(
            "Lower-level approximation not implemented for WatwaOS. "
            "Use approx_type='upper'."
        )


    def get_grb_features_with_x(self, x_oh, grb_model):
        """
        Build the feature matrix for the NN as Gurobi MVar.

        Shape: (s, n_inst_feats + n_dec_feats)

        Instance features (10, fixed per switch-point):
          time_ns_high, time_ns_low, power_nw_high, power_nw_low,
          energy_high, energy_low, loop_bound, is_uart,
          position_norm, n_switch_points

        Decision features (5, depend on x[i]):
          x_oh_0, x_oh_1, x_oh_2  (one-hot, directly the Gurobi vars)
          transition_cost_time, transition_cost_power
          (linear combination: sum_c x_oh[i,c] * cost_c)

        Total: 15 features per switch-point.
        """
        s          = self.s
        n_inst     = 10
        n_dec      = 5
        n_feats    = n_inst + n_dec

        # Parse instance features from PML (static, independent of x)
        inst_feats = self._get_instance_features_np()   # (s, n_inst)

        # Transition costs per alternative per switch-point: (s, 3, 2)
        trans_costs = self._get_transition_costs_np()

        # Feature MVar: (s, n_feats)
        x_wf = grb_model.addMVar(
            (s, n_feats),
            vtype=gp.GRB.CONTINUOUS,
            lb=-gp.GRB.INFINITY,
            name="x_wf"
        )

        for i in range(s):
            # Instance features (constant)
            for j in range(n_inst):
                grb_model.addConstr(
                    x_wf[i, j] == inst_feats[i, j],
                    name=f"inst_feat_{i}_{j}"
                )

            # Decision features: one-hot directly from Gurobi vars
            for c in range(3):
                grb_model.addConstr(
                    x_wf[i, n_inst + c] == x_oh[i, c],
                    name=f"dec_oh_{i}_{c}"
                )

            # Transition cost time: sum_c x_oh[i,c] * cost_time_c
            grb_model.addConstr(
                x_wf[i, n_inst + 3] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 0] for c in range(3)
                ),
                name=f"trans_time_{i}"
            )

            # Transition cost power: sum_c x_oh[i,c] * cost_power_c
            grb_model.addConstr(
                x_wf[i, n_inst + 4] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 1] for c in range(3)
                ),
                name=f"trans_power_{i}"
            )

        return x_wf


    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_instance_features_np(self):
        """
        Extract static instance features from the pre-parsed PML data.
        Returns numpy array of shape (s, 10).
        """
        from blo.data_preprocessor.watwa import WatwaDataPreprocessor
        dp = WatwaDataPreprocessor(
            model_type="inst_encoder",
            approx_type=self.args.approx_type,
            device=torch.device("cpu")
        )
        pml_feats = dp._parse_pml_features(self.instance)

        rows = []
        s = self.s
        for i, pf in enumerate(pml_feats):
            row = [
                pf["time_ns_high"]  / 1e6,
                pf["time_ns_low"]   / 1e6,
                pf["power_nw_high"] / 1e9,
                pf["power_nw_low"]  / 1e9,
                pf["energy_high"]   / 1e15,
                pf["energy_low"]    / 1e15,
                pf["loop_bound"]    / 2500,
                float(pf["is_uart"]),
                pf["position_norm"],
                s / 20,
            ]
            rows.append(row)

        return np.array(rows, dtype=np.float64)


    def _get_transition_costs_np(self):
        """
        Extract transition costs per switch-point and alternative.
        Returns numpy array of shape (s, 3, 2):
          [switch_point, alternative, (time_ns_norm, power_nw_norm)]
        """
        from blo.data_preprocessor.watwa import WatwaDataPreprocessor
        dp = WatwaDataPreprocessor(
            model_type="inst_encoder",
            approx_type=self.args.approx_type,
            device=torch.device("cpu")
        )
        pml_feats = dp._parse_pml_features(self.instance)

        costs = np.zeros((self.s, 3, 2), dtype=np.float64)
        for i, pf in enumerate(pml_feats):
            for c, tc in enumerate(pf["transition_costs"]):
                costs[i, c, 0] = tc["time_ns"]  / 1e6
                costs[i, c, 1] = tc["power_nw"] / 1e9

        return costs

    def embed_inst_encoder(self, y_valuefun, grb_model):
        import torch

        s     = self.s
        n_dec = 5

        x_oh = grb_model._x_oh

        # Compute instance embedding via PyTorch (fixed constant)
        inst_feats_np = self._get_instance_features_np()
        inst_feats_t  = torch.tensor(inst_feats_np, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            emb = self.net.instance_decision_embedder(inst_feats_t)
            emb = self.net.aggregate(emb, self.net.agg_type)
            emb = self.net.final_instance_embedder(emb)

        inst_embedding = emb.detach().cpu().numpy().reshape(-1)
        inst_emb_dim   = inst_embedding.shape[0]

        trans_costs = self._get_transition_costs_np()

        # Build input to value_predictor: [dec_features (5), inst_embedding (32)]
        # This is the "own features" block per switch point -- unchanged from
        # before. own_feat_dim = n_dec + inst_emb_dim (e.g. 5 + 32 = 37).
        own_feat_dim = n_dec + inst_emb_dim

        x_pred = grb_model.addMVar(
            (s, own_feat_dim),
            vtype=gp.GRB.CONTINUOUS,
            lb=-gp.GRB.INFINITY,
            name="x_pred"
        )

        for i in range(s):
            for c in range(3):
                grb_model.addConstr(x_pred[i, c] == x_oh[i, c],
                                    name=f"dec_oh_{i}_{c}")
            grb_model.addConstr(
                x_pred[i, 3] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 0] for c in range(3)),
                name=f"trans_t_{i}")
            grb_model.addConstr(
                x_pred[i, 4] == gp.quicksum(
                    x_oh[i, c] * trans_costs[i, c, 1] for c in range(3)),
                name=f"trans_p_{i}")
            for j in range(inst_emb_dim):
                grb_model.addConstr(
                    x_pred[i, n_dec + j] == inst_embedding[j],
                    name=f"inst_emb_{i}_{j}")

        # --- NEW: cross-switch-point context (MIP-compatible) ---
        # For each switch point i, compute the leave-one-out sum of x_pred
        # over all OTHER switch points j != i, project it through context_proj
        # (a Linear+ReLU sub-network, embedded via add_predictor_constr just
        # like value_predictor), and concatenate it with x_pred[i,:] before
        # the value prediction. This must use the FINAL x_pred (after dec
        # features + instance embedding are filled in), since context is
        # defined over the same feature space value_predictor was trained on.
        value_pred_input_dim = own_feat_dim
        if getattr(self, "use_context", False) and self.context_proj_grb is not None:
            context_hidden_dim = self.context_proj_grb_output_dim

            # total sum over all switch points (axis 0), shape (own_feat_dim,)
            total_sum = x_pred.sum(axis=0)

            context_raw = grb_model.addMVar(
                (s, own_feat_dim), vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY, name="context_raw"
            )
            for i in range(s):
                grb_model.addConstr(
                    context_raw[i, :] == total_sum - x_pred[i, :],
                    name=f"context_raw_{i}"
                )

            context_proj_out = grb_model.addMVar(
                (s, context_hidden_dim), vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY, name="context_proj_out"
            )
            for i in range(s):
                add_predictor_constr(
                    grb_model, self.context_proj_grb,
                    context_raw[i, :], context_proj_out[i, :]
                )

            # extended input: [own_features, projected_context]
            value_pred_input_dim = own_feat_dim + context_hidden_dim
            x_pred_ext = grb_model.addMVar(
                (s, value_pred_input_dim), vtype=gp.GRB.CONTINUOUS,
                lb=-gp.GRB.INFINITY, name="x_pred_ext"
            )
            for i in range(s):
                grb_model.addConstr(
                    x_pred_ext[i, :own_feat_dim] == x_pred[i, :],
                    name=f"concat_own_{i}"
                )
                grb_model.addConstr(
                    x_pred_ext[i, own_feat_dim:] == context_proj_out[i, :],
                    name=f"concat_context_{i}"
                )

            # use the extended features as input to value_predictor below
            x_pred = x_pred_ext

        y_pred = grb_model.addMVar(
            (s, 1), vtype=gp.GRB.CONTINUOUS, lb=-gp.GRB.INFINITY, name="y_pred")

        for i in range(s):
            add_predictor_constr(grb_model, self.net.value_predictor,
                                x_pred[i, :], y_pred[i])

        grb_model.addConstr(
            y_valuefun[0] == y_pred[:, 0].sum(), name="set_vf")