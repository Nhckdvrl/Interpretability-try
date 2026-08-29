#!/bin/bash
# 012 r3 re-run: identical to r2 except the source_credibility probe, which became a
# counterbalanced two-content-option item. Full re-run of both models, no row reuse.
# Gemma runs at batch 16: its 262k vocab makes the batch-64 logits tensor ~26 GB.
set -u
ROOT=/home/xiang/Interpretability-try/active/012_source_discount_recovery
PY=/home/xiang/Interpretability-try/.venv-vllm/bin/python
OUT=$ROOT/results/smoke_r3
QWEN_REV=b968826d9c46dd6066d109eabc6255188de91218
GEMMA_REV=96b6f1eccf38110c56df3a15bffe176da04bfd80
ENVS="HF_HUB_OFFLINE=1 TOKENIZERS_PARALLELISM=false PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True"

for i in 0 1 2 3; do
  ( cd $ROOT && env CUDA_VISIBLE_DEVICES=$i $ENVS $PY -m source_discount_g0.cli run \
      --data $OUT/shards/shard$i.jsonl --out $OUT/shards/qwen3_8b.raw.$i.jsonl \
      --config $ROOT/configs/frozen_g0.json --model Qwen/Qwen3-8B --family Qwen \
      --revision $QWEN_REV --size-b 8.0 --dtype bfloat16 --batch-size 32 \
      > $OUT/logs/qwen.$i.log 2>&1 ) &
done

for i in 0 1 2 3; do
  ssh -o BatchMode=yes fvcrc20 "cd $ROOT && env CUDA_VISIBLE_DEVICES=$i $ENVS $PY \
      -m source_discount_g0.cli run \
      --data $OUT/shards/shard$i.jsonl --out $OUT/shards/gemma3_12b_it.raw.$i.jsonl \
      --config $ROOT/configs/frozen_g0.json --model google/gemma-3-12b-it --family Gemma \
      --revision $GEMMA_REV --size-b 12.0 --dtype bfloat16 --batch-size 16" \
      > $OUT/logs/gemma.$i.log 2>&1 &
done

wait
echo "ALL SHARDS FINISHED"
for m in qwen3_8b gemma3_12b_it; do
  cat $OUT/shards/$m.raw.[0-3].jsonl > $OUT/$m.raw.jsonl
  echo "$m rows: $(wc -l < $OUT/$m.raw.jsonl)"
done
