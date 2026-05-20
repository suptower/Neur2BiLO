# Dockerfile for Neur2BiLO with CUDA Support on Windows
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# System dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3.11-dev \
    python3.11-distutils \
    git \
    build-essential \
    glpk-utils \
    wget \
    unzip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install pip for Python 3.11 explicitly
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Make python3.11 the default
RUN ln -sf /usr/bin/python3.11 /usr/bin/python && \
    ln -sf /usr/bin/python3.11 /usr/bin/python3

# Working directory
WORKDIR /app

# Clone Neur2BiLO
RUN git clone https://github.com/khalil-research/Neur2BiLO.git .

# Install PyTorch with CUDA 12.1 first (separate index-url)
RUN python -m pip install torch \
    --index-url https://download.pytorch.org/whl/cu121

# Install remaining dependencies
# numpy<2.0  : pao uses np.NINF/np.PINF removed in NumPy 2.0
# pyutilib   : required by pao (only available for Python >=3.11)
RUN python -m pip install \
        "numpy<2.0" \
        packaging \
        pyutilib \
        gurobipy \
        scikit-learn \
        pyomo \
        pao \
        pandas \
        scipy \
        matplotlib \
        gurobi-machinelearning \
        pyyaml

# Create required data directories
RUN mkdir -p data/kp/random_search \
             data/kp/results \
             data/kp/solver_instances \
             data/kp/solver_results \
             data/kp/gp_data

# Fix torch.load: weights_only default changed to True in PyTorch 2.6
RUN sed -i 's/net = torch.load(fp_nn)/net = torch.load(fp_nn, weights_only=False)/' \
    blo/scripts/05_run_ml_blo.py

# Gurobi license mounted at runtime:
# docker run --gpus all -it \
#   -v C:\gurobi\gurobi.lic:/root/gurobi.lic \
#   neur2bilo-docker

CMD ["/bin/bash"]