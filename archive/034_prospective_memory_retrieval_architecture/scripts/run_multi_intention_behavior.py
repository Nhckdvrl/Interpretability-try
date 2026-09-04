"""Run the frozen four-choice multi-intention PM behavioral validation."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot, score_choices  # noqa: E402


def format_chat(tokenizer, text: str) -> str:
    messages = [
        {"role": "system", "content": "Answer the final multiple-choice question using only A, B, C, or D. Do not explain."},
        {"role": "user", "content": text},
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--model-path", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model not frozen in config")
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_chat(tokenizer, row["prompt_text"]) for row in rows]
    scores = score_choices(tokenizer, model, prompts, config["candidate_answers"], int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata", "model_checkpoint": checkpoint, "model_revision": revision,
            "stimulus_version": config["stimulus_version"], "seed": config["seed"],
            "batch_size": config["batch_size"], "n_examples": len(rows),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for index, (row, prompt, values) in enumerate(zip(rows, prompts, scores)):
            by_label = {x["candidate"]: x for x in values}
            inverse = {label: semantic for semantic, label in row["semantic_to_label"].items()}
            semantic_scores = {semantic: by_label[label]["logprob"] for semantic, label in row["semantic_to_label"].items()}
            prediction_label = max(values, key=lambda x: x["logprob"])["candidate"]
            f.write(json.dumps({
                "record_type": "example", **row, "prompt": prompt, "scores": by_label,
                "semantic_scores": semantic_scores, "prediction_semantic": inverse[prediction_label],
            }, ensure_ascii=False) + "\n")
            if (index + 1) % 100 == 0:
                print(json.dumps({"completed": index + 1, "total": len(rows)}), flush=True)
    print(json.dumps({"output": str(args.output), "examples": len(rows), "model": args.model}))


if __name__ == "__main__":
    main()
