from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split")

@dataclass(frozen=True)
class Partition:
    partition_id: str
    branches: tuple[str, ...]
    unpacked_text: str
    reordered_unpacked_text: str
    repacked_text: str
    partial_text: str
    complement_text: str
    complement_branches: tuple[str, ...]
    complement_unpacked_text: str
    focal_length_control_text: str
    complement_length_control_text: str
    branch_count_family: str
    branch_count: int

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    packed_text: str
    packed_paraphrase: str
    partitions: tuple[Partition, ...]
    source: dict[str, Any]


def _nonempty_str(x: Any, name: str) -> str:
    if not isinstance(x, str) or not x.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return x.strip()


def validate_record(row: dict[str, Any], *, require_external_source: bool = True) -> Scenario:
    sid = _nonempty_str(row.get("scenario_id"), "scenario_id")
    domain = _nonempty_str(row.get("domain"), f"{sid}.domain")
    packed = _nonempty_str(row.get("packed_text"), f"{sid}.packed_text")
    paraphrase = _nonempty_str(row.get("packed_paraphrase"), f"{sid}.packed_paraphrase")
    if paraphrase == packed:
        raise ValueError(f"{sid}: packed_paraphrase must be a genuine wording control")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _nonempty_str(source.get(key), f"{sid}.source.{key}")
    provenance = str(source.get("provenance", "")).strip().lower()
    if require_external_source and provenance in {"synthetic", "self-constructed", "custom-only"}:
        raise ValueError(f"{sid}: custom-only source cannot satisfy external G0")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: source must provide url/path/citation provenance")

    raw_parts = row.get("partitions")
    if not isinstance(raw_parts, list) or not raw_parts:
        raise ValueError(f"{sid}: partitions must be a non-empty list")

    parts: list[Partition] = []
    seen: set[str] = set()
    for i, p in enumerate(raw_parts):
        if not isinstance(p, dict):
            raise ValueError(f"{sid}: partition[{i}] must be an object")
        pid = _nonempty_str(p.get("partition_id"), f"{sid}.partition_id")
        if pid in seen:
            raise ValueError(f"{sid}: duplicate partition_id={pid}")
        seen.add(pid)
        branches = p.get("branches")
        if not isinstance(branches, list) or len(branches) < 2:
            raise ValueError(f"{sid}/{pid}: need >=2 mutually exclusive branches")
        b = tuple(_nonempty_str(x, f"{sid}/{pid}.branch") for x in branches)
        if len(set(b)) != len(b):
            raise ValueError(f"{sid}/{pid}: duplicate branch text")
        cb_raw = p.get("complement_branches")
        if not isinstance(cb_raw, list) or len(cb_raw) != len(b):
            raise ValueError(f"{sid}/{pid}: complement_branches must match focal branch count")
        cb = tuple(_nonempty_str(x, f"{sid}/{pid}.complement_branch") for x in cb_raw)
        if len(set(cb)) != len(cb):
            raise ValueError(f"{sid}/{pid}: duplicate complement branch text")
        required_true = (
            "disjoint_gold", "exhaustive_gold", "equivalent_gold",
            "partial_is_strict_subset", "partial_strictly_lower_probability_gold",
            "complement_gold", "complement_partition_gold",
            "reordered_equivalent_gold", "length_controls_equivalent_gold",
            "length_controls_matched_gold", "branch_count_comparable_gold",
        )
        bad = [name for name in required_true if p.get(name) is not True]
        if bad:
            raise ValueError(f"{sid}/{pid}: D0 relation gold must be True for {bad}")
        unpacked = _nonempty_str(p.get("unpacked_text"), f"{sid}/{pid}.unpacked_text")
        reordered = _nonempty_str(p.get("reordered_unpacked_text"), f"{sid}/{pid}.reordered_unpacked_text")
        repacked = _nonempty_str(p.get("repacked_text"), f"{sid}/{pid}.repacked_text")
        partial = _nonempty_str(p.get("partial_text"), f"{sid}/{pid}.partial_text")
        complement = _nonempty_str(p.get("complement_text"), f"{sid}/{pid}.complement_text")
        complement_unpacked = _nonempty_str(p.get("complement_unpacked_text"), f"{sid}/{pid}.complement_unpacked_text")
        focal_length = _nonempty_str(p.get("focal_length_control_text"), f"{sid}/{pid}.focal_length_control_text")
        complement_length = _nonempty_str(p.get("complement_length_control_text"), f"{sid}/{pid}.complement_length_control_text")
        family = _nonempty_str(p.get("branch_count_family"), f"{sid}/{pid}.branch_count_family")
        if partial in {packed, unpacked}:
            raise ValueError(f"{sid}/{pid}: partial_text must be a distinct strict-subset description")
        if repacked == unpacked:
            raise ValueError(f"{sid}/{pid}: repacked_text must actually repack the branch list")
        if reordered == unpacked:
            raise ValueError(f"{sid}/{pid}: reordered_unpacked_text must change branch order")
        if complement == packed:
            raise ValueError(f"{sid}/{pid}: complement_text must differ from the focal event")
        if focal_length in {packed, unpacked} or complement_length in {complement, complement_unpacked}:
            raise ValueError(f"{sid}/{pid}: length controls must be distinct surface forms")
        parts.append(Partition(pid, b, unpacked, reordered, repacked, partial, complement, cb,
                               complement_unpacked, focal_length, complement_length, family, len(b)))
    return Scenario(sid, domain, packed, paraphrase, tuple(parts), dict(source))


def load_scenarios(path: str | Path, *, require_external_source: bool = True) -> list[Scenario]:
    rows: list[Scenario] = []
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
            rows.append(s)
    if not rows:
        raise ValueError("dataset is empty")
    return rows
