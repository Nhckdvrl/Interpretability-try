#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-/home/xiang/miniconda3/envs/fgvd/bin/python}"
export PYTHONPATH="$ROOT_DIR/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$ROOT_DIR/results/d0"

"$PYTHON_BIN" -m world_indexed_truth.build_bank
"$PYTHON_BIN" -m pytest "$ROOT_DIR/tests" -q

for specification in \
  "qwen:0:/home/xiang/.cache/huggingface" \
  "gemma:1:/tmp/hf_topic024_gemma3" \
  "llama:2:/tmp/hf_topic024_llama1" \
  "smollm:3:/tmp/hf_topic024_smollm360"
do
  IFS=: read -r family gpu cache <<<"$specification"
  CUDA_VISIBLE_DEVICES="$gpu" HF_HOME="$cache" \
    "$PYTHON_BIN" -m world_indexed_truth.run_model --family "$family" \
    >"$ROOT_DIR/results/d0_${family}.log" 2>&1 &
done
wait
"$PYTHON_BIN" -m world_indexed_truth.analyze | tee "$ROOT_DIR/results/d0_analysis.log"
