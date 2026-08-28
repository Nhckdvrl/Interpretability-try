from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

POLARITIES = {"supports_target", "supports_other"}
REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split", "provenance")
ALLOWED_PROVENANCE = {"external", "public-derived"}

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    case_facts: str
    evidence_text: str
    evidence_polarity: str
    target_verdict: str
    other_verdict: str
    admissible_ruling: str
    struck_ruling: str
    exclusion_scope: str
    neutral_evidence_text: str | None
    neutral_struck_ruling: str | None
    polarity_pair_id: str | None
    source: dict[str, Any]

def _s(x: Any, name: str) -> str:
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return x.strip()

def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    domain = _s(row.get("domain"), f"{sid}.domain")
    facts = _s(row.get("case_facts"), f"{sid}.case_facts")
    evidence = _s(row.get("evidence_text"), f"{sid}.evidence_text")
    polarity = _s(row.get("evidence_polarity"), f"{sid}.evidence_polarity")
    if polarity not in POLARITIES:
        raise ValueError(f"{sid}: evidence_polarity must be one of {sorted(POLARITIES)}")
    if row.get("polarity_gold") is not True:
        raise ValueError(f"{sid}: D0 must freeze polarity_gold=True")

    target = _s(row.get("target_verdict"), f"{sid}.target_verdict")
    other = _s(row.get("other_verdict"), f"{sid}.other_verdict")
    if target == other:
        raise ValueError(f"{sid}: target and other verdicts must differ")
    admitted = _s(row.get("admissible_ruling"), f"{sid}.admissible_ruling")
    struck = _s(row.get("struck_ruling"), f"{sid}.struck_ruling")
    scope = _s(row.get("exclusion_scope"), f"{sid}.exclusion_scope")
    if not all(row.get(k) is True for k in ("admitted_gold", "struck_gold", "exclusion_scope_gold", "must_ignore_for_verdict_gold")):
        raise ValueError(f"{sid}: D0 must freeze admitted/struck/scope/must-ignore gold=True")

    neutral = row.get("neutral_evidence_text")
    neutral_ruling = row.get("neutral_struck_ruling")
    if (neutral is None) != (neutral_ruling is None):
        raise ValueError(f"{sid}: neutral evidence and neutral struck ruling must be provided together")
    if neutral is not None:
        neutral = _s(neutral, f"{sid}.neutral_evidence_text")
        neutral_ruling = _s(neutral_ruling, f"{sid}.neutral_struck_ruling")
        if row.get("neutral_gold") is not True:
            raise ValueError(f"{sid}: neutral control requires neutral_gold=True")

    pair_id = row.get("polarity_pair_id")
    if pair_id is not None:
        pair_id = _s(pair_id, f"{sid}.polarity_pair_id")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _s(source.get(key), f"{sid}.source.{key}")
    provenance = str(source["provenance"]).strip().lower()
    if require_external_source and provenance not in ALLOWED_PROVENANCE:
        raise ValueError(f"{sid}: formal G0 provenance must be one of {sorted(ALLOWED_PROVENANCE)}, got {provenance!r}")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: source must provide url/path/citation provenance")
    if provenance == "public-derived":
        _s(source.get("derivation"), f"{sid}.source.derivation")

    return Scenario(
        sid, domain, facts, evidence, polarity, target, other, admitted, struck, scope,
        neutral, neutral_ruling, pair_id, dict(source)
    )

def _validate_pairs(rows: list[Scenario]) -> None:
    pairs: dict[str, list[Scenario]] = {}
    for s in rows:
        if s.polarity_pair_id is not None:
            pairs.setdefault(s.polarity_pair_id, []).append(s)
    for pid, ss in pairs.items():
        if len(ss) != 2:
            raise ValueError(f"polarity_pair_id={pid}: expected exactly two rows, found {len(ss)}")
        if {s.evidence_polarity for s in ss} != POLARITIES:
            raise ValueError(f"polarity_pair_id={pid}: pair must contain opposite evidence polarities")
        frozen = {(s.case_facts, s.target_verdict, s.other_verdict, s.exclusion_scope) for s in ss}
        if len(frozen) != 1:
            raise ValueError(f"polarity_pair_id={pid}: paired rows must share baseline facts, verdicts and exclusion scope")

def load_scenarios(path: str | Path, *, require_external_source: bool = True) -> list[Scenario]:
    out: list[Scenario] = []
    seen: set[str] = set()
    with Path(path).open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                raw = json.loads(line)
            except json.JSONDecodeError as e:
                raise ValueError(f"invalid JSONL line {lineno}") from e
            s = validate_record(raw, require_external_source=require_external_source)
            if s.scenario_id in seen:
                raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id)
            out.append(s)
    if not out:
        raise ValueError("dataset is empty")
    _validate_pairs(out)
    return out
