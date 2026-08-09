import pickle

with open("data/watwa/results/batch_eval_watwa_v7.pkl", "rb") as f:
    res = pickle.load(f)

print("Top-level type:", type(res))
if isinstance(res, dict):
    for k, v in res.items():
        print(f"  {k}: type={type(v)} len={len(v) if hasattr(v, '__len__') else '?'}")
    # ersten Eintrag der vielversprechendsten Liste anschauen
    for k, v in res.items():
        if isinstance(v, list) and len(v) > 0 and isinstance(v[0], dict):
            print(f"\nErster Eintrag von '{k}':")
            for kk, vv in v[0].items():
                print(f"    {kk}: {vv}")
            break
elif isinstance(res, list):
    print("Liste, Laenge:", len(res))
    print("Erster Eintrag:", res[0])