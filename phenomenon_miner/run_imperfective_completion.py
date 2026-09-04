#!/usr/bin/env python3
"""Smoke-test whether ongoing telic events are treated as completed states."""

import argparse
import asyncio
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import httpx


EVENTS = [
    ("file upload", "uploading the archive to the server", "the archive is fully stored on the server"),
    ("bank transfer", "transferring the funds to the recipient", "the recipient has received the funds"),
    ("software deployment", "deploying the release to production", "the release is live in production"),
    ("database migration", "migrating the customer records", "all customer records are in the new database"),
    ("backup restoration", "restoring the backup", "the backup has been fully restored"),
    ("contract approval", "approving the vendor contract", "the vendor contract is approved"),
    ("account creation", "creating the customer account", "the customer account exists and is active"),
    ("order shipment", "shipping the customer's order", "the order has been shipped"),
    ("report generation", "generating the compliance report", "the compliance report is complete"),
    ("machine calibration", "calibrating the measurement device", "the device is calibrated"),
    ("data export", "exporting the research dataset", "the dataset export is complete"),
    ("payment refund", "refunding the customer's payment", "the customer has received the refund"),
    ("access revocation", "revoking the contractor's access", "the contractor's access is revoked"),
    ("certificate issuance", "issuing the safety certificate", "the safety certificate has been issued"),
    ("clinical enrollment", "enrolling the participant in the trial", "the participant is enrolled"),
    ("application review", "reviewing and approving the loan application", "the loan application is approved"),
    ("document signing", "signing the final agreement", "the final agreement has been signed"),
    ("inventory update", "updating the inventory records", "all inventory records are updated"),
    ("building construction", "constructing the emergency shelter", "the emergency shelter is complete"),
    ("identity verification", "verifying the new user's identity", "the user's identity is verified"),
]


def build_items():
    rows = []
    for index, (domain, progressive, outcome) in enumerate(EVENTS):
        ongoing = (
            f"At 09:00, the operational log reported that the team was {progressive}. "
            "No later status or completion message is available."
        )
        completed = (
            f"At 09:00, the operational log reported that the team completed the {domain}. "
            f"A completion message confirms that {outcome}."
        )
        interrupted = (
            f"At 09:00, the team began {progressive}, but an error stopped the process "
            f"before it finished. The log confirms that it was not completed, so {outcome} is false."
        )
        for condition, context, outcome_gold, ongoing_gold in [
            ("ongoing_telic", ongoing, "UNKNOWN", "YES"),
            ("completed_telic", completed, "YES", "NO"),
            ("interrupted_telic", interrupted, "NO", "NO"),
        ]:
            rows.append({
                "id": f"{index:02d}_{condition}", "domain": domain,
                "condition": condition, "context": context,
                "outcome_gold": outcome_gold, "ongoing_gold": ongoing_gold,
                "outcome_prompt": (
                    f"{context}\n\nBased only on this record, is it established that {outcome}? "
                    "Answer only YES, NO, or UNKNOWN."
                ),
                "aspect_prompt": (
                    f"{context}\n\nDoes the record present the process as still ongoing, with "
                    "completion not stated? Answer only YES or NO."
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
    items = build_items()
    sem = asyncio.Semaphore(args.concurrency)
    async with httpx.AsyncClient() as client:
        tasks = []
        for item in items:
            tasks += [ask(client, args.endpoint, args.model, item["aspect_prompt"], sem),
                      ask(client, args.endpoint, args.model, item["outcome_prompt"], sem)]
        outputs = await asyncio.gather(*tasks)
    rows = []
    for i, item in enumerate(items):
        aspect_text, outcome_text = outputs[2*i:2*i+2]
        row = {**item, "aspect_response": aspect_text, "outcome_response": outcome_text,
               "aspect_prediction": parse(aspect_text, ["YES", "NO"]),
               "outcome_prediction": parse(outcome_text, ["YES", "NO", "UNKNOWN"])}
        row["aspect_correct"] = row["aspect_prediction"] == row["ongoing_gold"]
        row["outcome_correct"] = row["outcome_prediction"] == row["outcome_gold"]
        row["recognition_use_failure"] = row["aspect_correct"] and not row["outcome_correct"]
        rows.append(row)
    grouped = defaultdict(list)
    for row in rows: grouped[row["condition"]].append(row)
    summary = {"model": args.model, "by_condition": {}}
    for condition, rs in grouped.items():
        summary["by_condition"][condition] = {
            "n": len(rs),
            "aspect_accuracy": sum(r["aspect_correct"] for r in rs)/len(rs),
            "outcome_accuracy": sum(r["outcome_correct"] for r in rs)/len(rs),
            "recognition_use_failures": sum(r["recognition_use_failure"] for r in rs),
            "outcome_predictions": dict(Counter(r["outcome_prediction"] for r in rs)),
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
    parser.add_argument("--concurrency", type=int, default=32)
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
