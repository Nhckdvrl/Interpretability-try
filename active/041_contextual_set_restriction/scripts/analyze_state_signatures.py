"""Do the two states at the same modifier token have different downstream signatures?

C4 edits the referential-role state; C6 edits the event-relevance state. Both are estimated at the
same token, with the same estimator, held out over the same property families, and both are read out
on the same quantity: support for a fixed explanation continuation, for the true property and for
its contrasting value.

If a single undifferentiated relevance signal drove the explanation, the two edits would produce the
same signature. The question is whether they do.

Statistic is role minus shuffled, the S3 convention, averaged over **every** depth whose held-out
AUC is at least 0.6. Below that threshold the estimate is not a direction and editing there only
measures how fragile a layer is. Averaging rather than picking the AUC peak is deliberate: the peak
is a bad selector, and demonstrably so. In Mistral the event-relevance probe peaks at layer 10, the
one depth at which that state does nothing, while layers 20-30 carry the effect; the referential
probe saturates at 1.000 in the same model, which makes its argmax arbitrary. The threshold and the
averaging are fixed in advance and applied identically to both states and all families, so nothing
here is selected on the outcome.
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


def cell(rows, layers, label, alpha, rng):
    per_item = defaultdict(list)
    for row in rows:
        if row["continuation_label"] != label:
            continue
        for layer in layers:
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


def usable_depths(meta):
    usable = {int(k): v for k, v in meta["layers"].items() if v >= MIN_AUC}
    return sorted(usable), usable


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

    print(f"role minus shuffled, alpha {args.alpha}, held-out families, averaged over every "
          f"depth with held-out AUC >= {MIN_AUC}\n")
    print(f"{'model':<26}{'state edited':<14}{'depths':>10}"
          f"{'dES true property':>20}{'dES contrasting':>18}")
    for model, kinds in by_model.items():
        name = model.split("/")[-1]
        for kind in ("referential", "event"):
            if kind not in kinds:
                print(f"{name:<26}{kind:<14}{'--':>10}{'not run':>20}{'':>18}")
                continue
            rows = kinds[kind]
            meta = rows[0]
            selector = "p_restricts" if kind == "referential" else "p_relevant_to_event"
            held = [r for r in rows[1:] if r["held_out"] and r[selector]]
            layers, aucs = usable_depths(meta)
            rng = np.random.default_rng(SEED)
            if not layers:
                print(f"{name:<26}{kind:<14}{'--':>10}{'no usable depth':>20}{'':>18}")
                continue
            span = f"{len(layers)}/{len(meta['layers'])}"
            print(f"{name:<26}{kind:<14}{span:>10}"
                  f"{cell(held, layers, 'p', args.alpha, rng):>20}"
                  f"{cell(held, layers, 'p_contrast', args.alpha, rng):>18}")
            name = ""
    print("\nEach edit pushes the item toward the opposite class mean, so a negative true-property "
          "cell means the state was supporting that explanation.\n"
          "* = bootstrap interval over held-out items excludes zero.")


if __name__ == "__main__":
    main()
