import torch

ckpt = torch.load(
    "data/watwa/nn_inst_encoder_both_nsi-498_nspi-100000_s-7.pt",
    map_location="cpu",
    weights_only=False
)
sd = ckpt.state_dict() if hasattr(ckpt, "state_dict") else ckpt

for name, param in sd.items():
    print(f"{name:45s} shape={tuple(param.shape)!s:15s} "
          f"norm={param.norm().item():10.5f}  mean_abs={param.abs().mean().item():.6f}")
