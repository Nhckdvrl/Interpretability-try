"""Run the S1 arbitrary-history and type-control behavioral gate."""

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
    p.add_argument("--model-path", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_chat(tokenizer, f"Passage: {row['passage']}\nQuestion: {row['question']}") for row in rows]
    values = score_choices(tokenizer, model, prompts, config["candidate_answers"], int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(config["model"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata", "model_checkpoint": checkpoint, "model_revision": revision,
            "n_examples": len(rows), "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for row, prompt, scored in zip(rows, prompts, values):
            by_label = {value["candidate"]: value for value in scored}
            margin = by_label[row["target_label"]]["logprob"] - by_label[row["foil_label"]]["logprob"]
            f.write(json.dumps({
                "record_type": "example", **row, "prompt": prompt, "scores": by_label,
                "target_margin": margin, "correct": margin > 0,
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "examples": len(rows)}))


if __name__ == "__main__":
    main()
