"""Apply the frozen pass criteria to collected Z-causal norming ratings.

Input: a CSV with columns `participant_id`, `trial_id`, `rating` (1-7). `trial_id` is the id
emitted by `norming/build_z_causal_norm.py`, i.e. `<item>__<E_plus|E_minus>__<P|Z>`.

Frozen criteria. Per family, on item means:

    P(E+) > Z(E+)      the intended reason wins when the event is the one P bears on
    Z(E-) > P(E-)      the intended reason wins when the event is the one Z bears on
    P(E+) > P(E-)      P's explanatory force is event-dependent
    Z(E-) > Z(E+)      Z's explanatory force is event-dependent

A family passes only if all four hold. Across the set, the two crossing contrasts must also hold
by participant with bootstrap intervals excluding zero (5,000 resamples over participants), matching
the interval convention used elsewhere in 041.

Families that fail have their Z revised and are re-normed. This happens BEFORE the panel is opened
and is never informed by any model's behaviour.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

CELLS = [("E_plus", "P"), ("E_plus", "Z"), ("E_minus", "P"), ("E_minus", "Z")]
BOOTSTRAP = 5000
SEED = 20260904


def bootstrap_ci(values: np.ndarray, rng: np.random.Generator) -> tuple[float, float, float]:
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return float(values.mean()), float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ratings", type=Path, required=True)
    args = parser.parse_args()

    by_cell = defaultdict(list)              # (item, event, reason) -> ratings
    by_participant = defaultdict(dict)       # participant -> (item, event, reason) -> rating
    with args.ratings.open() as handle:
        for record in csv.DictReader(handle):
            item, event, reason = record["trial_id"].split("__")
            rating = float(record["rating"])
            by_cell[(item, event, reason)].append(rating)
            by_participant[record["participant_id"]][(item, event, reason)] = rating

    items = sorted({key[0] for key in by_cell})
    print(f"{len(items)} families, {len(by_participant)} participants\n")

    print(f"{'family':<12}{'P(E+)':>8}{'Z(E+)':>8}{'P(E-)':>8}{'Z(E-)':>8}   verdict")
    failures = []
    for item in items:
        means = {}
        for event, reason in CELLS:
            values = by_cell.get((item, event, reason), [])
            means[(event, reason)] = float(np.mean(values)) if values else float("nan")
        checks = {
            "P(E+)>Z(E+)": means[("E_plus", "P")] > means[("E_plus", "Z")],
            "Z(E-)>P(E-)": means[("E_minus", "Z")] > means[("E_minus", "P")],
            "P(E+)>P(E-)": means[("E_plus", "P")] > means[("E_minus", "P")],
            "Z(E-)>Z(E+)": means[("E_minus", "Z")] > means[("E_plus", "Z")],
        }
        passed = all(checks.values())
        if not passed:
            failures.append((item, [name for name, ok in checks.items() if not ok]))
        print(f"{item:<12}{means[('E_plus','P')]:>8.2f}{means[('E_plus','Z')]:>8.2f}"
              f"{means[('E_minus','P')]:>8.2f}{means[('E_minus','Z')]:>8.2f}   "
              f"{'PASS' if passed else 'FAIL'}")

    rng = np.random.default_rng(SEED)
    print()
    for label, positive, negative in (
            ("P(E+) - Z(E+)", ("E_plus", "P"), ("E_plus", "Z")),
            ("Z(E-) - P(E-)", ("E_minus", "Z"), ("E_minus", "P"))):
        # Under the Latin square a participant sees each family in only one condition, so the
        # paired unit is the participant's mean per condition (3 families each), not the item.
        per_participant = []
        for ratings in by_participant.values():
            hits = [v for key, v in ratings.items() if key[1:] == positive]
            misses = [v for key, v in ratings.items() if key[1:] == negative]
            if hits and misses:
                per_participant.append(float(np.mean(hits) - np.mean(misses)))
        if per_participant:
            mean, low, high = bootstrap_ci(np.array(per_participant), rng)
            verdict = "excludes zero" if low > 0 else "DOES NOT exclude zero"
            print(f"by participant  {label}: {mean:+.2f} [{low:+.2f}, {high:+.2f}]  {verdict}")

    print()
    if failures:
        print("REVISE Z AND RE-NORM before opening the panel:")
        for item, broken in failures:
            print(f"  {item}: {', '.join(broken)}")
    else:
        print("all families pass; the Z half of the E manipulation is human-normed")


if __name__ == "__main__":
    main()
