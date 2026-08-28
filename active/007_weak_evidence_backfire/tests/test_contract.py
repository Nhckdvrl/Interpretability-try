import json
import pytest
from weak_evidence_g0.data import validate_record
from weak_evidence_g0.metrics import signed_update, compute_direction_features, bootstrap_ci
from weak_evidence_g0.prompts import YES_NO_ORDERS, condition_text, support_prompt
from weak_evidence_g0.run import _require_authorized


def record(provenance="synthetic"):
    source = {"dataset": "unit", "record_id": "1", "license": "test", "split": "test", "provenance": provenance}
    if provenance != "synthetic":
        source["citation"] = "unit fixture"
    return {
        "scenario_id": "machine:1",
        "domain": "diagnostics",
        "background": "A fault is either cooling-related or power-related.",
        "calibration_text": "For TARGET versus OTHER, Cue T has likelihood ratio 1.38, Cue O 0.72, Marker T 5.67, Marker O 0.176, and Cue N 1.0.",
        "target_hypothesis": "cooling fault",
        "other_hypothesis": "power fault",
        "target_action": "run cooling follow-up",
        "other_action": "run power follow-up",
        "weak_target_evidence": "Cue T was observed.",
        "weak_other_evidence": "Cue O was observed.",
        "strong_target_evidence": "Marker T was observed.",
        "strong_other_evidence": "Marker O was observed.",
        "neutral_evidence": "Cue N was observed.",
        "pragmatic_completeness_text": "Only the scheduled cue is displayed in this comparison; omission of other possible cues conveys no information.",
        "matched_length_control_text": "The scheduled reporting field is displayed in the standard format used for this comparison.",
        "weak_target_lr": 1.38,
        "weak_other_lr": .72,
        "strong_target_lr": 5.67,
        "strong_other_lr": .176,
        "neutral_lr": 1.0,
        "calibration_valid_gold": True,
        "weak_target_support_gold": True,
        "weak_other_support_gold": True,
        "strong_target_support_gold": True,
        "strong_other_support_gold": True,
        "neutral_gold": True,
        "pragmatic_completeness_gold": True,
        "matched_length_control_gold": True,
        "actions_symmetric_gold": True,
        "hypotheses_exclusive_gold": True,
        "hypotheses_exhaustive_gold": True,
        "binary_choice_well_defined_gold": True,
        "core_wording_does_not_label_strength_gold": True,
        "direction_pair_matched_gold": True,
        "strong_weak_relation_comparable_gold": True,
        "neutral_control_matched_gold": True,
        "baseline_contains_no_case_specific_evidence_gold": True,
        "natural_setting_gold": True,
        "source": source,
    }


def cfg():
    return {
        "support_gate": {
            "min_support_probability": .8,
            "min_likelihood_relation_probability": .8,
            "min_complete_support_probability": .8,
            "min_strong_support_probability": .8,
            "min_strong_gt_weak_probability": .75,
            "min_neutral_non_support_probability": .75,
            "min_probe_variant_probability": .65,
        },
        "capability_gate": {
            "min_strong_belief_directional_shift": .08,
            "min_strong_action_directional_shift": .05,
            "min_strong_variant_positive_fraction": .75,
        },
        "strong_case": {
            "min_belief_backfire": .04,
            "min_action_backfire": .02,
            "min_complete_belief_backfire": .03,
            "min_complete_action_backfire": .02,
            "min_length_belief_backfire": .03,
            "min_length_action_backfire": .02,
            "max_neutral_abs_shift": .04,
            "min_primary_variant_backfire_fraction": .75,
            "min_control_variant_backfire_fraction": .75,
        },
    }


def readouts_target():
    return {
        "belief": {"no_evidence": .55, "weak": .45, "strong": .78, "neutral": .56, "no_evidence_complete": .55, "weak_complete": .47, "no_evidence_length": .55, "weak_length": .46},
        "action": {"no_evidence": .52, "weak": .47, "strong": .72, "neutral": .52, "no_evidence_complete": .52, "weak_complete": .48, "no_evidence_length": .52, "weak_length": .48},
    }


def support_scores():
    return {"support": .93, "likelihood_relation": .96, "support_complete": .92, "strong_support": .98, "strong_gt_weak": .95, "neutral_non_support": .95}


def variants_target():
    return {
        "belief": {"weak": [.11, .09, .10, .10], "weak_complete": [.08, .07, .09, .08], "weak_length": [.09, .08, .10, .09]},
        "action": {"weak": [.05, .04, .06, .05], "weak_complete": [.04, .03, .05, .04], "weak_length": [.04, .03, .05, .04]},
    }


def strong_variants_target():
    return {"belief": [.20, .22, .24, .23], "action": [.18, .19, .21, .20]}


def test_data_contract_and_external_gate():
    scenario = validate_record(record(), require_external_source=False)
    assert 1 < scenario.weak_target_lr < scenario.strong_target_lr
    assert 0 < scenario.strong_other_lr < scenario.weak_other_lr < 1
    with pytest.raises(ValueError, match="custom-only"):
        validate_record(record(), require_external_source=True)


def test_binary_readout_requires_exhaustive_hypotheses():
    row = record()
    row["hypotheses_exhaustive_gold"] = False
    with pytest.raises(ValueError, match="hypotheses_exhaustive_gold"):
        validate_record(row, require_external_source=False)


def test_reject_literal_strength_label_and_wrong_lr():
    row = record()
    row["weak_target_evidence"] = "This is weak evidence for cooling."
    with pytest.raises(ValueError, match="must not explicitly label"):
        validate_record(row, require_external_source=False)
    row = record()
    row["weak_target_lr"] = .9
    with pytest.raises(ValueError, match="1 < weak < strong"):
        validate_record(row, require_external_source=False)


def test_no_evidence_baseline_contains_no_negative_observation():
    scenario = validate_record(record(), require_external_source=False)
    text = condition_text(scenario, direction="supports_target", condition="no_evidence")
    assert "OBSERVATION:" not in text
    assert "No case-specific cue is observed" not in text


def test_sign_coding_is_symmetric():
    assert signed_update("supports_target", .45, .55) < 0
    assert signed_update("supports_other", .65, .55) < 0
    assert signed_update("supports_target", .75, .55) > 0
    assert signed_update("supports_other", .30, .55) > 0


def test_true_backfire_requires_support_strong_capability_and_protocol_controls():
    result = compute_direction_features(
        direction="supports_target",
        support=support_scores(),
        support_min_variant=.90,
        readouts=readouts_target(),
        variants=variants_target(),
        strong_variants=strong_variants_target(),
        cfg=cfg(),
    )
    assert result["support_gate"] and result["capability_gate"]
    assert result["pragmatic_robust"] and result["length_robust"] and result["strong"]


def test_control_variant_failure_cannot_hide_in_aggregate():
    variants = variants_target()
    variants["belief"]["weak_complete"] = [.08, .08, -.02, -.02]
    variants["action"]["weak_complete"] = [.04, .04, -.01, -.01]
    result = compute_direction_features(
        direction="supports_target",
        support=support_scores(),
        support_min_variant=.90,
        readouts=readouts_target(),
        variants=variants,
        strong_variants=strong_variants_target(),
        cfg=cfg(),
    )
    assert not result["pragmatic_robust"]
    assert not result["strong"]


def test_denied_support_or_neutral_misread_cannot_count():
    support = support_scores()
    support["neutral_non_support"] = .2
    result = compute_direction_features(
        direction="supports_target",
        support=support,
        support_min_variant=.2,
        readouts=readouts_target(),
        variants=variants_target(),
        strong_variants=strong_variants_target(),
        cfg=cfg(),
    )
    assert not result["support_gate"] and not result["strong"]


def test_support_prompt_label_order_bootstrap_and_auth(tmp_path):
    labels = []
    for mapping in YES_NO_ORDERS:
        _, correct = support_prompt(
            base="BACKGROUND:\nX",
            weak_evidence="Cue T was observed.",
            strong_evidence="Marker T was observed.",
            neutral_evidence="Cue N was observed.",
            focal_hypothesis="H",
            other_hypothesis="not-H",
            probe="support",
            mapping=mapping,
            pragmatic_text="Omission carries no information.",
        )
        labels.append(correct)
    assert labels == ["A", "B"]
    lo, hi = bootstrap_ci([.02, .04, .08, .10], seed=3, n_boot=500)
    assert lo > 0 and hi >= lo
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps({"validation_authorized": False}), encoding="utf-8")
    with pytest.raises(PermissionError, match="not authorized"):
        _require_authorized(str(p))
