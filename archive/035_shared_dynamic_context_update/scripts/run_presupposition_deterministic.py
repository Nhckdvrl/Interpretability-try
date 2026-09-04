"""Run forced candidate scoring for the counterbalanced presupposition task."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SHARED_040 = Path(__file__).resolve().parents[2] / "040_numerical_identity_vs_qualitative_sameness" / "scripts"
sys.path.insert(0, str(SHARED_040))
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
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_three_choice_chat(tokenizer, row["question"]) for row in rows]
    scored = score_choices(tokenizer, model, prompts, config["candidate_answers"], int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata", "model_checkpoint": checkpoint, "model_revision": revision,
            "n_examples": len(rows), "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for row, prompt, values in zip(rows, prompts, scored):
            by_label = {value["candidate"]: value for value in values}
            inverse = {label: semantic for semantic, label in row["semantic_to_label"].items()}
            prediction_label = max(values, key=lambda value: value["logprob"])["candidate"]
            semantic_scores = {semantic: by_label[label]["logprob"] for semantic, label in row["semantic_to_label"].items()}
            f.write(json.dumps({
                "record_type": "example", **row, "prompt": prompt, "scores": by_label,
                "semantic_scores": semantic_scores, "prediction_semantic": inverse[prediction_label],
                "gold_margin": semantic_scores[row["probability"]] - max(
                    score for semantic, score in semantic_scores.items() if semantic != row["probability"]
                ),
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "examples": len(rows)}))


if __name__ == "__main__":
    main()
