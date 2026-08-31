#!/usr/bin/env python3
"""Freeze the G0 sample and build items. Implements PREREGISTRATION.md sections 3-6.

Deterministic. No LLM calls. Run before any model is loaded.
"""
from __future__ import annotations

import csv, hashlib, json, random, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
csv.field_size_limit(10_000_000)

SEED = 20260831
TARGET_EVENTS = 600
MIN_NARR_WORDS = 60
MAX_NARR_WORDS = 1200

ROLE_SUFFIX = re.compile(r"\s-\s([CF])\s*$")

# E4: accident-role wording. "cause of death" / autopsy "contributory condition"
# are explicitly not matches.
LEAK = re.compile(
    r"probable\s+cause"
    r"|contributing\s+factors?"
    r"|contributed\s+to"
    r"|contributing\s+to"
    r"|causal\s+factor"
    r"|was\s+the\s+cause"
    r"|the\s+cause\s+of\s+the\s+accident",
    re.I,
)
DEATH = re.compile(r"cause\s+of\s+death", re.I)


def read(name):
    with (ROOT / "export" / name).open(newline="", encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh))


def strip_role(desc: str) -> str:
    return ROLE_SUFFIX.sub("", (desc or "").strip()).strip()


def leaky(text: str) -> list[str]:
    masked = DEATH.sub("XXXX", text or "")
    return sorted({m.group(0).lower() for m in LEAK.finditer(masked)})


def main() -> None:
    findings = read("Findings.csv")
    events = {r["ev_id"].strip(): r for r in read("events.csv")}
    narr: dict[tuple[str, int], dict] = {}
    for r in read("narratives.csv"):
        narr[(r["ev_id"].strip(), int(r["Aircraft_Key"] or 1))] = r

    units: dict[tuple[str, int], list[dict]] = defaultdict(list)
    for r in findings:
        units[(r["ev_id"].strip(), int(r["Aircraft_Key"] or 0))].append(r)

    def cf(r):
        return (r["Cause_Factor"] or "").strip()

    attrition = Counter()
    eligible: dict[str, tuple[int, list[dict], str, bool]] = {}

    for (eid, ak), rows in sorted(units.items()):
        cs = [r for r in rows if cf(r) == "C"]
        fs = [r for r in rows if cf(r) == "F"]
        if not (cs and fs):
            attrition["E1_not_mixed_role"] += 1
            continue
        if any(not strip_role(r["finding_description"]) for r in cs + fs):
            attrition["E2_empty_finding_text"] += 1
            continue
        n = narr.get((eid, ak))
        raw = (n or {}).get("narr_accp", "").strip()
        words = raw.split()
        if len(words) < MIN_NARR_WORDS:
            attrition["E3_no_or_short_factual_narrative"] += 1
            continue
        if leaky(raw):
            attrition["E4_narrative_role_wording"] += 1
            continue
        seen: dict[str, str] = {}
        conflict = False
        for r in cs + fs:
            t = strip_role(r["finding_description"])
            if seen.setdefault(t, cf(r)) != cf(r):
                conflict = True
        if conflict:
            attrition["E5_same_text_role_conflict"] += 1
            continue
        truncated = len(words) > MAX_NARR_WORDS
        text = " ".join(words[:MAX_NARR_WORDS])
        # one Aircraft_Key per event: keep the lowest eligible one
        if eid in eligible and eligible[eid][0] <= ak:
            attrition["E6_extra_aircraft_key_in_same_event"] += 1
            continue
        eligible[eid] = (ak, rows, text, truncated)

    # ---- frozen stratified draw -------------------------------------------
    rng = random.Random(SEED)
    by_year = defaultdict(list)
    for eid in sorted(eligible):
        by_year[events[eid].get("ev_year", "").strip()].append(eid)

    total = len(eligible)
    take = min(TARGET_EVENTS, total)
    exact = {y: len(v) * take / total for y, v in by_year.items()}
    alloc = {y: int(v) for y, v in exact.items()}
    for y in sorted(exact, key=lambda y: (-(exact[y] - alloc[y]), y))[: take - sum(alloc.values())]:
        alloc[y] += 1

    chosen: list[str] = []
    for y in sorted(by_year):
        pool = sorted(by_year[y])
        chosen += rng.sample(pool, alloc[y])
    chosen.sort()

    # ---- items -------------------------------------------------------------
    ev_rows, rel_rows, role_rows = [], [], []
    drop = Counter()
    for eid in chosen:
        ak, rows, text, truncated = eligible[eid]
        ev = events[eid]
        ev_rows.append({
            "ev_id": eid, "aircraft_key": ak, "ntsb_no": ev.get("ntsb_no", ""),
            "ev_year": ev.get("ev_year", ""), "ev_type": ev.get("ev_type", ""),
            "ev_date": ev.get("ev_date", ""),
            "narrative": text, "narrative_truncated": truncated,
            "narrative_words": len(text.split()),
        })
        for r in sorted(rows, key=lambda r: int(r["finding_no"] or 0)):
            if int(r["Aircraft_Key"] or 0) != ak:
                continue
            label = cf(r)
            t = strip_role(r["finding_description"])
            if not t:
                drop["empty_text"] += 1
                continue
            iid = f"{eid}:{ak}:{r['finding_no']}"
            inpc = (r["cm_inPc"] or "").strip()
            if label in ("C", "F"):
                rel_rows.append({"item_id": iid, "ev_id": eid, "aircraft_key": ak,
                                 "finding": t, "gold": "YES"})
                role_rows.append({"item_id": iid, "ev_id": eid, "aircraft_key": ak,
                                  "finding": t,
                                  "gold": "CAUSE" if label == "C" else "CONTRIBUTING_FACTOR",
                                  "contributed_to_outcome_modifier":
                                      t.split("-")[-1] == "Contributed to outcome"})
            elif inpc == "F":
                rel_rows.append({"item_id": iid, "ev_id": eid, "aircraft_key": ak,
                                 "finding": t, "gold": "NO"})
            else:
                drop["blank_cause_factor_but_cm_inPc_T"] += 1

    it = ROOT / "items"
    it.mkdir(exist_ok=True)
    for name, rows in [("g0_events", ev_rows), ("g0_relevance", rel_rows), ("g0_roles", role_rows)]:
        with (it / f"{name}.jsonl").open("w", encoding="utf-8") as fh:
            for r in rows:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    ev_with_neg = len({r["ev_id"] for r in rel_rows if r["gold"] == "NO"})
    manifest = {
        "seed": SEED,
        "frozen_at": "2026-08-31 (before any model load)",
        "preregistration": "PREREGISTRATION.md",
        "source_sha256_avall_zip": "0cf30a610d18eb109035b83106c227b248f27c6cff794ce622548f44c455238a",
        "eligibility": {
            "E1": "unit has >=1 Cause_Factor=C and >=1 Cause_Factor=F",
            "E2": "all C/F findings have non-empty text after role-suffix stripping",
            "E3": f"narr_accp present and >= {MIN_NARR_WORDS} words",
            "E4": "narr_accp contains no accident-role wording (cause-of-death excluded)",
            "E5": "no identical stripped finding text with conflicting C/F role",
            "E6": "one Aircraft_Key per event (lowest eligible)",
        },
        "attrition_units": dict(attrition),
        "eligible_events": total,
        "target_events": TARGET_EVENTS,
        "sampled_events": len(chosen),
        "year_allocation": {y: alloc[y] for y in sorted(alloc) if alloc[y]},
        "eligible_by_year": {y: len(v) for y, v in sorted(by_year.items())},
        "narrative_field": "narratives.narr_accp (NTSB 'Factual narrative')",
        "narrative_max_words": MAX_NARR_WORDS,
        "narratives_truncated": sum(1 for r in ev_rows if r["narrative_truncated"]),
        "relevance_items": len(rel_rows),
        "relevance_gold": dict(Counter(r["gold"] for r in rel_rows)),
        "relevance_events_with_at_least_one_negative": ev_with_neg,
        "role_items": len(role_rows),
        "role_gold": dict(Counter(r["gold"] for r in role_rows)),
        "role_items_with_contributed_to_outcome_modifier":
            sum(1 for r in role_rows if r["contributed_to_outcome_modifier"]),
        "dropped_items": dict(drop),
        "items_sha256": {
            f"{n}.jsonl": hashlib.sha256((it / f"{n}.jsonl").read_bytes()).hexdigest()
            for n in ("g0_events", "g0_relevance", "g0_roles")
        },
    }
    (it / "sampling_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
