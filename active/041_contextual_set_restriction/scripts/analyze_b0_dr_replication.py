"""B0: does the Davies & Richardson (2021) effect appear as LM window surprisal?

Their result, which is our denominator: main effects of referential relevance and of semantic
relevance on the noun-phrase window (both easing processing), no interaction, and only referential
relevance surviving into the wrap-up window.

Lower surprisal is the analogue of shorter reading time, so an easing effect is a NEGATIVE change in
surprisal. Contrasts are computed within item (each vignette contributes its own 2x2) and
bootstrapped over the 12 items.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def ci(values: np.ndarray, rng) -> tuple[float, float, float]:
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return float(values.mean()), float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, nargs="+", required=True)
    args = parser.parse_args()

    print(f"{'model':<22}{'window':<9}{'referential':>26}{'semantic':>26}{'interaction':>26}")
    for path in args.results:
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        metadata = rows[0]
        cells = defaultdict(dict)
        for row in rows[1:]:
            key = (row["semantic_relevance"], row["referential_relevance"])
            cells[row["item_id"]][key] = (row["np_surprisal"], row["wrapup_surprisal"])

        rng = np.random.default_rng(SEED)
        for window_index, window in enumerate(("np", "wrapup")):
            def cell(item, sem, ref):
                return cells[item][(sem, ref)][window_index]

            items = sorted(cells)
            # negative = the condition eases processing, matching shorter reading time
            referential = np.array([
                (cell(i, "plus_sem", "two_referents") + cell(i, "minus_sem", "two_referents")) / 2
                - (cell(i, "plus_sem", "one_referent") + cell(i, "minus_sem", "one_referent")) / 2
                for i in items])
            semantic = np.array([
                (cell(i, "plus_sem", "one_referent") + cell(i, "plus_sem", "two_referents")) / 2
                - (cell(i, "minus_sem", "one_referent") + cell(i, "minus_sem", "two_referents")) / 2
                for i in items])
            interaction = np.array([
                (cell(i, "plus_sem", "two_referents") - cell(i, "minus_sem", "two_referents"))
                - (cell(i, "plus_sem", "one_referent") - cell(i, "minus_sem", "one_referent"))
                for i in items])

            parts = []
            for values in (referential, semantic, interaction):
                mean, low, high = ci(values, rng)
                star = "*" if (low > 0) == (high > 0) else " "
                parts.append(f"{mean:+.3f} [{low:+.3f},{high:+.3f}]{star}")
            name = metadata["model_checkpoint"].split("/")[-1] if window == "np" else ""
            print(f"{name:<22}{window:<9}" + "".join(f"{p:>26}" for p in parts))
    print("\nsurprisal in nats/token; negative = eases processing; * = bootstrap interval "
          "excludes zero")


if __name__ == "__main__":
    main()
