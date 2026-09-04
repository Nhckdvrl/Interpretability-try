"""C4 depth profile: at which depth does editing the referential-role state move the explanation?

Reported at every captured depth rather than at the probe-AUC argmax, because held-out AUC saturates
in some families and the argmax is then arbitrary. The profile also answers the branch-point
question: where along the stack does the referential state start to govern the explanatory readout?
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def stat(per_item, rng):
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return values.mean(), low, high, "*" if (low > 0) == (high > 0) else " "


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    parser.add_argument("--alpha", default="a4")
    args = parser.parse_args()

    for path in args.results:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = rows[0]
        rows = [r for r in rows[1:] if r["held_out"] and r["p_restricts"]]
        rng = np.random.default_rng(SEED)
        n_blocks = max(int(k) for k in meta["layers"])
        print(f"\n=== {meta['model_checkpoint'].split('/')[-1]} | explanation context ===")
        print(f"{'depth':<8}{'AUC':>7}{'role: dES(true)':>26}{'role: dES(contrast)':>26}"
              f"{'shuffled(contrast)':>24}{'random(contrast)':>22}")
        for layer in meta["edited_layers"]:
            cells = []
            for name, label in (("role", "p"), ("role", "p_contrast"),
                                ("shuffled", "p_contrast"), ("random", "p_contrast")):
                key = f"L{layer}|{name}|{args.alpha}"
                per_item = defaultdict(list)
                for row in rows:
                    if row["continuation_label"] == label and key in row["scores"]:
                        per_item[row["item_id"]].append(row["scores"][key] - row["scores"]["baseline"])
                if not per_item:
                    cells.append("n/a")
                    continue
                mean, low, high, star = stat(per_item, rng)
                cells.append(f"{mean:+.4f} [{low:+.4f},{high:+.4f}]{star}")
            auc = meta["layers"][str(layer)]
            print(f"{layer:<8}{auc:>7.3f}{cells[0]:>26}{cells[1]:>26}{cells[2]:>24}{cells[3]:>22}")
    print("\nEdit pushes a restricting modifier toward the non-restricting class mean. "
          "* = bootstrap interval over held-out items excludes zero.")


if __name__ == "__main__":
    main()
