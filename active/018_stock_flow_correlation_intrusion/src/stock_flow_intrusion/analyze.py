"""Recognition-gated, dam-clustered analysis of inflow attraction."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .io import read_jsonl


CONDITIONS = ("direct", "actual_net_history", "explicit_correct_net",
              "masked_net_history", "formula_reminder")


def json_safe(value):
    """Replace non-finite floats with JSON null, recursively."""
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def aggregate(rows: list[dict]) -> tuple[list[dict], dict]:
    net = defaultdict(list)
    stock = defaultdict(list)
    for row in rows:
        if row["condition"] == "net_recognition":
            net[row["item_id"]].append(row)
        else:
            stock[row["item_id"], row["condition"]].append(row)
    item_ids = sorted(net)
    gated = {item_id for item_id in item_ids
             if len(net[item_id]) == 4 and all(row["correct"] for row in net[item_id])}
    output = []
    for item_id in sorted(gated):
        for condition in CONDITIONS:
            local = stock[item_id, condition]
            if len(local) != 4:
                raise ValueError(f"expected four stock presentations: {item_id}/{condition}")
            first = local[0]
            output.append({
                "item_id": item_id, "dam_id": first["dam_id"], "cell": first["cell"],
                "congruence": first["congruence"], "net_direction": first["net_direction"],
                "inflow_trend_direction": first["inflow_trend_direction"], "condition": condition,
                "prob_stock_up": float(np.mean([row["prob_stock_up"] for row in local])),
                "accuracy": float(np.mean([row["correct"] for row in local])),
                "column_prob_stock_up": {
                    order: float(np.mean([row["prob_stock_up"] for row in local if row["column_order"] == order]))
                    for order in ("inflow_first", "outflow_first")
                },
            })
    audit = {
        "total_items": len(item_ids), "gated_items": len(gated),
        "gate_rate": len(gated) / len(item_ids) if item_ids else 0,
        "gated_cells": dict(sorted(Counter(next(row for row in net[item] if True)["cell"] for item in gated).items())),
        "gated_dams": len({net[item][0]["dam_id"] for item in gated}),
    }
    return output, audit


def attraction(rows: list[dict], probability_key: str = "prob_stock_up") -> float:
    estimates = []
    for net_direction in ("positive", "negative"):
        up = [row[probability_key] for row in rows
              if row["net_direction"] == net_direction and row["inflow_trend_direction"] == "up"]
        down = [row[probability_key] for row in rows
                if row["net_direction"] == net_direction and row["inflow_trend_direction"] == "down"]
        if not up or not down:
            return float("nan")
        estimates.append(float(np.mean(up) - np.mean(down)))
    return float(np.mean(estimates))


def single_direction_attraction(rows: list[dict], probability_key: str = "prob_stock_up") -> float:
    up = [row[probability_key] for row in rows if row["inflow_trend_direction"] == "up"]
    down = [row[probability_key] for row in rows if row["inflow_trend_direction"] == "down"]
    if not up or not down:
        return float("nan")
    return float(np.mean(up) - np.mean(down))


def cluster_bootstrap(rows: list[dict], value, replicates: int, seed: int) -> dict:
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["dam_id"]].append(row)
    dams = sorted(grouped)
    if not rows or not dams:
        return {"estimate": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"),
                "n_dams": 0, "n_items": 0}
    samples = np.empty(replicates + 1)
    samples[0] = value(rows)
    if not np.isfinite(samples[0]):
        return {"estimate": float(samples[0]), "ci_low": float("nan"), "ci_high": float("nan"),
                "n_dams": len(dams), "n_items": len(rows)}
    rng = np.random.default_rng(seed)
    for index in range(1, replicates + 1):
        drawn = rng.choice(dams, len(dams), replace=True)
        sample = [row for dam in drawn for row in grouped[dam]]
        samples[index] = value(sample)
    finite = samples[np.isfinite(samples)]
    bootstrap_finite = finite[1:]
    return {"estimate": float(samples[0]),
            "ci_low": float(np.quantile(bootstrap_finite, .025)) if len(bootstrap_finite) else float("nan"),
            "ci_high": float(np.quantile(bootstrap_finite, .975)) if len(bootstrap_finite) else float("nan"),
            "n_dams": len(dams),
            "n_items": len(rows)}


def recognition_diagnostics(raw: list[dict]) -> dict:
    """Report Q1 accuracy by semantic cell and presentation factors."""
    rows = [row for row in raw if row["condition"] == "net_recognition"]
    output = {}
    for cell in sorted({row["cell"] for row in rows}):
        local = [row for row in rows if row["cell"] == cell]
        output[cell] = {
            "overall": float(np.mean([row["correct"] for row in local])),
            "presentations": {
                f"{column}__{option}": float(np.mean([
                    row["correct"] for row in local
                    if row["column_order"] == column and row["option_order"] == option
                ]))
                for column in ("inflow_first", "outflow_first")
                for option in ("canonical", "reversed")
            },
        }
    return output


def analyze_family(raw: list[dict], replicates: int, seed: int) -> dict:
    aggregated, gate = aggregate(raw)
    result = {
        "gate": gate,
        "recognition_diagnostics": recognition_diagnostics(raw),
        "conditions": {},
    }
    for offset, condition in enumerate(CONDITIONS):
        local = [row for row in aggregated if row["condition"] == condition]
        conflict = [row for row in local if row["congruence"] == "conflict"]
        aligned = [row for row in local if row["congruence"] == "aligned"]
        direction_effects = {}
        for net_direction in ("positive", "negative"):
            subset = [row for row in local if row["net_direction"] == net_direction]
            direction_effects[net_direction] = cluster_bootstrap(
                subset, single_direction_attraction, replicates,
                seed + offset * 20 + (net_direction == "negative"),
            )
        column_effects = {}
        for col_offset, column in enumerate(("inflow_first", "outflow_first")):
            projected = [{**row, "column_value": row["column_prob_stock_up"][column]} for row in local]
            column_effects[column] = cluster_bootstrap(
                projected, lambda rows: attraction(rows, "column_value"),
                replicates, seed + offset * 20 + 5 + col_offset,
            )
        result["conditions"][condition] = {
            "accuracy_aligned": float(np.mean([row["accuracy"] for row in aligned])),
            "accuracy_conflict": float(np.mean([row["accuracy"] for row in conflict])),
            "inflow_attraction": cluster_bootstrap(
                local, attraction, replicates, seed + offset * 20 + 10,
            ),
            "direction_effects": direction_effects,
            "column_order_effects": column_effects,
        }
    actual = result["conditions"]["actual_net_history"]
    explicit = result["conditions"]["explicit_correct_net"]
    cells_ok = all(count >= 50 for count in gate["gated_cells"].values()) and len(gate["gated_cells"]) == 4
    directions_ok = all(value["estimate"] > 0 for value in actual["direction_effects"].values())
    columns_ok = all(value["estimate"] > 0 for value in actual["column_order_effects"].values())
    checks = {
        "minimum_gated_items_per_cell": cells_ok,
        "minimum_gated_dams": gate["gated_dams"] >= 50,
        "actual_attraction_at_least_5pp": actual["inflow_attraction"]["estimate"] >= .05,
        "actual_attraction_ci_positive": actual["inflow_attraction"]["ci_low"] > 0,
        "explicit_correct_net_ci_positive": explicit["inflow_attraction"]["ci_low"] > 0,
        "both_net_directions_positive": directions_ok,
        "both_column_orders_positive": columns_ok,
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
    for index, path in enumerate(args.inputs):
        metadata = json.loads(Path(path).with_suffix(".metadata.json").read_text())
        family = metadata["family"]
        families[family] = {"metadata": metadata, "analysis": analyze_family(
            read_jsonl(path), args.replicates, args.seed + index * 1000,
        )}
    promoted = [family for family, value in families.items() if value["analysis"]["promotion"]]
    report = {"contract_id": "018-d0-v1", "families": families,
              "promoted_families": promoted, "overall_promotion": len(promoted) >= 2,
              "overall_decision": "PROMOTE-TO-SECOND-SOURCE" if len(promoted) >= 2 else "NO-PROMOTE"}
    safe_report = json_safe(report)
    serialized = json.dumps(safe_report, indent=2, allow_nan=False)
    Path(args.output).write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
