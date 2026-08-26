from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Iterable

FAMILIES = ("legal", "medical", "eligibility")


@dataclass(frozen=True)
class Scenario:
    scenario_id: str
    family: str
    context: str
    critical_fact: str
    direct_evidence: str
    inference_evidence: str
    target_conclusion: str
    alternative_conclusion: str


def generate_scenarios() -> list[Scenario]:
    rows: list[Scenario] = []

    legal_events = [
        "shipment", "court filing", "inspection", "safety report",
        "permit renewal", "payment", "appeal", "incident notice",
    ]
    legal_times = [(9, 20), (11, 35), (14, 50), (16, 10)]
    for event_i, event in enumerate(legal_events):
        for time_i, (hour, minute) in enumerate(legal_times):
            deadline_min = hour * 60 + minute
            delay = (15, 25, 40, 55)[time_i]
            actual = deadline_min + delay
            dh, dm = divmod(deadline_min, 60)
            ah, am = divmod(actual, 60)
            sid = f"legal-{event_i:02d}-{time_i:02d}"
            rows.append(Scenario(
                scenario_id=sid,
                family="legal",
                context=f"A compliance rule says the {event} violates the timing requirement if it occurs after the stated deadline. Treat the official record as accurate.",
                critical_fact=f"The {event} occurred after the deadline.",
                direct_evidence=f"The official record explicitly states: 'The {event} occurred after the deadline.'",
                inference_evidence=f"The official record states that the deadline was {dh:02d}:{dm:02d} and that the {event} occurred at {ah:02d}:{am:02d}.",
                target_conclusion="The timing requirement was violated.",
                alternative_conclusion="The timing requirement was satisfied.",
            ))

    tests = [
        "troponin", "D-dimer", "CRP", "fasting glucose",
        "ALT", "TSH", "LDL", "serum lactate",
    ]
    medical_values = [(10, 13), (20, 27), (50, 63), (100, 118)]
    for test_i, test in enumerate(tests):
        for value_i, (cutoff, measured) in enumerate(medical_values):
            sid = f"medical-{test_i:02d}-{value_i:02d}"
            rows.append(Scenario(
                scenario_id=sid,
                family="medical",
                context=f"For this screening protocol, the {test} screen is positive exactly when the measured value is above the stated cutoff. Treat the laboratory record as accurate.",
                critical_fact=f"The measured {test} value was above the cutoff.",
                direct_evidence=f"The laboratory record explicitly states: 'The measured {test} value was above the cutoff.'",
                inference_evidence=f"The laboratory record states that the {test} cutoff was {cutoff} units and the measured value was {measured} units.",
                target_conclusion="The screen is positive under the stated protocol.",
                alternative_conclusion="The screen is negative under the stated protocol.",
            ))

    quantities = [
        "annual income", "monthly rent burden", "household assets", "commute distance",
        "weekly work hours", "annual electricity use", "outstanding balance", "response time",
    ]
    eligibility_values = [(100, 85), (250, 210), (500, 430), (1000, 880)]
    for q_i, quantity in enumerate(quantities):
        for value_i, (cutoff, observed) in enumerate(eligibility_values):
            sid = f"eligibility-{q_i:02d}-{value_i:02d}"
            rows.append(Scenario(
                scenario_id=sid,
                family="eligibility",
                context=f"Under this program, an applicant qualifies exactly when their {quantity} is below the stated cutoff. Treat the application record as accurate.",
                critical_fact=f"The applicant's {quantity} was below the cutoff.",
                direct_evidence=f"The application record explicitly states: 'The applicant's {quantity} was below the cutoff.'",
                inference_evidence=f"The application record states that the cutoff for {quantity} was {cutoff} units and the applicant's recorded value was {observed} units.",
                target_conclusion="The applicant qualifies under the stated rule.",
                alternative_conclusion="The applicant does not qualify under the stated rule.",
            ))

    _validate_scenarios(rows, strict=True)
    return rows


def _validate_scenarios(rows: Iterable[Scenario], *, strict: bool) -> list[Scenario]:
    rows = list(rows)
    ids = [x.scenario_id for x in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate scenario IDs")
    for row in rows:
        if row.family not in FAMILIES:
            raise ValueError(f"unknown family {row.family!r}")
        values = asdict(row)
        if any(not str(v).strip() for v in values.values()):
            raise ValueError(f"empty field in {row.scenario_id}")
        if row.target_conclusion == row.alternative_conclusion:
            raise ValueError(f"identical conclusions in {row.scenario_id}")
    if strict:
        if len(rows) != 96:
            raise ValueError(f"expected 96 scenarios, found {len(rows)}")
        for family in FAMILIES:
            n = sum(x.family == family for x in rows)
            if n != 32:
                raise ValueError(f"expected 32 {family} scenarios, found {n}")
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
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                rows.append(Scenario(**obj))
            except (json.JSONDecodeError, TypeError) as e:
                raise ValueError(f"malformed scenario line {lineno}") from e
    return _validate_scenarios(rows, strict=strict)
