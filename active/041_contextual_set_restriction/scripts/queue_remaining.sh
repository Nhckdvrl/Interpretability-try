#!/bin/sh
# Waits on output files rather than pgrep: a pgrep pattern matches this script's own command line.
cd /home/xiang/Interpretability-try/active/041_contextual_set_restriction
PY=/home/xiang/Interpretability-try/.venv-vllm/bin/python
wait_for() { while [ ! -s "$1" ]; do sleep 60; done; }

dense() {  # gpu model tag
  for label in p_restricts p_relevant_to_event; do
    for split in fold_a fold_b; do
      CUDA_VISIBLE_DEVICES=$1 TOKENIZERS_PARALLELISM=false $PY -u scripts/run_c4_role_causal_cross_readout.py \
        --config configs/b1_function_cross.json --stimuli stimuli/b1_function_cross_v4.jsonl \
        --context explanation --every-layer --label $label --split $split \
        --model "$2" --model-path "$2" \
        --output results/raw/v4dense_${label}_${split}_$3.jsonl --batch-size 16 || return 1
    done
  done
}

( wait_for results/raw/v4dense_p_relevant_to_event_fold_b_qwen3_8b.jsonl
  dense 1 "google/gemma-3-12b-it" gemma3_12b ) > logs/queue_gemma.log 2>&1 &

( wait_for results/raw/v4dense_p_relevant_to_event_fold_b_llama3_1_8b.jsonl
  dense 2 "mistralai/Mistral-Small-24B-Instruct-2501" mistral_small_24b ) > logs/queue_mistral.log 2>&1 &

( wait_for results/raw/b1v4_reference_mistral_small_24b.jsonl
  for size in 1.7B 4B 14B 32B; do
    for label in p_restricts p_relevant_to_event; do
      CUDA_VISIBLE_DEVICES=0 TOKENIZERS_PARALLELISM=false $PY -u scripts/run_c4_role_causal_cross_readout.py \
        --config configs/b1_function_cross.json --stimuli stimuli/b1_function_cross_v4.jsonl \
        --context explanation --every-layer --label $label --split fold_a \
        --model "Qwen/Qwen3-${size}" --model-path "Qwen/Qwen3-${size}" \
        --output results/raw/v4scale_${label}_qwen3_${size}.jsonl --batch-size 8 || exit 1
    done
  done ) > logs/queue_scale.log 2>&1 &
wait
