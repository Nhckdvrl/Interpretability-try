"""Analyze D0-v2 using semantic, position-free net recognition."""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from .analyze import (
    CONDITIONS,
    attraction,
    cluster_bootstrap,
    json_safe,
    single_direction_attraction,
)
from .io import read_jsonl
from .run_model_v2 import CONTRACT_ID


def mean_or_nan(values: list[float]) -> float:
    """Return an explicit missing value for an empty diagnostic stratum."""
    return float(np.mean(values)) if values else float("nan")


def aggregate_v2(rows: list[dict]) -> tuple[list[dict], dict]:
    net = defaultdict(list)
    stock = defaultdict(list)
    for row in rows:
        if row["condition"] == "net_recognition_v2":
            net[row["item_id"]].append(row)
        else:
            stock[row["item_id"], row["condition"]].append(row)

    item_ids = sorted(net)
    decisions = {}
    for item_id in item_ids:
        local = net[item_id]
        if len(local) != 2 or {row["column_order"] for row in local} != {
            "inflow_first", "outflow_first"
        }:
            raise ValueError(f"expected two column-order recognition rows: {item_id}")
        mean_positive = float(np.mean([row["prob_positive"] for row in local]))
        decisions[item_id] = {
            "mean_positive": mean_positive,
            "predicted": "positive" if mean_positive >= 0.5 else "negative",
            "gold": local[0]["gold_label"],
        }
    gated = {item_id for item_id, value in decisions.items()
             if value["predicted"] == value["gold"]}

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
                "recognition_mean_prob_positive": decisions[item_id]["mean_positive"],
                "prob_stock_up": float(np.mean([row["prob_stock_up"] for row in local])),
                "accuracy": float(np.mean([row["correct"] for row in local])),
                "column_prob_stock_up": {
                    order: float(np.mean([
                        row["prob_stock_up"] for row in local if row["column_order"] == order
                    ]))
                    for order in ("inflow_first", "outflow_first")
                },
            })

    gated_cells = Counter(net[item_id][0]["cell"] for item_id in gated)
    diagnostics = {}
    for cell in sorted({row["cell"] for local in net.values() for row in local}):
        cell_rows = [row for local in net.values() for row in local if row["cell"] == cell]
        cell_items = [item_id for item_id in item_ids if net[item_id][0]["cell"] == cell]
        diagnostics[cell] = {
            "item_gate_accuracy": float(np.mean([item_id in gated for item_id in cell_items])),
            "mean_gold_probability": float(np.mean([
                row["prob_positive"] if row["gold_label"] == "positive" else row["prob_negative"]
                for row in cell_rows
            ])),
            "column_accuracy": {
                order: float(np.mean([
                    row["correct"] for row in cell_rows if row["column_order"] == order
                ]))
                for order in ("inflow_first", "outflow_first")
            },
        }
    audit = {
        "total_items": len(item_ids), "gated_items": len(gated),
        "gate_rate": len(gated) / len(item_ids) if item_ids else 0,
        "gated_cells": dict(sorted(gated_cells.items())),
        "gated_dams": len({net[item_id][0]["dam_id"] for item_id in gated}),
        "recognition_diagnostics": diagnostics,
    }
    return output, audit


def analyze_family_v2(raw: list[dict], replicates: int, seed: int) -> dict:
    aggregated, gate = aggregate_v2(raw)
    result = {"gate": gate, "conditions": {}}
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
            projected = [{**row, "column_value": row["column_prob_stock_up"][column]}
                         for row in local]
            column_effects[column] = cluster_bootstrap(
                projected, lambda values: attraction(values, "column_value"),
                replicates, seed + offset * 20 + 5 + col_offset,
            )
        result["conditions"][condition] = {
            "accuracy_aligned": mean_or_nan([row["accuracy"] for row in aligned]),
            "accuracy_conflict": mean_or_nan([row["accuracy"] for row in conflict]),
            "inflow_attraction": cluster_bootstrap(
                local, attraction, replicates, seed + offset * 20 + 10,
            ),
            "direction_effects": direction_effects,
            "column_order_effects": column_effects,
        }

    actual = result["conditions"]["actual_net_history"]
    explicit = result["conditions"]["explicit_correct_net"]
    cells_ok = len(gate["gated_cells"]) == 4 and all(
        count >= 50 for count in gate["gated_cells"].values()
    )
    checks = {
        "minimum_gated_items_per_cell": cells_ok,
        "minimum_gated_dams": gate["gated_dams"] >= 50,
        "actual_attraction_at_least_5pp": actual["inflow_attraction"]["estimate"] >= 0.05,
        "actual_attraction_ci_positive": actual["inflow_attraction"]["ci_low"] > 0,
        "explicit_correct_net_ci_positive": explicit["inflow_attraction"]["ci_low"] > 0,
        "both_net_directions_positive": all(
            value["estimate"] > 0 for value in actual["direction_effects"].values()
        ),
        "both_column_orders_positive": all(
            value["estimate"] > 0 for value in actual["column_order_effects"].values()
        ),
    }
    result["promotion_checks"] = checks
    result["promotion"] = all(checks.values())
    return result


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("--output", required=True)
    ap.add_argument("--replicates", type=int, default=10000)
    ap.add_argument("--seed", type=int, default=20260831)
    args = ap.parse_args()

    families = {}
    for index, path in enumerate(args.inputs):
        metadata = json.loads(Path(path).with_suffix(".metadata.json").read_text())
        if metadata["contract_id"] != CONTRACT_ID:
            raise ValueError(f"wrong contract for {path}: {metadata['contract_id']}")
        family = metadata["family"]
        families[family] = {
            "metadata": metadata,
            "analysis": analyze_family_v2(
                read_jsonl(path), args.replicates, args.seed + index * 1000,
            ),
        }
    promoted = [family for family, value in families.items() if value["analysis"]["promotion"]]
    report = {
        "contract_id": CONTRACT_ID, "families": families,
        "promoted_families": promoted, "overall_promotion": len(promoted) >= 2,
        "overall_decision": "PROMOTE-TO-SECOND-SOURCE" if len(promoted) >= 2 else "NO-PROMOTE",
    }
    serialized = json.dumps(json_safe(report), indent=2, allow_nan=False)
    Path(args.output).write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
