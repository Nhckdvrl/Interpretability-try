import json
from pathlib import Path

import pytest

from witness_collapse_g0.data import validate_record
from witness_collapse_g0.metrics import compute_case_features, summarize
from witness_collapse_g0.prompts import CONDITIONS, DOWNSTREAM_TEMPLATES, SEMANTIC_ORDERS, recognition_prompt
from witness_collapse_g0.run import RECOGNITION_PROBES, _require_authorized
from test_data import record


def cfg():
    return {
        "recognition_gate": {
            "min_existence_probability": .8,
            "min_no_shared_entailment_probability": .8,
            "min_identity_underdetermined_probability": .75,
            "min_label_order_probability": .65,
        },
        "capability_gate": {
            "min_same_explicit_collapse_probability": .7,
            "max_distinct_explicit_collapse_probability": .3,
            "min_control_variant_success_fraction": .75,
        },
        "strong_case": {
            "min_unknown_collapse_probability": .55,
            "min_paraphrase_collapse_probability": .55,
            "min_unknown_minus_distinct": .15,
            "max_neutral_abs_shift": .05,
            "min_natural_variant_positive_fraction": .75,
        },
    }


def variants():
    return {
        "unknown": [.70] * 4,
        "paraphrase": [.68] * 4,
        "same_explicit": [.96] * 4,
        "distinct_explicit": [.08] * 4,
        "neutral_control": [.69] * 4,
        "relation_reminder": [.20] * 4,
    }


def test_gold_and_external_gate():
    assert validate_record(record(), require_external_source=False).scenario_id == "staff:1"
    with pytest.raises(ValueError, match="custom-only"):
        validate_record(record(), require_external_source=True)


def test_both_identity_worlds_are_required_by_data_contract():
    row = record()
    row["distinct_witness_possible_gold"] = False
    with pytest.raises(ValueError, match="D0 gold"):
        validate_record(row, require_external_source=False)


def test_gate_before_illegal_join():
    p = {
        "unknown": .70,
        "paraphrase": .68,
        "same_explicit": .96,
        "distinct_explicit": .08,
        "neutral_control": .69,
        "relation_reminder": .20,
    }
    x = compute_case_features(
        recognition={"p_exists": .95, "q_exists": .95, "shared_entailment": .9, "identity_determined": .9},
        recognition_min_variant=.85,
        p=p,
        variants=variants(),
        cfg=cfg(),
    )
    assert x["capability_gate"] and x["strong"] and x["unknown_margin"] > 0

    y = compute_case_features(
        recognition={"p_exists": .95, "q_exists": .95, "shared_entailment": .2, "identity_determined": .2},
        recognition_min_variant=.2,
        p=p,
        variants=variants(),
        cfg=cfg(),
    )
    assert not y["capability_gate"] and not y["strong"]


def test_semantic_order_and_authorization(tmp_path):
    labels = [
        recognition_prompt(
            premise_p="There is an A.",
            premise_q="There is a B.",
            p_property="A",
            q_property="B",
            probe="shared_entailment",
            mapping=mapping,
        )[1]
        for mapping in SEMANTIC_ORDERS
    ]
    assert labels == ["A", "B"]
    p = tmp_path / "c.json"
    p.write_text('{"validation_authorized": false}')
    with pytest.raises(PermissionError):
        _require_authorized(str(p))


def test_summary_contract(tmp_path):
    row = record("external-derived")
    data = tmp_path / "d.jsonl"
    data.write_text(json.dumps(row) + "\n")
    meta = {"model": "m", "family": "Qwen", "revision": "r", "size_b": 8, "requested_dtype": "bfloat16"}
    rows = []
    for probe in RECOGNITION_PROBES:
        for order in (0, 1):
            rows.append({**meta, "kind": "recognition", "scenario_id": "staff:1", "domain": "staffing", "probe": probe, "label_order": order, "p_correct": .95})
    probs = {"unknown": .70, "paraphrase": .68, "same_explicit": .96, "distinct_explicit": .08, "neutral_control": .69, "relation_reminder": .20}
    for condition in CONDITIONS:
        for template_id in range(len(DOWNSTREAM_TEMPLATES)):
            for order in (0, 1):
                rows.append({**meta, "kind": "downstream", "scenario_id": "staff:1", "domain": "staffing", "condition": condition, "template_id": template_id, "label_order": order, "p_collapse_action": probs[condition]})
    results = tmp_path / "r.jsonl"
    results.write_text("".join(json.dumps(x) + "\n" for x in rows))
    conf = Path(__file__).parents[1] / "configs" / "frozen_g0.json"
    summary = summarize(data_path=str(data), results_path=str(results), config_path=str(conf))
    assert summary["cases"][0]["strong"] and not summary["model_pass"]
