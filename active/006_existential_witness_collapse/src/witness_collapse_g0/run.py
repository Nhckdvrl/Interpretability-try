from __future__ import annotations
from pathlib import Path
import json
from .data import load_scenarios
from .prompts import CONDITIONS,DOWNSTREAM_TEMPLATES,OUTCOME_ORDERS,YES_NO_ORDERS,condition_text,downstream_prompt,recognition_prompt
from .scoring import HFChoiceScorer
RECOGNITION_PROBES=("p_exists","q_exists","shared_entailment","identity_determined")
def _require_authorized(config_path:str)->dict:
    cfg=json.loads(Path(config_path).read_text(encoding="utf-8"))
    if cfg.get("validation_authorized") is not True: raise PermissionError("Formal model calls are not authorized by this frozen config. Do not bypass the N0/D0 gate; update authorization only after the authoritative registry is signed.")
    return cfg
def _write_jsonl(path:str,rows:list[dict])->None:
    p=Path(path);p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf-8") as f:
        for row in rows:f.write(json.dumps(row,ensure_ascii=False)+"\n")
def run(*,data_path:str,out_path:str,config_path:str,model_name:str,family:str,revision:str|None=None,dtype:str="auto",size_b:float|None=None,sequence_batch_size:int=64)->None:
    _require_authorized(config_path)
    if size_b is None or size_b<=0:raise ValueError("size_b must be explicitly provided and > 0")
    scenarios=load_scenarios(data_path,require_external_source=True);scorer=HFChoiceScorer(model_name,revision=revision,dtype=dtype);requests=[];metadata=[]
    for s in scenarios:
        for probe in RECOGNITION_PROBES:
            for oid,mapping in enumerate(YES_NO_ORDERS):
                prompt,correct=recognition_prompt(premise_p=s.premise_p,premise_q=s.premise_q,p_property=s.p_property,q_property=s.q_property,probe=probe,mapping=mapping);requests.append((prompt,("A","B")));metadata.append({"kind":"recognition","scenario_id":s.scenario_id,"domain":s.domain,"probe":probe,"label_order":oid,"correct_label":correct})
        contexts={c:condition_text(premise_p=s.premise_p,premise_q=s.premise_q,premise_paraphrase=s.premise_paraphrase,same_addendum=s.same_witness_addendum,distinct_addendum=s.distinct_witness_addendum,neutral_addendum=s.neutral_addendum,condition=c) for c in CONDITIONS}
        for tid,template in enumerate(DOWNSTREAM_TEMPLATES):
            for condition,context in contexts.items():
                for oid,mapping in enumerate(OUTCOME_ORDERS):
                    prompt,established=downstream_prompt(context=context,requirement=s.shared_requirement,decision_context=s.decision_context,template=template,mapping=mapping);requests.append((prompt,("A","B")));metadata.append({"kind":"downstream","scenario_id":s.scenario_id,"domain":s.domain,"condition":condition,"template_id":tid,"label_order":oid,"established_label":established})
    scores=scorer.score_batch(requests,sequence_batch_size=sequence_batch_size);rows=[]
    for meta,score in zip(metadata,scores):
        row=dict(meta);row.update({"model":model_name,"family":family,"revision":revision,"size_b":size_b,"requested_dtype":dtype,"label_probs":score.probs,"label_logprobs":score.logprobs});row["p_correct" if meta["kind"]=="recognition" else "p_established"]=score.probs[meta["correct_label"] if meta["kind"]=="recognition" else meta["established_label"]];rows.append(row)
    _write_jsonl(out_path,rows)
