"""Frozen entity-clustered analysis for the D1 r4 construct validation."""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

N_BOOT = 10_000
SEED = 20260830
FRAMES = ("F1", "F2")


def load_bank(path: str | Path) -> dict[str, dict]:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    bank = {row["item_id"]: row for row in rows}
    if len(bank) != len(rows):
        raise RuntimeError("D1 r4 bank contains duplicate item_id values")
    return bank


def capability_gate(path: str | Path) -> set[str]:
    cells: dict[tuple[str, int], dict[str, float]] = defaultdict(dict)
    gold: dict[tuple[str, int], str] = {}
    for row in (json.loads(line) for line in open(path, encoding="utf-8")):
        key = (row["item_id"], int(row["order"]))
        cells[key][row["letter"]] = float(row["logprob_sum"])
        gold[key] = row["gold"]
    per_item: dict[str, list[bool]] = defaultdict(list)
    for key, scores in cells.items():
        g = gold[key]
        per_item[key[0]].append(scores[g] > scores["B" if g == "A" else "A"])
    return {item_id for item_id, passed in per_item.items()
            if len(passed) == 2 and all(passed)}


def item_frame_deltas(path: str | Path) -> dict[str, dict[str, dict[str, float]]]:
    base: dict[str, float] = {}
    cells: dict[str, dict[str, dict[str, float]]] = defaultdict(lambda: defaultdict(dict))
    for row in (json.loads(line) for line in open(path, encoding="utf-8")):
        item_id = row["item_id"]
        if row["condition"] == "NOCTX":
            base[item_id] = float(row["logprob_sum"])
        else:
            cells[item_id][row["frame"]][row["condition"]] = float(row["logprob_sum"])
    for item_id, by_frame in cells.items():
        for values in by_frame.values():
            for condition in list(values):
                values[condition] -= base[item_id]
    return cells


def entity_equal_boot(values: dict[str, list[float]], n_boot: int = N_BOOT,
                      seed: int = SEED) -> dict:
    """Average dependent directions/pairs within entity, then bootstrap entities."""
    entity_values = np.array([np.mean(values[e]) for e in sorted(values)], dtype=float)
    if not len(entity_values):
        return {"estimate": None, "ci_low": None, "ci_high": None,
                "n_entities": 0, "n_items": 0}
    estimate = float(np.median(entity_values))
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(entity_values), size=(n_boot, len(entity_values)))
    boots = np.median(entity_values[idx], axis=1)
    low, high = np.percentile(boots, [2.5, 97.5])
    return {
        "estimate": estimate, "ci_low": float(low), "ci_high": float(high),
        "excludes_zero": bool(low > 0 or high < 0),
        "n_entities": len(entity_values), "n_items": sum(map(len, values.values())),
    }


def contrast(bank: dict[str, dict], deltas: dict, frame: str, condition_a: str,
             condition_b: str, predicate=lambda _: True) -> dict:
    values: dict[str, list[float]] = defaultdict(list)
    for item_id, item in bank.items():
        cell = deltas.get(item_id, {}).get(frame, {})
        if predicate(item) and condition_a in cell and condition_b in cell:
            values[item["entity_uri"]].append(cell[condition_a] - cell[condition_b])
    return entity_equal_boot(values)


def analyze_model(tag: str, results_dir: Path, bank: dict[str, dict]) -> dict:
    gate = capability_gate(results_dir / f"{tag}__probe.jsonl")
    deltas = item_frame_deltas(results_dir / f"{tag}__main.jsonl")
    intended = lambda x: bool(x["confirmatory_intended_surface"])
    q2 = lambda x: (intended(x) and x["structural_stratum"] == "opaque_strict"
                    and x["item_id"] in gate)
    report = {
        "model_label": tag,
        "bank_items": len(bank),
        "gate_items": len(gate),
        "gate_entities": len({bank[i]["entity_uri"] for i in gate}),
        "frames": {},
        "by_direction": {},
        "by_structure": {},
    }
    for frame in FRAMES:
        q1 = contrast(bank, deltas, frame, "ALIAS", "ASSOC_ANY", intended)
        q2r = contrast(bank, deltas, frame, "ALIAS", "ASSOC_ANY", q2)
        exact = contrast(bank, deltas, frame, "EXACT", "ASSOC_ANY", intended)
        same = contrast(
            bank, deltas, frame, "ALIAS", "ASSOC_SAMETYPE",
            lambda x: intended(x) and bool(x.get("assoc_sametype")),
        )
        report["frames"][frame] = {
            "q1_alias_minus_assoc_any": q1,
            "q2_gated_opaque_strict_alias_minus_assoc_any": q2r,
            "exact_minus_assoc_any": exact,
            "alias_minus_assoc_sametype": same,
        }
        for direction in ("alias_to_canonical", "canonical_to_alias"):
            report["by_direction"].setdefault(direction, {})[frame] = contrast(
                bank, deltas, frame, "ALIAS", "ASSOC_ANY",
                lambda x, d=direction: intended(x) and x["direction"] == d,
            )
        for structure in ("compositional", "partial", "opaque", "opaque_strict"):
            report["by_structure"].setdefault(structure, {})[frame] = contrast(
                bank, deltas, frame, "ALIAS", "ASSOC_ANY",
                lambda x, s=structure: intended(x) and x["structural_stratum"] == s,
            )
    q1_pass = all(report["frames"][f]["q1_alias_minus_assoc_any"].get("ci_low", -1) > 0
                  for f in FRAMES)
    q2_floor = min(report["frames"][f][
        "q2_gated_opaque_strict_alias_minus_assoc_any"]["n_entities"] for f in FRAMES) >= 60
    q2_pass = q2_floor and all(report["frames"][f][
        "q2_gated_opaque_strict_alias_minus_assoc_any"].get("ci_low", -1) > 0
        for f in FRAMES)
    report.update(q1_pass=q1_pass, q2_capability_floor_pass=q2_floor, q2_pass=q2_pass)
    return report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", default="data/frozen_d1_r4.jsonl")
    ap.add_argument("--results-dir", default="results/d1_r4")
    ap.add_argument("--tags", nargs="+", required=True)
    ap.add_argument("--output", default="results/d1_r4/analysis_d1_r4.json")
    args = ap.parse_args()
    bank = load_bank(args.bank)
    reports = [analyze_model(tag, Path(args.results_dir), bank) for tag in args.tags]
    q1_families = sum(report["q1_pass"] for report in reports)
    q2_families = sum(report["q2_pass"] for report in reports)
    if q1_families >= 2 and q2_families >= 2:
        verdict = "REFERENTIAL-IDENTITY-EFFECT"
    elif q1_families >= 2:
        verdict = "CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC"
    else:
        verdict = "INCONCLUSIVE"
    output = {
        "contract_id": "2026-08-29-d1-r4-scope-correction",
        "analysis": "entity-equal median; 10000 entity-cluster bootstrap replicates",
        "q1_passing_families": q1_families,
        "q2_passing_families": q2_families,
        "verdict": verdict,
        "models": reports,
    }
    Path(args.output).write_text(json.dumps(output, indent=2) + "\n")
    for report in reports:
        print(f"{report['model_label']}: gate {report['gate_items']}/{report['bank_items']} items")
        for frame in FRAMES:
            q1 = report["frames"][frame]["q1_alias_minus_assoc_any"]
            q2 = report["frames"][frame]["q2_gated_opaque_strict_alias_minus_assoc_any"]
            print(f"  {frame} Q1 {q1['estimate']:+.4f} [{q1['ci_low']:+.4f}, {q1['ci_high']:+.4f}] "
                  f"entities={q1['n_entities']}; Q2 {q2['estimate']!s} "
                  f"[{q2['ci_low']!s}, {q2['ci_high']!s}] entities={q2['n_entities']}")
        print(f"  Q1 pass={report['q1_pass']} Q2 floor={report['q2_capability_floor_pass']} "
              f"Q2 pass={report['q2_pass']}")


if __name__ == "__main__":
    main()
