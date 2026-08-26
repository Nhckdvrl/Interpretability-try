from __future__ import annotations

import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from meta_g0 import action_for, make_dataset, surfaces  # noqa: E402


def test_meta_dataset_balanced_across_tasks_and_actions() -> None:
    rows = make_dataset(per_task=24, seed=6060)
    assert len(rows) == 96
    tasks = {row["task_family"] for row in rows}
    assert len(tasks) == 4
    for task in tasks:
        group = [row for row in rows if row["task_family"] == task]
        assert len(group) == 24
        assert sum(row["gold_action"] == "ACT" for row in group) == 12
        assert sum(row["gold_action"] == "WAIT" for row in group) == 12
        assert all(abs(row["gold_p"] - row["threshold"]) >= 0.08 for row in group)


def test_meta_surfaces_counterbalance_mapping_and_rule_order() -> None:
    rows = surfaces()
    assert len(rows) == 8
    assert len({row["surface_id"] for row in rows}) == 8
    assert {tuple(row["mapping"]) for row in rows} == {
        ("ACT", "WAIT"),
        ("WAIT", "ACT"),
    }
    assert {row["rule_form"] for row in rows} == {"high_first", "low_first"}


def test_action_boundary_is_strict() -> None:
    assert action_for(0.5, 0.5) == "WAIT"
    assert action_for(0.500001, 0.5) == "ACT"
