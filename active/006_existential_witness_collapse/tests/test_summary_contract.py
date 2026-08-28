import json
from pathlib import Path
from witness_collapse_g0.metrics import summarize
from witness_collapse_g0.prompts import CONDITIONS, DOWNSTREAM_TEMPLATES
from witness_collapse_g0.run import RECOGNITION_PROBES
from test_data import record


def test_end_to_end_summary_preserves_gate_before_illegal_action(tmp_path):
    row = record("external-derived")
    data = tmp_path / "data.jsonl"
    data.write_text(json.dumps(row) + "\n")
    meta = {"model": "m", "family": "Qwen", "revision": "r", "size_b": 8, "requested_dtype": "bfloat16"}
    results = []
    for probe in RECOGNITION_PROBES:
        for order in (0, 1):
            results.append({**meta, "kind": "recognition", "scenario_id": "staff:1", "domain": "staffing", "probe": probe, "label_order": order, "p_correct": .95})
    p = {"unknown": .70, "paraphrase": .68, "same_explicit": .96, "distinct_explicit": .08, "neutral_control": .69, "relation_reminder": .20}
    for condition in CONDITIONS:
        for template_id in range(len(DOWNSTREAM_TEMPLATES)):
            for order in (0, 1):
                results.append({**meta, "kind": "downstream", "scenario_id": "staff:1", "domain": "staffing", "condition": condition, "template_id": template_id, "label_order": order, "p_collapse_action": p[condition]})
    result_path = tmp_path / "result.jsonl"
    result_path.write_text("".join(json.dumps(x) + "\n" for x in results))
    cfg_path = Path(__file__).parents[1] / "configs" / "frozen_g0.json"
    summary = summarize(data_path=str(data), results_path=str(result_path), config_path=str(cfg_path))
    case = summary["cases"][0]
    assert case["recognition_gate"] and case["capability_gate"] and case["strong"]
    assert case["unknown_margin"] > 0
    assert summary["model_pass"] is False
