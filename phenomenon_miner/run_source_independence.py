#!/usr/bin/env python3
"""Pilot: do models count documents or independent observations?

The scenarios instantiate a standard common-source evidence problem.  In the
independent condition, three reports are based on three independent firsthand
observations.  In the echoed condition, the same three outlets all relay one
firsthand observation.  A fourth, equally reliable firsthand source supports
the alternative in both conditions.
"""

import argparse
import json
import random
import re
import urllib.request


SCENARIOS = [
    ("which warehouse a delivery truck entered", "the north warehouse", "the south warehouse", "security guards", "a traffic camera operator"),
    ("which trail a missing hiker took", "the lake trail", "the ridge trail", "park visitors", "a ranger"),
    ("which harbor a small boat entered", "the east harbor", "the west harbor", "shore observers", "a lighthouse keeper"),
    ("which gate a stray dog left through", "the garden gate", "the driveway gate", "neighbors", "a postal worker"),
    ("which room a package was placed in", "the conference room", "the mail room", "office workers", "a custodian"),
    ("which road the parade used", "Oak Street", "Pine Street", "spectators", "a bus driver"),
    ("which field a weather balloon landed in", "the wheat field", "the corn field", "farm workers", "a surveyor"),
    ("which entrance a visitor used", "the front entrance", "the side entrance", "reception staff", "a delivery driver"),
    ("which platform the unannounced train used", "platform two", "platform four", "commuters", "a station cleaner"),
    ("which storage unit contained the old desk", "unit seven", "unit nine", "moving crew members", "the building manager"),
    ("which bridge the convoy crossed", "the stone bridge", "the steel bridge", "local residents", "a toll collector"),
    ("which classroom the guest lecture was held in", "room 201", "room 204", "students", "a facilities technician"),
    ("which orchard the escaped horse entered", "the apple orchard", "the pear orchard", "farmhands", "a veterinarian"),
    ("which loading bay received the machine", "bay three", "bay five", "warehouse clerks", "a crane operator"),
    ("which beach the seal was seen on", "North Beach", "South Beach", "walkers", "a lifeguard"),
    ("which elevator stopped unexpectedly", "the east elevator", "the west elevator", "employees", "a maintenance engineer"),
    ("which exit the suspect used", "exit A", "exit C", "shoppers", "an off-duty officer"),
    ("which campsite the bear approached", "campsite six", "campsite eight", "campers", "a park ranger"),
    ("which runway the private plane landed on", "runway one", "runway three", "airport workers", "an air-traffic observer"),
    ("which canal the debris came through", "the northern canal", "the southern canal", "boat owners", "a lock keeper"),
]


def ask(base_url, model, prompt, choices, constrained, max_tokens=None, completion_format=False):
    payload = {
        "model": model,
        "temperature": 0,
        "max_tokens": max_tokens or (4 if constrained else 24),
    }
    if completion_format:
        payload["prompt"] = f"[INST] {prompt} [/INST]"
        endpoint = "/v1/completions"
    else:
        payload["messages"] = [{"role": "user", "content": prompt}]
        payload["chat_template_kwargs"] = {"enable_thinking": False}
        endpoint = "/v1/chat/completions"
    if constrained:
        payload["structured_outputs"] = {"choice": choices}
    payload = json.dumps(payload).encode()
    req = urllib.request.Request(base_url.rstrip("/") + endpoint, data=payload,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as response:
        choice = json.load(response)["choices"][0]
        return (choice["text"] if completion_format else choice["message"]["content"]).strip()


def label(text, allowed):
    clean = re.sub(r"<think>.*?</think>", " ", text, flags=re.S | re.I).upper()
    lead = re.match(r"^[^A-Z0-9]{0,20}([A-D])\s*=", clean)
    if lead and lead.group(1) in allowed:
        return lead.group(1)
    stated = re.search(r"(?:ANSWER|CONCLUSION)(?:\s+IS|\s*:)?\s*\**([A-D])\b", clean)
    if stated and stated.group(1) in allowed:
        return stated.group(1)
    hits = re.findall(r"\b(?:A|B|C|D|1|2|3|4)\b", clean)
    digit_map = {"1": "A", "2": "B", "3": "C", "4": "D"}
    for hit in hits:
        hit = digit_map.get(hit, hit)
        if hit in allowed:
            return hit
    return "?"


def make_prompt(item, condition, probe, item_id):
    event, a, b, group, other = item
    people = [f"{group[:-1] if group.endswith('s') else group} 1",
              f"{group[:-1] if group.endswith('s') else group} 2",
              f"{group[:-1] if group.endswith('s') else group} 3"]
    if condition == "independent":
        reports = [
            f"Local outlet 1 interviewed {people[0]}, who personally observed {a}.",
            f"Local outlet 2 interviewed {people[1]}, who independently and personally observed {a}.",
            f"Local outlet 3 interviewed {people[2]}, who independently and personally observed {a}.",
        ]
    elif condition in ("echoed", "echoed_tally"):
        reports = [
            f"Local outlet 1 interviewed {people[0]}, who personally observed {a}.",
            f"Local outlet 2 reported {a}, explicitly citing outlet 1's interview with {people[0]} as its sole source.",
            f"Local outlet 3 also reported {a}, explicitly citing the same outlet 1 interview as its sole source.",
        ]
    elif condition == "echoed_reverse_tally":
        reports = [
            f"Local outlet 1 interviewed {other}, who personally observed {b}.",
            f"Local outlet 2 reported {b}, explicitly citing outlet 1's interview with {other} as its sole source.",
            f"Local outlet 3 also reported {b}, explicitly citing the same outlet 1 interview as its sole source.",
        ]
    else:  # balanced control: one firsthand observation on each side
        reports = [
            f"Local outlet 1 interviewed {people[0]}, who personally observed {a}.",
        ]
    if condition == "echoed_reverse_tally":
        reports.append(f"A separate report interviewed {people[0]}, who independently and personally observed {a}.")
    else:
        reports.append(f"A separate report interviewed {other}, who independently and personally observed {b}.")
    order_rng = random.Random(5000 + item_id + (100 if condition != "independent" else 0))
    order_rng.shuffle(reports)
    context = f"Reports discuss {event}. " + " ".join(reports)
    if condition in ("echoed_tally", "echoed_reverse_tally", "balanced_tally"):
        context += " In other words, there is exactly one independent firsthand observation for each conclusion."
    rng = random.Random(1000 * item_id + (100 if condition == "echoed" else 0) + (10 if probe == "decision" else 0))
    if probe == "count":
        options = ["1", "2", "3", "4"]
        rng.shuffle(options)
        labels = "ABCD"
        rendered = "; ".join(f"{lab}={value}" for lab, value in zip(labels, options))
        target = "3" if condition == "independent" else "1"
        gold = labels[options.index(target)]
        question = (f"How many independent firsthand observations in these reports support {a}? "
                    f"Answer only A, B, C, or D: {rendered}.")
    elif probe == "decision":
        options = [("first", f"{a} is more likely"),
                   ("second", f"{b} is more likely"),
                   ("equal", "the available evidence does not favor either conclusion")]
        rng.shuffle(options)
        labels = "ABC"
        rendered = "; ".join(f"{lab}={text}" for lab, (_, text) in zip(labels, options))
        target = "first" if condition == "independent" else "equal"
        gold = labels[[key for key, _ in options].index(target)]
        question = (f"Assume every firsthand observer is equally reliable. Considering both what each report says and whether reports share an upstream source, what assessment follows from the available evidence? "
                    f"Answer only A, B, or C: {rendered}.")
    else:
        gold = 50
        question = (f"Assume {a} and {b} are mutually exclusive and exhaustive, every firsthand observer is equally reliable, and there is no prior reason to favor either. "
                    f"Considering shared upstream sources, what probability from 0 to 100 should be assigned to {a}? Answer with one integer only.")
    return context + "\n\n" + question, gold


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--completion-format", action="store_true")
    parser.add_argument("--skip-count", action="store_true")
    parser.add_argument("--skip-probability", action="store_true")
    parser.add_argument("--limit", type=int, default=len(SCENARIOS))
    parser.add_argument(
        "--conditions",
        default="independent,echoed,balanced,balanced_tally,echoed_tally,echoed_reverse_tally",
        help="Comma-separated subset used for fast screening.",
    )
    args = parser.parse_args()
    rows = []
    conditions = tuple(c.strip() for c in args.conditions.split(",") if c.strip())
    valid_conditions = {"independent", "echoed", "balanced", "balanced_tally", "echoed_tally", "echoed_reverse_tally"}
    unknown = set(conditions) - valid_conditions
    if unknown:
        parser.error(f"unknown conditions: {sorted(unknown)}")
    for i, item in enumerate(SCENARIOS[:args.limit]):
        for condition in conditions:
            probes = ("count", "decision") if condition in ("independent", "echoed", "balanced") else ("decision", "probability")
            if args.skip_count:
                probes = tuple(p for p in probes if p != "count")
            if args.skip_probability:
                probes = tuple(p for p in probes if p != "probability")
            for probe in probes:
                prompt, gold = make_prompt(item, condition, probe, i)
                allowed = {"A", "B", "C", "D"} if probe == "count" else {"A", "B", "C"}
                raw = ask(args.base_url, args.model, prompt, sorted(allowed),
                          constrained=(probe == "count"),
                          max_tokens=256 if probe == "probability" else None,
                          completion_format=args.completion_format)
                if probe == "probability":
                    nums = re.findall(r"\b(?:100|[1-9]?\d)\b", raw)
                    pred = int(nums[-1]) if nums else -1
                    correct = abs(pred - gold) <= 5
                else:
                    pred = label(raw, allowed)
                    correct = pred == gold
                rows.append({"id": i, "condition": condition, "probe": probe, "gold": gold,
                             "prediction": pred, "correct": correct, "raw": raw, "prompt": prompt})
    summary = {}
    for condition in conditions:
        probes = ("count", "decision") if condition in ("independent", "echoed", "balanced") else ("decision", "probability")
        if args.skip_count:
            probes = tuple(p for p in probes if p != "count")
        if args.skip_probability:
            probes = tuple(p for p in probes if p != "probability")
        for probe in probes:
            subset = [r for r in rows if r["condition"] == condition and r["probe"] == probe]
            summary[f"{condition}_{probe}"] = sum(r["correct"] for r in subset) / len(subset)
            if probe == "probability":
                summary[f"{condition}_{probe}_mean"] = sum(r["prediction"] for r in subset) / len(subset)
    with open(args.output, "w") as f:
        json.dump({"model": args.model, "summary": summary, "rows": rows}, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
