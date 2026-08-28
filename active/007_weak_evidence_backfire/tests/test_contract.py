import json
from pathlib import Path
import pytest

from weak_evidence_g0.data import validate_record
from weak_evidence_g0.metrics import bootstrap_ci, compute_direction_features, signed_update, summarize
from weak_evidence_g0.prompts import CONDITIONS, DIRECTIONS, READOUT_TEMPLATES, YES_NO_ORDERS, support_prompt
from weak_evidence_g0.run import SUPPORT_PROBES, _require_authorized


def record(provenance="synthetic"):
    source={"dataset":"unit","record_id":"1","license":"test","split":"test","provenance":provenance}
    if provenance != "synthetic": source["citation"]="unit fixture"
    return {
        "scenario_id":"machine:1","domain":"diagnostics","background":"A machine fault is either a cooling fault or a power fault.",
        "calibration_text":"Cue T occurs more often with cooling faults; Cue O occurs more often with power faults; Cue N occurs equally often under both. Separate high-specificity cues are also calibrated.",
        "target_hypothesis":"cooling fault","other_hypothesis":"power fault","target_action":"run the cooling-system follow-up","other_action":"run the power-system follow-up",
        "weak_target_evidence":"Cue T was observed.","weak_other_evidence":"Cue O was observed.","strong_target_evidence":"The target-specific diagnostic marker was observed.","strong_other_evidence":"The alternative-specific diagnostic marker was observed.","neutral_evidence":"Cue N was observed.",
        "pragmatic_completeness_text":"The protocol reports exactly the scheduled cue; omission of any other cue conveys no information.","matched_length_control_text":"The protocol records the scheduled cue in the standard report field for this inspection.",
        "weak_target_lr":1.4,"weak_other_lr":.72,"strong_target_lr":4.0,"strong_other_lr":.25,"neutral_lr":1.0,
        "calibration_valid_gold":True,"weak_target_support_gold":True,"weak_other_support_gold":True,"strong_target_support_gold":True,"strong_other_support_gold":True,"neutral_gold":True,"pragmatic_completeness_gold":True,"matched_length_control_gold":True,"actions_symmetric_gold":True,"hypotheses_exclusive_gold":True,"core_wording_does_not_label_strength_gold":True,"natural_setting_gold":True,"source":source,
    }


def cfg():
    return {
        "support_gate":{"min_support_probability":.8,"min_likelihood_relation_probability":.8,"min_complete_support_probability":.8},
        "capability_gate":{"min_strong_directional_shift":.08},
        "strong_case":{"min_belief_backfire":.04,"min_action_backfire":.02,"min_complete_backfire":.03,"min_length_control_backfire":.03,"max_neutral_abs_shift":.04,"min_belief_variant_backfire_fraction":.75},
    }


def readouts_target():
    return {
        "belief":{"no_evidence":.55,"weak":.45,"strong":.78,"neutral":.56,"no_evidence_complete":.55,"weak_complete":.47,"no_evidence_length":.55,"weak_length":.46},
        "action":{"no_evidence":.52,"weak":.47,"strong":.72,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.48,"no_evidence_length":.52,"weak_length":.48},
    }


def test_likelihood_contract_and_custom_only_gate():
    s=validate_record(record(),require_external_source=False)
    assert 1<s.weak_target_lr<s.strong_target_lr and 0<s.strong_other_lr<s.weak_other_lr<1
    with pytest.raises(ValueError,match="custom-only"):
        validate_record(record(),require_external_source=True)


def test_rejects_explicit_strength_label_and_wrong_lr():
    row=record(); row["weak_target_evidence"]="A weak cue T was observed."
    with pytest.raises(ValueError,match="must not explicitly label"):
        validate_record(row,require_external_source=False)
    row=record(); row["weak_target_lr"]=.9
    with pytest.raises(ValueError,match="1 < weak < strong"):
        validate_record(row,require_external_source=False)


def test_sign_coding_is_symmetric():
    assert signed_update("supports_target",.45,.55)<0
    assert signed_update("supports_other",.65,.55)<0
    assert signed_update("supports_target",.75,.55)>0
    assert signed_update("supports_other",.30,.55)>0


def test_true_backfire_requires_support_and_strong_capability():
    variants={"belief":{"weak":[.44,.46,.45,.45]},"action":{"weak":[.46,.48,.47,.47]}}
    x=compute_direction_features(direction="supports_target",support={"support":.93,"likelihood_relation":.96,"support_complete":.92},readouts=readouts_target(),variants=variants,cfg=cfg())
    assert x["support_gate"] and x["capability_gate"] and x["pragmatic_robust"] and x["strong"]


def test_denied_support_cannot_count():
    variants={"belief":{"weak":[.4]*4},"action":{"weak":[.44]*4}}
    x=compute_direction_features(direction="supports_target",support={"support":.2,"likelihood_relation":.95,"support_complete":.2},readouts=readouts_target(),variants=variants,cfg=cfg())
    assert not x["support_gate"] and not x["capability_gate"] and not x["strong"]


def test_completeness_support_is_part_of_gate():
    variants={"belief":{"weak":[.45]*4},"action":{"weak":[.47]*4}}
    x=compute_direction_features(direction="supports_target",support={"support":.95,"likelihood_relation":.95,"support_complete":.20},readouts=readouts_target(),variants=variants,cfg=cfg())
    assert not x["support_gate"] and not x["capability_gate"] and not x["strong"]


def test_support_probe_label_order_and_bootstrap():
    labels=[]
    for mapping in YES_NO_ORDERS:
        _,correct=support_prompt(base="BACKGROUND:\nX",evidence="Cue was observed.",focal_hypothesis="H",other_hypothesis="not-H",probe="support",mapping=mapping,pragmatic_text="Omission carries no information.")
        labels.append(correct)
    assert labels==["A","B"]
    lo,hi=bootstrap_ci([.02,.04,.08,.10],seed=3,n_boot=500)
    assert lo>0 and hi>=lo


def test_authorization_guard(tmp_path):
    p=tmp_path/"cfg.json"; p.write_text('{"validation_authorized": false}')
    with pytest.raises(PermissionError,match="not authorized"):
        _require_authorized(str(p))


def test_end_to_end_summary_uses_directional_and_protocol_matched_baselines(tmp_path):
    row=record("external-derived")
    row["calibration_text"]="Cue T occurs in 58% of cooling faults and 42% of power faults. Cue O occurs in 42% of cooling faults and 58% of power faults. Marker T occurs in 85% versus 15%; marker O in 15% versus 85%. Cue N occurs in 50% of each."
    row["weak_target_lr"]=1.38; row["strong_target_lr"]=5.67; row["strong_other_lr"]=.176
    data=tmp_path/"data.jsonl"; data.write_text(json.dumps(row)+"\n")
    meta={"model":"m","family":"Qwen","revision":"r","size_b":8,"requested_dtype":"bfloat16"}; results=[]
    for direction in DIRECTIONS:
        for probe in SUPPORT_PROBES:
            for order in (0,1):
                results.append({**meta,"kind":"support_probe","scenario_id":"machine:1","domain":"diagnostics","direction":direction,"probe":probe,"label_order":order,"p_correct":.95})
    values={
        "supports_target":{"belief":{"no_evidence":.55,"weak":.45,"strong":.76,"neutral":.55,"no_evidence_complete":.55,"weak_complete":.47,"no_evidence_length":.55,"weak_length":.46},"action":{"no_evidence":.52,"weak":.47,"strong":.72,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.48,"no_evidence_length":.52,"weak_length":.48}},
        "supports_other":{"belief":{"no_evidence":.55,"weak":.65,"strong":.34,"neutral":.55,"no_evidence_complete":.55,"weak_complete":.63,"no_evidence_length":.55,"weak_length":.64},"action":{"no_evidence":.52,"weak":.57,"strong":.32,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.56,"no_evidence_length":.52,"weak_length":.56}},
    }
    for direction in DIRECTIONS:
        for template_id,(kind,_) in enumerate(READOUT_TEMPLATES):
            for condition in CONDITIONS:
                for order in (0,1):
                    results.append({**meta,"kind":"readout","scenario_id":"machine:1","domain":"diagnostics","direction":direction,"condition":condition,"template_id":template_id,"template_kind":kind,"label_order":order,"p_target":values[direction][kind][condition]})
    rp=tmp_path/"result.jsonl"; rp.write_text("".join(json.dumps(x)+"\n" for x in results))
    frozen=Path(__file__).parents[1]/"configs"/"frozen_g0.json"
    summary=summarize(data_path=str(data),results_path=str(rp),config_path=str(frozen))
    assert len(summary["directions"])==2
    assert all(x["support_gate"] and x["capability_gate"] and x["strong"] for x in summary["directions"])
    assert summary["scenario_pairs"][0]["belief_backfire_mean"]>0
    assert summary["model_pass"] is False
