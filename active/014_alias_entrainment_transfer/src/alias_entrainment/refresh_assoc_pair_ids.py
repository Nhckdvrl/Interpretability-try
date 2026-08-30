"""Refresh pair IDs after an ID-only surface-bank schema correction.

Wikidata associate expansion is expensive and its resolved labels/types are
already frozen in ``d1_assoc_candidates_r4.json``.  This deterministic utility
updates only ``pair_id`` by exact ``(subject_id, seen_form)`` lookup after the
case-sensitive ID fix; it refuses any content or cardinality mismatch.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", default="data/d1_surface_pairs_r4.json")
    ap.add_argument("--assoc", default="data/d1_assoc_candidates_r4.json")
    args = ap.parse_args()
    surface = json.load(open(args.surface, encoding="utf-8"))
    assoc = json.load(open(args.assoc, encoding="utf-8"))
    ids = {(row["subject_id"], row["seen_form"]): row["pair_id"] for row in surface}
    if len(ids) != len(surface):
        raise RuntimeError("surface lookup is not one-to-one")
    if len(assoc) != len(surface):
        raise RuntimeError("surface/ASSOC bank cardinality mismatch")
    refreshed = []
    for row in assoc:
        key = (row["subject_id"], row["seen_form"])
        if key not in ids:
            raise RuntimeError(f"ASSOC row missing from refreshed surface bank: {key!r}")
        refreshed.append({**row, "pair_id": ids[key]})
    pair_ids = [row["pair_id"] for row in refreshed]
    if len(pair_ids) != len(set(pair_ids)):
        raise RuntimeError("refreshed ASSOC pair IDs are not unique")
    Path(args.assoc).write_text(json.dumps(refreshed, indent=1, ensure_ascii=False))
    print(f"refreshed {len(refreshed)} exact surface pair IDs in {args.assoc}")


if __name__ == "__main__":
    main()
