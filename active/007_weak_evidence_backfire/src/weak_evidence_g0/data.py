from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json, re

DIRECTIONS = ("supports_target", "supports_other")
REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE = (
    "calibration_valid_gold", "weak_target_support_gold", "weak_other_support_gold",
    "strong_target_support_gold", "strong_other_support_gold", "neutral_gold",
    "pragmatic_completeness_gold", "matched_length_control_gold", "actions_symmetric_gold",
    "hypotheses_exclusive_gold", "core_wording_does_not_label_strength_gold", "natural_setting_gold",
)

@dataclass(frozen=True)
class Scenario:
    scenario_id: str; domain: str; background: str; calibration_text: str
    target_hypothesis: str; other_hypothesis: str; target_action: str; other_action: str
    weak_target_evidence: str; weak_other_evidence: str; strong_target_evidence: str; strong_other_evidence: str
    neutral_evidence: str; pragmatic_completeness_text: str; matched_length_control_text: str
    weak_target_lr: float; weak_other_lr: float; strong_target_lr: float; strong_other_lr: float; neutral_lr: float
    source: dict[str, Any]

def _s(x: Any, name: str) -> str:
    if not isinstance(x, str) or not x.strip(): raise ValueError(f"{name} must be a non-empty string")
    return x.strip()

def _f(x: Any, name: str) -> float:
    if isinstance(x, bool): raise ValueError(f"{name} must be numeric")
    try: v=float(x)
    except (TypeError,ValueError) as e: raise ValueError(f"{name} must be numeric") from e
    if not (v>0): raise ValueError(f"{name} must be > 0")
    return v

def validate_record(row: dict[str,Any], *, require_external_source: bool=True) -> Scenario:
    sid=_s(row.get("scenario_id"),"scenario_id"); domain=_s(row.get("domain"),f"{sid}.domain")
    background=_s(row.get("background"),f"{sid}.background"); calibration=_s(row.get("calibration_text"),f"{sid}.calibration_text")
    th=_s(row.get("target_hypothesis"),f"{sid}.target_hypothesis"); oh=_s(row.get("other_hypothesis"),f"{sid}.other_hypothesis")
    ta=_s(row.get("target_action"),f"{sid}.target_action"); oa=_s(row.get("other_action"),f"{sid}.other_action")
    if th==oh or ta==oa: raise ValueError(f"{sid}: hypothesis/action alternatives must differ")
    wt=_s(row.get("weak_target_evidence"),f"{sid}.weak_target_evidence"); wo=_s(row.get("weak_other_evidence"),f"{sid}.weak_other_evidence")
    st=_s(row.get("strong_target_evidence"),f"{sid}.strong_target_evidence"); so=_s(row.get("strong_other_evidence"),f"{sid}.strong_other_evidence")
    neutral=_s(row.get("neutral_evidence"),f"{sid}.neutral_evidence"); pragmatic=_s(row.get("pragmatic_completeness_text"),f"{sid}.pragmatic_completeness_text")
    length=_s(row.get("matched_length_control_text"),f"{sid}.matched_length_control_text")
    if len({wt,wo,st,so,neutral}) != 5: raise ValueError(f"{sid}: evidence texts must be distinct")
    for name,text in (("weak_target_evidence",wt),("weak_other_evidence",wo)):
        if re.search(r"\bweak(?:er|ly)?\b|\bslight(?:ly)?\b|\bsmall\s+amount\b", text, flags=re.I): raise ValueError(f"{sid}.{name}: core wording must not explicitly label evidence as weak")
    bad=[k for k in REQUIRED_TRUE if row.get(k) is not True]
    if bad: raise ValueError(f"{sid}: D0 gold must be True for {bad}")
    wtlr=_f(row.get("weak_target_lr"),f"{sid}.weak_target_lr"); wolr=_f(row.get("weak_other_lr"),f"{sid}.weak_other_lr")
    stlr=_f(row.get("strong_target_lr"),f"{sid}.strong_target_lr"); solr=_f(row.get("strong_other_lr"),f"{sid}.strong_other_lr"); nlr=_f(row.get("neutral_lr"),f"{sid}.neutral_lr")
    if not (1 < wtlr < stlr): raise ValueError(f"{sid}: target likelihood ratios must satisfy 1 < weak < strong")
    if not (0 < solr < wolr < 1): raise ValueError(f"{sid}: other-support likelihood ratios must satisfy 0 < strong < weak < 1")
    if abs(nlr-1.0)>1e-6: raise ValueError(f"{sid}: neutral_lr must equal 1")
    source=row.get("source")
    if not isinstance(source,dict): raise ValueError(f"{sid}: source must be an object")
    for k in REQUIRED_SOURCE_KEYS: _s(source.get(k),f"{sid}.source.{k}")
    prov=str(source.get("provenance","")).strip().lower()
    if require_external_source and prov in {"synthetic","self-constructed","custom-only"}: raise ValueError(f"{sid}: custom-only source cannot satisfy formal D0/G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")): raise ValueError(f"{sid}: external D0 requires url/path/citation")
    return Scenario(sid,domain,background,calibration,th,oh,ta,oa,wt,wo,st,so,neutral,pragmatic,length,wtlr,wolr,stlr,solr,nlr,dict(source))

def load_scenarios(path: str|Path, *, require_external_source: bool=True) -> list[Scenario]:
    out=[]; seen=set()
    with Path(path).open(encoding="utf-8") as f:
        for i,line in enumerate(f,1):
            if not line.strip(): continue
            try: row=json.loads(line)
            except json.JSONDecodeError as e: raise ValueError(f"invalid JSONL line {i}") from e
            s=validate_record(row,require_external_source=require_external_source)
            if s.scenario_id in seen: raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id); out.append(s)
    if not out: raise ValueError("dataset is empty")
    return out
