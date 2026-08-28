from pathlib import Path
import importlib.util

from weak_evidence_g0.data import load_scenarios, NEUTRAL_LR_MIN, NEUTRAL_LR_MAX


def _materializer():
    path = Path(__file__).resolve().parents[1] / "data" / "materialize_frozen_d0.py"
    spec = importlib.util.spec_from_file_location("materialize_007_d0", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_frozen_natural_d0_contract(tmp_path):
    module = _materializer()
    data_path = module.materialize(tmp_path / "frozen_d0.jsonl")
    scenarios = load_scenarios(data_path, require_external_source=True)
    assert len(scenarios) == 25
    assert {s.domain for s in scenarios} == {"breast-cytology", "wine-origin"}
    assert {s.source["license"] for s in scenarios} == {"CC BY 4.0"}
    assert {s.source["provenance"] for s in scenarios} == {"external-derived"}
    for s in scenarios:
        src = s.source
        assert 1 < float(src["weak_target_lr_validation"]) < float(src["strong_target_lr_validation"])
        assert 0 < float(src["strong_other_lr_validation"]) < float(src["weak_other_lr_validation"]) < 1
        assert NEUTRAL_LR_MIN <= float(src["neutral_lr_validation"]) <= NEUTRAL_LR_MAX
        assert src["derivation_seed"] == 20260829
        assert src["split"] == "derived-calibration/validation"


def test_frozen_d0_has_no_literal_strength_labels_in_core_weak_cues(tmp_path):
    module = _materializer()
    data_path = module.materialize(tmp_path / "frozen_d0.jsonl")
    scenarios = load_scenarios(data_path, require_external_source=True)
    for s in scenarios:
        text = (s.weak_target_evidence + " " + s.weak_other_evidence).lower()
        assert "weak evidence" not in text
        assert "weak support" not in text
