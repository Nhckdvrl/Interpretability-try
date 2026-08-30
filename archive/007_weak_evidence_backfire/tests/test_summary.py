import json
from pathlib import Path
from weak_evidence_g0.metrics import summarize
from weak_evidence_g0.prompts import CONDITIONS, DIRECTIONS, READOUT_TEMPLATES
from weak_evidence_g0.run import SUPPORT_PROBES
from test_contract import record


def test_end_to_end_bidirectional_summary_uses_scenario_as_statistical_unit(tmp_path):
    row = record("external-derived")
    data = tmp_path / "data.jsonl"
    data.write_text(json.dumps(row) + "\n")
    meta = {"model": "m", "family": "Qwen", "revision": "r", "size_b": 8, "requested_dtype": "bfloat16"}
    results = []
    for direction in DIRECTIONS:
        for probe in SUPPORT_PROBES:
            for order in (0, 1):
                results.append({**meta, "kind": "support_probe", "scenario_id": "machine:1", "domain": "diagnostics", "direction": direction, "probe": probe, "label_order": order, "p_correct": .95})

    values = {
        "supports_target": {
            "belief": {"no_evidence": .55, "weak": .45, "strong": .76, "neutral": .55, "no_evidence_complete": .55, "weak_complete": .47, "no_evidence_length": .55, "weak_length": .46},
            "action": {"no_evidence": .52, "weak": .47, "strong": .72, "neutral": .52, "no_evidence_complete": .52, "weak_complete": .48, "no_evidence_length": .52, "weak_length": .48},
        },
        "supports_other": {
            "belief": {"no_evidence": .55, "weak": .65, "strong": .34, "neutral": .55, "no_evidence_complete": .55, "weak_complete": .63, "no_evidence_length": .55, "weak_length": .64},
            "action": {"no_evidence": .52, "weak": .57, "strong": .32, "neutral": .52, "no_evidence_complete": .52, "weak_complete": .56, "no_evidence_length": .52, "weak_length": .56},
        },
    }
    for direction in DIRECTIONS:
        for template_id, (kind, _) in enumerate(READOUT_TEMPLATES):
            for condition in CONDITIONS:
                for order in (0, 1):
                    results.append({**meta, "kind": "readout", "scenario_id": "machine:1", "domain": "diagnostics", "direction": direction, "condition": condition, "template_id": template_id, "template_kind": kind, "label_order": order, "p_target": values[direction][kind][condition]})

    result_path = tmp_path / "result.jsonl"
    result_path.write_text("".join(json.dumps(x) + "\n" for x in results))
    cfg_path = Path(__file__).parents[1] / "configs" / "frozen_g0.json"
    summary = summarize(data_path=str(data), results_path=str(result_path), config_path=str(cfg_path))
    assert len(summary["directions"]) == 2
    assert len(summary["scenario_pairs"]) == 1
    assert all(entry["support_gate"] and entry["capability_gate"] and entry["strong"] for entry in summary["directions"])
    assert summary["scenario_pairs"][0]["belief_backfire_mean"] > 0
    assert summary["aggregate"]["gated_scenario_pairs"] == 1
    assert summary["model_pass"] is False
