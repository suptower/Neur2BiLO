import pickle

with open(
    "data/watwa/random_search/nn_res_inst_encoder_both_nsi-498_nspi-100000_s-7__bs-512_lr-0.001_o-Adam_ep-1000_do-0_in-eh-128_in-eo-64_in-ph-128_in-po-32_in-vh-128_in-ero-0_in-pro-0_in-vro-0_in-a-sum__.pkl",
    "rb",
) as f:
    res = pickle.load(f)

print(type(res), res.keys() if isinstance(res, dict) else res)
