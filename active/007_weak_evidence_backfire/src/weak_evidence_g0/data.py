from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import re

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE = (
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
    "hypotheses_exhaustive_gold",
    "binary_choice_well_defined_gold",
    "core_wording_does_not_label_strength_gold",
    "direction_pair_matched_gold",
    "strong_weak_relation_comparable_gold",
    "neutral_control_matched_gold",
    "baseline_contains_no_case_specific_evidence_gold",
    "natural_setting_gold",
)

# Finite real datasets virtually never contain a useful empirical cue with LR exactly 1.
# We require near-neutrality in BOTH the calibration and held-out validation partitions.
NEUTRAL_LR_MIN = 0.90
NEUTRAL_LR_MAX = 1.10


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


def _f(value: Any, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not result > 0:
        raise ValueError(f"{name} must be > 0")
    return result


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    domain = _s(row.get("domain"), f"{sid}.domain")
    background = _s(row.get("background"), f"{sid}.background")
    calibration = _s(row.get("calibration_text"), f"{sid}.calibration_text")
    target_h = _s(row.get("target_hypothesis"), f"{sid}.target_hypothesis")
    other_h = _s(row.get("other_hypothesis"), f"{sid}.other_hypothesis")
    target_a = _s(row.get("target_action"), f"{sid}.target_action")
    other_a = _s(row.get("other_action"), f"{sid}.other_action")
    if target_h == other_h or target_a == other_a:
        raise ValueError(f"{sid}: hypothesis/action alternatives must differ")

    weak_t = _s(row.get("weak_target_evidence"), f"{sid}.weak_target_evidence")
    weak_o = _s(row.get("weak_other_evidence"), f"{sid}.weak_other_evidence")
    strong_t = _s(row.get("strong_target_evidence"), f"{sid}.strong_target_evidence")
    strong_o = _s(row.get("strong_other_evidence"), f"{sid}.strong_other_evidence")
    neutral = _s(row.get("neutral_evidence"), f"{sid}.neutral_evidence")
    pragmatic = _s(row.get("pragmatic_completeness_text"), f"{sid}.pragmatic_completeness_text")
    length_control = _s(row.get("matched_length_control_text"), f"{sid}.matched_length_control_text")
    if len({weak_t, weak_o, strong_t, strong_o, neutral}) != 5:
        raise ValueError(f"{sid}: evidence texts must be distinct")

    strength_label = re.compile(r"\bweak(?:er|ly)?\s+evidence\b|\bweak\s+support\b|\bminor\s+evidence\b", flags=re.I)
    for name, text in (("weak_target_evidence", weak_t), ("weak_other_evidence", weak_o)):
        if strength_label.search(text):
            raise ValueError(f"{sid}.{name}: core wording must not explicitly label the item as weak evidence")

    bad = [key for key in REQUIRED_TRUE if row.get(key) is not True]
    if bad:
        raise ValueError(f"{sid}: D0 gold must be True for {bad}")

    weak_t_lr = _f(row.get("weak_target_lr"), f"{sid}.weak_target_lr")
    weak_o_lr = _f(row.get("weak_other_lr"), f"{sid}.weak_other_lr")
    strong_t_lr = _f(row.get("strong_target_lr"), f"{sid}.strong_target_lr")
    strong_o_lr = _f(row.get("strong_other_lr"), f"{sid}.strong_other_lr")
    neutral_lr = _f(row.get("neutral_lr"), f"{sid}.neutral_lr")
    if not (1 < weak_t_lr < strong_t_lr):
        raise ValueError(f"{sid}: target likelihood ratios must satisfy 1 < weak < strong")
    if not (0 < strong_o_lr < weak_o_lr < 1):
        raise ValueError(f"{sid}: other-support likelihood ratios must satisfy 0 < strong < weak < 1")
    if not (NEUTRAL_LR_MIN <= neutral_lr <= NEUTRAL_LR_MAX):
        raise ValueError(f"{sid}: neutral_lr must be within [{NEUTRAL_LR_MIN}, {NEUTRAL_LR_MAX}]")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _s(source.get(key), f"{sid}.source.{key}")
    provenance = str(source.get("provenance", "")).strip().lower()
    if require_external_source and provenance in {"synthetic", "self-constructed", "custom-only"}:
        raise ValueError(f"{sid}: custom-only source cannot satisfy formal D0/G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: external D0 requires url/path/citation")

    # When formal D0 includes a held-out split, enforce the same evidence relation there.
    # This prevents selecting thresholds that look diagnostic only because of calibration noise.
    heldout_keys = (
        "weak_target_lr_validation", "strong_target_lr_validation",
        "weak_other_lr_validation", "strong_other_lr_validation", "neutral_lr_validation",
    )
    if any(key in source for key in heldout_keys):
        missing = [key for key in heldout_keys if key not in source]
        if missing:
            raise ValueError(f"{sid}: incomplete held-out LR metadata: {missing}")
        wtv = _f(source["weak_target_lr_validation"], f"{sid}.source.weak_target_lr_validation")
        stv = _f(source["strong_target_lr_validation"], f"{sid}.source.strong_target_lr_validation")
        wov = _f(source["weak_other_lr_validation"], f"{sid}.source.weak_other_lr_validation")
        sov = _f(source["strong_other_lr_validation"], f"{sid}.source.strong_other_lr_validation")
        nv = _f(source["neutral_lr_validation"], f"{sid}.source.neutral_lr_validation")
        if not (1 < wtv < stv):
            raise ValueError(f"{sid}: held-out target LRs must satisfy 1 < weak < strong")
        if not (0 < sov < wov < 1):
            raise ValueError(f"{sid}: held-out other-support LRs must satisfy 0 < strong < weak < 1")
        if not (NEUTRAL_LR_MIN <= nv <= NEUTRAL_LR_MAX):
            raise ValueError(f"{sid}: held-out neutral LR is not near 1")

    return Scenario(
        sid, domain, background, calibration, target_h, other_h, target_a, other_a,
        weak_t, weak_o, strong_t, strong_o, neutral, pragmatic, length_control,
        weak_t_lr, weak_o_lr, strong_t_lr, strong_o_lr, neutral_lr, dict(source),
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
