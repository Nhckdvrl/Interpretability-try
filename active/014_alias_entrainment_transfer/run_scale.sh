#!/bin/bash
# Scale axis, contract r1c. Same D0, same metric, same harness.
cd "$(dirname "$0")"
PY=~/miniconda3/envs/fgvd/bin/python
run() { HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=$1 $PY src/alias_entrainment/run_phase1.py \
          --model "$2" --tag "$3" --out-dir results/phase1_r1 --batch-size "${4:-32}" \
          >> results/phase1_r1/logs/scale_gpu$1.log 2>&1; }
case "$1" in
  0) run 0 Qwen/Qwen3-32B qwen3_32b 16 ;;
  1) run 1 Qwen/Qwen3-14B qwen3_14b 24; run 1 google/gemma-3-4b-it gemma3_4b_it 32 ;;
  2) run 2 Qwen/Qwen3-4B qwen3_4b 32; run 2 Qwen/Qwen3-1.7B qwen3_1.7b 32 ;;
  3) run 3 Qwen/Qwen3-0.6B qwen3_0.6b 32 ;;
esac
echo "GPU$1 lane done"
