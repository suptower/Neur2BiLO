import re
import glob

TARGET_FILES = ["pruning.py", "pruning_recall_eval.py", "pruning_recall_multistart.py", "pruning_fullenum.py"]

pattern = re.compile(
    r'(    return best_obj, (?:model\.Runtime|runtime))'
)

for fname in TARGET_FILES:
    try:
        with open(fname) as f:
            content = f.read()
    except FileNotFoundError:
        print(f"{fname}: not found, skipping")
        continue

    if "model.dispose()" in content:
        print(f"{fname}: already patched, skipping")
        continue

    def replacer(m):
        line = m.group(1)
        if "model.Runtime" in line:
            return "    runtime = model.Runtime\n    model.dispose()\n    return best_obj, runtime"
        else:
            return "    model.dispose()\n" + line

    new_content, n = pattern.subn(replacer, content)
    if n == 0:
        print(f"{fname}: pattern not found — no change (check manually)")
        continue

    with open(fname, "w") as f:
        f.write(new_content)
    print(f"{fname}: patched {n} occurrence(s)")