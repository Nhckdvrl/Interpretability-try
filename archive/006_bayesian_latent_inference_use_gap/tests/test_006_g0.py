import importlib.util
from pathlib import Path


spec = importlib.util.spec_from_file_location("g0_006", Path(__file__).parents[1] / "g0.py")
g0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g0)


def test_closed_form_and_case_bank():
    assert abs(g0.posterior_a(0.5, 1, 0) - 0.8) < 1e-12
    cases = g0.make_cases()
    assert len(cases) == 72
    assert len({x["evidence_id"] for x in cases}) == 24
    assert all(x["gold_action"] == g0.action_for(x["gold_p_a"], x["decision_threshold"]) for x in cases)
    case = cases[0]
    assert g0.action_prompt(case, bridge=False, mapping=("ACT", "WAIT"))[1] != g0.action_prompt(case, bridge=False, mapping=("WAIT", "ACT"))[1]


def test_probability_parser():
    assert g0.parse_probability("0.625") == 0.625
    assert g0.parse_probability("62.5%") == 0.625
    assert g0.parse_probability("answer: .75") == 0.75


def test_summary_requires_reported_posterior_to_imply_gold_action():
    case = next(x for x in g0.make_cases() if x["gold_action"] == "ACT" and x["bayes_margin"] >= 0.10)
    row = {**case, "pred_p_a": case["decision_threshold"] - 0.01,
           "direct_probs": {"ACT": 0.1, "WAIT": 0.9}, "bridged_probs": {"ACT": 0.9, "WAIT": 0.1},
           "direct_pred": "WAIT", "bridged_pred": "ACT"}
    assert g0.summarize([row])["n_inference_good_action_identified_nonboundary"] == 0
