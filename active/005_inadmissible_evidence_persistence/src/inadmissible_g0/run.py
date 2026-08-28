from __future__ import annotations
from pathlib import Path
import json
from .data import load_scenarios
from .prompts import BINARY_ORDERS, RECOGNITION_ORDERS, VERDICT_TEMPLATES, condition_text, verdict_prompt, recognition_prompt
from .scoring import HFChoiceScorer, VLLMChoiceScorer

def _write(path,rows):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        for r in rows: f.write(json.dumps(r,ensure_ascii=False)+"\n")

def run(*,data_path:str,out_path:str,model_name:str,family:str,revision:str|None=None,dtype:str="auto",size_b:float|None=None,sequence_batch_size:int=64,base_url:str|None=None,served_model:str|None=None)->None:
    if size_b is None or size_b<=0: raise ValueError("size_b must be explicitly provided and > 0")
    scenarios=load_scenarios(data_path,require_external_source=True); scorer=VLLMChoiceScorer(model_name,base_url=base_url,revision=revision,served_model=served_model) if base_url else HFChoiceScorer(model_name,revision=revision,dtype=dtype); requests=[]; meta=[]
    for s in scenarios:
        for probe in ("inadmissible","scope","polarity"):
            for oid,mapping in enumerate(RECOGNITION_ORDERS):
                prompt,correct=recognition_prompt(s.case_facts,s.evidence_text,s.struck_ruling,s.exclusion_scope,s.target_verdict,s.other_verdict,probe,mapping,s.evidence_polarity)
                requests.append((prompt,("A","B"))); meta.append({"kind":"recognition","scenario_id":s.scenario_id,"polarity_pair_id":s.polarity_pair_id,"domain":s.domain,"probe":probe,"label_order":oid,"correct_label":correct,"polarity":s.evidence_polarity})
        conditions=[("never_seen",condition_text(s.case_facts,"",None,"never_seen")),
                    ("admitted",condition_text(s.case_facts,s.evidence_text,s.admissible_ruling,"admitted")),
                    ("struck",condition_text(s.case_facts,s.evidence_text,s.struck_ruling,"struck",s.exclusion_scope)),
                    ("neutral_struck",condition_text(s.case_facts,s.neutral_evidence_text,s.neutral_struck_ruling,"neutral_struck",s.exclusion_scope))]
        for tid,(kind,template) in enumerate(VERDICT_TEMPLATES):
            for cond,ctx in conditions:
                for oid,mapping in enumerate(BINARY_ORDERS):
                    requests.append((verdict_prompt(ctx,s.target_verdict,s.other_verdict,template,mapping),("A","B")))
                    target_label=next(l for l,v in mapping.items() if v=="target")
                    meta.append({"kind":"verdict","scenario_id":s.scenario_id,"polarity_pair_id":s.polarity_pair_id,"domain":s.domain,"condition":cond,"template_id":tid,"template_kind":kind,"label_order":oid,"target_label":target_label,"polarity":s.evidence_polarity})
    scores=scorer.score_batch(requests,sequence_batch_size=sequence_batch_size); rows=[]
    for m,sc in zip(meta,scores):
        r=dict(m); r.update({"model":model_name,"family":family,"revision":revision,"size_b":size_b,"requested_dtype":dtype,"label_probs":sc.probs})
        r["p_correct" if m["kind"]=="recognition" else "p_target"]=sc.probs[m["correct_label"] if m["kind"]=="recognition" else m["target_label"]]; rows.append(r)
    _write(out_path,rows)
