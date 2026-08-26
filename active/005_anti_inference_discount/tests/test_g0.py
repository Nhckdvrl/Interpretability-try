from __future__ import annotations

import json
from pathlib import Path
import pytest

from antiinf_g0.dataset import FAMILIES,generate_scenarios,load_scenarios,write_scenarios
from antiinf_g0.prompts import build_comprehension_prompt,build_judgment_prompt


def test_generator_has_frozen_size_and_balance() -> None:
    rows=generate_scenarios(); assert len(rows)==96; assert len({x.scenario_id for x in rows})==96
    assert {f:sum(x.family==f for x in rows) for f in FAMILIES}=={f:32 for f in FAMILIES}


def test_direct_and_inference_are_not_nested_or_verbatim_fact() -> None:
    for row in generate_scenarios():
        d=row.direct_evidence.lower(); i=row.inference_evidence.lower(); fact=row.critical_fact.lower().rstrip(".")
        assert d not in i and i not in d and fact not in d and fact not in i


def test_judgment_history_conditions_on_yes_and_same_evidence() -> None:
    row=generate_scenarios()[0]; comp=build_comprehension_prompt(row,"inference",0); hist,target=build_judgment_prompt(row,"inference",0,0,0)
    assert target=="A" and hist[0]==comp[0] and hist[1]==("assistant","Yes") and hist[-1][0]=="user" and row.inference_evidence in hist[0][1]


def test_judgment_label_order_swaps_target() -> None:
    row=generate_scenarios()[0]; h0,t0=build_judgment_prompt(row,"direct",0,0,0); h1,t1=build_judgment_prompt(row,"direct",0,0,1)
    assert t0=="A" and t1=="B" and row.target_conclusion in h0[-1][1] and row.target_conclusion in h1[-1][1]


def test_comprehension_asks_identical_critical_fact() -> None:
    row=generate_scenarios()[0]; direct=build_comprehension_prompt(row,"direct",0)[0][1]; inferred=build_comprehension_prompt(row,"inference",0)[0][1]
    assert row.critical_fact in direct and row.critical_fact in inferred and row.direct_evidence in direct and row.inference_evidence in inferred


def test_loader_rejects_duplicate_ids(tmp_path: Path) -> None:
    path=tmp_path/"scenarios.jsonl"; rows=write_scenarios(path)
    with path.open("a",encoding="utf-8") as f: f.write(json.dumps(rows[0].__dict__)+"\n")
    with pytest.raises(ValueError,match="duplicate scenario IDs"): load_scenarios(path,strict=False)
