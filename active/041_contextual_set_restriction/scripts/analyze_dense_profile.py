"""Layer-by-layer causal profile, both states, folds pooled.

Every decoder layer is edited, so nothing has to be selected: the profile is the evidence. Rows are
layers, and the two states are shown side by side on the contrasting-property continuation, which is
where B1's behavioural dissociation lives. `role - shuffled` at alpha 4, bootstrapped over the
held-out families of both folds pooled.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def load(paths):
    grouped = defaultdict(list)
    for path in paths:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        grouped[(rows[0]["model_checkpoint"], rows[0]["label"])].append((rows[0], rows[1:]))
    return grouped


def cell(files, layer, label, rng):
    per_item = defaultdict(list)
    for meta, rows in files:
        selector = meta["label"]
        for row in rows:
            if not (row["held_out"] and row[selector]):
                continue
            if row["continuation_label"] != label:
                continue
            role = row["scores"].get(f"L{layer}|role|a4")
            shuffled = row["scores"].get(f"L{layer}|shuffled|a4")
            if role is not None and shuffled is not None:
                per_item[row["item_id"]].append(role - shuffled)
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return "    --   ", 0
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return f"{values.mean():+.4f}{'*' if (low > 0) == (high > 0) else ' '}", values.size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    args = parser.parse_args()
    grouped = load(args.results)
    models = sorted({m for m, _ in grouped})

    for model in models:
        ref = grouped.get((model, "p_restricts"), [])
        evt = grouped.get((model, "p_relevant_to_event"), [])
        if not ref:
            continue
        layers = sorted(int(k) for k in ref[0][0]["layers"])
        rng = np.random.default_rng(SEED)
        n = cell(ref, layers[0], "p_contrast", rng)[1]
        print(f"\n=== {model.split('/')[-1]} | held-out families {n} | every layer edited ===")
        print(f"{'layer':>6}{'AUC(ref)':>10}{'ref: true':>12}{'ref: contrast':>15}"
              f"{'AUC(evt)':>10}{'evt: true':>12}{'evt: contrast':>15}")
        for layer in layers:
            rng = np.random.default_rng(SEED)
            auc_r = np.mean([m["layers"][str(layer)] for m, _ in ref])
            row = f"{layer:>6}{auc_r:>10.3f}"
            row += f"{cell(ref, layer, 'p', rng)[0]:>12}{cell(ref, layer, 'p_contrast', rng)[0]:>15}"
            if evt:
                auc_e = np.mean([m["layers"][str(layer)] for m, _ in evt])
                row += f"{auc_e:>10.3f}{cell(evt, layer, 'p', rng)[0]:>12}"
                row += f"{cell(evt, layer, 'p_contrast', rng)[0]:>15}"
            print(row)
    print("\n* = bootstrap interval over held-out families excludes zero")


if __name__ == "__main__":
    main()
