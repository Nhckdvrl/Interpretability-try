"""Run deterministic candidate scoring for the frozen 040 behavioral gate."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from model_scoring import format_chat, load_model, resolve_snapshot, score_choices


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--model-path", default=None, help="Optional node-local copy of the frozen checkpoint")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    records = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    if config.get("max_items") is not None:
        records = records[: int(config["max_items"])]

    tokenizer, model = load_model(args.model_path or args.model, config["dtype"])
    candidates = config["candidate_answers"]
    prompts = [format_chat(tokenizer, f"Passage: {r['passage']}\nQuestion: {r['question']}") for r in records]
    scored = score_choices(tokenizer, model, prompts, candidates, int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        meta = {
            "record_type": "metadata",
            "model_checkpoint": checkpoint,
            "model_revision": revision,
            "tokenizer": checkpoint,
            "dtype": config["dtype"],
            "decoding": "forced candidate sequence log probability",
            "seed": config["seed"],
            "commit_sha": commit,
            "stimuli": str(args.stimuli),
            "n_examples": len(records),
            "exclusions": [],
        }
        f.write(json.dumps(meta) + "\n")
        for record, prompt, scores in zip(records, prompts, scored):
            by_name = {x["candidate"]: x for x in scores}
            semantic_margin = by_name[record["same_label"]]["logprob"] - by_name[record["different_label"]]["logprob"]
            out = {
                "record_type": "example",
                **record,
                "prompt": prompt,
                "scores": by_name,
                "margin_same_different": semantic_margin,
                "prediction_label": max(scores, key=lambda x: x["logprob"])["candidate"],
                "prediction_semantic": "same" if semantic_margin >= 0 else "different",
            }
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "examples": len(records), "model": args.model}))


if __name__ == "__main__":
    main()
