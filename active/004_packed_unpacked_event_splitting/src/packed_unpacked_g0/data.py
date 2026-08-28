from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any
import json

REQUIRED_SOURCE_KEYS = ("dataset", "record_id", "license", "split", "provenance")
ALLOWED_PROVENANCE = {"external", "public-derived"}

@dataclass(frozen=True)
class Partition:
    partition_id: str
    branches: tuple[str, ...]
    unpacked_text: str
    partial_unpacked_text: str
    repacked_text: str | None
    branch_count: int
    alternative_packed_text: str | None
    alternative_branches: tuple[str, ...]
    alternative_unpacked_text: str | None

@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    domain: str
    information_context: str
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
    context = _nonempty_str(row.get("information_context"), f"{sid}.information_context")
    packed = _nonempty_str(row.get("packed_text"), f"{sid}.packed_text")
    paraphrase = _nonempty_str(row.get("packed_paraphrase"), f"{sid}.packed_paraphrase")
    if paraphrase == packed:
        raise ValueError(f"{sid}: packed_paraphrase must be a genuine wording control")

    source = row.get("source")
    if not isinstance(source, dict):
        raise ValueError(f"{sid}: source must be an object")
    for key in REQUIRED_SOURCE_KEYS:
        _nonempty_str(source.get(key), f"{sid}.source.{key}")
    provenance = str(source["provenance"]).strip().lower()
    if require_external_source and provenance not in ALLOWED_PROVENANCE:
        raise ValueError(f"{sid}: formal G0 provenance must be one of {sorted(ALLOWED_PROVENANCE)}, got {provenance!r}")
    if require_external_source and not (source.get("url") or source.get("path") or source.get("citation")):
        raise ValueError(f"{sid}: source must provide url/path/citation provenance")
    if provenance == "public-derived":
        _nonempty_str(source.get("derivation"), f"{sid}.source.derivation")

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
        if p.get("disjoint_gold") is not True or p.get("exhaustive_gold") is not True or p.get("equivalent_gold") is not True:
            raise ValueError(f"{sid}/{pid}: D0 must freeze disjoint/exhaustive/equivalent gold=True")

        partial = _nonempty_str(p.get("partial_unpacked_text"), f"{sid}/{pid}.partial_unpacked_text")
        if p.get("partial_is_strict_subset") is not True:
            raise ValueError(f"{sid}/{pid}: partial_is_strict_subset must be frozen True")

        unpacked = _nonempty_str(p.get("unpacked_text"), f"{sid}/{pid}.unpacked_text")
        repacked = p.get("repacked_text")
        if repacked is not None:
            repacked = _nonempty_str(repacked, f"{sid}/{pid}.repacked_text")
            if p.get("repacked_equivalent_gold") is not True:
                raise ValueError(f"{sid}/{pid}: repacked_text requires repacked_equivalent_gold=True")

        alt_packed = p.get("alternative_packed_text")
        alt_branches_raw = p.get("alternative_branches")
        alt_unpacked = p.get("alternative_unpacked_text")
        any_alt = alt_packed is not None or alt_branches_raw is not None or alt_unpacked is not None
        alt_branches: tuple[str, ...] = ()
        if any_alt:
            alt_packed = _nonempty_str(alt_packed, f"{sid}/{pid}.alternative_packed_text")
            alt_unpacked = _nonempty_str(alt_unpacked, f"{sid}/{pid}.alternative_unpacked_text")
            if not isinstance(alt_branches_raw, list) or len(alt_branches_raw) < 2:
                raise ValueError(f"{sid}/{pid}: alternative_branches must contain >=2 branches")
            alt_branches = tuple(_nonempty_str(x, f"{sid}/{pid}.alternative_branch") for x in alt_branches_raw)
            if len(set(alt_branches)) != len(alt_branches):
                raise ValueError(f"{sid}/{pid}: duplicate alternative branch text")
            required = (
                p.get("alternative_disjoint_gold") is True
                and p.get("alternative_exhaustive_gold") is True
                and p.get("alternative_equivalent_gold") is True
                and p.get("alternative_is_complement_gold") is True
            )
            if not required:
                raise ValueError(f"{sid}/{pid}: alternative frame requires disjoint/exhaustive/equivalent/complement gold=True")

        parts.append(Partition(pid, b, unpacked, partial, repacked, len(b), alt_packed, alt_branches, alt_unpacked))

    return Scenario(sid, domain, context, packed, paraphrase, tuple(parts), dict(source))

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
