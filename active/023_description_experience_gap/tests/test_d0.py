"""Invariant tests for the frozen 023 D0."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from description_experience.analyze import choice_units  # noqa: E402
from description_experience.build_bank import audit, build, exact_history, expected_value  # noqa: E402


def fixtures() -> tuple[dict, dict]:
    gambles = json.loads((ROOT / "data" / "gambles.json").read_text())
    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    return gambles, contract


def test_bank_size_balance_and_shared_stimulus() -> None:
    gambles, contract = fixtures()
    records = build(gambles, contract)
    audit(records, contract)
    assert len(records) == 1728
    assert len({row["scenario_id"] for row in records}) == 432
    for scenario_id in {row["scenario_id"] for row in records}:
        rows = [row for row in records if row["scenario_id"] == scenario_id]
        assert len({row["stimulus"] for row in rows}) == 1
        assert {row["query_type"] for row in rows} == {"choice", "expected_value", "frequency_a", "frequency_b"}


def test_histories_are_exact_and_ev_is_deterministic() -> None:
    gambles, _ = fixtures()
    for gamble in gambles["gambles"]:
        for label in ("A", "B"):
            history = exact_history(gamble[label], 10, 20, 7)
            assert len(history) == 20
            assert sum(history) / 20 == float(expected_value(gamble[label], 10))


def test_choice_pairing_removes_display_order() -> None:
    gambles, contract = fixtures()
    choices = [row for row in build(gambles, contract) if row["query_type"] == "choice"]
    frame = pd.DataFrame({**row, "p_target": 0.7} for row in choices)
    directed, order_difference = choice_units(frame)
    assert len(directed) == 36
    assert (order_difference["difference"] == 0).all()
    assert (directed["normalized_gap_probability"] == 0).all()
    assert (directed["normalized_gap_counts"] == 0).all()
