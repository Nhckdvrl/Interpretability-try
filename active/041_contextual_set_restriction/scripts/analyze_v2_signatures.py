"""The two-state signature table on 48 families: depth chosen on train, effect reported on test.

Three ways to pick the depth at which to report an intervention, and only one of them is sound:

  probe-AUC peak      -- arbitrary when AUC saturates, and demonstrably wrong: Mistral's
                         event-relevance probe peaks at a depth where that state does nothing.
  average over depths -- non-circular but dilutes, and the effect is sharply localised, so averaging
                         over seven depths of which one is active buries it.
  select on train     -- pick the depth where the causal effect is largest on the TRAINING families,
                         then report it on the held-out families. Non-circular, and it does not
                         dilute. This is what the table below does.

Complementary folds are pooled, so every family appears in a test set exactly once. The
`extended_to_core` split is separate: it estimates the direction entirely on the 36 authored
families and tests on the 12 inherited from Davies & Richardson, a transfer rather than a split.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def per_family(rows, selector, label, layer, source, held):
    out = defaultdict(list)
    for row in rows:
        if row["held_out"] != held or not row[selector]:
            continue
        if row["continuation_label"] != label:
            continue
        if source != "all" and row.get("source") != source:
            continue
        role = row["scores"].get(f"L{layer}|role|a4")
        shuffled = row["scores"].get(f"L{layer}|shuffled|a4")
        if role is not None and shuffled is not None:
            out[row["item_id"]].append(role - shuffled)
    return out


def mean_of(per_item):
    if not per_item:
        return float("nan")
    return float(np.mean([np.mean(v) for v in per_item.values()]))


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
        grouped[(meta["model_checkpoint"], split, meta["label"])].append((meta, rows[1:]))

    print(f"role minus shuffled at alpha 4; depth selected on TRAINING families by the size of the "
          f"contrasting-property effect, reported on held-out families. source={args.source}\n")
    print(f"{'model':<26}{'split':<18}{'state':<13}{'N':>4}{'depths':>18}"
          f"{'dES true':>13}{'dES contrast':>15}")
    for key in sorted(grouped):
        model, split, state = key
        chosen, test_true, test_contrast = [], defaultdict(list), defaultdict(list)
        for meta, rows in grouped[key]:
            selector = meta["label"]
            layers = sorted(int(k) for k in meta["layers"])
            scores = {}
            for layer in layers:
                train = per_family(rows, selector, "p_contrast", layer, "all", held=False)
                scores[layer] = abs(mean_of(train)) if train else -1.0
            best = max(layers, key=lambda layer: scores[layer])
            chosen.append(f"{best}/{max(layers)}")
            for label, store in (("p", test_true), ("p_contrast", test_contrast)):
                for item, values in per_family(rows, selector, label, best, args.source,
                                               held=True).items():
                    store[item].extend(values)
        rng = np.random.default_rng(SEED)
        cell_true, n_true = stat(test_true, rng)
        cell_contrast, n_contrast = stat(test_contrast, rng)
        pretty = "referential" if state == "p_restricts" else "event"
        print(f"{model.split('/')[-1]:<26}{split:<18}{pretty:<13}"
              f"{max(n_true, n_contrast):>4}{','.join(chosen):>18}"
              f"{cell_true:>13}{cell_contrast:>15}")
    print("\nDepth is chosen without ever looking at held-out families. "
          "* = bootstrap interval over held-out families excludes zero.")


if __name__ == "__main__":
    main()
