import json
from pathlib import Path
from weak_evidence_g0.metrics import summarize
from weak_evidence_g0.prompts import CONDITIONS,DIRECTIONS,READOUT_TEMPLATES
from weak_evidence_g0.run import SUPPORT_PROBES
from test_contract import record

def test_end_to_end_bidirectional_summary(tmp_path):
    row=record("external-derived");data=tmp_path/"d.jsonl";data.write_text(json.dumps(row)+"\n");meta={"model":"m","family":"Qwen","revision":"r","size_b":8,"requested_dtype":"bfloat16"};results=[]
    for d in DIRECTIONS:
        for p in SUPPORT_PROBES:
            for o in (0,1):results.append({**meta,"kind":"support_probe","scenario_id":"machine:1","domain":"diagnostics","direction":d,"probe":p,"label_order":o,"p_correct":.95})
    vals={"supports_target":{"belief":{"no_evidence":.55,"weak":.45,"strong":.76,"neutral":.55,"no_evidence_complete":.55,"weak_complete":.47,"length_control":.55,"weak_length":.46},"action":{"no_evidence":.52,"weak":.47,"strong":.72,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.48,"length_control":.52,"weak_length":.48}},"supports_other":{"belief":{"no_evidence":.55,"weak":.65,"strong":.34,"neutral":.55,"no_evidence_complete":.55,"weak_complete":.63,"length_control":.55,"weak_length":.64},"action":{"no_evidence":.52,"weak":.57,"strong":.32,"neutral":.52,"no_evidence_complete":.52,"weak_complete":.56,"length_control":.52,"weak_length":.56}}}
    for d in DIRECTIONS:
        for tid,(kind,_) in enumerate(READOUT_TEMPLATES):
            for c in CONDITIONS:
                for o in (0,1):results.append({**meta,"kind":"readout","scenario_id":"machine:1","domain":"diagnostics","direction":d,"condition":c,"template_id":tid,"template_kind":kind,"label_order":o,"p_target":vals[d][kind][c]})
    rp=tmp_path/"r.jsonl";rp.write_text("".join(json.dumps(x)+"\n" for x in results));cfg=Path(__file__).parents[1]/"configs"/"frozen_g0.json";s=summarize(data_path=str(data),results_path=str(rp),config_path=str(cfg));assert len(s["directions"])==2 and all(x["support_gate"] and x["capability_gate"] and x["strong"] for x in s["directions"]);assert s["scenario_pairs"][0]["belief_backfire_mean"]>0;assert s["model_pass"] is False
