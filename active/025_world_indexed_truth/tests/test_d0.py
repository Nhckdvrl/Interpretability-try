"""Invariant tests for the frozen 025 D0 pipeline."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from world_indexed_truth.analyze import joint_frame, summarize_family  # noqa: E402
from world_indexed_truth.build_bank import audit, build  # noqa: E402


def source() -> dict:
    return json.loads((ROOT / "data" / "source_facts.json").read_text())


def test_bank_balance_and_pair_identity() -> None:
    items = build(source())
    audit(items)
    assert len(items) == 256
    assert len({item["context_id"] for item in items}) == 128
    for context_id in {item["context_id"] for item in items}:
        pair = [item for item in items if item["context_id"] == context_id]
        assert len({item["context"] for item in pair}) == 1
        assert len({item["proposition"] for item in pair}) == 1
        assert {item["query_world"] for item in pair} == {"actual", "local"}


def test_conflict_gold_values_are_opposed() -> None:
    items = build(source())
    for item in items:
        if item["local_relation"] == "conflict":
            assert item["actual_truth"] != item["local_truth"]
        else:
            assert item["actual_truth"] == item["local_truth"]


def test_joint_and_family_gate_on_perfect_predictions() -> None:
    items = build(source())
    frame = pd.DataFrame({**item, "correct": True} for item in items)
    assert joint_frame(frame)["joint_correct"].all()
    gates = json.loads((ROOT / "configs" / "d0_contract.json").read_text())["family_gates"]
    summary = summarize_family(frame, gates)
    assert summary["family_pass"]
    assert summary["overall_joint_accuracy"] == 1.0
