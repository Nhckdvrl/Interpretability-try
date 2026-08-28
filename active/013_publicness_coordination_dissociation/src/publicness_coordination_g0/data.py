from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE = (
    "same_proposition_gold",
    "same_recipients_gold",
    "both_participants_first_order_know_gold",
    "private_receipts_not_mutually_observable_gold",
    "public_event_mutually_observable_gold",
    "public_event_common_knowledge_operator_valid_gold",
    "private_event_does_not_generate_common_knowledge_gold",
    "explicit_ck_states_epistemic_consequence_only_gold",
    "policy_direction_public_gt_private_gold",
    "policy_direction_ck_gt_private_gold",
    "policy_gold_independent_of_model_gold",
    "policy_gold_not_in_prompt_gold",
    "participant_roles_symmetric_gold",
    "action_payoffs_symmetric_gold",
    "paraphrase_semantics_preserved_gold",
    "length_control_semantics_preserved_gold",
    "length_control_approximately_matched_gold",
    "natural_setting_gold",
)


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    background: str
    proposition: str
    participant_a: str
    participant_b: str
    coordinate_action_a: str
    safe_action_a: str
    coordinate_action_b: str
    safe_action_b: str
    private_event_text: str
    public_event_text: str
    explicit_ck_text: str
    private_paraphrase_text: str
    public_paraphrase_text: str
    explicit_ck_paraphrase_text: str
    private_length_text: str
    public_length_text: str
    explicit_ck_length_text: str
    policy_gold_text: str
    source: dict[str, Any]


def _s(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return v.strip()


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    bad = [k for k in REQUIRED_TRUE if row.get(k) is not True]
    if bad:
        raise ValueError(f"{sid}: D0 gold must be True for {bad}")

    fields = {name: _s(row.get(name), f"{sid}.{name}") for name in (
        "domain", "background", "proposition", "participant_a", "participant_b",
        "coordinate_action_a", "safe_action_a", "coordinate_action_b", "safe_action_b",
        "private_event_text", "public_event_text", "explicit_ck_text",
        "private_paraphrase_text", "public_paraphrase_text", "explicit_ck_paraphrase_text",
        "private_length_text", "public_length_text", "explicit_ck_length_text", "policy_gold_text",
    )}
    if fields["participant_a"] == fields["participant_b"]:
        raise ValueError(f"{sid}: participants must differ")
    if fields["coordinate_action_a"] == fields["safe_action_a"] or fields["coordinate_action_b"] == fields["safe_action_b"]:
        raise ValueError(f"{sid}: coordinate and safe actions must differ")

    primary_events = {fields["private_event_text"], fields["public_event_text"], fields["explicit_ck_text"]}
    if len(primary_events) != 3:
        raise ValueError(f"{sid}: private/public/explicit-CK event texts must differ")
    para_events = {fields["private_paraphrase_text"], fields["public_paraphrase_text"], fields["explicit_ck_paraphrase_text"]}
    if len(para_events) != 3:
        raise ValueError(f"{sid}: paraphrase event texts must differ")
    length_events = [fields["private_length_text"], fields["public_length_text"], fields["explicit_ck_length_text"]]
    ratio = max(map(len, length_events)) / max(1, min(map(len, length_events)))
    if ratio > 1.30:
        raise ValueError(f"{sid}: length-control event texts are not approximately matched")

    gold = fields["policy_gold_text"].casefold()
    for name in ("background", "private_event_text", "public_event_text", "explicit_ck_text",
                 "private_paraphrase_text", "public_paraphrase_text", "explicit_ck_paraphrase_text",
                 "private_length_text", "public_length_text", "explicit_ck_length_text"):
        if gold == fields[name].casefold():
            raise ValueError(f"{sid}: policy gold text must not be used as model-visible text")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _s(source.get(key), f"{sid}.source.{key}")
    provenance = str(source.get("provenance", "")).strip().lower()
    if require_external_source and provenance in {"synthetic", "self-constructed", "custom-only"}:
        raise ValueError(f"{sid}: custom-only provenance cannot satisfy formal D0/G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: external D0 requires url/path/citation")

    return Scenario(
        sid, fields["domain"], fields["background"], fields["proposition"],
        fields["participant_a"], fields["participant_b"],
        fields["coordinate_action_a"], fields["safe_action_a"],
        fields["coordinate_action_b"], fields["safe_action_b"],
        fields["private_event_text"], fields["public_event_text"], fields["explicit_ck_text"],
        fields["private_paraphrase_text"], fields["public_paraphrase_text"], fields["explicit_ck_paraphrase_text"],
        fields["private_length_text"], fields["public_length_text"], fields["explicit_ck_length_text"],
        fields["policy_gold_text"], dict(source),
    )


def load_scenarios(path: str | Path, *, require_external_source: bool = True) -> list[Scenario]:
    out = []
    seen = set()
    with Path(path).open(encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL line {lineno}") from exc
            s = validate_record(row, require_external_source=require_external_source)
            if s.scenario_id in seen:
                raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id)
            out.append(s)
    if not out:
        raise ValueError("dataset is empty")
    return out
