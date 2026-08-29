from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json
import math

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")
REQUIRED_TRUE = (
    "binary_hypotheses_exclusive_gold",
    "binary_hypotheses_exhaustive_gold",
    "message_direction_gold",
    "same_message_content_across_sources_gold",
    "source_reliability_above_chance_gold",
    "source_reliability_order_gold",
    "directional_likelihood_ratios_valid_gold",
    "calibration_matches_likelihood_ratios_gold",
    "source_profiles_hypothesis_neutral_gold",
    "source_identity_content_independent_gold",
    "delay_material_message_neutral_gold",
    "delay_material_source_neutral_gold",
    "short_and_long_delays_natural_gold",
    "reinstatement_does_not_repeat_message_gold",
    "reinstatement_only_restores_source_metadata_gold",
    "matched_length_control_semantically_inert_gold",
    "direction_pair_matched_gold",
    "actions_symmetric_gold",
    "natural_setting_gold",
)


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    cell_id: str
    background: str
    calibration_text: str
    target_hypothesis: str
    other_hypothesis: str
    target_action: str
    other_action: str
    high_source: str
    low_source: str
    high_source_profile: str
    low_source_profile: str
    high_source_reliability: float
    low_source_reliability: float
    low_target_lr: float
    high_target_lr: float
    low_other_lr: float
    high_other_lr: float
    target_message: str
    other_message: str
    short_delay_text: str
    long_delay_text: str
    high_source_reinstatement: str
    low_source_reinstatement: str
    high_source_length_control: str
    low_source_length_control: str
    source: dict[str, Any]


def _s(v: Any, name: str) -> str:
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return v.strip()


def _p(v: Any, name: str) -> float:
    if isinstance(v, bool):
        raise ValueError(f"{name} must be numeric")
    try:
        x = float(v)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be numeric") from exc
    if not math.isfinite(x) or not (0.0 < x < 1.0):
        raise ValueError(f"{name} must be finite and in (0,1)")
    return x


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _s(row.get("scenario_id"), "scenario_id")
    bad = [k for k in REQUIRED_TRUE if row.get(k) is not True]
    if bad:
        raise ValueError(f"{sid}: D0 gold must be True for {bad}")

    domain = _s(row.get("domain"), f"{sid}.domain")
    # A cell is one (domain, binary label pair). It is the stratum the analysis averages
    # within, so it is stored rather than parsed out of the scenario id. Datasets whose
    # domain is already the finest stratum may omit it.
    cell_id = _s(row.get("cell_id"), f"{sid}.cell_id") if row.get("cell_id") is not None else domain
    background = _s(row.get("background"), f"{sid}.background")
    calibration = _s(row.get("calibration_text"), f"{sid}.calibration_text")
    target_h = _s(row.get("target_hypothesis"), f"{sid}.target_hypothesis")
    other_h = _s(row.get("other_hypothesis"), f"{sid}.other_hypothesis")
    target_a = _s(row.get("target_action"), f"{sid}.target_action")
    other_a = _s(row.get("other_action"), f"{sid}.other_action")
    if target_h == other_h or target_a == other_a:
        raise ValueError(f"{sid}: hypotheses/actions must differ")

    high_source = _s(row.get("high_source"), f"{sid}.high_source")
    low_source = _s(row.get("low_source"), f"{sid}.low_source")
    if high_source == low_source:
        raise ValueError(f"{sid}: source identities must differ")
    high_profile = _s(row.get("high_source_profile"), f"{sid}.high_source_profile")
    low_profile = _s(row.get("low_source_profile"), f"{sid}.low_source_profile")
    high_r = _p(row.get("high_source_reliability"), f"{sid}.high_source_reliability")
    low_r = _p(row.get("low_source_reliability"), f"{sid}.low_source_reliability")
    # Both sources must remain positively informative. Below-chance sources can make
    # discount/reversal normatively correct and are invalid for this phenomenon.
    if not (0.5 < low_r < high_r < 1.0):
        raise ValueError(f"{sid}: require 0.5 < low reliability < high reliability < 1")

    low_target_lr = float(row.get("low_target_lr"))
    high_target_lr = float(row.get("high_target_lr"))
    low_other_lr = float(row.get("low_other_lr"))
    high_other_lr = float(row.get("high_other_lr"))
    if not all(math.isfinite(x) and x > 0 for x in (low_target_lr, high_target_lr, low_other_lr, high_other_lr)):
        raise ValueError(f"{sid}: directional likelihood ratios must be finite and > 0")
    if not (1.0 < low_target_lr < high_target_lr):
        raise ValueError(f"{sid}: target-support LRs must satisfy 1 < low < high")
    if not (0.0 < high_other_lr < low_other_lr < 1.0):
        raise ValueError(f"{sid}: other-support LRs must satisfy 0 < high < low < 1")

    target_msg = _s(row.get("target_message"), f"{sid}.target_message")
    other_msg = _s(row.get("other_message"), f"{sid}.other_message")
    if target_msg == other_msg:
        raise ValueError(f"{sid}: directional messages must differ")

    short_delay = _s(row.get("short_delay_text"), f"{sid}.short_delay_text")
    long_delay = _s(row.get("long_delay_text"), f"{sid}.long_delay_text")
    if short_delay == long_delay:
        raise ValueError(f"{sid}: short and long delay material must differ")

    high_re = _s(row.get("high_source_reinstatement"), f"{sid}.high_source_reinstatement")
    low_re = _s(row.get("low_source_reinstatement"), f"{sid}.low_source_reinstatement")
    high_len = _s(row.get("high_source_length_control"), f"{sid}.high_source_length_control")
    low_len = _s(row.get("low_source_length_control"), f"{sid}.low_source_length_control")
    for text in (high_re, low_re):
        if target_msg in text or other_msg in text:
            raise ValueError(f"{sid}: reinstatement text must not repeat message content")
    # A crude but deterministic safeguard: matched-length control may differ modestly,
    # but should not be orders of magnitude shorter/longer than the corresponding cue.
    for cue, ctrl, name in ((high_re, high_len, "high"), (low_re, low_len, "low")):
        ratio = max(len(cue), len(ctrl)) / max(1, min(len(cue), len(ctrl)))
        if ratio > 1.75:
            raise ValueError(f"{sid}: {name} reinstatement/length-control texts are not length comparable")

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
        sid, domain, cell_id, background, calibration, target_h, other_h, target_a, other_a,
        high_source, low_source, high_profile, low_profile, high_r, low_r,
        low_target_lr, high_target_lr, low_other_lr, high_other_lr,
        target_msg, other_msg, short_delay, long_delay, high_re, low_re,
        high_len, low_len, dict(source),
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
            s = validate_record(row, require_external_source=require_external_source)
            if s.scenario_id in seen:
                raise ValueError(f"duplicate scenario_id={s.scenario_id}")
            seen.add(s.scenario_id)
            out.append(s)
    if not out:
        raise ValueError("dataset is empty")
    return out
