#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/home/xiang/miniconda3/envs/fgvd/bin/python}"
CONTRACT="$ROOT_DIR/configs/d0_strong_contract.json"
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$ROOT_DIR/results/d0_strong"

"$PYTHON_BIN" -m pytest "$ROOT_DIR/tests" -q
for specification in "qwen:0" "gemma:1" "llama:2" "mistral:3"
do
  IFS=: read -r family gpu <<<"$specification"
  CUDA_VISIBLE_DEVICES="$gpu" HF_HOME=/home/xiang/.cache/huggingface \
    "$PYTHON_BIN" -m world_indexed_truth.run_model \
      --contract "$CONTRACT" --family "$family" \
      --output "$ROOT_DIR/results/d0_strong/$family.jsonl" \
    >"$ROOT_DIR/results/d0_strong_${family}.log" 2>&1 &
done
wait
"$PYTHON_BIN" -m world_indexed_truth.analyze \
  --contract "$CONTRACT" --results-dir "$ROOT_DIR/results/d0_strong" \
  --output "$ROOT_DIR/results/d0_strong_analysis.json" \
  --summary-csv "$ROOT_DIR/results/d0_strong_summary.csv" \
  | tee "$ROOT_DIR/results/d0_strong_analysis.log"
