"""Run deterministic candidate scoring for the 034 S0-2 behavioral gate."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot, score_choices  # noqa: E402


def format_three_choice_chat(tokenizer, user_text: str) -> str:
    messages = [
        {"role": "system", "content": "Answer the final multiple-choice question using only A, B, or C. Do not explain."},
        {"role": "user", "content": user_text},
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
        raise ValueError(f"Model not frozen in config: {args.model}")
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    batch_size = int(config["batch_size"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_three_choice_chat(tokenizer, row["prompt_text"]) for row in rows]
    scores = score_choices(tokenizer, model, prompts, ["A", "B", "C"], batch_size)
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata", "model_checkpoint": checkpoint, "model_revision": revision,
            "tokenizer": checkpoint, "dtype": config["dtype"], "seed": config["seed"],
            "n_examples": len(rows), "batch_size": batch_size, "stimuli": str(args.stimuli),
            "decoding": "forced A/B/C sequence log probability",
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for index, (row, prompt, values) in enumerate(zip(rows, prompts, scores)):
            by_label = {x["candidate"]: x for x in values}
            prediction = max(values, key=lambda x: x["logprob"])["candidate"]
            f.write(json.dumps({
                "record_type": "example", **row, "prompt": prompt, "scores": by_label,
                "prediction": prediction, "correct": prediction == row["correct_label"],
            }, ensure_ascii=False) + "\n")
            if (index + 1) % 100 == 0:
                print(json.dumps({"completed": index + 1, "total": len(rows)}), flush=True)
    print(json.dumps({"output": str(args.output), "examples": len(rows), "model": args.model}))


if __name__ == "__main__":
    main()
