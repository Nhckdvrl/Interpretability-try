from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from weak_evidence_g0.data import load_scenarios
from weak_evidence_g0.prompts import YES_NO_ORDERS, support_prompt

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SHA = "d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _materialize(tmp_path: Path) -> Path:
    builder = _load_module("build_frozen_d0_test", ROOT / "data" / "build_frozen_d0.py")
    data = builder.render(builder.build_rows())
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA
    path = tmp_path / "frozen_d0.jsonl"
    path.write_bytes(data)
    return path


def test_frozen_natural_d0_contract_and_checksum(tmp_path: Path):
    data = _materialize(tmp_path)
    scenarios = load_scenarios(data, require_external_source=True)
    assert len(scenarios) == 30
    assert len({s.scenario_id for s in scenarios}) == 30
    assert {s.domain for s in scenarios} == {"breast-cytology", "wine-cultivar"}
    assert hashlib.sha256(data.read_bytes()).hexdigest() == EXPECTED_SHA
    for s in scenarios:
        assert 1 < s.weak_target_lr < s.strong_target_lr
        assert 0 < s.strong_other_lr < s.weak_other_lr < 1
        assert 0.90 <= s.neutral_lr <= 1.10
        assert 1 < s.source["weak_target_lr_validation"] < s.source["strong_target_lr_validation"]
        assert 0 < s.source["strong_other_lr_validation"] < s.source["weak_other_lr_validation"] < 1
        assert 0.90 <= s.source["neutral_lr_validation"] <= 1.10


def test_frozen_jsonl_rebuilds_byte_for_byte_from_source_arrays(tmp_path: Path):
    data = _materialize(tmp_path)
    verifier = _load_module("verify_frozen_d0_test", ROOT / "data" / "verify_frozen_d0.py")
    result = verifier.verify(data)
    assert result["verified_items"] == 30
    assert result["sha256"] == EXPECTED_SHA


def test_strong_gt_weak_probe_does_not_leak_strength_labels():
    base = "BACKGROUND:\nX\n\nCALIBRATION:\nreal conditional counts"
    for mapping in YES_NO_ORDERS:
        prompt, _ = support_prompt(
            base=base,
            weak_evidence="condition 1 occurred",
            strong_evidence="condition 2 occurred",
            neutral_evidence="condition 3 occurred",
            focal_hypothesis="H",
            other_hypothesis="not-H",
            probe="strong_gt_weak",
            mapping=mapping,
            pragmatic_text="fixed reporting protocol",
        )
        assert "WEAK-CANDIDATE" not in prompt
        assert "STRONG-CANDIDATE" not in prompt
        assert "OBSERVATION 1" in prompt and "OBSERVATION 2" in prompt
