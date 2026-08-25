#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RESULTS_DIR="${1:-$ROOT/upstream_results}"
OUTPUT_DIR="${2:-$ROOT/artifacts/g0}"

python -m facts_shortcuts_g0.cli \
  --results-dir "$RESULTS_DIR" \
  --output-dir "$OUTPUT_DIR"

cat "$OUTPUT_DIR/verdict.json"
