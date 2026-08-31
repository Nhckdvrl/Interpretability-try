#!/usr/bin/env python3
"""Build adjacent C/W transition cells from deterministic checkpoint scores."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def build(rows: list[dict]) -> dict:
    by_item: dict[str, dict[int, bool]] = defaultdict(dict)
    for row in rows:
        item_id = str(row["item_id"])
        step = int(row["checkpoint_step"])
        if step in by_item[item_id]:
            raise ValueError(f"Duplicate item/checkpoint row: {item_id}/{step}")
        by_item[item_id][step] = bool(row["correct"])

    steps = sorted({step for values in by_item.values() for step in values})
    pairs = list(zip(steps, steps[1:]))
    pair_summaries = {}
    sequences = {}
    for item_id, values in sorted(by_item.items()):
        sequences[item_id] = "".join("C" if values.get(step) else "W" for step in steps)
    for left, right in pairs:
        cells: dict[str, list[str]] = defaultdict(list)
        for item_id, values in by_item.items():
            if left not in values or right not in values:
                continue
            cell = ("C" if values[left] else "W") + "->" + ("C" if values[right] else "W")
            cells[cell].append(item_id)
        pair_summaries[f"{left}->{right}"] = {
            "counts": dict(sorted(Counter({cell: len(ids) for cell, ids in cells.items()}).items())),
            "item_ids": {cell: sorted(ids) for cell, ids in sorted(cells.items())},
        }
    return {
        "schema_version": 1,
        "checkpoint_steps": steps,
        "n_items": len(by_item),
        "sequences": sequences,
        "adjacent_pairs": pair_summaries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = [json.loads(line) for line in args.input.read_text(encoding="utf-8").splitlines() if line]
    result = build(rows)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
