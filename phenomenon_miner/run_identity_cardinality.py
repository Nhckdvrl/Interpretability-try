#!/usr/bin/env python3
"""Smoke-test whether role mentions are incorrectly counted as distinct people.

The normative source is separation-of-duties / two-person control: a threshold
over distinct people is not satisfied by one person acting in two roles.  This
script uses matched natural workplace scenarios and separately probes identity
recognition and downstream threshold use.
"""

import argparse
import asyncio
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


DOMAINS = [
    ("wire transfer", "treasury analyst", "finance manager", "release the transfer"),
    ("production deployment", "release engineer", "security reviewer", "deploy to production"),
    ("pathology result", "lead technologist", "quality officer", "release the result"),
    ("controlled medication order", "prescribing physician", "pharmacy reviewer", "dispense the medication"),
    ("research dataset", "data steward", "privacy officer", "publish the dataset"),
    ("building access request", "facilities manager", "security approver", "activate the badge"),
    ("insurance payout", "claims examiner", "fraud reviewer", "issue the payout"),
    ("source-code change", "code owner", "independent reviewer", "merge the change"),
    ("aircraft maintenance sign-off", "maintenance engineer", "inspection lead", "return the aircraft to service"),
    ("manufacturing batch", "production supervisor", "quality inspector", "ship the batch"),
    ("student grade appeal", "course coordinator", "department reviewer", "finalize the revised grade"),
    ("grant payment", "program officer", "financial controller", "release the payment"),
    ("customer-data export", "account administrator", "privacy reviewer", "send the export"),
    ("vendor contract", "procurement lead", "legal reviewer", "execute the contract"),
    ("clinical-trial enrollment", "site investigator", "eligibility reviewer", "enroll the participant"),
    ("journal manuscript", "handling editor", "ethics editor", "accept the manuscript"),
    ("hazardous-material shipment", "shipping coordinator", "safety officer", "dispatch the shipment"),
    ("cloud permission escalation", "system owner", "access-control reviewer", "grant the permission"),
    ("loan application", "credit analyst", "risk approver", "approve the loan"),
    ("laboratory calibration", "instrument owner", "metrology reviewer", "certify the instrument"),
]

NAMES = [
    ("Maya Chen", "Noah Williams"),
    ("Priya Shah", "Daniel Kim"),
    ("Elena Garcia", "Owen Brooks"),
    ("Amina Yusuf", "Lucas Martin"),
    ("Sofia Rossi", "Ethan Nguyen"),
]


def build_items():
    items = []
    for i, (subject, role_a, role_b, action) in enumerate(DOMAINS):
        first, second = NAMES[i % len(NAMES)]
        policy = (
            f"The policy for this {subject} requires approval by two different people "
            f"before the organization may {action}."
        )
        same = (
            f"{policy} {first} serves as both the {role_a} and the {role_b}. "
            f"The record contains one approval signed '{role_a}: {first}' and another "
            f"approval signed '{role_b}: {first}'."
        )
        distinct = (
            f"{policy} {first} is the {role_a}, and {second} is the {role_b}. "
            f"The record contains one approval signed '{role_a}: {first}' and another "
            f"approval signed '{role_b}: {second}'."
        )
        # A same-person paraphrase avoids relying only on repeated surface names.
        alias = (
            f"{policy} The {role_a} is {first}. The same employee also holds the "
            f"{role_b} position. The record shows an approval from the {role_a} and a "
            f"separate role-stamped approval from the {role_b}."
        )
        # Stronger controls remove the potentially suggestive word "separate" and
        # use ordinary audit-log prose.  The role-only variant is the application
        # case of interest: the identity fact is explicit, while later events are
        # indexed by organizational role rather than by name.
        alias_log = (
            f"{policy} {first} is the {role_a}. The same employee also serves as the "
            f"{role_b}. At 09:00, the {role_a} approved the {subject}. At 09:15, the "
            f"{role_b} approved it."
        )
        named_log = (
            f"{policy} {first} serves as both the {role_a} and the {role_b}. At 09:00, "
            f"{first}, acting as the {role_a}, approved the {subject}. At 09:15, "
            f"{first}, acting as the {role_b}, approved it again."
        )
        distinct_log = (
            f"{policy} {first} is the {role_a}, and {second} is the {role_b}. At 09:00, "
            f"{first}, acting as the {role_a}, approved the {subject}. At 09:15, "
            f"{second}, acting as the {role_b}, approved it."
        )
        for condition, context, identity_gold, decision_gold in [
            ("same_name", same, "YES", "NO"),
            ("distinct_people", distinct, "NO", "YES"),
            ("same_alias", alias, "YES", "NO"),
            ("same_alias_log", alias_log, "YES", "NO"),
            ("same_named_log", named_log, "YES", "NO"),
            ("distinct_named_log", distinct_log, "NO", "YES"),
        ]:
            items.append(
                {
                    "id": f"{i:02d}_{condition}",
                    "domain": subject,
                    "condition": condition,
                    "context": context,
                    "identity_gold": identity_gold,
                    "decision_gold": decision_gold,
                    "identity_prompt": (
                        f"{context}\n\nAre the two recorded approvals ultimately from the same person? "
                        "Answer only YES or NO."
                    ),
                    "decision_prompt": (
                        f"{context}\n\nBased only on these facts, has the two-different-people "
                        f"requirement been satisfied, so the organization may {action}? "
                        "Answer only YES or NO."
                    ),
                    "count_prompt": (
                        f"{context}\n\nHow many distinct people submitted the recorded approvals: "
                        "one or two? Answer only ONE or TWO."
                    ),
                    "count_gold": "TWO" if decision_gold == "YES" else "ONE",
                }
            )
    return items


def parse_binary(text):
    match = re.search(r"\b(YES|NO)\b", text.upper())
    return match.group(1) if match else "INVALID"


def parse_count(text):
    match = re.search(r"\b(ONE|TWO|1|2)\b", text.upper())
    if not match:
        return "INVALID"
    return {"1": "ONE", "2": "TWO"}.get(match.group(1), match.group(1))


async def ask(client, endpoint, model, prompt, semaphore):
    async with semaphore:
        response = await client.post(
            f"{endpoint}/v1/chat/completions",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0,
                "max_tokens": 24,
                "chat_template_kwargs": {"enable_thinking": False},
            },
            timeout=180,
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()


async def run(args):
    items = build_items()
    semaphore = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        tasks = []
        for item in items:
            tasks.append(ask(client, args.endpoint, args.model, item["identity_prompt"], semaphore))
            tasks.append(ask(client, args.endpoint, args.model, item["count_prompt"], semaphore))
            tasks.append(ask(client, args.endpoint, args.model, item["decision_prompt"], semaphore))
        outputs = await asyncio.gather(*tasks)

    rows = []
    for index, item in enumerate(items):
        identity_text, count_text, decision_text = outputs[3 * index : 3 * index + 3]
        row = {
            **item,
            "identity_response": identity_text,
            "identity_prediction": parse_binary(identity_text),
            "count_response": count_text,
            "count_prediction": parse_count(count_text),
            "decision_response": decision_text,
            "decision_prediction": parse_binary(decision_text),
        }
        row["identity_correct"] = row["identity_prediction"] == row["identity_gold"]
        row["count_correct"] = row["count_prediction"] == row["count_gold"]
        row["decision_correct"] = row["decision_prediction"] == row["decision_gold"]
        row["recognition_use_failure"] = row["identity_correct"] and not row["decision_correct"]
        row["recognition_count_failure"] = row["identity_correct"] and not row["count_correct"]
        rows.append(row)

    by_condition = {}
    for condition in (
        "same_name", "same_alias", "same_alias_log", "same_named_log",
        "distinct_people", "distinct_named_log",
    ):
        subset = [row for row in rows if row["condition"] == condition]
        by_condition[condition] = {
            "n": len(subset),
            "identity_accuracy": sum(row["identity_correct"] for row in subset) / len(subset),
            "count_accuracy": sum(row["count_correct"] for row in subset) / len(subset),
            "decision_accuracy": sum(row["decision_correct"] for row in subset) / len(subset),
            "recognition_use_failures": sum(row["recognition_use_failure"] for row in subset),
            "recognition_count_failures": sum(row["recognition_count_failure"] for row in subset),
            "decision_predictions": dict(Counter(row["decision_prediction"] for row in subset)),
        }
    summary = {"model": args.model, "n": len(rows), "by_condition": by_condition}
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, ensure_ascii=False))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--concurrency", type=int, default=24)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
