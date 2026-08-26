import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location("g0_007", Path(__file__).parents[1] / "g0.py")
g0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g0)


def test_bank_is_mirrored_and_second_report_is_normatively_decisive():
    cases = g0.make_cases()
    assert len(cases) == 72
    assert {x["first"] for x in cases} == {"A", "B"}
    assert all(x["gold_final"] == x["second"] and x["r2"] > x["r1"] for x in cases)


def test_attribution_prompts_hold_evidence_fixed():
    case = g0.make_cases()[0]
    prompts = {c: g0.stage2_prompt(case, c, "A") for c in ("hidden", "own", "other")}
    assert all(p[0]["content"] == case["stage1_prompt"] for p in prompts.values())
    assert prompts["own"][1]["content"].endswith("A")
    assert prompts["hidden"][1]["content"].endswith("xx")
    assert "another language model" in prompts["other"][2]["content"].lower()
    assert "no additional information" in prompts["other"][2]["content"]


def test_summary_uses_probability_not_only_greedy_change():
    case = g0.make_cases()[0]
    row = {**case, "initial": case["gold_initial"]}
    for name, p in (("hidden", .8), ("own", .3), ("other", .75)):
        row[f"conflict_{name}_probs"] = {case["gold_final"]: p, case["gold_initial"]: 1-p}
        row[f"conflict_{name}_pred"] = case["gold_final"] if p > .5 else case["gold_initial"]
        row[f"neutral_{name}_probs"] = {case["gold_final"]: .1, case["gold_initial"]: .9}
        row[f"neutral_{name}_pred"] = case["gold_initial"]
    summary = g0.summarize([row])
    assert abs(summary["hidden_minus_own"] - .5) < 1e-12
    assert abs(summary["other_minus_own"] - .45) < 1e-12
