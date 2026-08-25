#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UPSTREAM="${UPSTREAM:-$ROOT/vendor/facts-vs-shortcuts}"
MODEL="${1:?usage: run_upstream_model.sh MODEL [BATCH_SIZE]}"
BATCH_SIZE="${2:-32}"
RESULTS_DIR="${RESULTS_DIR:-$ROOT/upstream_results}"

if [[ ! -f "$UPSTREAM/main.py" ]]; then
  echo "Missing upstream checkout at $UPSTREAM; run scripts/bootstrap_upstream.sh first." >&2
  exit 2
fi

# Run the upstream paper's natural pointwise + pairwise tasks without any
# synthetic perturbation. Dataset defaults are intentionally left to the
# pinned upstream code so G0 stays aligned with the published setup.
(
  cd "$UPSTREAM"
  python main.py \
    --model "$MODEL" \
    --task pointwise pairwise \
    --batch-size "$BATCH_SIZE" \
    --output-dir "$RESULTS_DIR"
)
