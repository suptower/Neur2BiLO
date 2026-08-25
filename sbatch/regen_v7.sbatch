#!/bin/bash
#SBATCH --job-name=regen_data_v7
#SBATCH --partition=full
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=36:00:00
#SBATCH --oversubscribe
set -euo pipefail
cd /home/cip/2024/hy47pini/watwa-nn-blo/
export GRB_LICENSE_FILE=/home/cip/2024/hy47pini/watwa-nn-blo/gurobi/gurobi.lic
mkdir -p logs
/home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/python3 -u -m blo.scripts.02_generate_data --problem watwa_v7
