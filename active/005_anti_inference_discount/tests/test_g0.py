from __future__ import annotations

import json
from pathlib import Path

import pytest

from antiinf_g0.dataset import FAMILIES, generate_scenarios, load_scenarios, write_scenarios
from antiinf_g0.prompts import build_comprehension_prompt, build_judgment_prompt


def test_generator_has_frozen_size_and_balance() -> None:
    rows = generate_scenarios()
    assert len(rows) == 96
    assert len({x.scenario_id for x in rows}) == 96
    assert {f: sum(x.family == f for x in rows) for f in FAMILIES} == {f: 32 for f in FAMILIES}


def test_inference_condition_does_not_repeat_critical_fact_verbatim() -> None:
    for row in generate_scenarios():
        assert row.critical_fact.lower().rstrip(".") not in row.inference_evidence.lower()
        assert row.critical_fact.lower().rstrip(".") in row.direct_evidence.lower()


def test_judgment_label_order_swaps_target() -> None:
    row = generate_scenarios()[0]
    p0, target0 = build_judgment_prompt(row, "direct", 0, 0)
    p1, target1 = build_judgment_prompt(row, "direct", 0, 1)
    assert target0 == "A"
    assert target1 == "B"
    assert row.target_conclusion in p0 and row.target_conclusion in p1


def test_comprehension_prompt_asks_same_critical_fact() -> None:
    row = generate_scenarios()[0]
    direct = build_comprehension_prompt(row, "direct", 0)
    inferred = build_comprehension_prompt(row, "inference", 0)
    assert row.critical_fact in direct
    assert row.critical_fact in inferred
    assert row.direct_evidence in direct
    assert row.inference_evidence in inferred


def test_loader_rejects_duplicate_ids(tmp_path: Path) -> None:
    path = tmp_path / "scenarios.jsonl"
    rows = write_scenarios(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rows[0].__dict__) + "\n")
    with pytest.raises(ValueError, match="duplicate scenario IDs"):
        load_scenarios(path, strict=False)
