#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/home/xiang/miniconda3/envs/fgvd/bin/python}"
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"

"$PYTHON_BIN" -m alignment_arbitration.build_bank

families=(qwen gemma llama smollm)
for gpu in 0 1 2 3; do
  family="${families[$gpu]}"
  (
    CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON_BIN" -m alignment_arbitration.run_model --family "$family" --role base
    CUDA_VISIBLE_DEVICES="$gpu" "$PYTHON_BIN" -m alignment_arbitration.run_model --family "$family" --role aligned
  ) >"$ROOT_DIR/results/d0_${family}.log" 2>&1 &
done
wait

"$PYTHON_BIN" -m alignment_arbitration.analyze
