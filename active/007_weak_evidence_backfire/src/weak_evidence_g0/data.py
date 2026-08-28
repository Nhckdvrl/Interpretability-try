from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import math
import re

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE_GOLD = (
    "calibration_valid_gold",
    "weak_target_support_gold",
    "weak_other_support_gold",
    "strong_target_support_gold",
    "strong_other_support_gold",
    "neutral_gold",
    "pragmatic_completeness_gold",
    "matched_length_control_gold",
    "actions_symmetric_gold",
    "hypotheses_exclusive_gold",
    "core_wording_does_not_label_strength_gold",
    "natural_setting_gold",
)
BANNED_STRENGTH_WORDS = re.compile(
    r"\b(?:weak|weakly|strong|strongly|slight|limited)\s+(?:evidence|cue|signal|support)\b", re.I
)


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    background: str
    calibration_text: str
    target_hypothesis: str
    other_hypothesis: str
    target_action: str
    other_action: str
    weak_target_evidence: str
    weak_other_evidence: str
    strong_target_evidence: str
    strong_other_evidence: str
    neutral_evidence: str
    pragmatic_completeness_text: str
    matched_length_control_text: str
    weak_target_lr: float
    weak_other_lr: float
    strong_target_lr: float
    strong_other_lr: float
    neutral_lr: float
    source: dict[str, Any]


def _s(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value.strip()


def _positive_float(value: Any, name: str) -> float:
    try:
        x = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(x) or x <= 0:
        raise ValueError(f"{name} must be finite and > 0")
    return x


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    domain = _s(row.get("domain"), f"{sid}.domain")
    background = _s(row.get("background"), f"{sid}.background")
    calibration = _s(row.get("calibration_text"), f"{sid}.calibration_text")
    target = _s(row.get("target_hypothesis"), f"{sid}.target_hypothesis")
    other = _s(row.get("other_hypothesis"), f"{sid}.other_hypothesis")
    target_action = _s(row.get("target_action"), f"{sid}.target_action")
    other_action = _s(row.get("other_action"), f"{sid}.other_action")
    if target == other:
        raise ValueError(f"{sid}: target and other hypotheses must differ")
    if target_action == other_action:
        raise ValueError(f"{sid}: target and other actions must differ")

    weak_target = _s(row.get("weak_target_evidence"), f"{sid}.weak_target_evidence")
    weak_other = _s(row.get("weak_other_evidence"), f"{sid}.weak_other_evidence")
    strong_target = _s(row.get("strong_target_evidence"), f"{sid}.strong_target_evidence")
    strong_other = _s(row.get("strong_other_evidence"), f"{sid}.strong_other_evidence")
    neutral = _s(row.get("neutral_evidence"), f"{sid}.neutral_evidence")
    pragmatic = _s(row.get("pragmatic_completeness_text"), f"{sid}.pragmatic_completeness_text")
    length_control = _s(row.get("matched_length_control_text"), f"{sid}.matched_length_control_text")

    evidence_texts = (weak_target, weak_other, strong_target, strong_other, neutral)
    if len(set(evidence_texts)) != len(evidence_texts):
        raise ValueError(f"{sid}: all evidence texts must be distinct")
    for text in (calibration, weak_target, weak_other):
        if BANNED_STRENGTH_WORDS.search(text):
            raise ValueError(f"{sid}: core weak-evidence text must not explicitly label evidence strength")
    if pragmatic == length_control:
        raise ValueError(f"{sid}: pragmatic and matched-length controls must differ")

    weak_target_lr = _positive_float(row.get("weak_target_lr"), f"{sid}.weak_target_lr")
    weak_other_lr = _positive_float(row.get("weak_other_lr"), f"{sid}.weak_other_lr")
    strong_target_lr = _positive_float(row.get("strong_target_lr"), f"{sid}.strong_target_lr")
    strong_other_lr = _positive_float(row.get("strong_other_lr"), f"{sid}.strong_other_lr")
    neutral_lr = _positive_float(row.get("neutral_lr"), f"{sid}.neutral_lr")

    if not (1.0 < weak_target_lr < strong_target_lr):
        raise ValueError(f"{sid}: target-supporting LR must satisfy 1 < weak < strong")
    if not (0.0 < strong_other_lr < weak_other_lr < 1.0):
        raise ValueError(f"{sid}: other-supporting target/other LR must satisfy 0 < strong < weak < 1")
    if abs(neutral_lr - 1.0) > 0.02:
        raise ValueError(f"{sid}: neutral_lr must be approximately 1")

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
        background=background,
        calibration_text=calibration,
        target_hypothesis=target,
        other_hypothesis=other,
        target_action=target_action,
        other_action=other_action,
        weak_target_evidence=weak_target,
        weak_other_evidence=weak_other,
        strong_target_evidence=strong_target,
        strong_other_evidence=strong_other,
        neutral_evidence=neutral,
        pragmatic_completeness_text=pragmatic,
        matched_length_control_text=length_control,
        weak_target_lr=weak_target_lr,
        weak_other_lr=weak_other_lr,
        strong_target_lr=strong_target_lr,
        strong_other_lr=strong_other_lr,
        neutral_lr=neutral_lr,
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
