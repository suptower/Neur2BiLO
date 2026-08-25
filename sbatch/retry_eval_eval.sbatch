#!/bin/bash
#SBATCH --job-name=eval_retry:v7_adamW
#SBATCH --partition=full
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=36:00:00
#SBATCH --oversubscribe
#SBATCH --output=logs/eval_retry_v7_adamw_full_decay_%j.log
#SBATCH --error=logs/eval_retry_v7_adamw_full_decay_%j.err
set -euo pipefail
cd /home/cip/2024/hy47pini/watwa-nn-blo/
export GRB_LICENSE_FILE=/home/cip/2024/hy47pini/watwa-nn-blo/gurobi/gurobi.lic
mkdir -p logs
/home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/python3 -u -m blo.scripts.evaluate_watwa_batch \
  --problem watwa_v7 \
  --use_context 1 \
  --context_hidden_dim 32
