import collections
import torch
import torch.nn as nn


class PrintLayer(nn.Module):
    """Debugging layer that prints tensor statistics during the forward pass."""

    def __init__(self, printx=False):
        super().__init__()
        self.printx = printx

    def forward(self, x):
        if self.printx:
            print(x)
        print(x.size(), torch.mean(x).item(), torch.count_nonzero(x, dim=1))
        return x


class FeedForwardBase(nn.Module):
    """Standard feed-forward network with export support for Gurobi MILP constraints."""

    def __init__(
        self,
        input_dim,
        hidden_dims,
        output_dim,
        output_relu=False,
        dropout=0.0,
        bias=True,
        name="net",
        activation="relu",
        leaky_relu_slope=0.01,
    ):
        """
        Parameters
        ----------
        input_dim : int
            Number of input features.
        hidden_dims : list of int
            Dimensions of hidden layers.
        output_dim : int
            Number of output features.
        output_relu : bool
            Whether to apply activation after the output layer.
        dropout : float
            Dropout probability between hidden layers.
        bias : bool
            Whether linear layers include bias terms.
        name : str
            Prefix used for layer naming in the sequential container.
        activation : str
            Activation function ('relu', 'leaky_relu', 'gelu', or 'silu').
            LeakyReLU can be used to prevent dying neurons during training.
        leaky_relu_slope : float
            Negative slope coefficient when activation is 'leaky_relu'.
        """
        super().__init__()

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
            raise ValueError(
                f"Unknown activation: {activation!r} (expected 'relu', 'leaky_relu', 'gelu', or 'silu')"
            )

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

        layers[f"{self.name}_out"] = nn.Linear(hidden_dims[-1], output_dim, bias=self.bias)
        if output_relu:
            layers[f"{self.name}_out_relu"] = make_activation()

        self.layers = layers
        self.net = nn.Sequential(self.layers)

    def forward(self, x):
        return self.net(x)

    def get_grb_net(self):
        """
        Returns a Gurobi-compatible Sequential model by removing dropout
        and adding explicit zero-biases where bias was None.

        Note: Verify that your gurobi-ml installation supports LeakyReLU
        in add_predictor_constr() before using it for MIP formulation.
        """
        grb_layers = collections.OrderedDict()

        for name, layer in self.layers.items():
            if isinstance(layer, (nn.ReLU, nn.LeakyReLU)):
                grb_layers[name] = layer
            elif isinstance(layer, nn.Dropout):
                continue
            elif isinstance(layer, nn.Linear):
                if layer.bias is None:
                    layer_cp = nn.Linear(layer.in_features, layer.out_features)
                    layer_cp.weight = layer.weight
                    layer_cp.bias = nn.Parameter(torch.zeros(layer.out_features))
                    grb_layers[name] = layer_cp
                else:
                    grb_layers[name] = layer

        net = nn.Sequential(grb_layers)
        return net.cpu().eval()


class FeedForwardNetwork(nn.Module):
    """Feed-forward network with optional coefficient dot-product output."""

    def __init__(self, feedforward_net, use_coef):
        super().__init__()
        self.feedforward_net = feedforward_net
        self.use_coef = use_coef

    def forward(self, x, p):
        out = self.feedforward_net(x)
        if self.use_coef:
            out = torch.sum(torch.mul(out, p), dim=1)
        return out


class SetBasedNetwork(nn.Module):
    """Set-based network for variable-sized decision inputs with aggregation."""

    def __init__(self, decision_embedder, value_predictor, agg_type, use_coef):
        super().__init__()
        self.decision_embedder = decision_embedder
        self.value_predictor = value_predictor
        self.agg_type = agg_type
        self.use_coef = use_coef

    def forward(self, x, p, fs_size=None):
        out = self.decision_embedder(x)
        out = self.aggregate(out, self.agg_type, fs_size)
        out = self.value_predictor(out)

        if not self.use_coef:
            return out

        return torch.sum(torch.mul(out, p), dim=1)

    def aggregate(self, x, agg_type, fs_size=None):
        """Aggregates tensors across the set dimension."""
        if agg_type == "mean":
            if fs_size is None:
                fs_size = x.shape[1]
            x = torch.sum(x, dim=1)
            x = torch.div(x, fs_size.unsqueeze(1))
        elif agg_type == "sum":
            x = torch.sum(x, dim=1)
        return x


class SetInstanceEncodingNetwork(nn.Module):
    """
    Set-based instance encoding network supporting MIP-compatible context
    aggregation and optional multi-head self-attention.
    """

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
        use_attention=False,
        attention_proj=None,
        attention=None,
        attention_num_heads=4,
    ):
        """
        Parameters
        ----------
        instance_decision_embedder : nn.Module
            Embedder for per-decision instance features.
        final_instance_embedder : nn.Module
            Embedder applied to the aggregated instance representation.
        value_predictor : nn.Module
            Per-decision value predictor.
        agg_type : str
            Aggregation strategy ('mean' or 'sum').
        use_coef : bool
            Whether to multiply predictions element-wise by cost coefficients.
        problem : str
            Problem identifier ('kp', 'dr', 'cng', 'watwa').
        approx_type : str
            Approximation direction ('upper' or 'lower').
        use_context : bool
            If True, computes leave-one-out context sums over other switch points.
        context_proj : FeedForwardBase, optional
            Projection network for context features (required if use_context=True).
        use_inst_embedding_norm : bool
            If True, applies LayerNorm to the aggregated instance embedding
            before passing to final_instance_embedder.
        use_attention : bool
            If True, applies multi-head self-attention across switch points.
            Note: Attention contains Softmax and is not MIP-representable.
        attention_proj : FeedForwardBase, optional
            Projection mapping decision features to the attention embedding dimension.
        attention : nn.MultiheadAttention, optional
            Multi-head attention module (expected batch_first=True).
        attention_num_heads : int
            Number of attention heads (stored for checkpoint metadata).
        """
        super().__init__()
        self.instance_decision_embedder = instance_decision_embedder
        self.final_instance_embedder = final_instance_embedder
        self.value_predictor = value_predictor

        self.agg_type = agg_type
        self.use_coef = use_coef
        self.problem = problem
        self.approx_type = approx_type

        self.use_context = use_context
        self.context_proj = context_proj
        if self.use_context and self.context_proj is None:
            raise ValueError("use_context=True requires context_proj to be provided.")

        self.use_attention = use_attention
        self.attention_proj = attention_proj
        self.attention = attention
        self.attention_num_heads = attention_num_heads
        if self.use_attention and (self.attention_proj is None or self.attention is None):
            raise ValueError(
                "use_attention=True requires both attention_proj and attention to be provided."
            )

        self.use_inst_embedding_norm = use_inst_embedding_norm
        if self.use_inst_embedding_norm:
            agg_dim = instance_decision_embedder.output_dim
            self.inst_embedding_norm = nn.LayerNorm(agg_dim)
            # Ensure LayerNorm matches the device of instance_decision_embedder if already moved
            try:
                target_device = next(instance_decision_embedder.parameters()).device
                self.inst_embedding_norm = self.inst_embedding_norm.to(target_device)
            except StopIteration:
                pass

    @property
    def is_mip_representable(self):
        """Returns False if components (e.g. self-attention) cannot be converted to MIP constraints."""
        return not self.use_attention

    def forward(
        self,
        x_inst_features,
        x_decisions_features,
        x_decision,
        p,
        fs_size=None,
        print_embedding=False,
    ):
        # Embed and aggregate instance features
        x_inst_embedding = self.instance_decision_embedder(x_inst_features)
        x_inst_embedding = self.aggregate(x_inst_embedding, self.agg_type, fs_size)
        if self.use_inst_embedding_norm:
            x_inst_embedding = self.inst_embedding_norm(x_inst_embedding)
        x_inst_embedding = self.final_instance_embedder(x_inst_embedding)

        if print_embedding:
            print(x_inst_embedding)

        # Broadcast instance embedding across decisions
        x_inst_embedding = x_inst_embedding.reshape(
            x_inst_embedding.shape[0], x_inst_embedding.shape[1]
        )
        x_inst_embedding = x_inst_embedding[:, None, :].repeat(
            1, x_inst_features.shape[1], 1
        )
        x_decisions_features = torch.cat(
            [x_decisions_features, x_inst_embedding], dim=2
        )

        if "kp" in self.problem:
            x_decision = x_decision[:, :, None].repeat(
                1, 1, x_decisions_features.shape[-1]
            )
            x_decisions_features = torch.mul(1 - x_decision, x_decisions_features)

        # Compute optional context sum and/or multi-head self-attention
        extra_features = []

        if self.use_context:
            # Leave-one-out context sum across other switch points
            total_sum = torch.sum(x_decisions_features, dim=1, keepdim=True)
            context = total_sum - x_decisions_features
            context = self.context_proj(context)
            extra_features.append(context)

        if self.use_attention:
            attn_input = self.attention_proj(x_decisions_features)
            attn_out, _ = self.attention(
                attn_input, attn_input, attn_input, need_weights=False
            )
            extra_features.append(attn_out)

        if extra_features:
            x_decisions_features = torch.cat([x_decisions_features] + extra_features, dim=2)

        # Predict value per decision
        pred_per_decision = self.value_predictor(x_decisions_features)
        pred_per_decision = pred_per_decision.reshape(
            pred_per_decision.shape[0], pred_per_decision.shape[1]
        )

        out = None
        if "kp" in self.problem:
            out = torch.sum(torch.mul(pred_per_decision, p), dim=1)

        elif "dr" in self.problem:
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

        elif "watwa" in self.problem:
            out = torch.sum(pred_per_decision, dim=1)

        return out

    def aggregate(self, x, agg_type, fs_size=None):
        """Aggregates tensors across the set dimension."""
        if agg_type == "mean":
            if fs_size is None:
                fs_size = x.shape[1]
            x = torch.sum(x, dim=1)
            x = torch.div(x, fs_size.unsqueeze(1))
        elif agg_type == "sum":
            x = torch.sum(x, dim=1)
        return x