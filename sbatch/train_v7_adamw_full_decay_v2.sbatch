#!/bin/bash
#SBATCH --job-name=v7_adamw_ctxdecay
#SBATCH --partition=full
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=08:00:00
#SBATCH --output=logs/v7_adamw_ctxdecay_%j.log
#SBATCH --error=logs/v7_adamw_ctxdecay_%j.err

set -euo pipefail

cd /home/cip/2024/hy47pini/watwa-nn-blo/

mkdir -p logs

/home/cip/2024/hy47pini/watwa-nn-blo/.venv/bin/python3 -u -m blo.scripts.03_train_nn \
  --problem watwa_v7 \
  --use_context 1 \
  --context_hidden_dim 32 \
  --batch_size 512 \
  --lr 0.001 \
  --n_epochs 1000 \
  --metric top1_acc \
  --weight_decay 1e-6 \
  --ranking_loss_weight 0.0 \
  --optimizer AdamW
