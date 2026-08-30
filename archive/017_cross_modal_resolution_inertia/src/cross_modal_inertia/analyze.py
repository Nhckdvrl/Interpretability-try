"""Cluster-bootstrap analysis for the preregistered correction-failure gate."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .io import read_jsonl


CONDITIONS = (
    "text_first_actual_label", "text_first_actual_ordinal", "text_first_masked",
    "matched_history", "image_first",
)


def interval(values: np.ndarray) -> dict:
    return {
        "estimate": float(values[0]),
        "ci_low": float(np.quantile(values[1:], 0.025)),
        "ci_high": float(np.quantile(values[1:], 0.975)),
    }


def cluster_bootstrap(rows: list[dict], value, replicates: int, seed: int) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["pair_id"]].append(row)
    clusters = sorted(grouped)
    observed = float(np.mean([value(row) for row in rows]))
    rng = np.random.default_rng(seed)
    samples = np.empty(replicates + 1)
    samples[0] = observed
    for index in range(1, replicates + 1):
        drawn = rng.choice(clusters, len(clusters), replace=True)
        vals = [value(row) for cluster in drawn for row in grouped[cluster]]
        samples[index] = np.mean(vals)
    result = interval(samples)
    result["n_item_orders"] = len(rows)
    result["n_pair_clusters"] = len(clusters)
    return result


def gated_rows(raw: list[dict]) -> tuple[list[dict], dict]:
    keyed = {(row["item_id"], row["order"], row["condition"]): row for row in raw}
    item_orders = sorted({(row["item_id"], row["order"]) for row in raw})
    output = []
    missing = []
    for item_id, order in item_orders:
        try:
            records = {condition: keyed[item_id, order, condition]
                       for condition in ("text_only", "simultaneous", *CONDITIONS)}
        except KeyError as exc:
            missing.append(str(exc))
            continue
        initial, simultaneous = records["text_only"], records["simultaneous"]
        if initial["pred_letter"] != initial["gold_letter"] and simultaneous["pred_letter"] == simultaneous["gold_letter"]:
            output.append({
                "item_id": item_id,
                "order": order,
                "pair_id": initial["pair_id"],
                "language": initial["language"],
                "initial_letter": initial["pred_letter"],
                "records": records,
            })
    audit = {"complete_item_orders": len(item_orders) - len(missing), "missing": missing,
             "gated_item_orders": len(output)}
    return output, audit


def analyze_family(raw: list[dict], replicates: int = 10000, seed: int = 20260830) -> dict:
    gate, audit = gated_rows(raw)
    condition_rows: dict[str, list[dict]] = defaultdict(list)
    for row in raw:
        condition_rows[row["condition"]].append(row)
    result = {
        "gate": audit,
        "gated_pair_clusters": len({row["pair_id"] for row in gate}),
        "gated_languages": dict(sorted(Counter(str(row["language"]) for row in gate).items())),
        "gated_orders": dict(sorted(Counter(row["order"] for row in gate).items())),
        "all_item_order_accuracy": {
            condition: float(np.mean([row["pred_letter"] == row["gold_letter"] for row in rows]))
            for condition, rows in sorted(condition_rows.items())
        },
        "conditions": {},
        "language_descriptives": {},
    }
    if not gate:
        result["promotion"] = False
        result["promotion_reasons"] = ["empty correction-failure gate"]
        return result
    for offset, condition in enumerate(CONDITIONS):
        result["conditions"][condition] = {
            "persistence": cluster_bootstrap(
                gate,
                lambda row, c=condition: float(row["records"][c]["pred_letter"] == row["initial_letter"]),
                replicates, seed + offset,
            ),
            "gold_probability_drop_from_simultaneous": cluster_bootstrap(
                gate,
                lambda row, c=condition: row["records"]["simultaneous"]["prob_gold"] - row["records"][c]["prob_gold"],
                replicates, seed + 20 + offset,
            ),
        }
    for language in sorted({str(row["language"]) for row in gate}):
        subset = [row for row in gate if str(row["language"]) == language]
        result["language_descriptives"][language] = {
            "n_item_orders": len(subset),
            "actual_persistence": float(np.mean([
                row["records"]["text_first_actual_label"]["pred_letter"] == row["initial_letter"]
                for row in subset
            ])),
            "ordinal_persistence": float(np.mean([
                row["records"]["text_first_actual_ordinal"]["pred_letter"] == row["initial_letter"]
                for row in subset
            ])),
            "masked_persistence": float(np.mean([
                row["records"]["text_first_masked"]["pred_letter"] == row["initial_letter"]
                for row in subset
            ])),
        }
    for name, left, right, offset in (
        ("actual_minus_matched_persistence", "text_first_actual_label", "matched_history", 40),
        ("ordinal_minus_matched_persistence", "text_first_actual_ordinal", "matched_history", 41),
        ("masked_minus_matched_persistence", "text_first_masked", "matched_history", 42),
        ("actual_minus_masked_persistence", "text_first_actual_label", "text_first_masked", 43),
        ("ordinal_minus_masked_persistence", "text_first_actual_ordinal", "text_first_masked", 44),
    ):
        result[name] = cluster_bootstrap(
            gate,
            lambda row, a=left, b=right: float(row["records"][a]["pred_letter"] == row["initial_letter"])
            - float(row["records"][b]["pred_letter"] == row["initial_letter"]),
            replicates, seed + offset,
        )
    actual_diff = result["actual_minus_matched_persistence"]
    ordinal_diff = result["ordinal_minus_matched_persistence"]
    ordinal_masked_diff = result["ordinal_minus_masked_persistence"]
    prob_drop = result["conditions"]["text_first_actual_label"]["gold_probability_drop_from_simultaneous"]
    checks = {
        "minimum_gated_item_orders": len(gate) >= 50,
        "minimum_gated_pair_clusters": result["gated_pair_clusters"] >= 25,
        "actual_minus_matched_at_least_10pp": actual_diff["estimate"] >= 0.10,
        "actual_minus_matched_ci_positive": actual_diff["ci_low"] > 0,
        "ordinal_minus_matched_ci_positive": ordinal_diff["ci_low"] > 0,
        "ordinal_minus_masked_ci_positive": ordinal_masked_diff["ci_low"] > 0,
        "actual_gold_probability_drop_ci_positive": prob_drop["ci_low"] > 0,
    }
    result["promotion_checks"] = checks
    result["promotion"] = all(checks.values())
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--output", required=True)
    ap.add_argument("--replicates", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20260830)
    args = ap.parse_args()
    families = {}
    for path in args.inputs:
        raw = read_jsonl(path)
        metadata_path = Path(path).with_suffix(".metadata.json")
        metadata = json.loads(metadata_path.read_text())
        family = metadata["family"]
        families[family] = {"metadata": metadata, "analysis": analyze_family(
            raw, args.replicates, args.seed + len(families) * 100,
        )}
    promoted = [family for family, value in families.items() if value["analysis"]["promotion"]]
    report = {
        "contract_id": "017-d0-v1",
        "families": families,
        "promoted_families": promoted,
        "overall_promotion": len(promoted) >= 2,
        "overall_decision": "PROMOTE" if len(promoted) >= 2 else "NO-PROMOTE",
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
