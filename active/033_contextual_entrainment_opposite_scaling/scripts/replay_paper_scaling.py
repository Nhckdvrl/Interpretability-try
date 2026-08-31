#!/usr/bin/env python3
"""Replay the Pythia power-law signs from the paper's published raw table."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


PARAMETERS = [410e6, 1e9, 1.4e9, 2.8e9, 6.9e9, 12e9]
DISTRACTOR_DELTA = {
    "Related": [4.78, 4.30, 4.27, 4.21, 3.40, 3.69],
    "Irrelevant": [2.09, 2.34, 2.37, 2.59, 2.69, 2.72],
    "Random": [1.68, 1.66, 1.91, 2.25, 2.36, 2.78],
    "Counterfactual": [4.85, 3.91, 3.63, 2.93, 2.34, 2.06],
}
PAPER_EXPONENT = {
    "Related": -0.089,
    "Irrelevant": 0.078,
    "Random": 0.156,
    "Counterfactual": -0.258,
}


def log_log_fit(x_values: list[float], y_values: list[float]) -> tuple[float, float]:
    x = [math.log(value) for value in x_values]
    y = [math.log(value) for value in y_values]
    x_mean = sum(x) / len(x)
    y_mean = sum(y) / len(y)
    ss_x = sum((value - x_mean) ** 2 for value in x)
    slope = sum((left - x_mean) * (right - y_mean) for left, right in zip(x, y)) / ss_x
    intercept = y_mean - slope * x_mean
    predicted = [intercept + slope * value for value in x]
    ss_res = sum((actual - estimate) ** 2 for actual, estimate in zip(y, predicted))
    ss_tot = sum((actual - y_mean) ** 2 for actual in y)
    return slope, 1.0 - ss_res / ss_tot


def replay() -> dict:
    conditions = {}
    for condition, values in DISTRACTOR_DELTA.items():
        exponent, r_squared = log_log_fit(PARAMETERS, values)
        conditions[condition] = {
            "published_raw_delta": values,
            "replayed_exponent": exponent,
            "replayed_r_squared": r_squared,
            "paper_exponent": PAPER_EXPONENT[condition],
            "absolute_exponent_difference": abs(exponent - PAPER_EXPONENT[condition]),
        }
    return {
        "schema_version": 1,
        "source": "Kukreja et al., Findings ACL 2026, Table 5",
        "model_parameters": PARAMETERS,
        "conditions": conditions,
        "semantic_negative": all(conditions[name]["replayed_exponent"] < 0 for name in ("Related", "Counterfactual")),
        "nonsemantic_positive": all(conditions[name]["replayed_exponent"] > 0 for name in ("Irrelevant", "Random")),
        "scope": "aggregate table replay; not item-level V0",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = replay()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
