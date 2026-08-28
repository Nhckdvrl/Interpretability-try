import json
from pathlib import Path

from witness_collapse_g0.metrics import summarize
from witness_collapse_g0.prompts import CONDITIONS, DOWNSTREAM_TEMPLATES
from witness_collapse_g0.run import RECOGNITION_PROBES
from test_data import record


def _run_panel_fixture(tmp_path, unknown_probability: float):
    data_rows = []
    result_rows = []
    meta = {"model": "fixture", "family": "Qwen", "revision": "r", "size_b": 8, "requested_dtype": "bfloat16"}
    for i in range(20):
        row = record("external-derived")
        sid = f"staff:{i}"
        domain = "staffing" if i < 10 else "compliance"
        row["scenario_id"] = sid
        row["domain"] = domain
        row["source"]["record_id"] = str(i)
        data_rows.append(row)
        for probe in RECOGNITION_PROBES:
            for order in (0, 1):
                result_rows.append({**meta, "kind": "recognition", "scenario_id": sid, "domain": domain, "probe": probe, "label_order": order, "p_correct": .95})
        values = {
            "unknown": unknown_probability,
            "paraphrase": unknown_probability - .01,
            "same_explicit": .96,
            "distinct_explicit": .08,
            "neutral_control": unknown_probability - .01,
            "relation_reminder": .20,
        }
        for condition in CONDITIONS:
            for template_id in range(len(DOWNSTREAM_TEMPLATES)):
                for order in (0, 1):
                    result_rows.append({**meta, "kind": "downstream", "scenario_id": sid, "domain": domain, "condition": condition, "template_id": template_id, "label_order": order, "p_collapse_action": values[condition]})
    data = tmp_path / "data.jsonl"
    results = tmp_path / "results.jsonl"
    data.write_text("".join(json.dumps(x) + "\n" for x in data_rows), encoding="utf-8")
    results.write_text("".join(json.dumps(x) + "\n" for x in result_rows), encoding="utf-8")
    cfg = Path(__file__).parents[1] / "configs" / "frozen_g0.json"
    return summarize(data_path=str(data), results_path=str(results), config_path=str(cfg))


def test_model_level_illegal_join_signature_can_pass(tmp_path):
    summary = _run_panel_fixture(tmp_path, .70)
    assert summary["model_pass"] is True
    assert summary["verdict"] == "PASS-TO-PANEL"


def test_model_level_correct_identity_preservation_is_hard_killed(tmp_path):
    summary = _run_panel_fixture(tmp_path, .30)
    assert summary["model_pass"] is False
    assert summary["verdict"] == "HARD-KILL-NO-ILLEGAL-JOIN"
