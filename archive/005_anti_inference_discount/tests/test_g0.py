from __future__ import annotations

import json
from pathlib import Path
import pytest

from antiinf_g0.dataset import FAMILIES, OUTCOMES, generate_scenarios, load_scenarios, write_scenarios
from antiinf_g0.prompts import build_comprehension_prompt, build_natural_judgment_prompt, build_bridged_judgment_prompt


def test_generator_has_frozen_family_and_outcome_balance() -> None:
    rows = generate_scenarios()
    assert len(rows) == 96
    assert len({x.scenario_id for x in rows}) == 96
    assert {f: sum(x.family == f for x in rows) for f in FAMILIES} == {f: 32 for f in FAMILIES}
    for family in FAMILIES:
        assert {o: sum(x.family == family and x.outcome == o for x in rows) for o in OUTCOMES} == {o: 16 for o in OUTCOMES}


def test_gold_conclusion_flips_with_criterion_direction() -> None:
    rows = generate_scenarios()
    for family in FAMILIES:
        met = next(x for x in rows if x.family == family and x.outcome == "criterion_met")
        not_met = next(x for x in rows if x.family == family and x.outcome == "criterion_not_met")
        assert met.target_conclusion == not_met.alternative_conclusion
        assert met.alternative_conclusion == not_met.target_conclusion


def test_direct_and_inference_are_not_nested_or_verbatim_fact() -> None:
    for row in generate_scenarios():
        d = row.direct_evidence.lower()
        i = row.inference_evidence.lower()
        fact = row.critical_fact.lower().rstrip(".")
        assert d not in i and i not in d
        assert fact not in d and fact not in i


def test_natural_judgment_has_no_forced_acknowledgement() -> None:
    row = generate_scenarios()[0]
    hist, target = build_natural_judgment_prompt(row, "inference", 0, 0)
    assert target == "A" and len(hist) == 1 and hist[0][0] == "user" and row.inference_evidence in hist[0][1]
    assert all(role != "assistant" for role, _ in hist)


def test_bridged_judgment_conditions_on_yes_and_same_evidence() -> None:
    row = generate_scenarios()[0]
    comp = build_comprehension_prompt(row, "inference", 0)
    hist, target = build_bridged_judgment_prompt(row, "inference", 0, 0, 0)
    assert target == "A"
    assert hist[0] == comp[0]
    assert hist[1] == ("assistant", "Yes")
    assert hist[-1][0] == "user"
    assert row.inference_evidence in hist[0][1]


def test_label_order_swaps_target_in_both_paths() -> None:
    row = generate_scenarios()[0]
    _, n0 = build_natural_judgment_prompt(row, "direct", 0, 0)
    _, n1 = build_natural_judgment_prompt(row, "direct", 0, 1)
    _, b0 = build_bridged_judgment_prompt(row, "direct", 0, 0, 0)
    _, b1 = build_bridged_judgment_prompt(row, "direct", 0, 0, 1)
    assert (n0, n1) == ("A", "B") and (b0, b1) == ("A", "B")


def test_comprehension_asks_identical_critical_fact() -> None:
    row = generate_scenarios()[0]
    direct = build_comprehension_prompt(row, "direct", 0)[0][1]
    inferred = build_comprehension_prompt(row, "inference", 0)[0][1]
    assert row.critical_fact in direct and row.critical_fact in inferred
    assert row.direct_evidence in direct and row.inference_evidence in inferred


def test_loader_rejects_duplicate_ids(tmp_path: Path) -> None:
    path = tmp_path / "scenarios.jsonl"
    rows = write_scenarios(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rows[0].__dict__) + "\n")
    with pytest.raises(ValueError, match="duplicate scenario IDs"):
        load_scenarios(path, strict=False)
