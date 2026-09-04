"""C4: is the R->E coupling carried causally by the referential-role state?

The edit replaces the modifier token's component along the restriction-role direction with the
opposite class mean, so a restricting modifier is pushed toward the non-restricting mean. If the
coupling B1 found behaviourally is carried by this state, the edit should reproduce it in miniature:
support for the true-property explanation falls and support for the contrasting property rises.

Held-out property families only. Bootstrap over items, 5,000 resamples.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def fmt(per_item: dict[str, list[float]], rng) -> str:
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return "n/a"
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    star = "*" if (low > 0) == (high > 0) else " "
    return f"{values.mean():+.4f} [{low:+.4f},{high:+.4f}]{star}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--explanation", type=Path, nargs="+", required=True)
    parser.add_argument("--reference", type=Path, nargs="*", default=[])
    args = parser.parse_args()

    for path in args.explanation:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = rows[0]
        rows = [r for r in rows[1:] if r["held_out"] and r["p_restricts"]]
        rng = np.random.default_rng(SEED)
        model = meta["model_checkpoint"].split("/")[-1]
        print(f"\n=== {model} | explanation context | layer {meta['layer']} "
              f"| held-out probe AUC {meta['held_out_auc']:.3f} "
              f"| held-out families {', '.join(meta['held_out_families'])} ===")
        edits = [k for k in rows[0]["scores"] if k != "baseline"]
        print(f"{'edit':<16}{'dES(true property)':>26}{'dES(contrasting property)':>30}")
        for edit in edits:
            cells = []
            for label in ("p", "p_contrast"):
                per_item = defaultdict(list)
                for row in rows:
                    if row["continuation_label"] == label:
                        per_item[row["item_id"]].append(row["scores"][edit] - row["scores"]["baseline"])
                cells.append(fmt(per_item, rng))
            print(f"{edit:<16}{cells[0]:>26}{cells[1]:>30}")

    for path in args.reference:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = rows[0]
        rows = [r for r in rows[1:] if r["held_out"]]
        rng = np.random.default_rng(SEED)
        model = meta["model_checkpoint"].split("/")[-1]
        print(f"\n=== {model} | reference context | layer {meta['layer']} "
              f"| held-out probe AUC {meta['held_out_auc']:.3f} ===")
        edits = [k for k in rows[0]["scores"] if k != "baseline"]
        print(f"{'edit':<16}{'dReferenceMargin (P restricting)':>36}"
              f"{'(P not restricting)':>26}")
        for edit in edits:
            cells = []
            for restricting in (True, False):
                per_item = defaultdict(list)
                for row in rows:
                    if row["p_restricts"] == restricting:
                        per_item[row["item_id"]].append(row["scores"][edit] - row["scores"]["baseline"])
                cells.append(fmt(per_item, rng))
            print(f"{edit:<16}{cells[0]:>36}{cells[1]:>26}")

    print("\nEdit pushes each modifier toward the opposite class mean. "
          "* = bootstrap interval over held-out items excludes zero.")


if __name__ == "__main__":
    main()
