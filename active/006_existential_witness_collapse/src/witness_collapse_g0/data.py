from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE_GOLD = (
    "p_exists_gold",
    "q_exists_gold",
    "shared_witness_not_entailed_gold",
    "identity_underdetermined_gold",
    "joint_witness_possible_gold",
    "distinct_witness_possible_gold",
    "premises_do_not_identify_witnesses_gold",
    "same_explicit_authorizes_collapse_gold",
    "distinct_explicit_blocks_collapse_gold",
    "unknown_requires_identity_check_gold",
    "action_pair_matched_gold",
    "paraphrase_equivalent_gold",
    "neutral_control_equivalent_gold",
    "matched_base_gold",
    "natural_setting_gold",
)


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    premise_p: str
    premise_q: str
    premise_paraphrase: str
    p_property: str
    q_property: str
    shared_requirement: str
    decision_context: str
    collapse_action: str
    preserve_action: str
    same_witness_addendum: str
    distinct_witness_addendum: str
    neutral_addendum: str
    source: dict[str, Any]


def _s(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    domain = _s(row.get("domain"), f"{sid}.domain")
    premise_p = _s(row.get("premise_p"), f"{sid}.premise_p")
    premise_q = _s(row.get("premise_q"), f"{sid}.premise_q")
    paraphrase = _s(row.get("premise_paraphrase"), f"{sid}.premise_paraphrase")
    p_property = _s(row.get("p_property"), f"{sid}.p_property")
    q_property = _s(row.get("q_property"), f"{sid}.q_property")
    requirement = _s(row.get("shared_requirement"), f"{sid}.shared_requirement")
    decision_context = _s(row.get("decision_context"), f"{sid}.decision_context")
    collapse_action = _s(row.get("collapse_action"), f"{sid}.collapse_action")
    preserve_action = _s(row.get("preserve_action"), f"{sid}.preserve_action")
    same = _s(row.get("same_witness_addendum"), f"{sid}.same_witness_addendum")
    distinct = _s(row.get("distinct_witness_addendum"), f"{sid}.distinct_witness_addendum")
    neutral = _s(row.get("neutral_addendum"), f"{sid}.neutral_addendum")

    if premise_p == premise_q:
        raise ValueError(f"{sid}: the two existential premises must be distinct statements")
    if paraphrase in {premise_p, premise_q, f"{premise_p} {premise_q}"}:
        raise ValueError(f"{sid}: premise_paraphrase must be a genuine surface-form control")
    if collapse_action == preserve_action:
        raise ValueError(f"{sid}: downstream actions must differ")
    if same == distinct:
        raise ValueError(f"{sid}: same/distinct identity controls must differ")
    if neutral in {same, distinct}:
        raise ValueError(f"{sid}: neutral control must not encode witness identity")

    bad = [name for name in REQUIRED_TRUE_GOLD if row.get(name) is not True]
    if bad:
        raise ValueError(f"{sid}: D0 gold must be True for {bad}")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _s(source.get(key), f"{sid}.source.{key}")
    provenance = str(source.get("provenance", "")).strip().lower()
    if require_external_source and provenance in {"synthetic", "self-constructed", "custom-only"}:
        raise ValueError(f"{sid}: custom-only source cannot satisfy formal D0/G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: external D0 requires url/path/citation provenance")

    return Scenario(
        scenario_id=sid,
        domain=domain,
        premise_p=premise_p,
        premise_q=premise_q,
        premise_paraphrase=paraphrase,
        p_property=p_property,
        q_property=q_property,
        shared_requirement=requirement,
        decision_context=decision_context,
        collapse_action=collapse_action,
        preserve_action=preserve_action,
        same_witness_addendum=same,
        distinct_witness_addendum=distinct,
        neutral_addendum=neutral,
        source=dict(source),
    )


def load_scenarios(path: str | Path, *, require_external_source: bool = True) -> list[Scenario]:
    out: list[Scenario] = []
    seen: set[str] = set()
    with Path(path).open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL line {lineno}") from exc
            scenario = validate_record(row, require_external_source=require_external_source)
            if scenario.scenario_id in seen:
                raise ValueError(f"duplicate scenario_id={scenario.scenario_id}")
            seen.add(scenario.scenario_id)
            out.append(scenario)
    if not out:
        raise ValueError("dataset is empty")
    return out
