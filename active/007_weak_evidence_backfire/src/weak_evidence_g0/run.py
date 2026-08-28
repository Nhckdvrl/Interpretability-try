from __future__ import annotations
from pathlib import Path
import json
from .data import load_scenarios
from .prompts import CHOICE_ORDERS, CONDITIONS, DIRECTIONS, READOUT_TEMPLATES, YES_NO_ORDERS, base_text, condition_text, evidence_for, readout_prompt, support_prompt
from .scoring import HFChoiceScorer
SUPPORT_PROBES=("support","likelihood_relation","support_complete","strong_support")

def _require_authorized(config_path:str)->dict:
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8"))
    if cfg.get("validation_authorized") is not True: raise PermissionError("Formal model calls are not authorized; independent N0 + D0 must sign the authoritative registry first.")
    return cfg

def _write(path,rows):
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        for r in rows:f.write(json.dumps(r,ensure_ascii=False)+"\n")

def run(*,data_path:str,out_path:str,config_path:str,model_name:str,family:str,revision:str|None=None,dtype:str="auto",size_b:float|None=None,sequence_batch_size:int=64)->None:
    _require_authorized(config_path)
    if size_b is None or size_b<=0: raise ValueError("size_b must be explicitly provided and > 0")
    ss=load_scenarios(data_path,require_external_source=True); scorer=HFChoiceScorer(model_name,revision=revision,dtype=dtype); req=[];meta=[]
    for s in ss:
        base=base_text(s.background,s.calibration_text)
        for direction in DIRECTIONS:
            focal=s.target_hypothesis if direction=="supports_target" else s.other_hypothesis; other=s.other_hypothesis if direction=="supports_target" else s.target_hypothesis
            for probe in SUPPORT_PROBES:
                ev=evidence_for(s,direction,"strong" if probe=="strong_support" else "weak")
                for oid,mapping in enumerate(YES_NO_ORDERS):
                    prompt,correct=support_prompt(base=base,evidence=ev,focal_hypothesis=focal,other_hypothesis=other,probe=probe,mapping=mapping,pragmatic_text=s.pragmatic_completeness_text)
                    req.append((prompt,("A","B")));meta.append({"kind":"support_probe","scenario_id":s.scenario_id,"domain":s.domain,"direction":direction,"probe":probe,"label_order":oid,"correct_label":correct})
            for tid,(kind,template) in enumerate(READOUT_TEMPLATES):
                target_text=s.target_hypothesis if kind=="belief" else s.target_action; other_text=s.other_hypothesis if kind=="belief" else s.other_action
                for condition in CONDITIONS:
                    ctx=condition_text(s,direction=direction,condition=condition)
                    for oid,mapping in enumerate(CHOICE_ORDERS):
                        prompt,target=readout_prompt(context=ctx,target_text=target_text,other_text=other_text,template=template,mapping=mapping)
                        req.append((prompt,("A","B")));meta.append({"kind":"readout","scenario_id":s.scenario_id,"domain":s.domain,"direction":direction,"condition":condition,"template_id":tid,"template_kind":kind,"label_order":oid,"target_label":target})
    scores=scorer.score_batch(req,sequence_batch_size=sequence_batch_size);rows=[]
    for m,sc in zip(meta,scores):
        r=dict(m);r.update({"model":model_name,"family":family,"revision":revision,"size_b":size_b,"requested_dtype":dtype,"label_probs":sc.probs,"label_logprobs":sc.logprobs})
        r["p_correct" if m["kind"]=="support_probe" else "p_target"]=sc.probs[m["correct_label"] if m["kind"]=="support_probe" else m["target_label"]];rows.append(r)
    _write(out_path,rows)
