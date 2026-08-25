#!/bin/bash
#SBATCH --job-name=eval_v7_ctxDecay
#SBATCH --partition=full
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=36:00:00
#SBATCH --oversubscribe
#SBATCH --output=logs/eval_v7_adamw_ctxdecay.log
set -euo pipefail
cd /home/cip/2024/hy47pini/watwa-nn-blo/
source /home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/activate
export GRB_LICENSE_FILE=/home/cip/2024/hy47pini/watwa-nn-blo/gurobi/gurobi.lic
mkdir -p logs
/home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/python3 -u -m blo.scripts.evaluate_watwa_batch \
  --problem watwa_v7 \
  --use_context 1 \
  --context_hidden_dim 32
