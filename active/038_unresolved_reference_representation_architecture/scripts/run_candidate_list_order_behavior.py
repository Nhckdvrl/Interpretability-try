"""Counterbalance response-list order after resolved and unresolved references."""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import subprocess
import sys
from pathlib import Path

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot, score_variable_choices  # noqa: E402
from extract_itdepends_activations import format_reference_prompt  # noqa: E402


def semantic_split(value: str) -> str:
    bucket = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) % 10
    return "train" if bucket < 6 else "validation" if bucket < 8 else "test"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    source = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    source = [row for row in source if semantic_split(row["semantic_id"]) == "test"]
    rows = []
    for row in source:
        for order_index, candidate_order in enumerate(itertools.permutations(row["candidates"])):
            rows.append({**row, "response_order_index": order_index, "response_candidate_order": list(candidate_order)})
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_reference_prompt(tokenizer, row["conversation"], row["response_candidate_order"]) for row in rows]
    candidate_lists = [row["candidates"] for row in rows]
    scores = score_variable_choices(tokenizer, model, prompts, candidate_lists, int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision, "seed": config["seed"],
            "n_examples": len(rows), "n_source_discourse_rows": len(source),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for row, prompt, values in zip(rows, prompts, scores):
            by_candidate = {value["candidate"]: value for value in values}
            handle.write(json.dumps({
                "record_type": "example", **row, "prompt": prompt, "scores": by_candidate,
                "prediction": max(values, key=lambda value: value["logprob"])["candidate"],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "examples": len(rows), "source_rows": len(source), "model": args.model}))


if __name__ == "__main__":
    main()
