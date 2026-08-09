import pickle

with open("ml_data_v7.pkl", "rb") as f:
    dataset = pickle.load(f)

row = dataset["tr_data"][0]
scenarios = row["instance"]["scenarios"]
first_key = next(iter(scenarios))
first_val = scenarios[first_key]
print("Beispiel-Key:", first_key)
print("Beispiel-Value type:", type(first_val))
print("Beispiel-Value:", first_val)
print()
print("program_dir dieser Zeile:", row["instance"]["program_dir"])