"""Score all licensed and distractor candidates for 038 S0."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot, score_variable_choices  # noqa: E402


def format_reference_prompt(tokenizer, conversation: list[dict], candidates: list[str]) -> str:
    system = {
        "role": "system",
        "content": (
            "This is a controlled reference experiment. Reply with exactly one entity from "
            "the candidate list and no explanation. Choose the entity that the final pronoun most naturally refers to."
        ),
    }
    candidate_turn = {
        "role": "user",
        "content": "Candidate entities: " + " | ".join(candidates) + "\nAnswer with one exact candidate entity:",
    }
    messages = [system, *conversation, candidate_turn]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--model-path", default=None, help="Optional node-local copy of the frozen checkpoint")
    p.add_argument("--batch-size", type=int, default=None, help="Throughput-only override; recorded in metadata")
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    limit = config.get("max_semantic_items")
    if limit is not None:
        keep = sorted(set(x["semantic_id"] for x in rows))[: int(limit)]
        rows = [x for x in rows if x["semantic_id"] in set(keep)]
    tokenizer, model = load_model(args.model_path or args.model, config["dtype"])
    batch_size = args.batch_size or int(config["batch_size"])
    checkpoint, revision = resolve_snapshot(args.model)
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata",
            "model_checkpoint": checkpoint,
            "model_revision": revision,
            "tokenizer": checkpoint,
            "dtype": config["dtype"],
            "decoding": "forced candidate sequence log probability",
            "seed": config["seed"],
            "commit_sha": commit,
            "stimuli": str(args.stimuli),
            "n_examples": len(rows),
            "batch_size": batch_size,
            "exclusions": [],
        }) + "\n")
        prompts = [format_reference_prompt(tokenizer, row["conversation"], row["candidates"]) for row in rows]
        all_scores = score_variable_choices(
            tokenizer, model, prompts, [row["candidates"] for row in rows], batch_size
        )
        for index, (row, prompt, scored) in enumerate(zip(rows, prompts, all_scores)):
            by_name = {x["candidate"]: x for x in scored}
            out = {"record_type": "example", **row, "prompt": prompt, "scores": by_name,
                   "prediction": max(scored, key=lambda x: x["logprob"])["candidate"]}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
            if (index + 1) % 50 == 0:
                print(json.dumps({"completed": index + 1, "total": len(rows)}), flush=True)
    print(json.dumps({"output": str(args.output), "examples": len(rows), "model": args.model}))


if __name__ == "__main__":
    main()
