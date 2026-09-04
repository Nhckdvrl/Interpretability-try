"""Do the two states at the same modifier token have different downstream signatures?

C4 edits the referential-role state; C6 edits the event-relevance state. Both are estimated at the
same token, with the same estimator, held out over the same property families, and both are read out
on the same quantity: support for a fixed explanation continuation, for the true property and for
its contrasting value.

If a single undifferentiated relevance signal drove the explanation, the two edits would produce the
same signature. The question is whether they do.

Statistic is role minus shuffled, the S3 convention. The site for each state is the depth where that
state's own held-out probe peaks among depths whose AUC is above 0.6 -- below that the direction is
not a direction, and editing there only measures how fragile the layer is.
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


def cell(rows, layer, label, alpha, rng):
    per_item = defaultdict(list)
    for row in rows:
        if row["continuation_label"] != label:
            continue
        role = row["scores"].get(f"L{layer}|role|a{alpha}")
        shuffled = row["scores"].get(f"L{layer}|shuffled|a{alpha}")
        if role is None or shuffled is None:
            continue
        per_item[row["item_id"]].append(role - shuffled)
    values = np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])
    if values.size == 0:
        return "     --     "
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    low, high = float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))
    return f"{values.mean():+.4f}{'*' if (low > 0) == (high > 0) else ' '}"


def site(meta):
    usable = {int(k): v for k, v in meta["layers"].items() if v >= MIN_AUC}
    if not usable:
        return None, None
    layer = max(usable, key=usable.get)
    return layer, usable[layer]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--referential", type=Path, nargs="+", required=True)
    parser.add_argument("--event", type=Path, nargs="+", required=True)
    parser.add_argument("--alpha", default="4")
    args = parser.parse_args()

    by_model = defaultdict(dict)
    for kind, paths in (("referential", args.referential), ("event", args.event)):
        for path in paths:
            rows = [json.loads(line) for line in path.read_text().splitlines() if line]
            by_model[rows[0]["model_checkpoint"]][kind] = rows

    print(f"role minus shuffled, alpha {args.alpha}, held-out families, at each state's own "
          f"probe peak among depths with AUC >= {MIN_AUC}\n")
    print(f"{'model':<26}{'state edited':<14}{'site':>6}{'AUC':>7}"
          f"{'dES true property':>20}{'dES contrasting':>18}")
    for model, kinds in by_model.items():
        name = model.split("/")[-1]
        for kind in ("referential", "event"):
            if kind not in kinds:
                print(f"{name:<26}{kind:<14}{'--':>6}{'--':>7}{'not run':>20}{'':>18}")
                continue
            rows = kinds[kind]
            meta = rows[0]
            selector = "p_restricts" if kind == "referential" else "p_relevant_to_event"
            held = [r for r in rows[1:] if r["held_out"] and r[selector]]
            layer, auc = site(meta)
            rng = np.random.default_rng(SEED)
            if layer is None:
                print(f"{name:<26}{kind:<14}{'--':>6}{'--':>7}{'no usable depth':>20}{'':>18}")
                continue
            print(f"{name:<26}{kind:<14}{layer:>6}{auc:>7.3f}"
                  f"{cell(held, layer, 'p', args.alpha, rng):>20}"
                  f"{cell(held, layer, 'p_contrast', args.alpha, rng):>18}")
            name = ""
    print("\nEach edit pushes the item toward the opposite class mean, so a negative true-property "
          "cell means the state was supporting that explanation.\n"
          "* = bootstrap interval over held-out items excludes zero.")


if __name__ == "__main__":
    main()
