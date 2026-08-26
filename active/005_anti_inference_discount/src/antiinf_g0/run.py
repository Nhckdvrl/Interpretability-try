from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from .dataset import load_scenarios
from .prompts import COMPREHENSION_TEMPLATES,NATURAL_JUDGMENT_TEMPLATES,BRIDGED_JUDGMENT_TEMPLATES,ChatPrompt,build_comprehension_prompt,build_natural_judgment_prompt,build_bridged_judgment_prompt
from .scoring import HFChoiceScorer


def run_g0(*,model_name:str,data_path:str|Path,out_path:str|Path,limit:int|None=None,sequence_batch_size:int=96,dtype:str="auto")->None:
    scenarios=load_scenarios(data_path,strict=limit is None)
    if limit is not None:
        if limit<=0: raise ValueError("--limit must be positive")
        scenarios=scenarios[:limit]
    scorer=HFChoiceScorer(model_name=model_name,dtype=dtype); requests:list[tuple[ChatPrompt,tuple[str,...]]]=[]; metadata:list[dict[str,Any]]=[]
    for s in scenarios:
        for mode in ("direct","inference"):
            for ct in range(len(COMPREHENSION_TEMPLATES)):
                requests.append((build_comprehension_prompt(s,mode,ct),("Yes","No"))); metadata.append({"kind":"comprehension","scenario_id":s.scenario_id,"family":s.family,"mode":mode,"template_id":ct})
            for jt in range(len(NATURAL_JUDGMENT_TEMPLATES)):
                for lo in (0,1):
                    prompt,target=build_natural_judgment_prompt(s,mode,jt,lo); requests.append((prompt,("A","B"))); metadata.append({"kind":"natural_judgment","scenario_id":s.scenario_id,"family":s.family,"mode":mode,"template_id":jt,"label_order":lo,"target_label":target})
            for ct in range(len(COMPREHENSION_TEMPLATES)):
                for jt in range(len(BRIDGED_JUDGMENT_TEMPLATES)):
                    for lo in (0,1):
                        prompt,target=build_bridged_judgment_prompt(s,mode,ct,jt,lo); requests.append((prompt,("A","B"))); metadata.append({"kind":"bridged_judgment","scenario_id":s.scenario_id,"family":s.family,"mode":mode,"comprehension_template_id":ct,"template_id":jt,"label_order":lo,"target_label":target,"conditioned_on_yes":True})
    scores=scorer.score_batch(requests,sequence_batch_size=sequence_batch_size); out=Path(out_path); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as f:
        for meta,score in zip(metadata,scores,strict=True):
            row={**meta,"model":model_name,"probs":score.probs,"logprobs":score.logprobs}
            if meta["kind"]=="comprehension": row["p_yes"]=score.probs["Yes"]; row["pred"]=max(score.probs,key=score.probs.get)
            else: row["p_target"]=score.probs[meta["target_label"]]; row["pred"]=max(score.probs,key=score.probs.get)
            f.write(json.dumps(row,ensure_ascii=False)+"\n")
