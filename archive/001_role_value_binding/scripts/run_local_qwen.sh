#!/usr/bin/env bash
set -euo pipefail

DATA_DIR="${DATA_DIR:-data/bfcl}"
ART_DIR="${ART_DIR:-artifacts}"
MODEL="${MODEL:-Qwen/Qwen3-4B-Instruct-2507}"
CATEGORY="simple_python"

if [[ ! -f "$ART_DIR/eligible_${CATEGORY}.jsonl" ]]; then
  echo "Missing $ART_DIR/eligible_${CATEGORY}.jsonl; run scripts/run_public_g0.sh first." >&2
  exit 2
fi

binding-infer \
  --model "$MODEL" \
  --data "$DATA_DIR/BFCL_v4_${CATEGORY}.json" \
  --ids "$ART_DIR/eligible_${CATEGORY}.jsonl" \
  --out "$ART_DIR/qwen3_4b_local.jsonl"

binding-classify \
  --data "$DATA_DIR/BFCL_v4_${CATEGORY}.json" \
  --answers "$DATA_DIR/BFCL_v4_${CATEGORY}_answers.json" \
  --outputs "$ART_DIR/qwen3_4b_local.jsonl" \
  --out "$ART_DIR/qwen3_4b_local_diagnosis.jsonl"
