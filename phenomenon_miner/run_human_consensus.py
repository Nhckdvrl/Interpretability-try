#!/usr/bin/env python3
"""Natural-source replication of the illusion-of-consensus paradigm.

The design follows the election-poll materials used by Connor Desai et al.:
news outlets are secondary sources and polling companies are primary sources.
The dependent condition repeats one poll through several outlets; the
independent condition reports distinct polls.  Names, order, and answer labels
are rotated, but the evidential structure is unchanged.
"""

import argparse
import json
import random
import re
import urllib.request


POLLSTERS = ["Gamma", "Omega", "Kappa", "Sigma", "Theta", "Lambda", "Delta", "Iota"]
OUTLETS = ["The Chronicle", "City News", "The Herald", "Public Radio", "Daily Report",
           "Evening News", "The Observer", "National Bulletin"]
CANDIDATE_PAIRS = [("Candidate X", "Candidate Y"), ("Candidate R", "Candidate S"),
                   ("Candidate L", "Candidate M"), ("Candidate P", "Candidate Q")]


def ask(base_url, model, prompt, max_tokens=24):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "chat_template_kwargs": {"enable_thinking": False},
        "temperature": 0,
        "max_tokens": max_tokens,
    }).encode()
    req = urllib.request.Request(base_url.rstrip("/") + "/v1/chat/completions", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.load(response)["choices"][0]["message"]["content"].strip()


def parse_label(text):
    clean = re.sub(r"<think>.*?</think>", " ", text, flags=re.S | re.I).upper()
    lead = re.match(r"^[^A-Z0-9]{0,20}(?:FINAL\s*=\s*|ANSWER\s*[:=]?\s*)?\**([ABC])(?:\**\s*=|\b)", clean)
    if lead:
        return lead.group(1)
    stated = re.search(r"(?:FINAL|ANSWER|CONCLUSION)(?:\s+IS|\s*[:=])\s*\**([ABC])\b", clean)
    return stated.group(1) if stated else "?"


def make_item(item_id, condition, probe):
    rng = random.Random(31000 + item_id)
    pollsters = rng.sample(POLLSTERS, 5)
    outlets = rng.sample(OUTLETS, 5)
    x, y = CANDIDATE_PAIRS[item_id % len(CANDIDATE_PAIRS)]
    if item_id % 2:
        x, y = y, x

    if condition == "dependent":
        x_sources = [pollsters[0]] * 4
    elif condition == "independent":
        x_sources = pollsters[:4]
    else:  # balanced baseline
        x_sources = [pollsters[0]]

    posts = [f"{outlet} reports that polling company {source}'s poll predicts {x} will win."
             for outlet, source in zip(outlets, x_sources)]
    posts.append(f"{outlets[-1]} reports that polling company {pollsters[-1]}'s poll predicts {y} will win.")
    rng.shuffle(posts)
    context = (
        "An election is approaching in an unfamiliar democratic country. The polling companies are equally "
        "reputable, have comparable past accuracy, and use independent samples unless the same named poll is "
        "being reported again. News outlets do not conduct polls; they report the named polling company's result.\n\n"
        + "\n".join(f"- {post}" for post in posts)
    )

    if probe == "count":
        prompt = context + f"\n\nHow many distinct polling-company polls in the posts predict {x}? Your entire response must be one integer and nothing else."
        gold = 4 if condition == "independent" else 1
    elif probe == "relation":
        prompt = context + (f"\n\nDo the news posts predicting {x} ultimately report the SAME underlying "
                            "poll or DIFFERENT underlying polls? Your entire response must be SAME or DIFFERENT.")
        gold = "DIFFERENT" if condition == "independent" else "SAME"
    else:
        options = [("x", f"{x} is more likely to win"), ("y", f"{y} is more likely to win"),
                   ("tie", "the available polling evidence does not favor either candidate")]
        label_rng = random.Random(47000 + item_id)
        label_rng.shuffle(options)
        rendered = "; ".join(f"{lab}={text}" for lab, (_, text) in zip("ABC", options))
        target = "x" if condition == "independent" else "tie"
        gold = "ABC"[[key for key, _ in options].index(target)]
        prompt = context + ("\n\nConsidering the independence of the underlying polls, which assessment follows? "
                            f"Answer only A, B, or C: {rendered}.")
    return prompt, gold


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--n", type=int, default=20)
    args = ap.parse_args()
    rows = []
    for i in range(args.n):
        for condition in ("balanced", "dependent", "independent"):
            probes = ("count", "decision") if condition == "balanced" else ("count", "relation", "decision")
            for probe in probes:
                prompt, gold = make_item(i, condition, probe)
                raw = ask(args.base_url, args.model, prompt, max_tokens=8 if probe == "count" else 24)
                if probe == "count":
                    nums = re.findall(r"\b\d+\b", raw)
                    pred = int(nums[0]) if nums else -1
                elif probe == "relation":
                    upper = raw.strip().upper()
                    pred = "DIFFERENT" if upper.startswith("DIFFERENT") else ("SAME" if upper.startswith("SAME") else "?")
                else:
                    pred = parse_label(raw)
                rows.append({"id": i, "condition": condition, "probe": probe, "gold": gold,
                             "prediction": pred, "correct": pred == gold, "raw": raw, "prompt": prompt})
    summary = {}
    for condition in ("balanced", "dependent", "independent"):
        probes = ("count", "decision") if condition == "balanced" else ("count", "relation", "decision")
        for probe in probes:
            subset = [r for r in rows if r["condition"] == condition and r["probe"] == probe]
            summary[f"{condition}_{probe}"] = sum(r["correct"] for r in subset) / len(subset)
    with open(args.output, "w") as f:
        json.dump({"model": args.model, "summary": summary, "rows": rows}, f, indent=2)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
