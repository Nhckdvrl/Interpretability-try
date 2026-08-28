import json,pytest
from pathlib import Path
from witness_collapse_g0.data import validate_record
from witness_collapse_g0.metrics import compute_case_features,summarize
from witness_collapse_g0.prompts import CONDITIONS,DOWNSTREAM_TEMPLATES,YES_NO_ORDERS,recognition_prompt
from witness_collapse_g0.run import RECOGNITION_PROBES,_require_authorized

def fixture(prov="synthetic"):
    src={"dataset":"unit","record_id":"1","license":"test","split":"test","provenance":prov}
    if prov!="synthetic":src["citation"]="fixture"
    return {"scenario_id":"staff:1","domain":"staffing","premise_p":"At least one technician inspected cooling.","premise_q":"At least one technician inspected power.","premise_paraphrase":"Logs show a technician inspected cooling and a technician inspected power.","p_property":"inspected cooling","q_property":"inspected power","shared_requirement":"One technician must have inspected both.","decision_context":"Decide whether that single-technician fact is confirmed.","same_witness_addendum":"The record explicitly states that one and the same technician is the cooling inspector and the power inspector.","distinct_witness_addendum":"The complete staffing record states that no technician inspected both systems; the cooling-inspection and power-inspection personnel sets are disjoint.","neutral_addendum":"Both logs were filed today.","p_exists_gold":True,"q_exists_gold":True,"shared_witness_not_entailed_gold":True,"identity_underdetermined_gold":True,"same_explicit_establishes_gold":True,"distinct_explicit_blocks_shared_gold":True,"paraphrase_equivalent_gold":True,"neutral_control_equivalent_gold":True,"matched_base_gold":True,"natural_setting_gold":True,"source":src}
def cfg():return {"recognition_gate":{"min_existence_probability":.8,"min_no_shared_entailment_probability":.8,"min_identity_underdetermined_probability":.75},"capability_gate":{"min_same_explicit_established_probability":.7,"max_distinct_explicit_established_probability":.3},"strong_case":{"min_unknown_established_probability":.55,"min_paraphrase_established_probability":.55,"min_unknown_minus_distinct":.15,"max_neutral_abs_shift":.05,"min_natural_variant_positive_fraction":.75}}
def test_gold_and_external_gate():
    assert validate_record(fixture(),require_external_source=False).scenario_id=="staff:1"
    with pytest.raises(ValueError,match="custom-only"):validate_record(fixture(),require_external_source=True)
def test_blocking_distinct_gold_is_required():
    row=fixture();row["distinct_explicit_blocks_shared_gold"]=False
    with pytest.raises(ValueError,match="D0 gold"):validate_record(row,require_external_source=False)
def test_gate_before_illegal_join():
    p={"unknown":.70,"paraphrase":.68,"same_explicit":.95,"distinct_explicit":.08,"neutral_control":.69,"relation_reminder":.20};x=compute_case_features(recognition={"p_exists":.95,"q_exists":.95,"shared_entailment":.9,"identity_determined":.9},p=p,variant_unknown=[.7]*4,variant_paraphrase=[.68]*4,cfg=cfg());assert x["capability_gate"] and x["strong"] and x["unknown_margin"]>0
    y=compute_case_features(recognition={"p_exists":.95,"q_exists":.95,"shared_entailment":.2,"identity_determined":.2},p=p,variant_unknown=[.7]*4,variant_paraphrase=[.68]*4,cfg=cfg());assert not y["capability_gate"] and not y["strong"]
def test_label_order_and_authorization(tmp_path):
    labels=[recognition_prompt(premise_p="There is an A.",premise_q="There is a B.",p_property="A",q_property="B",probe="shared_entailment",mapping=m)[1] for m in YES_NO_ORDERS];assert labels==["B","A"]
    p=tmp_path/"c.json";p.write_text('{"validation_authorized":false}')
    with pytest.raises(PermissionError):_require_authorized(str(p))
def test_summary_contract(tmp_path):
    row=fixture("external-derived");d=tmp_path/"d.jsonl";d.write_text(json.dumps(row)+"\n");meta={"model":"m","family":"Qwen","revision":"r","size_b":8,"requested_dtype":"bfloat16"};rows=[]
    for probe in RECOGNITION_PROBES:
        for o in (0,1):rows.append({**meta,"kind":"recognition","scenario_id":"staff:1","domain":"staffing","probe":probe,"label_order":o,"p_correct":.95})
    probs={"unknown":.70,"paraphrase":.68,"same_explicit":.96,"distinct_explicit":.08,"neutral_control":.69,"relation_reminder":.20}
    for c in CONDITIONS:
        for t in range(len(DOWNSTREAM_TEMPLATES)):
            for o in (0,1):rows.append({**meta,"kind":"downstream","scenario_id":"staff:1","domain":"staffing","condition":c,"template_id":t,"label_order":o,"p_established":probs[c]})
    r=tmp_path/"r.jsonl";r.write_text("".join(json.dumps(x)+"\n" for x in rows));conf=Path(__file__).parents[1]/"configs"/"frozen_g0.json";s=summarize(data_path=str(d),results_path=str(r),config_path=str(conf));assert s["cases"][0]["strong"] and not s["model_pass"]
