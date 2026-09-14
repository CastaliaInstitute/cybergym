#!/usr/bin/env bash
set -euo pipefail

UPSTREAM_DIR="${CYBERGYM_UPSTREAM_DIR:-$PWD/.upstream/cybergym}"
DATA_DIR="${CYBERGYM_DATA_DIR:-$PWD/.data/cybergym_data}"

if [[ ! -d "$UPSTREAM_DIR/.git" ]]; then
  mkdir -p "$(dirname "$UPSTREAM_DIR")"
  git clone https://github.com/cybergym-iclr26/cybergym.git "$UPSTREAM_DIR"
fi
python3 -m pip install -e "$UPSTREAM_DIR[dev,server]"
git lfs install
if [[ ! -d "$DATA_DIR/.git" ]]; then
  mkdir -p "$(dirname "$DATA_DIR")"
  git clone https://huggingface.co/datasets/cybergym-iclr26/cybergym "$DATA_DIR"
fi
echo "upstream=$UPSTREAM_DIR"
echo "data=$DATA_DIR"
