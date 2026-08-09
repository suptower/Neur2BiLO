#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit

source /srv/scratch/watwa-nn-blo/watwa_nn_blo_env/bin/activate || echo "Failed to activate virtual environment 'watwa_nn_blo_env'. Please check the path and try again."
echo "Virtual environment 'watwa_nn_blo_env' activated."