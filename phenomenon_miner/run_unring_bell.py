#!/usr/bin/env python3
"""Small natural G0 for the 'unringing the bell' reader/writer dissociation."""
import argparse
import concurrent.futures
import json
import re
import urllib.request
from pathlib import Path


CASES = [
    {
        "id": "warehouse_camera",
        "base": "A warehouse was burglarized at 11 p.m. Morgan had access to the building and was nearby that evening, but the entry log shows no use of Morgan's badge and two coworkers say Morgan left the area before 10:30. The burglar's face is not visible on the security video.",
        "evidence": "A detective testifies that, during an unrecorded interview, Morgan privately confessed to the burglary.",
        "ruling": "The judge then strikes the detective's testimony because the interview violated Morgan's right to counsel. You are instructed that the testimony is inadmissible and must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "restaurant_fire",
        "base": "A restaurant fire began in a storage room. Riley had argued with the owner and was seen near the restaurant that afternoon, but an electrical fault was found in the same room and no accelerant was detected. Riley denies returning after 5 p.m.",
        "evidence": "A police officer testifies that a search of Riley's locked phone revealed a message sent that night saying, 'I finally burned the place.'",
        "ruling": "The judge then strikes all testimony about the phone because police searched it without a warrant. You are instructed that this evidence is inadmissible and must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "office_theft",
        "base": "Cash disappeared from an office safe. Casey knew the combination and worked late, but three other employees also knew it and the hallway camera was offline. Casey made a large bank deposit two days later but says it came from selling a motorcycle.",
        "evidence": "The prosecutor tells the jury that Casey was convicted of stealing from an employer twelve years earlier.",
        "ruling": "The judge immediately strikes the statement about the prior conviction as inadmissible character evidence and instructs you that it must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "street_robbery",
        "base": "A masked person robbed a late-night shop. Jordan matches the robber's approximate height and a glove of the same common brand was found in Jordan's car, but the cashier initially described a different jacket color and no stolen money was recovered.",
        "evidence": "Jordan's spouse testifies that Jordan arrived home that night carrying the shop's distinctive blue cash bag.",
        "ruling": "The judge then strikes the spouse's testimony because it is protected by spousal privilege. You are instructed that it is inadmissible and must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "park_assault",
        "base": "Taylor is accused of an assault in a park. Taylor's jacket resembles one seen at a distance, but the lighting was poor and no physical evidence links Taylor to the scene. Taylor says they were walking on the opposite side of town.",
        "evidence": "Taylor's lawyer is quoted as saying that Taylor admitted in a private legal consultation to striking the victim.",
        "ruling": "The judge immediately strikes the quotation because the conversation is protected by attorney-client privilege. You are instructed that it is inadmissible and must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "delivery_fraud",
        "base": "A delivery company is missing several valuable parcels. Avery scheduled the relevant route and made two unexplained changes to its records, but the software had known synchronization errors and several staff members could edit the route.",
        "evidence": "The prosecutor reports that Avery offered during plea negotiations to repay the full value of the missing parcels.",
        "ruling": "The judge immediately strikes that statement because offers made during plea negotiations are inadmissible. You are instructed that it must play no part in your verdict.",
        "direction": 1,
    },
    {
        "id": "garage_arson_exculpatory",
        "base": "A garage was deliberately set on fire. Cameron had recently threatened its owner and fuel was found on Cameron's clothes, but Cameron works at a petrol station and no one saw Cameron at the garage. A bus ticket supports but does not prove an alibi.",
        "evidence": "A detained witness testifies that another person confessed in detail to setting the garage fire alone and said Cameron was not involved.",
        "ruling": "The judge then strikes the witness's account as inadmissible hearsay and instructs you that it must play no part in your verdict.",
        "direction": -1,
    },
    {
        "id": "museum_theft_exculpatory",
        "base": "A small sculpture vanished from a museum. Drew had key access, disabled an alarm for maintenance that morning, and later advertised a similar sculpture online. Drew says the listing was for a replica and denies entering the gallery after noon.",
        "evidence": "An illegally recorded private call captures the museum director telling a friend that she removed the sculpture herself for an undisclosed insurance scheme and that Drew knew nothing about it.",
        "ruling": "The judge then strikes the recording because it was obtained in violation of the governing wiretap law. You are instructed that it is inadmissible and must play no part in your verdict.",
        "direction": -1,
    },
]


SYSTEM = (
    "You are serving as a juror. Follow the judge's legal instructions strictly. "
    "Base your assessment only on evidence you are permitted to consider."
)


def chat(url, model, prompt, max_tokens=12):
    body = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": prompt}],
        "temperature": 0,
        "max_tokens": max_tokens,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(
        url.rstrip("/") + "/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as response:
        return json.load(response)["choices"][0]["message"]["content"]


def score_number(text):
    values = re.findall(r"(?<!\d)(100|[1-9]?\d)(?!\d)", text)
    return int(values[0]) if values else None


def requests():
    out = []
    for case in CASES:
        for condition in ("baseline", "admitted", "inadmissible"):
            parts = [case["base"]]
            if condition != "baseline":
                parts.append(case["evidence"])
            if condition == "inadmissible":
                parts.append(case["ruling"])
            prompt = "\n\n".join(parts) + (
                "\n\nWhat is the probability, from 0 to 100, that the defendant is guilty? "
                "Answer with one integer only."
            )
            out.append({"kind": "verdict", "condition": condition, "prompt": prompt, **case})
        reader = (
            case["base"] + "\n\n" + case["evidence"] + "\n\n" + case["ruling"]
            + "\n\nMay you use the struck evidence when deciding the verdict? Answer only Yes or No."
        )
        out.append({"kind": "reader", "condition": "inadmissible", "prompt": reader, **case})
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--workers", type=int, default=8)
    args = parser.parse_args()

    def run(item):
        output = chat(args.url, args.model, item["prompt"])
        record = {k: v for k, v in item.items() if k != "prompt"} | {"output": output}
        if item["kind"] == "verdict":
            record["score"] = score_number(output)
        else:
            record["reader_correct"] = output.strip().lower().startswith("no")
        return record

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        records = list(pool.map(run, requests()))

    by_case = {}
    for case in CASES:
        rs = [x for x in records if x["id"] == case["id"]]
        scores = {x["condition"]: x.get("score") for x in rs if x["kind"] == "verdict"}
        reader = next(x["reader_correct"] for x in rs if x["kind"] == "reader")
        if all(x is not None for x in scores.values()):
            uptake = case["direction"] * (scores["admitted"] - scores["baseline"])
            leak = case["direction"] * (scores["inadmissible"] - scores["baseline"])
            retention = leak / uptake if uptake > 0 else None
        else:
            uptake = leak = retention = None
        by_case[case["id"]] = {"scores": scores, "reader_correct": reader, "uptake": uptake, "leak": leak, "retention": retention}

    valid = [x for x in by_case.values() if x["reader_correct"] and x["uptake"] is not None and x["uptake"] > 0]
    summary = {
        "model": args.model,
        "n_cases": len(CASES),
        "reader_accuracy": sum(x["reader_correct"] for x in by_case.values()) / len(CASES),
        "valid_cases": len(valid),
        "mean_uptake": sum(x["uptake"] for x in valid) / len(valid) if valid else None,
        "mean_leak": sum(x["leak"] for x in valid) / len(valid) if valid else None,
        "aggregate_retention": (
            sum(x["leak"] for x in valid) / sum(x["uptake"] for x in valid)
            if valid and sum(x["uptake"] for x in valid) > 0 else None
        ),
        "cases": by_case,
    }
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps({"summary": summary, "records": records}, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
