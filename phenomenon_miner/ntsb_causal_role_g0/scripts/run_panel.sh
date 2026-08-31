#!/usr/bin/env bash
# Sequential G0 panel run. One family at a time (each needs the whole GPU).
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PY="$ROOT/../../.venv-vllm/bin/python"
export VLLM_USE_FLASHINFER_SAMPLER=0   # flashinfer JIT needs ninja, absent here
for fam in qwen gemma llama mistral; do
  echo "===== $fam $(date -u +%FT%TZ) ====="
  "$PY" "$ROOT/scripts/run_g0.py" --family "$fam" > "$ROOT/results/run_${fam}.log" 2>&1
  echo "$fam exit=$?"
  grep -E "^\[$fam/" "$ROOT/results/run_${fam}.log" || tail -25 "$ROOT/results/run_${fam}.log"
done
echo "===== PANEL DONE $(date -u +%FT%TZ) ====="
