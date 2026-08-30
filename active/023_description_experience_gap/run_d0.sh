#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/home/xiang/miniconda3/envs/fgvd/bin/python}"
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$ROOT_DIR/results/d0"

"$PYTHON_BIN" -m description_experience.build_bank
"$PYTHON_BIN" -m pytest "$ROOT_DIR/tests" -q
for specification in "qwen:0" "gemma:1" "llama:2" "mistral:3"
do
  IFS=: read -r family gpu <<<"$specification"
  CUDA_VISIBLE_DEVICES="$gpu" HF_HOME=/home/xiang/.cache/huggingface \
    "$PYTHON_BIN" -m description_experience.run_model --family "$family" \
    >"$ROOT_DIR/results/d0_${family}.log" 2>&1 &
done
wait
"$PYTHON_BIN" -m description_experience.analyze | tee "$ROOT_DIR/results/d0_analysis.log"
