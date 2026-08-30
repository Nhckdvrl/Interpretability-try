import json
from pathlib import Path

from weak_evidence_g0.panel import evaluate_panel


def _write(tmp_path, family, model, size, passed=True, verdict="PASS-TO-PANEL"):
    p = tmp_path / f"{family}_{model}_{size}.json"
    p.write_text(json.dumps({"family": family, "model": model, "size_b": size, "model_pass": passed, "verdict": verdict}), encoding="utf-8")
    return str(p)


def test_panel_counts_only_actual_passes_and_requires_three_size_family(tmp_path):
    paths = [
        _write(tmp_path, "Qwen", "q4", 4),
        _write(tmp_path, "Qwen", "q8", 8),
        _write(tmp_path, "Qwen", "q32", 32),
        _write(tmp_path, "Gemma", "g12", 12),
        _write(tmp_path, "Phi", "p4", 4),
        _write(tmp_path, "Llama", "l8", 8, passed=False, verdict="FAIL-MODEL-G0"),
        _write(tmp_path, "Mistral", "m24", 24, passed=False, verdict="HOLD-WORDING-ARTIFACT"),
    ]
    out = evaluate_panel(paths)
    assert out["smoke_cross_family_pass"] is True
    assert out["generality_pass"] is True
    assert out["passed_families"] == ["Gemma", "Phi", "Qwen"]
    assert out["three_size_families"] == ["Qwen"]


def test_hold_with_model_pass_true_is_not_counted(tmp_path):
    paths = [
        _write(tmp_path, "Qwen", "q8", 8, passed=True, verdict="HOLD-WORDING-ARTIFACT"),
        _write(tmp_path, "Gemma", "g12", 12),
    ]
    out = evaluate_panel(paths)
    assert out["passed_families"] == ["Gemma"]
    assert out["smoke_cross_family_pass"] is False
