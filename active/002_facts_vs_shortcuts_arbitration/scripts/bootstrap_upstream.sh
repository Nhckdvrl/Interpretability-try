#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${1:-$ROOT/vendor/facts-vs-shortcuts}"
UPSTREAM_URL="https://github.com/HeLehm/facts-vs-shortcuts.git"
UPSTREAM_COMMIT="91d320541f44518266ffa34f6138bd16eb775d83"

if [[ -e "$DEST" ]]; then
  echo "Refusing to overwrite existing path: $DEST" >&2
  exit 2
fi

git clone "$UPSTREAM_URL" "$DEST"
git -C "$DEST" checkout --detach "$UPSTREAM_COMMIT"
printf 'Pinned upstream at %s\n' "$UPSTREAM_COMMIT"
