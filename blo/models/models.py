import torch.nn as nn
import collections

import torch
import torch.nn as nn


class PrintLayer(nn.Module):
    """ PrintLayer class for debugging. """
    def __init__(self, printx=False):
        super(PrintLayer, self).__init__()
        self.printx = printx

    def forward(self, x):
        # Do your print / debug stuff here
        if self.printx:
            print(x)
        print(x.size(), torch.mean(x).item(), torch.count_nonzero(x, dim=1))
        return x


class FeedForwardBase(nn.Module):
    """ Standard feed forward network, with some slight Gurobi specific functions. """
    def __init__(self, input_dim, hidden_dims, output_dim, output_relu=False, dropout=0.0, bias=True, name="net",
                 activation="relu", leaky_relu_slope=0.01):
        """ Constructor for feed-forward net.

        New args
        --------
        activation : str
            Which activation to use between layers: "relu" (default,
            unchanged behavior) or "leaky_relu". Motivated by a dying-ReLU
            collapse observed empirically in instance_decision_embedder and
            final_instance_embedder during training (see
            check_dead_at_init.py / check_scale_mismatch.py: healthy
            ~48-53% dead at random init, but the trained checkpoint reached
            ~97-100% dead across every switch-point-count bucket). Unlike
            plain ReLU, LeakyReLU has a nonzero gradient for negative
            inputs, so a neuron that drifts negative during training can
            still receive gradient and recover instead of being permanently
            silenced.
        leaky_relu_slope : float
            Negative-side slope for LeakyReLU (ignored if activation="relu").
        """
        super(FeedForwardBase, self).__init__()

        self.input_dim = input_dim
        self.hidden_dims = hidden_dims
        self.output_dim = output_dim
        self.output_relu = output_relu
        self.dropout = dropout
        self.bias = bias
        self.name = name
        self.activation = activation
        self.leaky_relu_slope = leaky_relu_slope

        def make_activation():
            if activation == "leaky_relu":
                return nn.LeakyReLU(negative_slope=leaky_relu_slope)
            elif activation == "relu":
                return nn.ReLU()
            elif activation == "gelu":
                return nn.GELU()
            elif activation == "silu":
                return nn.SiLU()
            else:
                raise ValueError(f"Unknown activation: {activation!r} (expected 'relu', 'leaky_relu', 'gelu', or 'silu')")

        layers = collections.OrderedDict()
        layers[f"{self.name}_in"] = nn.Linear(input_dim, hidden_dims[0], bias=self.bias)
        layers[f"{self.name}_act_in"] = make_activation()
        
        if len(hidden_dims) == 1:
            if self.dropout:
               layers[f"{self.name}_drop_in"] = nn.Dropout(self.dropout)
            
        else:
            for i in range(len(hidden_dims) - 1):
                layers[f"{self.name}_{i}"] = nn.Linear(hidden_dims[i], hidden_dims[i + 1])
                layers[f"{self.name}_act_{i}"] = make_activation()
                if self.dropout:
                    layers[f"{self.name}_drop_{i}"] = nn.Dropout(self.dropout)

        if output_relu:
            layers[f"{self.name}_out"] = nn.Linear(hidden_dims[-1], output_dim, bias=self.bias)
            layers[f"{self.name}_out_relu"] = make_activation()
        else:
            layers[f"{self.name}_out"] = nn.Linear(hidden_dims[-1], output_dim, bias=self.bias)


        self.layers = layers
        self.net = torch.nn.Sequential(self.layers)


    def forward(self, x):
        """ Forward for feed-forward net. """
        out = self.net(x)
        return out


    def get_grb_net(self):
        """ Gets gurobi compatible nn.sequential.  Specifically,
                - Remove dropout
                - Adds bias of 0's if no bias in layer
        """
        grb_layers = collections.OrderedDict()
        
        for name, layer in self.layers.items():

            # add ReLU / LeakyReLU layers to list.
            # ACHTUNG: LeakyReLU ist zwar wie ReLU stueckweise-linear und
            # damit GRUNDSAETZLICH MIP-repraesentierbar, aber ob gurobi-ml's
            # add_predictor_constr() sie tatsaechlich unterstuetzt, ist NICHT
            # verifiziert (nur ReLU war bisher in diesem Projekt im Einsatz).
            # Vor einer Wiederverwendung des Surrogate-MIP-Pfads (Chapter 5)
            # mit activation="leaky_relu" unbedingt zuerst pruefen, ob
            # gurobi-ml den Layer-Typ erkennt -- sonst wird er hier zwar
            # mitgenommen, aber add_predictor_constr() koennte ihn intern
            # ignorieren oder einen Fehler werfen.
            if type(layer) in (torch.nn.modules.activation.ReLU, torch.nn.modules.activation.LeakyReLU):
                grb_layers[name] = layer

            # remove dropout layer by skipping
            elif type(layer) == torch.nn.modules.dropout.Dropout:
                continue

            # linear layer
            if type(layer) == torch.nn.modules.linear.Linear:

                # if layer does not have bias, then copy weights and set bias to zero
                if layer.bias is None:
                    layer_cp = nn.Linear(layer.in_features, layer.out_features)
                    layer_cp.weight = layer.weight
                    layer_cp.bias = nn.Parameter(torch.zeros(layer.out_features))

                    grb_layers[name] = layer_cp
                    
                 # if layer has bias, then do nothing
                else:
                    grb_layers[name] = layer

        net = torch.nn.Sequential(grb_layers)
        net = net.cpu()
        net = net.eval()
            
        return net




class FeedForwardNetwork(nn.Module):
    """ Autoencoder...  """
    def __init__(self, feedforward_net, use_coef):
        """ Constructor for standard FeedForward net. """
        super(FeedForwardNetwork, self).__init__()
        self.feedforward_net = feedforward_net
        # self.sigmoid = nn.Sigmoid()
        self.use_coef = use_coef


    def forward(self, x, p):
        """ Forward for auto-encoder net. """
        # pass output through network
        out = self.feedforward_net(x)

        # dot product of ouput with coefficients
        if self.use_coef:
            out = torch.sum(torch.mul(out, p), dim=1)

        return out




class SetBasedNetwork(nn.Module):
    """ SetBasedNetwork network for variable decision size.  """
    def __init__(self, decision_embedder, value_predictor, agg_type, use_coef):
        """ Constructor for SetBasedNetwork net. """
        super(SetBasedNetwork, self).__init__()
        self.decision_embedder = decision_embedder
        self.value_predictor = value_predictor
        self.agg_type = agg_type
        self.use_coef = use_coef


    def forward(self, x, p, fs_size = None):
        """ Forward for auto-encoder net. """
        # embed upper-level decisions/information
        out = self.decision_embedder(x)
        out = self.aggregate(out, self.agg_type, fs_size)
    
        # value function prediction
        out = self.value_predictor(out)

        # if not multiplying by costs, then return
        if not self.use_coef:
            return out

        # otherwise, multiply element-wise by p
        out = torch.sum(torch.mul(out, p), dim=1)

        return out

    def aggregate(self, x, agg_type, fs_size = None):
        """ Aggregates tensors output from network. """
        if agg_type == "mean":
            if fs_size is None: # set default to being size of tensor
                fs_size = x.shape[1]

            # take true mean by summing, then dividing by first-stage dimensions
            x = torch.sum(x, axis=1)
            x = torch.div(x, fs_size.unsqueeze(1))

        elif agg_type == "sum":
            x = torch.sum(x, 1)

        return x



import torch
import torch.nn as nn
 
 
class SetInstanceEncodingNetwork(nn.Module):
    """Set based instance encoding network with MIP-compatible
    cross-switch-point context (context-sum) instead of attention."""
 
    def __init__(
        self,
        instance_decision_embedder,
        final_instance_embedder,
        value_predictor,
        agg_type,
        use_coef,
        problem,
        approx_type,
        use_context=False,
        context_proj=None,
        use_inst_embedding_norm=False,
    ):
        """Constructor for SetInstanceEncodingNetwork.
 
        New args
        --------
        use_context : bool
            If True, computes for each switch point the leave-one-out sum
            of decision features over all OTHER switch points ("context"),
            projects it through context_proj, and concatenates it with
            that switch point's own features before the value predictor.
            MIP-compatible replacement for attention-based interaction
            (no softmax involved).
        context_proj : FeedForwardBase or None
            Linear(+ReLU) projection applied to the raw context sum.
            Must be provided (not None) if use_context=True. Built the
            same way as value_predictor, so it is exportable via
            get_grb_net() / add_predictor_constr exactly like the other
            sub-networks.
        use_inst_embedding_norm : bool
            If True, applies LayerNorm to the aggregated instance embedding
            (output of instance_decision_embedder + sum/mean aggregation)
            BEFORE it is passed into final_instance_embedder. Mitigates a
            dying-ReLU failure mode: the aggregated embedding's scale grows
            with the number of switch points s (aggregation sums over s
            terms), and final_instance_embedder's bottleneck layer was
            found to collapse to ~100% dead ReLUs across ALL s during
            training (while healthy at random init, ~48-53% dead) --
            consistent with a self-reinforcing dying-ReLU spiral rather
            than an architectural or initialization defect. LayerNorm
            re-centers the input to this layer on every forward pass,
            independent of how its scale evolves during training.
        """
        super(SetInstanceEncodingNetwork, self).__init__()
        self.instance_decision_embedder = instance_decision_embedder
        self.final_instance_embedder = final_instance_embedder
        self.value_predictor = value_predictor  # per decision value predictor
 
        self.agg_type = agg_type
        self.use_coef = use_coef
 
        self.problem = problem
        self.approx_type = approx_type
 
        self.use_context = use_context
        self.context_proj = context_proj
        if self.use_context and self.context_proj is None:
            raise ValueError("use_context=True requires context_proj to be provided.")
 
        self.use_inst_embedding_norm = use_inst_embedding_norm
        if self.use_inst_embedding_norm:
            # Normalization dim = output_dim of instance_decision_embedder,
            # i.e. the size of the aggregated instance embedding h1_agg.
            agg_dim = instance_decision_embedder.output_dim
            self.inst_embedding_norm = nn.LayerNorm(agg_dim)
            # WICHTIG: instance_decision_embedder/final_instance_embedder/
            # value_predictor werden in 03_train_nn.py VOR dem Konstruktor-
            # Aufruf einzeln per .to(device) auf die GPU verschoben; es gibt
            # dort keinen globalen net.to(device)-Aufruf danach. Ein hier neu
            # erzeugtes nn.LayerNorm bliebe daher auf der CPU, waehrend der
            # Rest des Netzes auf der GPU laeuft -- explizit auf dasselbe
            # Device wie instance_decision_embedder verschieben, um das
            # "Expected all tensors to be on the same device"-Problem zu
            # vermeiden, unabhaengig davon, ob CPU oder GPU verwendet wird.
            try:
                target_device = next(instance_decision_embedder.parameters()).device
                self.inst_embedding_norm = self.inst_embedding_norm.to(target_device)
            except StopIteration:
                pass  # instance_decision_embedder hat keine Parameter (sollte nicht vorkommen)
 
    def forward(
        self,
        x_inst_features,
        x_decisions_features,
        x_decision,
        p,
        fs_size=None,
        print_embedding=False,
    ):
        """ """
        # embed instance information
        x_inst_embedding = self.instance_decision_embedder(x_inst_features)
        x_inst_embedding = self.aggregate(x_inst_embedding, self.agg_type, fs_size)
        if self.use_inst_embedding_norm:
            x_inst_embedding = self.inst_embedding_norm(x_inst_embedding)
        x_inst_embedding = self.final_instance_embedder(x_inst_embedding)
        if print_embedding:
            print(x_inst_embedding)
 
        x_inst_embedding = x_inst_embedding.reshape(
            x_inst_embedding.shape[0], x_inst_embedding.shape[1]
        )
 
        x_inst_embedding = x_inst_embedding[:, None, :].repeat(
            1, x_inst_features.shape[1], 1
        )
 
        x_decisions_features = torch.cat(
            [x_decisions_features, x_inst_embedding], axis=2
        )
 
        if "kp" in self.problem:
            x_decision = x_decision[:, :, None].repeat(
                1, 1, x_decisions_features.shape[-1]
            )
            x_decisions_features = torch.mul(1 - x_decision, x_decisions_features)
 
        # --- Cross-switch-point context (MIP-compatible) ---
        # context_i = sum_j(x_decisions_features[j]) - x_decisions_features[i]
        # i.e. leave-one-out sum, computed via one total-sum reduction.
        if self.use_context:
            total_sum = torch.sum(x_decisions_features, dim=1, keepdim=True)
            context = total_sum - x_decisions_features  # (batch, s, feat_dim)
            context = self.context_proj(context)        # (batch, s, context_hidden_dim)
            x_decisions_features = torch.cat([x_decisions_features, context], axis=2)
 
        # value function prediction
        pred_per_decision = self.value_predictor(x_decisions_features)
        pred_per_decision = pred_per_decision.reshape(
            pred_per_decision.shape[0], pred_per_decision.shape[1]
        )
 
        if "kp" in self.problem:
            out = torch.sum(torch.mul(pred_per_decision, p), dim=1)
 
        if "dr" in self.problem:
            if self.approx_type == "upper":
                out = torch.sum(torch.mul(pred_per_decision, p[:, :, 0]), dim=1)
            elif self.approx_type == "lower":
                pred_1 = torch.sum(torch.mul(pred_per_decision, p[:, :, 0]))
                pred_2 = p[:, 0, 1] * (
                    p[:, 0, 3] - torch.sum(torch.mul(pred_per_decision, p[:, :, 2]))
                )
                out = pred_1 + pred_2
 
        elif "cng" in self.problem:
            if self.approx_type == "lower":
                pred_1 = torch.sum(torch.mul(1 - pred_per_decision, p[:, 0, :]), dim=1)
                pred_2 = torch.sum(torch.mul(pred_per_decision, p[:, 1, :]), dim=1)
                pred_3 = torch.sum(torch.mul(pred_per_decision, p[:, 2, :]), dim=1)
                out = pred_1 + pred_2 + pred_3
            else:
                pred_1 = torch.sum(torch.mul(1 - pred_per_decision, p[:, 0, :]), dim=1)
                pred_2 = torch.sum(torch.mul(pred_per_decision, p[:, 1, :]), dim=1)
                pred_3 = torch.sum(torch.mul(1 - pred_per_decision, p[:, 2, :]), dim=1)
                pred_4 = torch.sum(torch.mul(pred_per_decision, p[:, 3, :]), dim=1)
                out = pred_1 + pred_2 + pred_3 + pred_4
 
        if "watwa" in self.problem:
            out = torch.sum(pred_per_decision, dim=1)
 
        return out
 
    def aggregate(self, x, agg_type, fs_size=None):
        """Aggregates tensors output from network."""
        if agg_type == "mean":
            if fs_size is None:
                fs_size = x.shape[1]
            x = torch.sum(x, axis=1)
            x = torch.div(x, fs_size.unsqueeze(1))
        elif agg_type == "sum":
            x = torch.sum(x, 1)
        return x