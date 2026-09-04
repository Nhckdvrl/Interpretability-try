"""C5: where does the referential-role state gain its influence over the explanation pathway?

B1 and C4 established that referential status reshapes what the same content is taken to explain,
and that the role state carries it. This asks *where*. Two readings are alive:

  local multiplexing   -- the causal effect on explanation appears as soon as the role is decodable
  shared-then-branch   -- the role becomes decodable first and only influences explanation later

The table puts held-out probe AUC and the causal effect side by side at each depth, so the two can
be compared directly. Depth is reported as a fraction of the stack, because the four families have
different numbers of blocks.

Note on novelty: that upper layers are more discourse-like is already established for LMs
(Discursive Circuits, EMNLP 2025). Nothing here may be claimed on that basis. The question is only
whether the *ordering* between decodability and causal influence explains the R->E asymmetry.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def stat(per_item: dict[str, list[float]], rng):
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return None
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return values.mean(), low, high


def cell(rows, edit, label, rng) -> str:
    per_item = defaultdict(list)
    for row in rows:
        if row["continuation_label"] == label and edit in row["scores"]:
            per_item[row["item_id"]].append(row["scores"][edit] - row["scores"]["baseline"])
    result = stat(per_item, rng)
    if result is None:
        return "     --     "
    mean, low, high = result
    return f"{mean:+.4f}{'*' if (low > 0) == (high > 0) else ' '}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    parser.add_argument("--alpha", default="4")
    args = parser.parse_args()

    for path in args.results:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = rows[0]
        rows = [r for r in rows[1:] if r["held_out"] and r["p_restricts"]]
        n_blocks = max(int(k) for k in meta["layers"]) or 1
        rng = np.random.default_rng(SEED)
        print(f"\n=== {meta['model_checkpoint'].split('/')[-1]} | explanation context "
              f"| held-out families {', '.join(meta['held_out_families'])} ===")
        print(f"{'layer':>7}{'depth':>8}{'probe AUC':>12}"
              f"{'role: dES true':>17}{'role: dES contrast':>21}"
              f"{'random: true':>15}{'random: contrast':>19}")
        layers = sorted(int(k) for k in meta["layers"])
        deepest = max(layers)
        for layer in layers:
            auc = meta["layers"][str(layer)]
            role = f"L{layer}|role|a{args.alpha}"
            random = f"L{layer}|random|a{args.alpha}"
            print(f"{layer:>7}{layer / deepest:>8.2f}{auc:>12.3f}"
                  f"{cell(rows, role, 'p', rng):>17}{cell(rows, role, 'p_contrast', rng):>21}"
                  f"{cell(rows, random, 'p', rng):>15}{cell(rows, random, 'p_contrast', rng):>19}")
    print("\ndepth is layer / deepest captured layer; * = bootstrap interval over held-out items "
          "excludes zero")


if __name__ == "__main__":
    main()
