#!/bin/bash
cd "$(dirname "$0")"
PY=~/miniconda3/envs/fgvd/bin/python
# wait for both sweeps
while ps -eo cmd | grep -q "[r]un_phase2.py --mode sweep"; do sleep 15; done
for f in results/phase2_r1/llama31_8b_it__sweep.json results/phase2_r1/qwen3_8b__sweep.json; do
  [ -f "$f" ] || { echo "MISSING $f -- sweep failed"; exit 1; }
done
echo "both sweeps done, starting ablate"
HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=2 $PY src/alias_entrainment/run_phase2.py \
  --mode ablate --model NousResearch/Meta-Llama-3.1-8B-Instruct --tag llama31_8b_it \
  --batch-size 64 > results/phase2_ablate_llama.log 2>&1 &
P1=$!
HF_HUB_OFFLINE=1 CUDA_VISIBLE_DEVICES=1 $PY src/alias_entrainment/run_phase2.py \
  --mode ablate --model Qwen/Qwen3-8B --tag qwen3_8b \
  --batch-size 64 > results/phase2_ablate_qwen.log 2>&1 &
P2=$!
wait $P1 $P2
echo "ablate done"
