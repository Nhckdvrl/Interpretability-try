#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-data/bfcl}"
ART_DIR="${ART_DIR:-artifacts}"
CATEGORY="simple_python"
mkdir -p "$DATA_DIR" "$ART_DIR"

binding-fetch --category "$CATEGORY" --out-dir "$DATA_DIR"

binding-scan \
  --data "$DATA_DIR/BFCL_v4_${CATEGORY}.json" \
  --answers "$DATA_DIR/BFCL_v4_${CATEGORY}_answers.json" \
  --out "$ART_DIR/eligible_${CATEGORY}.jsonl"

for spec in \
  "qwen3_4b|Qwen_Qwen3-4B-Instruct-2507-FC" \
  "gemma3_4b|google_gemma-3-4b-it"
do
  tag="${spec%%|*}"
  model_dir="${spec#*|}"
  binding-official \
    --category "$CATEGORY" \
    --model-dir "$model_dir" \
    --out "$ART_DIR/${tag}_official.jsonl"

  echo "=== ${tag} ==="
  binding-classify \
    --data "$DATA_DIR/BFCL_v4_${CATEGORY}.json" \
    --answers "$DATA_DIR/BFCL_v4_${CATEGORY}_answers.json" \
    --outputs "$ART_DIR/${tag}_official.jsonl" \
    --out "$ART_DIR/${tag}_diagnosis.jsonl"
done
