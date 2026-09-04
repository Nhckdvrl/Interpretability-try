"""The two-state signature table on 48 families, with complementary folds pooled.

Inputs are the outputs of `run_c4_role_causal_cross_readout.py` on the 48-family stimuli. Files are
grouped by (model, edited state, split). The two complementary folds are pooled, so every family
appears in a test set exactly once and the held-out N is the full item count; the
`extended_to_core` split is reported separately, since it estimates the direction entirely on the
authored families and tests on the twelve inherited from Davies & Richardson, which is a transfer
test rather than a split.

Statistic is role minus shuffled, averaged over every depth whose held-out AUC is at least 0.6, and
reported per source so the human-validated core never hides inside the extension.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904
MIN_AUC = 0.6
SELECTOR = {"p_restricts": "p_restricts", "p_relevant_to_event": "p_relevant_to_event"}


def gather(files, label, source):
    per_item = defaultdict(list)
    aucs = []
    for meta, rows in files:
        layers = [int(k) for k, v in meta["layers"].items() if v >= MIN_AUC]
        aucs.extend(v for v in meta["layers"].values() if v >= MIN_AUC)
        selector = SELECTOR[meta["label"]]
        for row in rows:
            if not (row["held_out"] and row[selector]):
                continue
            if row["continuation_label"] != label:
                continue
            if source != "all" and row.get("source") != source:
                continue
            for layer in layers:
                role = row["scores"].get(f"L{layer}|role|a4")
                shuffled = row["scores"].get(f"L{layer}|shuffled|a4")
                if role is not None and shuffled is not None:
                    per_item[row["item_id"]].append(role - shuffled)
    return per_item, (float(np.mean(aucs)) if aucs else float("nan"))


def stat(per_item, rng):
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return "     --     ", 0
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return f"{values.mean():+.4f}{'*' if (low > 0) == (high > 0) else ' '}", values.size


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    parser.add_argument("--source", choices=["all", "davies_richardson", "extended"], default="all")
    args = parser.parse_args()

    grouped = defaultdict(list)
    for path in args.results:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        meta = rows[0]
        split = "folds" if meta["split"] in {"fold_a", "fold_b"} else meta["split"]
        grouped[(meta["model_checkpoint"], split)].append((meta, rows[1:]))

    print(f"role minus shuffled, alpha 4, averaged over depths with held-out AUC >= {MIN_AUC}, "
          f"source={args.source}\n")
    print(f"{'model':<26}{'split':<17}{'state':<14}{'N':>4}{'mean AUC':>10}"
          f"{'dES true':>13}{'dES contrast':>15}")
    for (model, split) in sorted(grouped):
        name = model.split("/")[-1]
        for state in ("p_restricts", "p_relevant_to_event"):
            files = [(m, r) for m, r in grouped[(model, split)] if m["label"] == state]
            if not files:
                continue
            rng = np.random.default_rng(SEED)
            cells, sizes = [], []
            for label in ("p", "p_contrast"):
                per_item, auc = gather(files, label, args.source)
                cell, size = stat(per_item, rng)
                cells.append(cell)
                sizes.append(size)
            pretty = "referential" if state == "p_restricts" else "event"
            print(f"{name:<26}{split:<17}{pretty:<14}{max(sizes):>4}{auc:>10.3f}"
                  f"{cells[0]:>13}{cells[1]:>15}")
            name = ""
    print("\nEach edit pushes the item toward the opposite class mean. "
          "* = bootstrap interval over held-out families excludes zero.")


if __name__ == "__main__":
    main()
