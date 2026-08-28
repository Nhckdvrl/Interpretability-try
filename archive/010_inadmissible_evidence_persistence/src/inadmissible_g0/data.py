from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

POLARITIES={"supports_target","supports_other"}
EXCLUSION_REASONS={"procedural_truth_neutral","reliability_based"}
REQUIRED_SOURCE_KEYS=("dataset","record_id","license","split")

@dataclass(frozen=True)
class Scenario:
    scenario_id:str; polarity_pair_id:str; domain:str; case_facts:str; evidence_text:str; evidence_polarity:str
    target_verdict:str; other_verdict:str; admissible_ruling:str; struck_ruling:str; exclusion_scope:str
    neutral_evidence_text:str; neutral_struck_ruling:str; exclusion_reason_type:str; source:dict[str,Any]

def _s(x,name):
    if not isinstance(x,str) or not x.strip(): raise ValueError(f"{name} must be a non-empty string")
    return x.strip()

def validate_record(row:dict[str,Any],*,require_external_source:bool=True)->Scenario:
    sid=_s(row.get("scenario_id"),"scenario_id"); pair=_s(row.get("polarity_pair_id"),f"{sid}.polarity_pair_id")
    domain=_s(row.get("domain"),f"{sid}.domain"); facts=_s(row.get("case_facts"),f"{sid}.case_facts")
    lowered=facts.lower()
    dangling=("statement below","evidence below","following statement","following evidence")
    if any(phrase in lowered for phrase in dangling): raise ValueError(f"{sid}: never_seen baseline contains a dangling evidence reference")
    evidence=_s(row.get("evidence_text"),f"{sid}.evidence_text"); polarity=_s(row.get("evidence_polarity"),f"{sid}.evidence_polarity")
    if polarity not in POLARITIES: raise ValueError(f"{sid}: invalid evidence_polarity")
    target=_s(row.get("target_verdict"),f"{sid}.target_verdict"); other=_s(row.get("other_verdict"),f"{sid}.other_verdict")
    if target==other: raise ValueError(f"{sid}: target and other verdicts must differ")
    admitted=_s(row.get("admissible_ruling"),f"{sid}.admissible_ruling"); struck=_s(row.get("struck_ruling"),f"{sid}.struck_ruling")
    scope=_s(row.get("exclusion_scope"),f"{sid}.exclusion_scope"); neutral=_s(row.get("neutral_evidence_text"),f"{sid}.neutral_evidence_text")
    neutral_ruling=_s(row.get("neutral_struck_ruling"),f"{sid}.neutral_struck_ruling")
    reason=_s(row.get("exclusion_reason_type"),f"{sid}.exclusion_reason_type")
    if reason not in EXCLUSION_REASONS: raise ValueError(f"{sid}: invalid exclusion_reason_type")
    required_true=("admitted_gold","struck_gold","must_ignore_for_verdict_gold","evidence_polarity_gold","exclusion_scope_gold",
                   "baseline_excludes_evidence_gold","neutral_evidence_gold","neutral_control_matched_gold","neutral_ruling_matched_gold",
                   "content_swap_gold","matched_base_gold","baseline_no_dangling_reference_gold","exclusion_reason_gold",
                   "polarity_options_symmetric_gold","pair_statistical_unit_gold")
    bad=[k for k in required_true if row.get(k) is not True]
    if bad: raise ValueError(f"{sid}: D0 gold must be True for {bad}")
    source=row.get("source")
    if not isinstance(source,dict): raise ValueError(f"{sid}: source must be an object")
    for k in REQUIRED_SOURCE_KEYS: _s(source.get(k),f"{sid}.source.{k}")
    provenance=str(source.get("provenance","")).strip().lower()
    if require_external_source and provenance in {"synthetic","self-constructed","custom-only"}: raise ValueError(f"{sid}: custom-only source cannot satisfy external G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")): raise ValueError(f"{sid}: source must provide url/path/citation provenance")
    return Scenario(sid,pair,domain,facts,evidence,polarity,target,other,admitted,struck,scope,neutral,neutral_ruling,reason,dict(source))

def load_scenarios(path,*,require_external_source=True):
    out=[]; seen=set()
    with Path(path).open(encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: raw=json.loads(line)
            except json.JSONDecodeError as e: raise ValueError(f"invalid JSONL line {i}") from e
            s=validate_record(raw,require_external_source=require_external_source)
            if s.scenario_id in seen: raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id); out.append(s)
    if not out: raise ValueError("dataset is empty")
    pairs={}
    for s in out: pairs.setdefault(s.polarity_pair_id,[]).append(s)
    invariant=("domain","case_facts","target_verdict","other_verdict","admissible_ruling","struck_ruling","exclusion_scope","neutral_evidence_text","neutral_struck_ruling","exclusion_reason_type")
    for pid,rs in pairs.items():
        if len(rs)!=2 or {r.evidence_polarity for r in rs}!=POLARITIES:
            raise ValueError(f"{pid}: each polarity_pair_id must contain exactly one supports_target and one supports_other case")
        for field in invariant:
            if len({getattr(r,field) for r in rs})!=1: raise ValueError(f"{pid}: matched polarity pair differs on {field}")
        if rs[0].evidence_text==rs[1].evidence_text: raise ValueError(f"{pid}: polarity-swapped evidence texts must differ")
    return out
