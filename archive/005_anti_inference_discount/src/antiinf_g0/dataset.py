from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

FAMILIES = ("legal", "medical", "eligibility")
OUTCOMES = ("criterion_met", "criterion_not_met")


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    outcome: str
    context: str
    critical_fact: str
    direct_evidence: str
    inference_evidence: str
    target_conclusion: str
    alternative_conclusion: str


def generate_scenarios() -> list[Scenario]:
    rows: list[Scenario] = []

    legal_events = ["shipment", "court filing", "inspection", "safety report", "permit renewal", "payment", "appeal", "incident notice"]
    legal_offsets = (15, 40, -20, -50)
    legal_deadlines = ((9, 20), (11, 35), (14, 50), (16, 10))
    for event_i, event in enumerate(legal_events):
        for variant_i, ((hour, minute), offset) in enumerate(zip(legal_deadlines, legal_offsets, strict=True)):
            deadline = hour * 60 + minute
            actual = deadline + offset
            dh, dm = divmod(deadline, 60)
            ah, am = divmod(actual, 60)
            met = offset > 0
            if met:
                fact = f"The {event} occurred after the deadline."
                direct = f"The official record directly states that the {event} occurred later than the deadline."
                target, alternative = "The timing requirement was violated.", "The timing requirement was satisfied."
            else:
                fact = f"The {event} occurred at or before the deadline."
                direct = f"The official record directly states that the {event} occurred no later than the deadline."
                target, alternative = "The timing requirement was satisfied.", "The timing requirement was violated."
            rows.append(Scenario(
                f"legal-{event_i:02d}-{variant_i:02d}", "legal", "criterion_met" if met else "criterion_not_met",
                f"A compliance rule says the {event} violates the timing requirement exactly when it occurs after the deadline. Treat a direct relation stated in the official record and the record's listed timestamps as equally authoritative and accurate.",
                fact, direct,
                f"The official record lists the deadline as {dh:02d}:{dm:02d} and the {event} time as {ah:02d}:{am:02d}.",
                target, alternative,
            ))

    tests = ["troponin", "D-dimer", "CRP", "fasting glucose", "ALT", "TSH", "LDL", "serum lactate"]
    medical_values = ((10, 13), (20, 27), (50, 46), (100, 92))
    for test_i, test in enumerate(tests):
        for variant_i, (cutoff, measured) in enumerate(medical_values):
            met = measured > cutoff
            if met:
                fact = f"The measured {test} value was above the cutoff."
                direct = f"The laboratory record directly classifies the measured {test} value as exceeding the cutoff."
                target, alternative = "The screen is positive under the stated protocol.", "The screen is negative under the stated protocol."
            else:
                fact = f"The measured {test} value was at or below the cutoff."
                direct = f"The laboratory record directly classifies the measured {test} value as not exceeding the cutoff."
                target, alternative = "The screen is negative under the stated protocol.", "The screen is positive under the stated protocol."
            rows.append(Scenario(
                f"medical-{test_i:02d}-{variant_i:02d}", "medical", "criterion_met" if met else "criterion_not_met",
                f"For this screening protocol, the {test} screen is positive exactly when the measured value is above the cutoff. Treat a direct relation stated in the laboratory record and the record's listed numeric values as equally authoritative and accurate.",
                fact, direct,
                f"The laboratory record lists the {test} cutoff as {cutoff} units and the measured value as {measured} units.",
                target, alternative,
            ))

    quantities = ["annual income", "monthly rent burden", "household assets", "commute distance", "weekly work hours", "annual electricity use", "outstanding balance", "response time"]
    eligibility_values = ((100, 85), (250, 210), (500, 540), (1000, 1120))
    for q_i, quantity in enumerate(quantities):
        for variant_i, (cutoff, observed) in enumerate(eligibility_values):
            met = observed < cutoff
            if met:
                fact = f"The applicant's {quantity} was below the cutoff."
                direct = f"The application record directly classifies the applicant's {quantity} as under the cutoff."
                target, alternative = "The applicant qualifies under the stated rule.", "The applicant does not qualify under the stated rule."
            else:
                fact = f"The applicant's {quantity} was at or above the cutoff."
                direct = f"The application record directly classifies the applicant's {quantity} as not below the cutoff."
                target, alternative = "The applicant does not qualify under the stated rule.", "The applicant qualifies under the stated rule."
            rows.append(Scenario(
                f"eligibility-{q_i:02d}-{variant_i:02d}", "eligibility", "criterion_met" if met else "criterion_not_met",
                f"Under this program, an applicant qualifies exactly when their {quantity} is below the cutoff. Treat a direct relation stated in the application record and the record's listed numeric values as equally authoritative and accurate.",
                fact, direct,
                f"The application record lists the cutoff for {quantity} as {cutoff} units and the applicant's value as {observed} units.",
                target, alternative,
            ))

    return _validate_scenarios(rows, strict=True)


def _validate_scenarios(rows: Iterable[Scenario], *, strict: bool) -> list[Scenario]:
    rows = list(rows)
    ids = [x.scenario_id for x in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate scenario IDs")
    for row in rows:
        if row.family not in FAMILIES:
            raise ValueError(f"unknown family {row.family!r}")
        if row.outcome not in OUTCOMES:
            raise ValueError(f"unknown outcome {row.outcome!r}")
        if any(not str(v).strip() for v in asdict(row).values()):
            raise ValueError(f"empty field in {row.scenario_id}")
        if row.target_conclusion == row.alternative_conclusion:
            raise ValueError(f"identical conclusions in {row.scenario_id}")
        d = row.direct_evidence.strip().lower()
        i = row.inference_evidence.strip().lower()
        fact = row.critical_fact.lower().rstrip(".")
        if d in i or i in d:
            raise ValueError(f"one evidence condition contains the other in {row.scenario_id}")
        if fact in d or fact in i:
            raise ValueError(f"evidence repeats the critical-fact query verbatim in {row.scenario_id}")
    if strict:
        if len(rows) != 96:
            raise ValueError(f"expected 96 scenarios, found {len(rows)}")
        for family in FAMILIES:
            family_rows = [x for x in rows if x.family == family]
            if len(family_rows) != 32:
                raise ValueError(f"expected 32 {family} scenarios, found {len(family_rows)}")
            for outcome in OUTCOMES:
                n = sum(x.outcome == outcome for x in family_rows)
                if n != 16:
                    raise ValueError(f"expected 16 {family}/{outcome} scenarios, found {n}")
    return rows


def write_scenarios(path: str | Path) -> list[Scenario]:
    rows = generate_scenarios()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")
    return rows


def load_scenarios(path: str | Path, *, strict: bool = True) -> list[Scenario]:
    rows: list[Scenario] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                rows.append(Scenario(**json.loads(line)))
            except (json.JSONDecodeError, TypeError) as e:
                raise ValueError(f"malformed scenario line {lineno}") from e
    return _validate_scenarios(rows, strict=strict)
