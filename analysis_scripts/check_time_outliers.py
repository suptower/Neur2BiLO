import pickle
import numpy as np

with open("data/watwa/results/batch_eval_watwa_v7.pkl", "rb") as f:
    metrics = pickle.load(f)

ml_times = np.array([m["ml_time"] for m in metrics])

print("min:", ml_times.min())
print("median:", np.median(ml_times))
print("mean:", ml_times.mean())
print("max:", ml_times.max())
print()
print("Anzahl Instanzen mit ml_time > 10s:", (ml_times > 10).sum())
print("Anzahl Instanzen mit ml_time > 100s:", (ml_times > 100).sum())
print("Anzahl Instanzen mit ml_time > 1000s:", (ml_times > 1000).sum())

# Top 10 langsamste
idx_sorted = np.argsort(ml_times)[::-1][:10]
print("\nTop 10 langsamste Instanzen:")
for i in idx_sorted:
    print(f"  inst_idx={metrics[i]['inst_idx']}  ml_time={ml_times[i]:.2f}s  program_dir={metrics[i]['program_dir']}")

# Bereinigte Metriken ohne Ausreisser (z.B. alles > 60s als Sleep-Artefakt behandeln)
clean = [m for m in metrics if m["ml_time"] <= 60]
print(f"\nBereinigt (<=60s): {len(clean)}/{len(metrics)} Instanzen")
clean_times = np.array([m["ml_time"] for m in clean])
watwaos_times = np.array([m["watwaos_time"] for m in clean])
print(f"Avg inference time (bereinigt): {clean_times.mean()*1000:.2f} ms")
print(f"Median inference time (bereinigt): {np.median(clean_times)*1000:.2f} ms")
speedups_clean = watwaos_times / clean_times
print(f"Mean speedup (bereinigt): {speedups_clean.mean():.2f}x")
print(f"Median speedup (bereinigt): {np.median(speedups_clean):.2f}x")