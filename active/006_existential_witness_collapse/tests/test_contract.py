import json
from pathlib import Path
import pytest

from witness_collapse_g0.data import validate_record
from witness_collapse_g0.metrics import bootstrap_ci, compute_case_features, summarize
from witness_collapse_g0.prompts import CONDITIONS, DOWNSTREAM_TEMPLATES, YES_NO_ORDERS, recognition_prompt
from witness_collapse_g0.run import RECOGNITION_PROBES, _require_authorized


def record(provenance="synthetic"):
    source={"dataset":"unit","record_id":"1","license":"test","split":"test","provenance":provenance}
    if provenance != "synthetic": source["citation"]="unit fixture"
    return {
        "scenario_id":"staff:1","domain":"staffing",
        "premise_p":"At least one technician inspected the cooling system.",
        "premise_q":"At least one technician inspected the power system.",
        "premise_paraphrase":"The logs confirm a cooling inspection by a technician and a power inspection by a technician.",
        "p_property":"inspected the cooling system","q_property":"inspected the power system",
        "shared_requirement":"One technician must personally have inspected both systems.",
        "decision_context":"A manager must decide whether that staffing fact is already confirmed.",
        "same_witness_addendum":"The log explicitly states that the same technician performed both inspections.",
        "distinct_witness_addendum":"The log explicitly states that the two recorded inspections were performed by different technicians.",
        "neutral_addendum":"Both entries were filed on the same afternoon.",
        "p_exists_gold":True,"q_exists_gold":True,"shared_witness_not_entailed_gold":True,
        "identity_underdetermined_gold":True,"same_explicit_establishes_gold":True,
        "distinct_explicit_does_not_establish_gold":True,"paraphrase_equivalent_gold":True,
        "neutral_control_equivalent_gold":True,"matched_base_gold":True,"natural_setting_gold":True,
        "source":source,
    }


def feature_cfg():
    return {
        "recognition_gate":{"min_existence_probability":.8,"min_no_shared_entailment_probability":.8,"min_identity_underdetermined_probability":.75},
        "capability_gate":{"min_same_explicit_established_probability":.7,"max_distinct_explicit_established_probability":.3},
        "strong_case":{"min_unknown_established_probability":.55,"min_paraphrase_established_probability":.55,"min_unknown_minus_distinct":.15,"max_neutral_abs_shift":.05,"min_natural_variant_positive_fraction":.75},
    }


def test_d0_rejects_custom_only_and_requires_no_shared_entailment_gold():
    assert validate_record(record(), require_external_source=False).scenario_id == "staff:1"
    with pytest.raises(ValueError, match="custom-only"):
        validate_record(record(), require_external_source=True)
    bad=record(); bad["shared_witness_not_entailed_gold"]=False
    with pytest.raises(ValueError, match="D0 gold"):
        validate_record(bad, require_external_source=False)


def test_shared_entailment_gold_is_no_under_both_label_orders():
    labels=[]
    for mapping in YES_NO_ORDERS:
        _,correct=recognition_prompt(premise_p="At least one analyst reviewed A.",premise_q="At least one analyst reviewed B.",p_property="reviewed A",q_property="reviewed B",probe="shared_entailment",mapping=mapping)
        labels.append(correct)
    assert labels == ["B","A"]


def test_quantifier_failure_cannot_count_as_witness_collapse():
    good=compute_case_features(
        recognition={"p_exists":.95,"q_exists":.95,"shared_entailment":.9,"identity_determined":.9},
        p={"unknown":.70,"paraphrase":.68,"same_explicit":.95,"distinct_explicit":.08,"neutral_control":.69,"relation_reminder":.20},
        variant_unknown=[.68,.72,.66,.74],variant_paraphrase=[.66,.70,.64,.72],cfg=feature_cfg())
    assert good["capability_gate"] and good["strong"] and good["unknown_margin"]>0
    bad=compute_case_features(
        recognition={"p_exists":.95,"q_exists":.95,"shared_entailment":.2,"identity_determined":.2},
        p={"unknown":.85,"paraphrase":.85,"same_explicit":.95,"distinct_explicit":.05,"neutral_control":.85,"relation_reminder":.10},
        variant_unknown=[.8]*4,variant_paraphrase=[.8]*4,cfg=feature_cfg())
    assert not bad["recognition_gate"] and not bad["strong"]


def test_bootstrap_and_authorization_guard(tmp_path):
    lo,hi=bootstrap_ci([.05,.1,.15,.2],seed=7,n_boot=500)
    assert lo>0 and hi>=lo
    cfg=tmp_path/"cfg.json"; cfg.write_text('{"validation_authorized": false}')
    with pytest.raises(PermissionError, match="not authorized"):
        _require_authorized(str(cfg))


def test_end_to_end_summary_preserves_gate_before_illegal_join(tmp_path):
    data=tmp_path/"data.jsonl"; data.write_text(json.dumps(record("external-derived"))+"\n")
    meta={"model":"m","family":"Qwen","revision":"r","size_b":8,"requested_dtype":"bfloat16"}
    results=[]
    for probe in RECOGNITION_PROBES:
        for order in (0,1):
            results.append({**meta,"kind":"recognition","scenario_id":"staff:1","domain":"staffing","probe":probe,"label_order":order,"p_correct":.95})
    probs={"unknown":.70,"paraphrase":.68,"same_explicit":.96,"distinct_explicit":.08,"neutral_control":.69,"relation_reminder":.20}
    for condition in CONDITIONS:
        for template_id in range(len(DOWNSTREAM_TEMPLATES)):
            for order in (0,1):
                results.append({**meta,"kind":"downstream","scenario_id":"staff:1","domain":"staffing","condition":condition,"template_id":template_id,"label_order":order,"p_established":probs[condition]})
    rp=tmp_path/"results.jsonl"; rp.write_text("".join(json.dumps(x)+"\n" for x in results))
    cfg=Path(__file__).parents[1]/"configs"/"frozen_g0.json"
    summary=summarize(data_path=str(data),results_path=str(rp),config_path=str(cfg))
    case=summary["cases"][0]
    assert case["recognition_gate"] and case["capability_gate"] and case["strong"]
    assert summary["model_pass"] is False
