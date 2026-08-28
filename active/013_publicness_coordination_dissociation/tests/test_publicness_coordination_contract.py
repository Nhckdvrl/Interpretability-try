from __future__ import annotations

import json
from pathlib import Path
import pytest

from publicness_coordination_g0.data import validate_record
from publicness_coordination_g0.metrics import compute_participant_features
from publicness_coordination_g0.prompts import action_prompt, capability_prompt, ACTION_ORDERS, ACTION_TEMPLATES, YES_NO_ORDERS
from publicness_coordination_g0.run import run


def row() -> dict:
    r = {
        "scenario_id": "c1", "domain": "coordination",
        "background": "Two operators each choose whether to switch to a shared backup channel. The switch is beneficial only if both switch; switching alone is costly.",
        "proposition": "The primary channel will be unavailable at noon.",
        "participant_a": "Alice", "participant_b": "Bob",
        "coordinate_action_a": "Alice switches to the backup channel", "safe_action_a": "Alice stays on the primary channel",
        "coordinate_action_b": "Bob switches to the backup channel", "safe_action_b": "Bob stays on the primary channel",
        "private_event_text": "Alice and Bob each receive the proposition in separate private messages. Each can see only their own receipt and cannot observe whether the other received a message.",
        "public_event_text": "The proposition is announced in a joint meeting attended and visibly heard by both Alice and Bob; each can observe that the other heard the announcement.",
        "explicit_ck_text": "Both Alice and Bob know the proposition, each knows that the other knows it, and each knows that the other knows that both received it.",
        "private_paraphrase_text": "The same proposition is sent separately to Alice and Bob through private channels whose delivery is not mutually observable.",
        "public_paraphrase_text": "The same proposition is stated once in front of Alice and Bob while both can see that the other is present and hears it.",
        "explicit_ck_paraphrase_text": "The proposition is known by both participants, and this mutual receipt and knowledge is itself mutually known.",
        "private_length_text": "The proposition reaches Alice and Bob separately through private notifications; each sees their own notice, while the other's receipt remains unobservable to them.",
        "public_length_text": "The proposition reaches Alice and Bob together through a shared announcement; each sees the other present and can observe that the other receives it.",
        "explicit_ck_length_text": "The proposition is known to Alice and Bob together; each knows the other received and knows it, with that mutual receipt and knowledge mutually known.",
        "policy_gold_text": "Because unilateral switching is costly and successful switching requires both, common knowledge raises the normative incentive to coordinate relative to separate private receipt.",
        "source": {"dataset": "published-coordination-material", "record_id": "1", "license": "CC-BY", "split": "test", "url": "https://example.org", "provenance": "external-derived"},
    }
    for k in (
        "same_proposition_gold", "same_recipients_gold", "both_participants_first_order_know_gold",
        "private_receipts_not_mutually_observable_gold", "public_event_mutually_observable_gold",
        "public_event_common_knowledge_operator_valid_gold", "private_event_does_not_generate_common_knowledge_gold",
        "explicit_ck_states_epistemic_consequence_only_gold", "policy_direction_public_gt_private_gold",
        "policy_direction_ck_gt_private_gold", "policy_gold_independent_of_model_gold", "policy_gold_not_in_prompt_gold",
        "participant_roles_symmetric_gold", "action_payoffs_symmetric_gold", "paraphrase_semantics_preserved_gold",
        "length_control_semantics_preserved_gold", "length_control_approximately_matched_gold", "natural_setting_gold",
    ):
        r[k] = True
    return r


def cfg() -> dict:
    return {
        "capability_gate": {"min_mean_probe_probability": .8, "min_probe_variant_probability": .65},
        "strong_case": {"min_explicit_ck_gain": .10, "min_dissociation": .06, "max_public_use_ratio": .45,
                        "min_control_dissociation": .05, "max_control_public_use_ratio": .55,
                        "min_variant_signature_fraction": .75, "max_participant_dissociation_asymmetry": .08},
    }


def good_inputs():
    probes = ("self_knows_proposition", "other_knows_proposition_world", "event_publicly_observable", "knows_other_received", "knows_other_knows_self_received", "knows_other_knows_self_knows_other_received")
    capability = {(state, p): .95 for state in ("private", "public") for p in probes}
    action = {
        "primary": {"private": .30, "public": .33, "explicit_ck": .50},
        "paraphrase": {"private": .31, "public": .34, "explicit_ck": .50},
        "length": {"private": .29, "public": .32, "explicit_ck": .49},
    }
    variants = {}
    for v in ("primary", "paraphrase", "length"):
        variants[v] = {
            "ck_gain": [.20, .18, .19, .17],
            "dissociation": [.16, .14, .15, .13],
            "public_use_ratio": [.20, .22, .21, .24],
        }
    return capability, action, variants


def test_valid_record():
    s = validate_record(row())
    assert s.participant_a == "Alice" and s.participant_b == "Bob"


def test_policy_gold_is_never_in_action_prompt():
    s = validate_record(row())
    prompt, _ = action_prompt(s, who="a", state="public", version="primary", template=ACTION_TEMPLATES[0], mapping=ACTION_ORDERS[0])
    assert s.policy_gold_text not in prompt
    assert "normative incentive" not in prompt


def test_policy_gold_exact_leak_rejected():
    bad = row(); bad["background"] = bad["policy_gold_text"]
    with pytest.raises(ValueError, match="policy gold text"):
        validate_record(bad)


def test_length_control_mismatch_rejected():
    bad = row(); bad["private_length_text"] = "short"
    with pytest.raises(ValueError, match="not approximately matched"):
        validate_record(bad)


def test_private_and_public_capability_questions_have_opposite_higher_order_gold():
    s = validate_record(row())
    p_private, correct_private = capability_prompt(s, who="a", state="private", probe="knows_other_received", mapping=YES_NO_ORDERS[0])
    p_public, correct_public = capability_prompt(s, who="a", state="public", probe="knows_other_received", mapping=YES_NO_ORDERS[0])
    assert correct_private != correct_public
    assert "separate private messages" in p_private and "joint meeting" in p_public


def test_injected_report_use_dissociation_passes():
    capability, action, variants = good_inputs()
    f = compute_participant_features(capability=capability, capability_min=.9, action=action, variants=variants, cfg=cfg())
    assert f["capability_gate"] and f["action_capability"]
    assert f["target_dissociation"] and f["controls_robust"] and f["strong"]


def test_normal_publicness_use_is_a_null_not_a_positive():
    capability, action, variants = good_inputs()
    for v in action:
        action[v]["public"] = action[v]["explicit_ck"] - .01
        variants[v]["dissociation"] = [.01, .01, .01, .01]
        variants[v]["public_use_ratio"] = [.95, .95, .95, .95]
    f = compute_participant_features(capability=capability, capability_min=.9, action=action, variants=variants, cfg=cfg())
    assert f["action_capability"] and not f["target_dissociation"] and not f["strong"]


def test_tom_failure_blocks_interpretation():
    capability, action, variants = good_inputs()
    capability[("public", "knows_other_knows_self_received")] = .4
    f = compute_participant_features(capability=capability, capability_min=.4, action=action, variants=variants, cfg=cfg())
    assert not f["capability_gate"] and not f["action_capability"] and not f["strong"]


def test_explicit_ck_action_floor_blocks_interpretation():
    capability, action, variants = good_inputs()
    for v in action:
        action[v]["explicit_ck"] = action[v]["private"] + .02
        variants[v]["ck_gain"] = [.02]*4
    f = compute_participant_features(capability=capability, capability_min=.9, action=action, variants=variants, cfg=cfg())
    assert f["capability_gate"] and not f["action_capability"] and not f["strong"]


def test_paraphrase_or_length_failure_blocks_strong():
    capability, action, variants = good_inputs()
    action["paraphrase"]["public"] = action["paraphrase"]["explicit_ck"]
    variants["paraphrase"]["dissociation"] = [0,0,0,0]
    variants["paraphrase"]["public_use_ratio"] = [1,1,1,1]
    f = compute_participant_features(capability=capability, capability_min=.9, action=action, variants=variants, cfg=cfg())
    assert f["target_dissociation"] and not f["controls_robust"] and not f["strong"]


def test_authorization_blocks_before_data_or_model_construction(tmp_path: Path):
    cfg_path = tmp_path / "cfg.json"
    cfg_path.write_text(json.dumps({"validation_authorized": False}))
    with pytest.raises(PermissionError):
        run(data_path=str(tmp_path/"missing.jsonl"), out_path=str(tmp_path/"out.jsonl"),
            config_path=str(cfg_path), model_name="should-not-load", family="Qwen", size_b=8)
