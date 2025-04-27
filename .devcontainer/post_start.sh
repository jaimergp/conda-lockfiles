#!/bin/bash

# This script assumes we are running in a Miniconda container where:
# - /opt/conda is the Miniconda or Miniforge installation directory
# - https://github.com/conda/conda is mounted at /workspaces/conda
# - https://github.com/conda/conda-lockfiles is mounted at
#   /workspaces/conda-lockfiles

set -euo pipefail

BASE_CONDA=${BASE_CONDA:-/opt/conda}
SRC_CONDA=${SRC_CONDA:-/workspaces/conda}
SRC_conda_lockfiles=${SRC_conda_lockfiles:-/workspaces/conda-lockfiles}

echo "Installing conda-lockfiles in dev mode..."
"$BASE_CONDA/bin/python" -m pip install -e "$SRC_conda_lockfiles"
