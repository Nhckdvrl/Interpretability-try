#!/usr/bin/env bash
# NTSB avall.mdb extraction — Phase A/B of NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md
# Requires mdbtools (installed here via conda into .conda-mdbtools/).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PATH="$ROOT/.conda-mdbtools/bin:$PATH"
MDB="$ROOT/raw/avall.mdb"

# ---- Phase A: official download (already recorded in raw/) -------------------
# curl -fL --retry 5 --retry-delay 3 --retry-all-errors \
#   'https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip' \
#   -o "$ROOT/raw/avall.zip"
# sha256sum avall.zip | tee SHA256SUMS.txt ; unzip -o avall.zip

# ---- Phase B: schema enumeration -------------------------------------------
mdb-tables -1 "$MDB" > "$ROOT/audit/tables.txt"
mdb-schema "$MDB"    > "$ROOT/audit/schema.sql"

# ---- Phase B: exports -------------------------------------------------------
mkdir -p "$ROOT/export"
for t in Findings events narratives eADMSPUB_DataDictionary aircraft; do
  mdb-export "$MDB" "$t" > "$ROOT/export/${t}.csv"
done
wc -l "$ROOT"/export/*.csv
