from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

REQUIRED_SOURCE_KEYS=("dataset","record_id","license","split")
REQUIRED_TRUE_GOLD=("p_exists_gold","q_exists_gold","shared_witness_not_entailed_gold","identity_underdetermined_gold","same_explicit_establishes_gold","distinct_explicit_blocks_shared_gold","paraphrase_equivalent_gold","neutral_control_equivalent_gold","matched_base_gold","natural_setting_gold")
@dataclass(frozen=True)
class Scenario:
    scenario_id:str;domain:str;premise_p:str;premise_q:str;premise_paraphrase:str;p_property:str;q_property:str;shared_requirement:str;decision_context:str;same_witness_addendum:str;distinct_witness_addendum:str;neutral_addendum:str;source:dict[str,Any]
def _s(v:Any,n:str)->str:
    if not isinstance(v,str) or not v.strip(): raise ValueError(f"{n} must be a non-empty string")
    return v.strip()
def validate_record(row:dict[str,Any],*,require_external_source:bool=True)->Scenario:
    sid=_s(row.get("scenario_id"),"scenario_id");domain=_s(row.get("domain"),f"{sid}.domain");p=_s(row.get("premise_p"),f"{sid}.premise_p");q=_s(row.get("premise_q"),f"{sid}.premise_q");para=_s(row.get("premise_paraphrase"),f"{sid}.premise_paraphrase");pp=_s(row.get("p_property"),f"{sid}.p_property");qp=_s(row.get("q_property"),f"{sid}.q_property");req=_s(row.get("shared_requirement"),f"{sid}.shared_requirement");dc=_s(row.get("decision_context"),f"{sid}.decision_context");same=_s(row.get("same_witness_addendum"),f"{sid}.same_witness_addendum");distinct=_s(row.get("distinct_witness_addendum"),f"{sid}.distinct_witness_addendum");neutral=_s(row.get("neutral_addendum"),f"{sid}.neutral_addendum")
    if p==q: raise ValueError(f"{sid}: the two existential premises must be distinct statements")
    if para in {p,q,f"{p} {q}"}: raise ValueError(f"{sid}: premise_paraphrase must be a genuine surface-form control")
    if same==distinct: raise ValueError(f"{sid}: same/distinct identity controls must differ")
    if neutral in {same,distinct}: raise ValueError(f"{sid}: neutral control must not encode witness identity")
    bad=[n for n in REQUIRED_TRUE_GOLD if row.get(n) is not True]
    if bad: raise ValueError(f"{sid}: D0 gold must be True for {bad}")
    source=row.get("source")
    if not isinstance(source,dict): raise ValueError(f"{sid}: source must be an object")
    for k in REQUIRED_SOURCE_KEYS:_s(source.get(k),f"{sid}.source.{k}")
    prov=str(source.get("provenance","")).strip().lower()
    if require_external_source and prov in {"synthetic","self-constructed","custom-only"}: raise ValueError(f"{sid}: custom-only source cannot satisfy formal D0/G0")
    if require_external_source and not(source.get("url") or source.get("path") or source.get("citation")): raise ValueError(f"{sid}: external D0 requires url/path/citation provenance")
    return Scenario(sid,domain,p,q,para,pp,qp,req,dc,same,distinct,neutral,dict(source))
def load_scenarios(path:str|Path,*,require_external_source:bool=True)->list[Scenario]:
    out=[];seen=set()
    with Path(path).open(encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip():continue
            try:row=json.loads(line)
            except json.JSONDecodeError as e:raise ValueError(f"invalid JSONL line {i}") from e
            s=validate_record(row,require_external_source=require_external_source)
            if s.scenario_id in seen:raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id);out.append(s)
    if not out:raise ValueError("dataset is empty")
    return out
