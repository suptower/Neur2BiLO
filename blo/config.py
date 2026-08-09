"""
Separate configuration for slurm and i4watwa
"""
import os

SCRIPTS_DIR_RELATIVE = os.path.join(os.path.dirname(__file__), "scripts")
SCRIPT_RUN_ML_BLO = SCRIPTS_DIR_RELATIVE + "/05_run_ml_blo.py"
SCRIPT_EVAL_WATWA_BATCH = SCRIPTS_DIR_RELATIVE + "/evaluate_watwa_batch.py"

# blo/scripts/evaluate_watwa_batch.py @ line 88
EVAL_WATWA_BATCH_I4WATWA = '"python", "-m", "blo.scripts.05_run_ml_blo",'
EVAL_WATWA_BATCH_SLURM = '"/home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/python3", "-m", "blo.scripts.05_run_ml_blo",'


# blo/scripts/05_run_ml_blo.py @ line 458
RUN_ML_BLO_MAP_LOCATION_I4WATWA = "net = torch.load(fp_nn, weights_only=False)"
RUN_ML_BLO_MAP_LOCATION_SLURM = 'net = torch.load(fp_nn, weights_only=False, map_location="cpu")'

def switch_config_for_slurm():
    # Open RUN_ML_BLO and replace the map_location line
    with open(SCRIPT_RUN_ML_BLO, "r") as f:
        lines = f.readlines()
    with open(SCRIPT_RUN_ML_BLO, "w") as f:
        for line in lines:
            if RUN_ML_BLO_MAP_LOCATION_I4WATWA in line:
                f.write(line.replace(RUN_ML_BLO_MAP_LOCATION_I4WATWA, RUN_ML_BLO_MAP_LOCATION_SLURM))
            else:
                f.write(line)

    # Open EVAL_WATWA_BATCH and replace the command line
    with open(SCRIPT_EVAL_WATWA_BATCH, "r") as f:
        lines = f.readlines()
    with open(SCRIPT_EVAL_WATWA_BATCH, "w") as f:
        for line in lines:
            if EVAL_WATWA_BATCH_I4WATWA in line:
                f.write(line.replace(EVAL_WATWA_BATCH_I4WATWA, EVAL_WATWA_BATCH_SLURM))
            else:
                f.write(line)

def switch_config_for_i4watwa():
    # Open RUN_ML_BLO and replace the map_location line
    with open(SCRIPT_RUN_ML_BLO, "r") as f:
        lines = f.readlines()
    with open(SCRIPT_RUN_ML_BLO, "w") as f:
        for line in lines:
            if RUN_ML_BLO_MAP_LOCATION_SLURM in line:
                f.write(line.replace(RUN_ML_BLO_MAP_LOCATION_SLURM, RUN_ML_BLO_MAP_LOCATION_I4WATWA))
            else:
                f.write(line)

    # Open EVAL_WATWA_BATCH and replace the command line
    with open(SCRIPT_EVAL_WATWA_BATCH, "r") as f:
        lines = f.readlines()
    with open(SCRIPT_EVAL_WATWA_BATCH, "w") as f:
        for line in lines:
            if EVAL_WATWA_BATCH_SLURM in line:
                f.write(line.replace(EVAL_WATWA_BATCH_SLURM, EVAL_WATWA_BATCH_I4WATWA))
            else:
                f.write(line)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Switch configuration for slurm or i4watwa")
    parser.add_argument("--slurm", action="store_true", help="Switch to slurm configuration")
    parser.add_argument("--i4watwa", action="store_true", help="Switch to i4watwa configuration")

    args = parser.parse_args()

    if args.slurm:
        switch_config_for_slurm()
        print("Switched configuration to slurm.")
    elif args.i4watwa:
        switch_config_for_i4watwa()
        print("Switched configuration to i4watwa.")
    else:
        print("No action specified. Use --slurm or --i4watwa.")