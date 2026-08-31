#!/usr/bin/env python3
"""Phase C — data-only population audit of the NTSB Findings table.

No LLM calls. Produces:
  audit/population_summary.json
  audit/cause_factor_cm_inPC_crosstab.csv
  audit/mixed_role_summary.json
  audit/findings_per_event.csv
  audit/cf_by_year.csv

Semantic rule enforced throughout (NTSB_LOCAL_AGENT_HANDOFF_2026-08-31.md sec. 2):
    cm_inPc  = finding was cited in the probable-cause statement as a cause OR a
               contributing factor  -> RELEVANCE, never C-vs-F gold.
    Cause_Factor = legacy C (cause) vs F (contributing factor) ROLE label.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPORT = ROOT / "export"
AUDIT = ROOT / "audit"

csv.field_size_limit(10_000_000)


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8", errors="replace") as fh:
        return list(csv.DictReader(fh))


def norm(value: str | None) -> str:
    return (value or "").strip()


def main() -> None:
    findings = read_csv(EXPORT / "Findings.csv")
    events = read_csv(EXPORT / "events.csv")
    narratives = read_csv(EXPORT / "narratives.csv")

    ev_year = {}
    ev_type = {}
    ev_invest = {}
    for row in events:
        eid = norm(row["ev_id"])
        ev_year[eid] = norm(row.get("ev_year"))
        ev_type[eid] = norm(row.get("ev_type"))
        ev_invest[eid] = norm(row.get("invest_agy"))

    # ---- narrative availability -------------------------------------------
    narr_have_accp = set()
    narr_have_accf = set()
    narr_have_cause = set()
    for row in narratives:
        eid = norm(row["ev_id"])
        if norm(row.get("narr_accp")):
            narr_have_accp.add(eid)
        if norm(row.get("narr_accf")):
            narr_have_accf.add(eid)
        if norm(row.get("narr_cause")):
            narr_have_cause.add(eid)

    # ---- findings-table audit ---------------------------------------------
    cf_counter: Counter[str] = Counter()
    inpc_counter: Counter[str] = Counter()
    crosstab: Counter[tuple[str, str]] = Counter()
    desc_missing = 0
    code_missing = 0
    # does finding_description literally end in the role letter?
    suffix_role = Counter()

    per_event: dict[str, Counter] = defaultdict(Counter)
    per_event_ac: dict[tuple[str, int], Counter] = defaultdict(Counter)

    for row in findings:
        eid = norm(row["ev_id"])
        cf = norm(row.get("Cause_Factor")) or "<blank>"
        inpc = norm(row.get("cm_inPc")) or "<blank>"
        cf_counter[cf] += 1
        inpc_counter[inpc] += 1
        crosstab[(cf, inpc)] += 1
        desc = norm(row.get("finding_description"))
        if not desc:
            desc_missing += 1
        if not norm(row.get("finding_code")):
            code_missing += 1
        m = re.search(r"\s-\s([CF])\s*$", desc)
        suffix_role[m.group(1) if m else "<none>"] += 1

        key = "C" if cf == "C" else "F" if cf == "F" else "other"
        per_event[eid][key] += 1
        try:
            ackey = int(norm(row.get("Aircraft_Key")) or 0)
        except ValueError:
            ackey = 0
        per_event_ac[(eid, ackey)][key] += 1

    # ---- C/F availability by year -----------------------------------------
    by_year = defaultdict(Counter)
    for row in findings:
        eid = norm(row["ev_id"])
        y = ev_year.get(eid, "<no-event-row>")
        cf = norm(row.get("Cause_Factor")) or "<blank>"
        inpc = norm(row.get("cm_inPc")) or "<blank>"
        by_year[y][f"cf_{cf}"] += 1
        by_year[y][f"inpc_{inpc}"] += 1
        by_year[y]["rows"] += 1

    # ---- mixed-role events -------------------------------------------------
    mixed_events = [e for e, c in per_event.items() if c["C"] >= 1 and c["F"] >= 1]
    mixed_set = set(mixed_events)
    mixed_C = sum(per_event[e]["C"] for e in mixed_events)
    mixed_F = sum(per_event[e]["F"] for e in mixed_events)
    mixed_other = sum(per_event[e]["other"] for e in mixed_events)

    mixed_ac = [k for k, c in per_event_ac.items() if c["C"] >= 1 and c["F"] >= 1]

    def dist(vals: list[int]) -> dict:
        vals = sorted(vals)
        if not vals:
            return {}
        n = len(vals)
        return {
            "n": n,
            "min": vals[0],
            "p25": vals[n // 4],
            "median": vals[n // 2],
            "p75": vals[(3 * n) // 4],
            "max": vals[-1],
            "mean": round(sum(vals) / n, 3),
        }

    mixed_year = Counter(ev_year.get(e, "<none>") for e in mixed_events)
    mixed_type = Counter(ev_type.get(e, "<none>") for e in mixed_events)
    mixed_agy = Counter(ev_invest.get(e, "<none>") for e in mixed_events)

    narr_ok = sum(1 for e in mixed_events if e in narr_have_accp)
    narr_accf_ok = sum(1 for e in mixed_events if e in narr_have_accf)
    narr_cause_ok = sum(1 for e in mixed_events if e in narr_have_cause)

    population = {
        "source_artifact": "raw/avall.mdb (official NTSB avall.zip)",
        "findings_rows": len(findings),
        "findings_columns": list(findings[0].keys()) if findings else [],
        "events_rows": len(events),
        "narrative_rows": len(narratives),
        "unique_events_in_findings": len(per_event),
        "unique_event_aircraft_in_findings": len(per_event_ac),
        "cause_factor_values": dict(cf_counter),
        "cause_factor_missing_frac": round(cf_counter["<blank>"] / max(len(findings), 1), 5),
        "cm_inPc_values": dict(inpc_counter),
        "cm_inPc_missing_frac": round(inpc_counter["<blank>"] / max(len(findings), 1), 5),
        "finding_description_missing": desc_missing,
        "finding_code_missing": code_missing,
        "finding_description_trailing_role_suffix": dict(suffix_role),
        "findings_per_event": dist([sum(c.values()) for c in per_event.values()]),
        "event_year_range": sorted(v for v in set(ev_year.values()) if v),
        "narratives_available_all_events": {
            "narr_accp_factual": len(narr_have_accp),
            "narr_accf_final": len(narr_have_accf),
            "narr_cause_probable_cause": len(narr_have_cause),
        },
    }

    mixed = {
        "definition": "event has >=1 Cause_Factor=='C' AND >=1 Cause_Factor=='F'",
        "mixed_role_events": len(mixed_events),
        "mixed_role_event_aircraft_units": len(mixed_ac),
        "C_rows_in_mixed_events": mixed_C,
        "F_rows_in_mixed_events": mixed_F,
        "CF_rows_in_mixed_events": mixed_C + mixed_F,
        "non_CF_rows_in_mixed_events": mixed_other,
        "C_per_mixed_event": dist([per_event[e]["C"] for e in mixed_events]),
        "F_per_mixed_event": dist([per_event[e]["F"] for e in mixed_events]),
        "non_CF_per_mixed_event": dist([per_event[e]["other"] for e in mixed_events]),
        "mixed_by_year": dict(sorted(mixed_year.items())),
        "mixed_by_ev_type": dict(mixed_type),
        "mixed_by_invest_agy": dict(mixed_agy),
        "mixed_with_narr_accp_factual": narr_ok,
        "mixed_with_narr_accf_final": narr_accf_ok,
        "mixed_with_narr_cause": narr_cause_ok,
        "n_years_with_mixed_events": len([y for y, c in mixed_year.items() if c > 0]),
        "max_single_year_share": (
            round(max(mixed_year.values()) / len(mixed_events), 4) if mixed_events else None
        ),
    }

    # preregistered minimum viability gate (handoff sec. 5.3)
    gate = {
        "criterion": ">=500 mixed-role events AND >=1000 C/F rows in mixed events AND spread across years/categories",
        "mixed_role_events": len(mixed_events),
        "cf_rows_in_mixed_events": mixed_C + mixed_F,
        "years_with_mixed": mixed["n_years_with_mixed_events"],
        "max_single_year_share": mixed["max_single_year_share"],
        "pass_events_500": len(mixed_events) >= 500,
        "pass_cf_rows_1000": (mixed_C + mixed_F) >= 1000,
    }
    gate["verdict"] = "PASS" if gate["pass_events_500"] and gate["pass_cf_rows_1000"] else "FAIL"

    AUDIT.mkdir(parents=True, exist_ok=True)
    (AUDIT / "population_summary.json").write_text(
        json.dumps({"population": population, "minimum_viability_gate": gate}, indent=2), encoding="utf-8"
    )
    (AUDIT / "mixed_role_summary.json").write_text(json.dumps(mixed, indent=2), encoding="utf-8")

    with (AUDIT / "cause_factor_cm_inPC_crosstab.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["Cause_Factor", "cm_inPc", "n_findings"])
        for (cf, inpc), n in sorted(crosstab.items()):
            w.writerow([cf, inpc, n])

    with (AUDIT / "cf_by_year.csv").open("w", newline="", encoding="utf-8") as fh:
        keys = sorted({k for c in by_year.values() for k in c})
        w = csv.writer(fh)
        w.writerow(["ev_year", *keys, "mixed_role_events"])
        for y in sorted(by_year):
            w.writerow([y, *[by_year[y][k] for k in keys], mixed_year.get(y, 0)])

    (AUDIT / "mixed_role_event_ids.txt").write_text("\n".join(sorted(mixed_set)), encoding="utf-8")

    json.dump({"population": population, "minimum_viability_gate": gate, "mixed": mixed},
              sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
