import pytest
from weak_evidence_g0.data import validate_record
from weak_evidence_g0.metrics import signed_update,compute_direction_features,bootstrap_ci
from weak_evidence_g0.prompts import YES_NO_ORDERS,condition_text,support_prompt
from weak_evidence_g0.run import _require_authorized

def record(provenance="synthetic"):
    src={"dataset":"unit","record_id":"1","license":"test","split":"test","provenance":provenance}
    if provenance!="synthetic":src["citation"]="unit fixture"
    return {"scenario_id":"machine:1","domain":"diagnostics","background":"A fault is either cooling-related or power-related.","calibration_text":"Cue T occurs 58% vs 42%; Cue O 42% vs 58%; Marker T 85% vs 15%; Marker O 15% vs 85%; Cue N and fillers occur 50% vs 50%.","target_hypothesis":"cooling fault","other_hypothesis":"power fault","target_action":"run cooling follow-up","other_action":"run power follow-up","weak_target_evidence":"Cue T was observed.","weak_other_evidence":"Cue O was observed.","strong_target_evidence":"Marker T was observed.","strong_other_evidence":"Marker O was observed.","neutral_evidence":"Cue N was observed.","pragmatic_completeness_text":"The protocol reports exactly the scheduled cue; omission of all other cues conveys no information.","target_length_control_evidence":"Code X was observed.","other_length_control_evidence":"Code Y was observed.","weak_target_lr":1.38,"weak_other_lr":.72,"strong_target_lr":5.67,"strong_other_lr":.176,"neutral_lr":1.0,"target_length_control_lr":1.0,"other_length_control_lr":1.0,"calibration_valid_gold":True,"weak_target_support_gold":True,"weak_other_support_gold":True,"strong_target_support_gold":True,"strong_other_support_gold":True,"neutral_gold":True,"pragmatic_completeness_gold":True,"matched_length_control_gold":True,"actions_symmetric_gold":True,"hypotheses_exclusive_gold":True,"core_wording_does_not_label_strength_gold":True,"natural_setting_gold":True,"source":src}
def cfg():return {"support_gate":{"min_support_probability":.8,"min_likelihood_relation_probability":.8,"min_complete_support_probability":.8,"min_strong_support_probability":.8},"capability_gate":{"min_strong_belief_directional_shift":.08,"min_strong_action_directional_shift":.05},"strong_case":{"min_belief_backfire":.04,"min_action_backfire":.02,"min_complete_belief_backfire":.03,"min_complete_action_backfire":.02,"min_length_belief_backfire":.03,"min_length_action_backfire":.02,"max_neutral_abs_shift":.04,"min_variant_backfire_fraction":.75}}
def readouts_target():return {"belief":{"no_evidence":.55,"weak":.45,"strong":.78,"neutral":.56,"no_evidence_complete":.55,"weak_complete":.47,"length_control":.55,"weak_length":.46},"action":{"no_evidence":.52,"weak":.47,"strong":.72,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.48,"length_control":.52,"weak_length":.48}}
def test_data_contract_and_external_gate():
    s=validate_record(record(),require_external_source=False);assert 1<s.weak_target_lr<s.strong_target_lr and 0<s.strong_other_lr<s.weak_other_lr<1 and s.target_length_control_lr==1
    with pytest.raises(ValueError,match="custom-only"):validate_record(record(),require_external_source=True)
def test_reject_strength_label_wrong_lr_and_informative_length_control():
    r=record();r["weak_target_evidence"]="A weak cue T was observed."
    with pytest.raises(ValueError,match="must not explicitly label"):validate_record(r,require_external_source=False)
    r=record();r["weak_target_lr"]=.9
    with pytest.raises(ValueError,match="1 < weak < strong"):validate_record(r,require_external_source=False)
    r=record();r["target_length_control_lr"]=1.1
    with pytest.raises(ValueError,match="must equal 1"):validate_record(r,require_external_source=False)
def test_length_control_is_direction_specific_observation():
    s=validate_record(record(),require_external_source=False);t=condition_text(s,direction="supports_target",condition="length_control");o=condition_text(s,direction="supports_other",condition="length_control");assert "Code X" in t and "Code Y" in o and t!=o
def test_sign_coding_is_symmetric():
    assert signed_update("supports_target",.45,.55)<0 and signed_update("supports_other",.65,.55)<0
    assert signed_update("supports_target",.75,.55)>0 and signed_update("supports_other",.30,.55)>0
def test_true_backfire_requires_support_strong_capability_and_protocol_controls():
    variants={"belief":{"weak":[.10,.08,.09,.07]},"action":{"weak":[.05,.04,.03,.02]}};x=compute_direction_features(direction="supports_target",support={"support":.93,"likelihood_relation":.96,"support_complete":.92,"strong_support":.98},readouts=readouts_target(),variants=variants,cfg=cfg());assert x["support_gate"] and x["capability_gate"] and x["pragmatic_robust"] and x["length_robust"] and x["strong"]
def test_denied_support_cannot_count():
    variants={"belief":{"weak":[.1]*4},"action":{"weak":[.05]*4}};x=compute_direction_features(direction="supports_target",support={"support":.2,"likelihood_relation":.95,"support_complete":.2,"strong_support":.95},readouts=readouts_target(),variants=variants,cfg=cfg());assert not x["support_gate"] and not x["capability_gate"] and not x["strong"]
def test_support_prompt_label_order_bootstrap_and_auth(tmp_path):
    labels=[]
    for mapping in YES_NO_ORDERS:
        _,correct=support_prompt(base="BACKGROUND:\nX",evidence="Cue was observed.",focal_hypothesis="H",other_hypothesis="not-H",probe="support",mapping=mapping,pragmatic_text="Omission carries no information.");labels.append(correct)
    assert labels==["A","B"];lo,hi=bootstrap_ci([.02,.04,.08,.10],seed=3,n_boot=500);assert lo>0 and hi>=lo
    p=tmp_path/"cfg.json";p.write_text('{"validation_authorized": false}')
    with pytest.raises(PermissionError,match="not authorized"):_require_authorized(str(p))
