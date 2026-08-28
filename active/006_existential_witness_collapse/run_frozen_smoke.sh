#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

QWEN_MODEL="${QWEN_MODEL:-Qwen/Qwen3-8B}"
GEMMA_MODEL="${GEMMA_MODEL:-google/gemma-3-12b-it}"
QWEN_REVISION="${QWEN_REVISION:-b968826d9c46dd6066d109eabc6255188de91218}"
GEMMA_REVISION="${GEMMA_REVISION:-96b6f1eccf38110c56df3a15bffe176da04bfd80}"
DTYPE="${DTYPE:-bfloat16}"
BATCH_SIZE="${BATCH_SIZE:-64}"
CONFIG="configs/frozen_g0.json"
DATA="data/frozen_d0.jsonl"
EXPECTED_DATA_SHA="6076ad3de2e756b1361799a21baef155586cb641303a9779b4b8c9d3452220e0"

mkdir -p results

printf '\n[1/8] Unit tests\n'
pytest -q

printf '\n[2/8] Build frozen D0\n'
python data/build_frozen_d0.py
ACTUAL_DATA_SHA="$(sha256sum "$DATA" | awk '{print $1}')"
if [[ "$ACTUAL_DATA_SHA" != "$EXPECTED_DATA_SHA" ]]; then
  echo "FATAL: frozen D0 SHA mismatch: $ACTUAL_DATA_SHA != $EXPECTED_DATA_SHA" >&2
  exit 2
fi

printf '\n[3/8] Validate frozen D0\n'
existential-witness-run validate-data --data "$DATA"

printf '\n[4/8] Qwen3-8B smoke\n'
existential-witness-run run \
  --data "$DATA" \
  --out results/qwen3_8b.smoke.jsonl \
  --config "$CONFIG" \
  --model "$QWEN_MODEL" \
  --family Qwen \
  --revision "$QWEN_REVISION" \
  --dtype "$DTYPE" \
  --size-b 8 \
  --batch-size "$BATCH_SIZE"

printf '\n[5/8] Qwen3-8B summary\n'
existential-witness-run summarize \
  --data "$DATA" \
  --results results/qwen3_8b.smoke.jsonl \
  --config "$CONFIG" \
  --out results/qwen3_8b.smoke.summary.json

printf '\n[6/8] Gemma3-12B smoke\n'
existential-witness-run run \
  --data "$DATA" \
  --out results/gemma3_12b.smoke.jsonl \
  --config "$CONFIG" \
  --model "$GEMMA_MODEL" \
  --family Gemma \
  --revision "$GEMMA_REVISION" \
  --dtype "$DTYPE" \
  --size-b 12 \
  --batch-size "$BATCH_SIZE"

printf '\n[7/8] Gemma3-12B summary\n'
existential-witness-run summarize \
  --data "$DATA" \
  --results results/gemma3_12b.smoke.jsonl \
  --config "$CONFIG" \
  --out results/gemma3_12b.smoke.summary.json

printf '\n[8/8] Frozen two-family panel\n'
existential-witness-run panel \
  --summary results/qwen3_8b.smoke.summary.json results/gemma3_12b.smoke.summary.json \
  --config "$CONFIG" \
  --out results/smoke_panel_summary.json

printf '\nDONE\n'
printf 'data_sha256=%s\n' "$ACTUAL_DATA_SHA"
printf 'qwen_summary=%s\n' "$ROOT/results/qwen3_8b.smoke.summary.json"
printf 'gemma_summary=%s\n' "$ROOT/results/gemma3_12b.smoke.summary.json"
printf 'panel=%s\n' "$ROOT/results/smoke_panel_summary.json"
