import pytest
from witness_collapse_g0.data import validate_record


def record(provenance="synthetic"):
    source = {"dataset": "unit", "record_id": "1", "license": "test", "split": "test", "provenance": provenance}
    if provenance != "synthetic":
        source["citation"] = "unit fixture"
    return {
        "scenario_id": "staff:1",
        "domain": "staffing",
        "premise_p": "At least one technician inspected the cooling system.",
        "premise_q": "At least one technician inspected the power system.",
        "premise_paraphrase": "The logs confirm a cooling inspection by a technician and also a power inspection by a technician.",
        "p_property": "inspected the cooling system",
        "q_property": "inspected the power system",
        "shared_requirement": "One technician must personally have inspected both systems before sign-off.",
        "decision_context": "A compliance manager must decide whether the requirement can be signed off now.",
        "collapse_action": "Sign off the single-technician requirement as already satisfied.",
        "preserve_action": "Keep the requirement unresolved until witness identity is established.",
        "same_witness_addendum": "The log explicitly states that the same technician performed both inspections.",
        "distinct_witness_addendum": "The log explicitly states that the two inspections were performed by different technicians.",
        "neutral_addendum": "Both inspection entries were filed on the same afternoon.",
        "p_exists_gold": True,
        "q_exists_gold": True,
        "shared_witness_not_entailed_gold": True,
        "identity_underdetermined_gold": True,
        "joint_witness_possible_gold": True,
        "distinct_witness_possible_gold": True,
        "premises_do_not_identify_witnesses_gold": True,
        "same_explicit_authorizes_collapse_gold": True,
        "distinct_explicit_blocks_collapse_gold": True,
        "unknown_requires_identity_check_gold": True,
        "action_pair_matched_gold": True,
        "paraphrase_equivalent_gold": True,
        "neutral_control_equivalent_gold": True,
        "matched_base_gold": True,
        "natural_setting_gold": True,
        "source": source,
    }


def test_valid_synthetic_unit_record_when_external_not_required():
    s = validate_record(record(), require_external_source=False)
    assert s.collapse_action != s.preserve_action


def test_formal_loader_rejects_custom_only_data():
    with pytest.raises(ValueError, match="custom-only"):
        validate_record(record(), require_external_source=True)


def test_requires_both_same_and_distinct_to_be_logically_possible():
    row = record()
    row["joint_witness_possible_gold"] = False
    with pytest.raises(ValueError, match="D0 gold"):
        validate_record(row, require_external_source=False)
