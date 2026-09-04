#!/usr/bin/env python3
"""Test whether a salient class member captures an unresolved existential witness."""

import argparse
import asyncio
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


CASES = [
    ("service outage", "software defect", "Bug Delta", "contributed to the outage"),
    ("foodborne illness", "contaminated ingredient", "the basil batch", "caused the illness"),
    ("data breach", "compromised credential", "credential C-17", "was used in the breach"),
    ("allergic reaction", "medication given to the patient", "amoxicillin", "caused the reaction"),
    ("factory vibration", "cracked component", "bearing B-4", "caused the vibration"),
    ("false laboratory result", "contaminated sample", "sample S-12", "caused the false result"),
    ("fraud investigation", "flagged transaction", "transfer T-91", "was fraudulent"),
    ("confidential-file leak", "unauthorized account", "account Orion", "downloaded the file"),
    ("invoice audit", "contractor under review", "Apex Services", "submitted the false invoice"),
    ("wetland damage", "invasive plant species", "purple loosestrife", "damaged the wetland"),
    ("aircraft warning", "faulty sensor", "sensor AOA-3", "triggered the warning"),
    ("power interruption", "overloaded circuit", "circuit C-8", "caused the interruption"),
    ("delivery loss", "misrouted parcel", "parcel P-42", "was lost"),
    ("building alarm", "smoke detector with a fault", "detector D-6", "triggered the alarm"),
    ("clinical-trial deviation", "enrollment with a protocol violation", "participant E-19", "caused the deviation"),
    ("database corruption", "failed storage device", "drive R-2", "caused the corruption"),
    ("crop failure", "infected seed lot", "seed lot L-7", "caused the crop failure"),
    ("network slowdown", "misconfigured router", "router Edge-5", "caused the slowdown"),
    ("tax review", "return selected for audit", "return 24-108", "contained the reporting error"),
    ("warehouse shortage", "inventory adjustment", "adjustment J-31", "caused the shortage"),
    ("research anomaly", "instrument with calibration drift", "spectrometer Q", "caused the anomaly"),
    ("security incident", "employee with badge access", "Morgan Lee", "entered the restricted room"),
    ("payment dispute", "merchant transaction", "the Northwind charge", "was unauthorized"),
    ("bridge inspection", "corroded support", "support pier P3", "caused the structural warning"),
]


def build_items():
    rows = []
    for index, (incident, category, entity, predicate) in enumerate(CASES):
        existential = (
            f"Incident summary: At least one {category} {predicate}.\n"
            f"Registry record: {entity} is a {category}."
        )
        universal = (
            f"Incident summary: Every {category} {predicate}.\n"
            f"Registry record: {entity} is a {category}."
        )
        named = (
            f"Incident summary: {entity} {predicate}.\n"
            f"Registry record: {entity} is a {category}."
        )
        negative = (
            f"Incident summary: No {category} {predicate}.\n"
            f"Registry record: {entity} is a {category}."
        )
        for condition, context, attribution_gold, identified_gold in [
            ("existential_member", existential, "UNKNOWN", "NO"),
            ("universal_member", universal, "YES", "YES"),
            ("named_witness", named, "YES", "YES"),
            ("negative_member", negative, "NO", "YES"),
        ]:
            rows.append({
                "id": f"{index:02d}_{condition}", "domain": incident,
                "condition": condition, "context": context,
                "attribution_gold": attribution_gold,
                "identified_gold": identified_gold,
                "membership_prompt": (
                    f"{context}\n\nDoes the registry identify {entity} as a {category}? "
                    "Answer only YES or NO."
                ),
                "identified_prompt": (
                    f"{context}\n\nDoes the incident summary itself identify {entity} as one "
                    f"that {predicate}? Answer only YES or NO."
                ),
                "attribution_prompt": (
                    f"{context}\n\nBased only on these records, is it logically guaranteed that "
                    f"{entity} {predicate}? Answer only YES, NO, or UNKNOWN."
                ),
            })
    return rows


def parse(text, labels):
    matches = re.findall(r"\b(" + "|".join(labels) + r")\b", text.upper())
    return matches[-1] if matches else "INVALID"


async def ask(client, endpoint, model, prompt, semaphore):
    async with semaphore:
        response = await client.post(
            endpoint.rstrip("/") + "/v1/chat/completions",
            json={"model": model, "messages": [{"role": "user", "content": prompt}],
                  "temperature": 0, "max_tokens": 24,
                  "chat_template_kwargs": {"enable_thinking": False}},
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


async def run(args):
    items = build_items(); sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        tasks = []
        for item in items:
            tasks.extend([
                ask(client, args.endpoint, args.model, item["membership_prompt"], sem),
                ask(client, args.endpoint, args.model, item["identified_prompt"], sem),
                ask(client, args.endpoint, args.model, item["attribution_prompt"], sem),
            ])
        outputs = await asyncio.gather(*tasks)
    rows = []
    for i, item in enumerate(items):
        membership, identified, attribution = outputs[3*i:3*i+3]
        row = {**item, "membership_response": membership,
               "identified_response": identified, "attribution_response": attribution,
               "membership_prediction": parse(membership, ["YES", "NO"]),
               "identified_prediction": parse(identified, ["YES", "NO"]),
               "attribution_prediction": parse(attribution, ["YES", "NO", "UNKNOWN"])}
        row["membership_correct"] = row["membership_prediction"] == "YES"
        row["identified_correct"] = row["identified_prediction"] == row["identified_gold"]
        row["attribution_correct"] = row["attribution_prediction"] == row["attribution_gold"]
        row["capture"] = (item["condition"] == "existential_member" and
                          row["membership_correct"] and row["identified_correct"] and
                          row["attribution_prediction"] == "YES")
        rows.append(row)
    by = defaultdict(list)
    for row in rows: by[row["condition"]].append(row)
    summary = {"model": args.model, "by_condition": {}}
    for condition, rs in by.items():
        summary["by_condition"][condition] = {
            "n": len(rs),
            "membership_accuracy": sum(r["membership_correct"] for r in rs)/len(rs),
            "identified_accuracy": sum(r["identified_correct"] for r in rs)/len(rs),
            "attribution_accuracy": sum(r["attribution_correct"] for r in rs)/len(rs),
            "capture_count": sum(r["capture"] for r in rs),
            "attribution_predictions": dict(Counter(r["attribution_prediction"] for r in rs)),
        }
    out = Path(args.output); out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2,
                              ensure_ascii=False))
    print(json.dumps(summary, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--concurrency", type=int, default=48)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
