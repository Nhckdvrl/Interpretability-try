#!/usr/bin/env python3
"""Deterministic S0 artifact audit for official NTSB avall MDB exports.

Input CSVs are produced by mdb-export on a GitHub-hosted runner after downloading
`avall.zip` from the official NTSB data directory. This script performs no model
calls and creates no new core labels.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def canon(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def lookup(fieldnames: Iterable[str], *candidates: str) -> Optional[str]:
    cmap = {canon(x): x for x in fieldnames}
    for c in candidates:
        if canon(c) in cmap:
            return cmap[canon(c)]
    return None


def clean(v: Any) -> str:
    return "" if v is None else str(v).strip()


def norm_bool(v: Any) -> str:
    x = clean(v).upper()
    if x in {"T", "TRUE", "Y", "YES", "1"}:
        return "T"
    if x in {"F", "FALSE", "N", "NO", "0"}:
        return "F"
    return "BLANK" if x == "" else x


def norm_cause(v: Any) -> str:
    x = clean(v).upper()
    if x in {"C", "F"}:
        return x
    return "BLANK" if x == "" else x


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return list(r.fieldnames or []), rows


def parse_year(v: Any) -> Optional[int]:
    s = clean(v)
    if not s:
        return None
    # common MDB exports: MM/DD/YY..., MM/DD/YYYY..., YYYY-MM-DD...
    m = re.search(r"\b(19\d{2}|20\d{2})\b", s)
    if m:
        return int(m.group(1))
    m = re.match(r"\d{1,2}/\d{1,2}/(\d{2})(?:\D|$)", s)
    if m:
        y = int(m.group(1))
        return 2000 + y if y <= 68 else 1900 + y
    return None


def event_year_map(events_path: Optional[Path]) -> Tuple[Dict[str, int], Dict[str, Any]]:
    if not events_path or not events_path.exists():
        return {}, {"events_csv_available": False}
    fields, rows = read_csv(events_path)
    ev = lookup(fields, "ev_id", "event_id")
    date = lookup(fields, "ev_date", "event_date", "date")
    out: Dict[str, int] = {}
    if ev and date:
        for r in rows:
            y = parse_year(r.get(date))
            if y is not None:
                out[clean(r.get(ev))] = y
    return out, {
        "events_csv_available": True,
        "events_rows": len(rows),
        "event_id_column": ev,
        "event_date_column": date,
        "event_year_mapped": len(out),
    }


def hash_rank(seed: str, key: str) -> str:
    return hashlib.sha256((seed + "\0" + key).encode("utf-8")).hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--findings", required=True)
    p.add_argument("--events")
    p.add_argument("--out-dir", required=True)
    p.add_argument("--seed", default="2026-08-31-ntsb-s0")
    args = p.parse_args()

    findings_path = Path(args.findings)
    events_path = Path(args.events) if args.events else None
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    fields, rows = read_csv(findings_path)
    ev_col = lookup(fields, "ev_id", "event_id")
    aircraft_col = lookup(fields, "Aircraft_Key", "aircraft_key")
    finding_no_col = lookup(fields, "finding_no", "finding_number")
    desc_col = lookup(fields, "finding_description", "description")
    cause_col = lookup(fields, "Cause_Factor", "cause_factor")
    inpc_col = lookup(fields, "cm_inPc", "cm_inPC")
    if not ev_col or not cause_col or not inpc_col or not desc_col:
        raise SystemExit(
            f"Required findings columns missing. fields={fields!r}; resolved="
            f"ev={ev_col}, cause={cause_col}, cm_inPC={inpc_col}, desc={desc_col}"
        )

    years, events_meta = event_year_map(events_path)

    cause_counts: Counter[str] = Counter()
    inpc_counts: Counter[str] = Counter()
    cross: Counter[Tuple[str, str]] = Counter()
    by_event: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    by_event_legacy_roles: Dict[str, set[str]] = defaultdict(set)
    by_event_inpc_true = Counter()
    rows_by_year: Counter[str] = Counter()
    cause_by_year: Dict[str, Counter[str]] = defaultdict(Counter)
    inpc_by_year: Dict[str, Counter[str]] = defaultdict(Counter)

    for r in rows:
        ev_id = clean(r.get(ev_col))
        c = norm_cause(r.get(cause_col))
        t = norm_bool(r.get(inpc_col))
        cause_counts[c] += 1
        inpc_counts[t] += 1
        cross[(c, t)] += 1
        by_event[ev_id].append(r)
        if c in {"C", "F"}:
            by_event_legacy_roles[ev_id].add(c)
        if t == "T":
            by_event_inpc_true[ev_id] += 1
        y = years.get(ev_id)
        ys = str(y) if y is not None else "UNKNOWN"
        rows_by_year[ys] += 1
        cause_by_year[ys][c] += 1
        inpc_by_year[ys][t] += 1

    event_class: Counter[str] = Counter()
    multi_finding = 0
    mixed_cf_events: List[str] = []
    inpc_multi_events = 0
    for ev_id, rs in by_event.items():
        if len(rs) >= 2:
            multi_finding += 1
        roles = by_event_legacy_roles.get(ev_id, set())
        if roles == {"C", "F"}:
            event_class["MIXED_C_F"] += 1
            mixed_cf_events.append(ev_id)
        elif roles == {"C"}:
            event_class["C_ONLY"] += 1
        elif roles == {"F"}:
            event_class["F_ONLY"] += 1
        else:
            event_class["NO_LEGACY_C_F"] += 1
        if by_event_inpc_true[ev_id] >= 2:
            inpc_multi_events += 1

    # Deterministic random-20 event audit from mixed C/F population.
    mixed_cf_events = sorted(mixed_cf_events, key=lambda x: hash_rank(args.seed, x))
    audit_ids = mixed_cf_events[:20]
    audit_rows: List[Dict[str, Any]] = []
    for ev_id in audit_ids:
        rs = sorted(
            by_event[ev_id],
            key=lambda r: (
                clean(r.get(aircraft_col)) if aircraft_col else "",
                clean(r.get(finding_no_col)) if finding_no_col else "",
                clean(r.get(desc_col)),
            ),
        )
        for r in rs:
            audit_rows.append(
                {
                    "ev_id": ev_id,
                    "event_year": years.get(ev_id),
                    "aircraft_key": clean(r.get(aircraft_col)) if aircraft_col else None,
                    "finding_no": clean(r.get(finding_no_col)) if finding_no_col else None,
                    "finding_description": clean(r.get(desc_col)),
                    "Cause_Factor": norm_cause(r.get(cause_col)),
                    "cm_inPC": norm_bool(r.get(inpc_col)),
                }
            )

    with (out_dir / "random20_mixed_cf_findings.csv").open(
        "w", encoding="utf-8", newline=""
    ) as f:
        cols = [
            "ev_id",
            "event_year",
            "aircraft_key",
            "finding_no",
            "finding_description",
            "Cause_Factor",
            "cm_inPC",
        ]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(audit_rows)

    cross_json = {
        f"{c}|{t}": n for (c, t), n in sorted(cross.items(), key=lambda x: x[0])
    }
    year_json = {}
    all_years = sorted(
        set(rows_by_year), key=lambda x: (x == "UNKNOWN", int(x) if x.isdigit() else 9999)
    )
    for y in all_years:
        year_json[y] = {
            "finding_rows": rows_by_year[y],
            "cause_factor": dict(cause_by_year[y]),
            "cm_inPC": dict(inpc_by_year[y]),
        }

    summary = {
        "source": {
            "official_url": "https://data.ntsb.gov/avdata/FileDirectory/DownloadFile?fileID=C%3A%5Cavdata%5Cavall.zip",
            "audit_date": "2026-08-31",
            "findings_export": str(findings_path),
            **events_meta,
        },
        "schema": {
            "fields": fields,
            "resolved": {
                "ev_id": ev_col,
                "aircraft_key": aircraft_col,
                "finding_no": finding_no_col,
                "finding_description": desc_col,
                "cause_factor": cause_col,
                "cm_inPC": inpc_col,
            },
        },
        "counts": {
            "finding_rows": len(rows),
            "events_with_findings": len(by_event),
            "events_with_2plus_findings": multi_finding,
            "cause_factor": dict(cause_counts),
            "cm_inPC": dict(inpc_counts),
            "cause_factor_x_cm_inPC": cross_json,
            "event_legacy_role_class": dict(event_class),
            "events_with_2plus_cm_inPC_true_findings": inpc_multi_events,
            "mixed_C_F_events": len(mixed_cf_events),
        },
        "year_breakdown": year_json,
        "random20": {
            "sampling": "SHA256(seed || ev_id) rank over events containing >=1 C and >=1 F",
            "seed": args.seed,
            "event_ids": audit_ids,
            "rows_written": len(audit_rows),
        },
        "semantic_warning": (
            "cm_inPC is inclusion in the probable-cause statement as cause OR contributing factor; "
            "it must not be interpreted as a principal-cause-vs-factor label. Legacy Cause_Factor "
            "C/F is the role distinction audited here."
        ),
    }
    (out_dir / "ntsb_s0_audit.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
