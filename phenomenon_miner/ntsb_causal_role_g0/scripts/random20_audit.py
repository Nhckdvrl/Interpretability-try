#!/usr/bin/env python3
"""Phase D — fixed-seed random-20 mixed-role semantic / leakage audit.

Writes audit/random20_mixed_role.md and audit/random20_leakage_stats.json.
No LLM calls. SEED is frozen at 20260831 per the handoff.
"""
from __future__ import annotations

import csv, json, random, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
csv.field_size_limit(10_000_000)
SEED = 20260831

ROLE_SUFFIX = re.compile(r"\s-\s([CF])\s*$")
LEAK_TERMS = [
    "probable cause", "contributing factor", "contributing to", "contributed to",
    "the cause of", "causal factor", "factor in the accident", "was the cause",
]


def read(name):
    with (ROOT / "export" / name).open(newline="", encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh))


def strip_role(desc: str) -> str:
    return ROLE_SUFFIX.sub("", (desc or "").strip()).strip()


def main():
    findings = read("Findings.csv")
    events = {r["ev_id"].strip(): r for r in read("events.csv")}
    narr = defaultdict(dict)
    for r in read("narratives.csv"):
        narr[r["ev_id"].strip()][int(r["Aircraft_Key"] or 1)] = r

    by_event = defaultdict(list)
    for r in findings:
        by_event[r["ev_id"].strip()].append(r)

    def cf(r):
        return (r["Cause_Factor"] or "").strip()

    mixed = sorted(e for e, rows in by_event.items()
                   if any(cf(r) == "C" for r in rows) and any(cf(r) == "F" for r in rows))

    rng = random.Random(SEED)
    sample = rng.sample(mixed, 20)

    stats = Counter()
    lines = [
        "# Random-20 Mixed-Role Semantic / Leakage Audit",
        "",
        f"Seed: `{SEED}`  ·  drawn from {len(mixed)} mixed-role events (>=1 `C` and >=1 `F`).",
        "",
        "Model-visible input is **only**: `narr_accp` (NTSB *Factual narrative*) + "
        "role-suffix-stripped `finding_description`. `Cause_Factor`, `cm_inPc`, "
        "`narr_cause` (probable cause) and `narr_accf` are audit-only.",
        "",
        "---",
        "",
    ]

    for i, eid in enumerate(sample, 1):
        ev = events.get(eid, {})
        rows = sorted(by_event[eid], key=lambda r: (int(r["Aircraft_Key"] or 0), int(r["finding_no"] or 0)))
        acks = sorted({int(r["Aircraft_Key"] or 0) for r in rows})
        lines += [
            f"## {i}. `{eid}` — {ev.get('ntsb_no','?')}",
            "",
            f"- date: `{ev.get('ev_date','')}`  year `{ev.get('ev_year','')}`  type `{ev.get('ev_type','')}`",
            f"- location: {ev.get('ev_city','')}, {ev.get('ev_state','')} {ev.get('ev_country','')}",
            f"- Aircraft_Key values in findings: `{acks}`",
            "",
            "### Findings (model sees only the stripped text)",
            "",
            "| ac | # | Cause_Factor | cm_inPc | stripped finding_description | raw suffix | code |",
            "|---:|---:|:---:|:---:|---|:---:|---|",
        ]
        descs = []
        for r in rows:
            raw = (r["finding_description"] or "").strip()
            m = ROLE_SUFFIX.search(raw)
            s = strip_role(raw)
            descs.append(s.lower())
            lines.append(
                f"| {r['Aircraft_Key']} | {r['finding_no']} | `{cf(r) or '-'}` | `{r['cm_inPc']}` | "
                f"{s} | `{m.group(1) if m else '-'}` | `{r['finding_code']}` |"
            )
            stats[f"role_{cf(r) or 'blank'}"] += 1
            if m:
                stats["desc_had_role_suffix"] += 1
        dupes = len(descs) - len(set(descs))
        stats["events_with_duplicate_finding_text"] += 1 if dupes else 0

        for ak in acks:
            n = narr[eid].get(ak) or narr[eid].get(1) or {}
            factual = (n.get("narr_accp") or "").strip()
            cause = (n.get("narr_cause") or "").strip()
            hits = [t for t in LEAK_TERMS if t in factual.lower()]
            if hits:
                stats["events_factual_narrative_contains_leak_term"] += 1
            stats["factual_narrative_present"] += 1 if factual else 0
            lines += [
                "",
                f"### Aircraft_Key {ak} — `narr_accp` FACTUAL NARRATIVE (model-visible), "
                f"{len(factual.split())} words",
                "",
                "> " + (factual.replace("\n", "\n> ") if factual else "*(EMPTY)*"),
                "",
                f"- conclusion-term hits in factual narrative: `{hits}`",
                "",
                "### AUDIT-ONLY `narr_cause` (probable cause — never shown to a model)",
                "",
                "> " + (cause.replace("\n", "\n> ") if cause else "*(EMPTY)*"),
                "",
            ]
        lines += [f"- duplicate stripped finding descriptions in this event: **{dupes}**", "", "---", ""]

    (ROOT / "audit" / "random20_mixed_role.md").write_text("\n".join(lines), encoding="utf-8")

    # ---- population-scale leakage diagnostics (not only the 20) -------------
    pop = Counter()
    for eid in mixed:
        for ak, n in narr.get(eid, {}).items():
            f_ = (n.get("narr_accp") or "").strip().lower()
            if not f_:
                pop["mixed_ac_without_factual_narrative"] += 1
                continue
            pop["mixed_ac_with_factual_narrative"] += 1
            for t in LEAK_TERMS:
                if t in f_:
                    pop[f"leakterm::{t}"] += 1
    out = {"seed": SEED, "sampled_ev_ids": sample, "sample_stats": dict(stats),
           "mixed_population_narrative_leak_scan": dict(pop)}
    (ROOT / "audit" / "random20_leakage_stats.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
