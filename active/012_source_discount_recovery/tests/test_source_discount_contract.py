from __future__ import annotations

import json
from pathlib import Path
import pytest

from source_discount_g0.data import validate_record
from source_discount_g0.metrics import compute_direction_features
from source_discount_g0.prompts import context_text, message_block
from source_discount_g0.run import run


def row() -> dict:
    r = {
        "scenario_id": "s1", "domain": "diagnostics", "background": "A binary diagnostic decision is pending.",
        "calibration_text": "External validation gives the source-specific conditional reporting rates used to compute the stored likelihood ratios.",
        "target_hypothesis": "cooling fault", "other_hypothesis": "power fault",
        "target_action": "inspect cooling", "other_action": "inspect power",
        "high_source": "Lab A", "low_source": "Lab B",
        "high_source_profile": "On matched historical cases Lab A was correct 90% of the time.",
        "low_source_profile": "On matched historical cases Lab B was correct 60% of the time.",
        "high_source_reliability": 0.90, "low_source_reliability": 0.60,
        "low_target_lr": 1.5, "high_target_lr": 5.0,
        "low_other_lr": 0.67, "high_other_lr": 0.20,
        "target_message": "The observed pattern is the pattern associated with a cooling fault.",
        "other_message": "The observed pattern is the pattern associated with a power fault.",
        "short_delay_text": "The operator records unrelated maintenance notes.",
        "long_delay_text": "Several unrelated maintenance, scheduling, and inventory notes are reviewed before returning to the case.",
        "high_source_reinstatement": "Recall that the earlier message came from Lab A, whose audited record is the stronger one.",
        "low_source_reinstatement": "Recall that the earlier message came from Lab B, whose audited record is the weaker one.",
        "high_source_length_control": "Before answering, recall the administrative context surrounding the earlier report and continue with the same case.",
        "low_source_length_control": "Before answering, recall the administrative context surrounding the earlier report and continue with the same case.",
        "source": {"dataset": "external", "record_id": "1", "license": "CC-BY", "split": "test", "url": "https://example.org", "provenance": "external-derived"},
    }
    for k in (
        "binary_hypotheses_exclusive_gold", "binary_hypotheses_exhaustive_gold", "message_direction_gold",
        "same_message_content_across_sources_gold", "source_reliability_above_chance_gold", "source_reliability_order_gold",
        "directional_likelihood_ratios_valid_gold", "calibration_matches_likelihood_ratios_gold", "source_profiles_hypothesis_neutral_gold",
        "source_identity_content_independent_gold", "delay_material_message_neutral_gold", "delay_material_source_neutral_gold",
        "short_and_long_delays_natural_gold", "reinstatement_does_not_repeat_message_gold",
        "reinstatement_only_restores_source_metadata_gold", "matched_length_control_semantically_inert_gold",
        "direction_pair_matched_gold", "actions_symmetric_gold", "natural_setting_gold",
    ):
        r[k] = True
    return r


def cfg() -> dict:
    return {
        "support_gate": {"min_low_positive_probability": .8, "min_high_positive_probability": .8,
                         "min_high_gt_low_probability": .75, "min_probe_variant_probability": .65},
        "memory_gate": {"min_mean_probe_probability": .8, "min_probe_variant_probability": .65},
        "strong_case": {"min_belief_low_initial_influence": .02, "min_belief_high_initial_influence": .08,
                        "min_action_low_initial_influence": .015, "min_action_high_initial_influence": .06,
                        "min_belief_initial_discount_gap": .05, "min_action_initial_discount_gap": .04,
                        "min_belief_low_rebound": .04, "min_action_low_rebound": .03,
                        "min_belief_gap_shrink": .04, "min_action_gap_shrink": .03,
                        "min_high_source_retention_fraction": .6,
                        "min_belief_reinstatement_gain": .03, "min_action_reinstatement_gain": .02,
                        "min_belief_selective_reinstatement": .025, "min_action_selective_reinstatement": .015,
                        "max_matched_length_gap_change": .025, "max_no_message_baseline_drift": .08,
                        "min_variant_signature_fraction": .75},
    }


def good_inputs():
    support = {"low_positive": .95, "high_positive": .97, "high_gt_low": .94}
    memory = {(s,d,p): .95 for s in ("low","high") for d in ("short","long") for p in ("source_identity","message_direction","source_credibility")}
    readouts = {}
    variants = {}
    for kind in ("belief", "action"):
        readouts[kind] = {
            "baseline_immediate": .50, "baseline_long": .51,
            "low_immediate": .08, "high_immediate": .20,
            "low_long": .14, "high_long": .19,
            "low_long_reinstated": .08, "high_long_reinstated": .20,
            "low_long_length": .14, "high_long_length": .19,
        }
        variants[kind] = {
            "initial_gap": [.12, .11, .12, .10],
            "low_rebound": [.06, .05, .06, .05],
            "gap_shrink": [.07, .06, .07, .05],
            "selective_reinstatement": [.07, .06, .07, .05],
        }
    return support, memory, readouts, variants


def test_valid_record_and_directional_lr_guard():
    s = validate_record(row())
    assert s.low_target_lr > 1 and s.high_target_lr > s.low_target_lr
    bad = row(); bad["low_target_lr"] = 0.9
    with pytest.raises(ValueError, match="target-support LRs"):
        validate_record(bad)


def test_below_chance_source_rejected_even_if_called_low_credibility():
    bad = row(); bad["low_source_reliability"] = .40
    with pytest.raises(ValueError, match="0.5 < low reliability"):
        validate_record(bad)


def test_same_message_content_is_used_for_high_and_low_source():
    s = validate_record(row())
    low = message_block(s, direction="supports_target", source="low")
    high = message_block(s, direction="supports_target", source="high")
    assert s.target_message in low and s.target_message in high
    assert s.other_message not in low and s.other_message not in high


def test_reinstatement_does_not_repeat_message():
    bad = row(); bad["low_source_reinstatement"] = bad["target_message"]
    with pytest.raises(ValueError, match="must not repeat message"):
        validate_record(bad)


def test_no_message_long_contains_delay_but_no_case_message():
    s = validate_record(row())
    text = context_text(s, direction="supports_target", condition="no_message_long")
    assert s.long_delay_text in text
    assert s.target_message not in text and s.other_message not in text


def test_injected_recovery_signature_passes_direction_logic():
    support, memory, readouts, variants = good_inputs()
    f = compute_direction_features(support=support, support_min=.9, memory=memory, memory_min=.9,
                                   readouts=readouts, variant_readouts=variants, cfg=cfg())
    assert f["support_gate"] and f["memory_gate"] and f["weighting_capability"]
    assert f["recovery"] and f["reinstatement"] and f["strong"]


def test_no_recovery_cannot_be_strong():
    support, memory, readouts, variants = good_inputs()
    for kind in ("belief", "action"):
        readouts[kind]["low_long"] = readouts[kind]["low_immediate"]
        readouts[kind]["high_long"] = readouts[kind]["high_immediate"]
        variants[kind]["low_rebound"] = [0,0,0,0]
        variants[kind]["gap_shrink"] = [0,0,0,0]
    f = compute_direction_features(support=support, support_min=.9, memory=memory, memory_min=.9,
                                   readouts=readouts, variant_readouts=variants, cfg=cfg())
    assert not f["recovery"] and not f["strong"]


def test_memory_failure_at_short_delay_blocks_capability():
    support, memory, readouts, variants = good_inputs()
    memory[("low", "short", "source_identity")] = .4
    f = compute_direction_features(support=support, support_min=.9, memory=memory, memory_min=.4,
                                   readouts=readouts, variant_readouts=variants, cfg=cfg())
    assert not f["memory_gate"] and not f["weighting_capability"]


def test_generic_high_source_decay_blocks_strong_signature():
    support, memory, readouts, variants = good_inputs()
    for kind in ("belief", "action"):
        readouts[kind]["high_long"] = .02
    f = compute_direction_features(support=support, support_min=.9, memory=memory, memory_min=.9,
                                   readouts=readouts, variant_readouts=variants, cfg=cfg())
    assert not f["generic_delay_ok"] and not f["strong"]


def test_matched_length_restoration_blocks_selective_reinstatement():
    support, memory, readouts, variants = good_inputs()
    for kind in ("belief", "action"):
        readouts[kind]["low_long_length"] = readouts[kind]["low_long_reinstated"]
        readouts[kind]["high_long_length"] = readouts[kind]["high_long_reinstated"]
        variants[kind]["selective_reinstatement"] = [0,0,0,0]
    f = compute_direction_features(support=support, support_min=.9, memory=memory, memory_min=.9,
                                   readouts=readouts, variant_readouts=variants, cfg=cfg())
    assert not f["reinstatement"] and not f["strong"]


def test_authorization_blocks_before_data_or_model_construction(tmp_path: Path):
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps({"validation_authorized": False}))
    with pytest.raises(PermissionError):
        run(data_path=str(tmp_path/"missing.jsonl"), out_path=str(tmp_path/"out.jsonl"),
            config_path=str(cfg_path), model_name="should-not-load", family="Qwen", size_b=8)
