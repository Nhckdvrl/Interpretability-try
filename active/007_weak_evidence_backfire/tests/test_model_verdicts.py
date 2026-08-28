import json
from pathlib import Path

from weak_evidence_g0.metrics import summarize
from weak_evidence_g0.prompts import CONDITIONS, DIRECTIONS, READOUT_TEMPLATES
from weak_evidence_g0.run import SUPPORT_PROBES
from test_contract import record


def _fixture(tmp_path, mode: str):
    data_rows = []
    result_rows = []
    meta = {"model": "fixture", "family": "Qwen", "revision": "r", "size_b": 8, "requested_dtype": "bfloat16"}
    for i in range(20):
        row = record("external-derived")
        sid = f"machine:{i}"
        domain = "diagnostics" if i < 10 else "screening"
        row["scenario_id"] = sid
        row["domain"] = domain
        row["source"]["record_id"] = str(i)
        data_rows.append(row)
        for direction in DIRECTIONS:
            for probe in SUPPORT_PROBES:
                for order in (0, 1):
                    result_rows.append({**meta, "kind": "support_probe", "scenario_id": sid, "domain": domain, "direction": direction, "probe": probe, "label_order": order, "p_correct": .95})

        if mode == "backfire":
            target_weak, other_weak = .47, .63
            target_complete, other_complete = .47, .63
            target_length, other_length = .47, .63
        elif mode == "normal":
            target_weak, other_weak = .63, .47
            target_complete, other_complete = .63, .47
            target_length, other_length = .63, .47
        elif mode == "pragmatic_only":
            target_weak, other_weak = .47, .63
            target_complete, other_complete = .63, .47
            target_length, other_length = .47, .63
        else:
            raise ValueError(mode)

        values = {
            "supports_target": {
                "belief": {"no_evidence": .55, "weak": target_weak, "strong": .78, "neutral": .55, "no_evidence_complete": .55, "weak_complete": target_complete, "no_evidence_length": .55, "weak_length": target_length},
                "action": {"no_evidence": .52, "weak": target_weak - .03, "strong": .74, "neutral": .52, "no_evidence_complete": .52, "weak_complete": target_complete - .03, "no_evidence_length": .52, "weak_length": target_length - .03},
            },
            "supports_other": {
                "belief": {"no_evidence": .55, "weak": other_weak, "strong": .30, "neutral": .55, "no_evidence_complete": .55, "weak_complete": other_complete, "no_evidence_length": .55, "weak_length": other_length},
                "action": {"no_evidence": .52, "weak": other_weak - .03, "strong": .28, "neutral": .52, "no_evidence_complete": .52, "weak_complete": other_complete - .03, "no_evidence_length": .52, "weak_length": other_length - .03},
            },
        }
        # Keep action shifts symmetric in directional sign and magnitude relative to their own baselines.
        if mode in {"backfire", "pragmatic_only"}:
            values["supports_target"]["action"]["weak"] = .47
            values["supports_other"]["action"]["weak"] = .57
            values["supports_target"]["action"]["weak_length"] = .48
            values["supports_other"]["action"]["weak_length"] = .56
        if mode == "backfire":
            values["supports_target"]["action"]["weak_complete"] = .48
            values["supports_other"]["action"]["weak_complete"] = .56
        elif mode == "pragmatic_only":
            values["supports_target"]["action"]["weak_complete"] = .60
            values["supports_other"]["action"]["weak_complete"] = .44
        elif mode == "normal":
            values["supports_target"]["action"]["weak"] = .60
            values["supports_other"]["action"]["weak"] = .44
            values["supports_target"]["action"]["weak_complete"] = .60
            values["supports_other"]["action"]["weak_complete"] = .44
            values["supports_target"]["action"]["weak_length"] = .60
            values["supports_other"]["action"]["weak_length"] = .44

        for direction in DIRECTIONS:
            for template_id, (kind, _) in enumerate(READOUT_TEMPLATES):
                for condition in CONDITIONS:
                    for order in (0, 1):
                        result_rows.append({**meta, "kind": "readout", "scenario_id": sid, "domain": domain, "direction": direction, "condition": condition, "template_id": template_id, "template_kind": kind, "label_order": order, "p_target": values[direction][kind][condition]})

    data = tmp_path / "data.jsonl"
    results = tmp_path / "results.jsonl"
    data.write_text("".join(json.dumps(x) + "\n" for x in data_rows), encoding="utf-8")
    results.write_text("".join(json.dumps(x) + "\n" for x in result_rows), encoding="utf-8")
    cfg = Path(__file__).parents[1] / "configs" / "frozen_g0.json"
    return summarize(data_path=str(data), results_path=str(results), config_path=str(cfg))


def test_bidirectional_sign_reversal_can_pass_full_model_gate(tmp_path):
    summary = _fixture(tmp_path, "backfire")
    assert summary["model_pass"] is True
    assert summary["verdict"] == "PASS-TO-PANEL"
    assert summary["aggregate"]["bidirectional_backfire_fraction"] == 1.0


def test_normal_bayesian_direction_is_hard_killed(tmp_path):
    summary = _fixture(tmp_path, "normal")
    assert summary["model_pass"] is False
    assert summary["verdict"] == "HARD-KILL-NO-BACKFIRE"


def test_effect_removed_by_completeness_protocol_is_hard_killed(tmp_path):
    summary = _fixture(tmp_path, "pragmatic_only")
    assert summary["model_pass"] is False
    assert summary["verdict"] == "HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE"
