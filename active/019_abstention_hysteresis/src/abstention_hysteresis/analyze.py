"""Recognition-gated paired analysis of abstention hysteresis."""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from pathlib import Path

import numpy as np

from .io import read_jsonl


FINAL_CONDITIONS = (
    "direct_full",
    "self_abstention",
    "teacher_abstention",
    "paraphrased_abstention",
    "neutral_same_context",
    "answered_history",
)


def json_safe(value):
    if isinstance(value, float) and not math.isfinite(value):
        return None
    if isinstance(value, dict):
        return {key: json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_safe(item) for item in value]
    return value


def gated_items(rows: list[dict]) -> set[str]:
    lookup = {(row["item_id"], row["condition"]): row for row in rows}
    item_ids = {row["item_id"] for row in rows}
    return {
        item_id for item_id in item_ids
        if lookup.get((item_id, "capability_full"), {}).get("correct", False)
        and lookup.get((item_id, "initial_missing"), {}).get("is_abstention", False)
    }


def paired_records(rows: list[dict], gate: set[str], condition: str,
                   source: str | None = None) -> list[dict]:
    lookup = {(row["item_id"], row["condition"]): row for row in rows}
    output = []
    for item_id in sorted(gate):
        direct = lookup[item_id, "direct_full"]
        target = lookup.get((item_id, condition))
        if target is None or (source is not None and direct["source"] != source):
            continue
        output.append({
            "item_id": item_id,
            "source": direct["source"],
            "abstention_delta": float(target["is_abstention"]) - float(direct["is_abstention"]),
            "probability_delta": target["prob_abstain_mode"] - direct["prob_abstain_mode"],
            "correct_delta": float(target["correct"]) - float(direct["correct"]),
            "target_abstention": float(target["is_abstention"]),
            "direct_abstention": float(direct["is_abstention"]),
            "target_correct": float(target["correct"]),
            "direct_correct": float(direct["correct"]),
        })
    return output


def bootstrap_mean(records: list[dict], key: str, replicates: int, seed: int) -> dict:
    if not records:
        return {"estimate": float("nan"), "ci_low": float("nan"), "ci_high": float("nan"),
                "n_items": 0}
    values = np.asarray([row[key] for row in records], dtype=float)
    rng = np.random.default_rng(seed)
    indices = rng.integers(0, len(values), size=(replicates, len(values)))
    samples = values[indices].mean(axis=1)
    return {
        "estimate": float(values.mean()),
        "ci_low": float(np.quantile(samples, .025)),
        "ci_high": float(np.quantile(samples, .975)),
        "n_items": len(values),
    }


def analyze_family(rows: list[dict], replicates: int, seed: int) -> dict:
    gate = gated_items(rows)
    base_rows = [row for row in rows if row["item_id"] in gate]
    sources = sorted({row["source"] for row in rows})
    gate_counts = Counter(row["source"] for row in base_rows if row["condition"] == "capability_full")
    total_counts = Counter(row["source"] for row in rows if row["condition"] == "capability_full")
    result = {
        "gate": {
            "total_items": sum(total_counts.values()),
            "gated_items": len(gate),
            "gate_rate": len(gate) / sum(total_counts.values()) if total_counts else 0.0,
            "total_by_source": dict(sorted(total_counts.items())),
            "gated_by_source": dict(sorted(gate_counts.items())),
        },
        "protocol_audit": {},
        "conditions": {},
    }
    for condition in sorted({row["condition"] for row in rows}):
        local = [row for row in rows if row["condition"] == condition]
        prefixes = Counter(
            "answer" if row["response"].lstrip().casefold().startswith("answer")
            else "abstain" if row["response"].lstrip().casefold().startswith("abstain")
            else "other"
            for row in local
        )
        result["protocol_audit"][condition] = {
            "n": len(local),
            "prefix_counts": dict(sorted(prefixes.items())),
            "classified_abstentions": sum(row["is_abstention"] for row in local),
        }
    for offset, condition in enumerate(FINAL_CONDITIONS):
        records = paired_records(rows, gate, condition)
        condition_result = {
            "target_abstention_rate": bootstrap_mean(
                records, "target_abstention", replicates, seed + offset * 50,
            ),
            "direct_abstention_rate": bootstrap_mean(
                records, "direct_abstention", replicates, seed + offset * 50 + 1,
            ),
            "abstention_delta": bootstrap_mean(
                records, "abstention_delta", replicates, seed + offset * 50 + 2,
            ),
            "abstain_probability_delta": bootstrap_mean(
                records, "probability_delta", replicates, seed + offset * 50 + 3,
            ),
            "target_correct_rate": bootstrap_mean(
                records, "target_correct", replicates, seed + offset * 50 + 4,
            ),
            "direct_correct_rate": bootstrap_mean(
                records, "direct_correct", replicates, seed + offset * 50 + 5,
            ),
            "correct_delta": bootstrap_mean(
                records, "correct_delta", replicates, seed + offset * 50 + 6,
            ),
            "by_source": {},
        }
        for source_offset, source in enumerate(sources):
            local = paired_records(rows, gate, condition, source)
            condition_result["by_source"][source] = {
                "abstention_delta": bootstrap_mean(
                    local, "abstention_delta", replicates,
                    seed + offset * 50 + 10 + source_offset * 3,
                ),
                "abstain_probability_delta": bootstrap_mean(
                    local, "probability_delta", replicates,
                    seed + offset * 50 + 11 + source_offset * 3,
                ),
                "correct_delta": bootstrap_mean(
                    local, "correct_delta", replicates,
                    seed + offset * 50 + 12 + source_offset * 3,
                ),
            }
        result["conditions"][condition] = condition_result

    self_effect = result["conditions"]["self_abstention"]
    teacher = result["conditions"]["teacher_abstention"]["abstention_delta"]
    paraphrase = result["conditions"]["paraphrased_abstention"]["abstention_delta"]
    neutral = result["conditions"]["neutral_same_context"]["abstention_delta"]
    answered = result["conditions"]["answered_history"]["abstention_delta"]
    self_abstention = self_effect["abstention_delta"]
    self_probability = self_effect["abstain_probability_delta"]
    checks = {
        "minimum_gated_items_per_source": all(gate_counts[source] >= 50 for source in sources),
        "self_abstention_delta_at_least_5pp": self_abstention["estimate"] >= .05,
        "self_abstention_delta_ci_positive": self_abstention["ci_low"] > 0,
        "self_probability_delta_ci_positive": self_probability["ci_low"] > 0,
        "teacher_direction_positive": teacher["estimate"] > 0,
        "paraphrase_direction_positive": paraphrase["estimate"] > 0,
        "self_exceeds_neutral": self_abstention["estimate"] > neutral["estimate"],
        "self_exceeds_answered_history": self_abstention["estimate"] > answered["estimate"],
        "both_sources_positive": all(
            value["abstention_delta"]["estimate"] > 0
            for value in self_effect["by_source"].values()
        ),
    }
    result["promotion_checks"] = checks
    result["promotion"] = all(checks.values())
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--output", required=True)
    parser.add_argument("--replicates", type=int, default=10000)
    parser.add_argument("--seed", type=int, default=20260830)
    args = parser.parse_args()
    families = {}
    for index, path in enumerate(args.inputs):
        metadata = json.loads(Path(path).with_suffix(".metadata.json").read_text())
        family = metadata["family"]
        families[family] = {
            "metadata": metadata,
            "analysis": analyze_family(read_jsonl(path), args.replicates, args.seed + index * 1000),
        }
    promoted = [family for family, result in families.items()
                if result["analysis"]["promotion"]]
    report = {
        "contract_id": "019-d0-v1",
        "families": families,
        "promoted_families": promoted,
        "overall_promotion": len(promoted) >= 2,
        "overall_decision": "PROMOTE-TO-MECHANISMS" if len(promoted) >= 2 else "NO-PROMOTE",
    }
    serialized = json.dumps(json_safe(report), indent=2, allow_nan=False)
    Path(args.output).write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
