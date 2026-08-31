#!/usr/bin/env python3
"""Prepare (but do not run) the NTSB causal-relevance / causal-role G0 population.

Core labels come only from official NTSB fields:
- cm_inPC: finding cited in probable-cause statement as cause OR contributing factor.
- legacy Cause_Factor: C=Cause, F=Factor, blank=Finding.

The tested model must never see narr_cause or the C/F suffixes embedded in legacy
finding_description strings.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
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
    return x if x in {"C", "F"} else ("BLANK" if x == "" else x)


def read_csv(path: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        r = csv.DictReader(f)
        rows = list(r)
        return list(r.fieldnames or []), rows


def strip_legacy_role_suffix(desc: str, role: str) -> str:
    s = clean(desc)
    if role in {"C", "F"}:
        # Legacy public export often appends ` - C` / ` - F` directly to the text.
        s = re.sub(r"\s+-\s+" + re.escape(role) + r"\s*$", "", s, flags=re.I)
    return s.strip()


def rank(seed: str, key: str) -> str:
    return hashlib.sha256((seed + "\0" + key).encode("utf-8")).hexdigest()


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--findings", required=True)
    p.add_argument("--narratives", required=True)
    p.add_argument("--out-dir", required=True)
    p.add_argument("--seed", default="2026-08-31-ntsb-g0-pop")
    p.add_argument("--manifest-n", type=int, default=300)
    args = p.parse_args()

    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    ff, findings = read_csv(Path(args.findings))
    evf = lookup(ff, "ev_id", "event_id")
    acf = lookup(ff, "Aircraft_Key", "aircraft_key")
    nof = lookup(ff, "finding_no", "finding_number")
    df = lookup(ff, "finding_description", "description")
    cf = lookup(ff, "Cause_Factor", "cause_factor")
    pc = lookup(ff, "cm_inPc", "cm_inPC")
    if not all([evf, df, cf, pc]):
        raise SystemExit(f"Missing required findings columns: {ff}")

    nf, narratives = read_csv(Path(args.narratives))
    evn = lookup(nf, "ev_id", "event_id")
    acn = lookup(nf, "Aircraft_Key", "aircraft_key")
    finalf = lookup(nf, "narr_accf")
    prelimf = lookup(nf, "narr_accp")
    causef = lookup(nf, "narr_cause")
    if not evn or not causef or (not finalf and not prelimf):
        raise SystemExit(f"Missing required narrative columns: {nf}")

    by_event: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in findings:
        by_event[clean(r.get(evf))].append(r)

    narr_by_event: Dict[str, List[Dict[str, str]]] = defaultdict(list)
    for r in narratives:
        narr_by_event[clean(r.get(evn))].append(r)

    stats = Counter()
    population: List[Dict[str, Any]] = []
    for ev_id, rs in by_event.items():
        roles = {norm_cause(r.get(cf)) for r in rs}
        if not ({"C", "F"} <= roles):
            continue
        stats["mixed_cf_events"] += 1
        nrs = narr_by_event.get(ev_id, [])
        if not nrs:
            stats["mixed_missing_narrative_row"] += 1
            continue

        # Event-level input: choose the longest final narrative available. If all
        # final narratives are empty, fall back to longest preliminary narrative.
        finals = [clean(r.get(finalf)) for r in nrs] if finalf else []
        prelims = [clean(r.get(prelimf)) for r in nrs] if prelimf else []
        final_text = max(finals, key=len, default="")
        prelim_text = max(prelims, key=len, default="")
        input_text = final_text or prelim_text
        input_source = "narr_accf" if final_text else "narr_accp"
        cause_texts = [clean(r.get(causef)) for r in nrs if clean(r.get(causef))]
        cause_text = max(cause_texts, key=len, default="")
        if not input_text:
            stats["mixed_missing_input_narrative"] += 1
            continue
        if not cause_text:
            stats["mixed_missing_probable_cause_narrative"] += 1
            continue
        stats["mixed_with_input_and_cause"] += 1

        lower = input_text.lower()
        leak_probable = "probable cause" in lower
        leak_factor = "contributing factor" in lower or "contributing factors" in lower
        if leak_probable:
            stats["input_contains_probable_cause_phrase"] += 1
        if leak_factor:
            stats["input_contains_contributing_factor_phrase"] += 1

        candidates = []
        for r in sorted(
            rs,
            key=lambda x: (
                clean(x.get(acf)) if acf else "",
                clean(x.get(nof)) if nof else "",
                clean(x.get(df)),
            ),
        ):
            role = norm_cause(r.get(cf))
            desc_raw = clean(r.get(df))
            desc = strip_legacy_role_suffix(desc_raw, role)
            candidates.append(
                {
                    "aircraft_key": clean(r.get(acf)) if acf else None,
                    "finding_no": clean(r.get(nof)) if nof else None,
                    "finding_text": desc,
                    "gold_relevant": norm_bool(r.get(pc)) == "T",
                    "gold_legacy_role": role if role in {"C", "F"} else None,
                }
            )

        population.append(
            {
                "ev_id": ev_id,
                "input_narrative_source": input_source,
                "input_narrative": input_text,
                "hidden_probable_cause_narrative": cause_text,
                "input_contains_probable_cause_phrase": leak_probable,
                "input_contains_contributing_factor_phrase": leak_factor,
                "candidates": candidates,
            }
        )

    population.sort(key=lambda x: rank(args.seed, x["ev_id"]))
    audit20 = population[:20]
    # For first G0 manifest, exclude explicit role-language leakage using a rule
    # fixed before model outputs. This is an input-quality filter, not a result rescue.
    leak_clean = [
        x
        for x in population
        if not x["input_contains_probable_cause_phrase"]
        and not x["input_contains_contributing_factor_phrase"]
    ]
    manifest = leak_clean[: args.manifest_n]

    (out / "population_stats.json").write_text(
        json.dumps(
            {
                "counts": dict(stats),
                "population_with_input_and_cause": len(population),
                "leak_clean_population": len(leak_clean),
                "manifest_n_requested": args.manifest_n,
                "manifest_n_written": len(manifest),
                "sampling": "SHA256(seed || ev_id) deterministic rank",
                "seed": args.seed,
                "narrative_fields": {
                    "preferred_input": "narr_accf (NTSB Final Narrative)",
                    "fallback_input": "narr_accp (NTSB Preliminary Narrative)",
                    "held_out_gold_only": "narr_cause (NTSB Probable Cause Narrative)",
                },
                "anti_leakage": {
                    "finding_description_legacy_suffix_removed": True,
                    "manifest_excludes_input_phrase_probable_cause": True,
                    "manifest_excludes_input_phrase_contributing_factor": True,
                },
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (out / "random20_population_audit.json").write_text(
        json.dumps(audit20, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    with (out / "g0_manifest_300.jsonl").open("w", encoding="utf-8") as f:
        for x in manifest:
            f.write(json.dumps(x, ensure_ascii=False) + "\n")

    print((out / "population_stats.json").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
