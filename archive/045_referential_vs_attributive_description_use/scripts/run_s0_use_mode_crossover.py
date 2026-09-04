"""Score the frozen S0 role-swap microscope with deterministic single-token forced choice."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import torch

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


def format_chat(tokenizer, text: str) -> str:
    messages = [
        {"role": "system", "content": "Answer the final multiple-choice question using only A or B. Do not explain."},
        {"role": "user", "content": text},
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    for candidate in (messages, [{"role": "user",
                                  "content": f"{messages[0]['content']}\n\n{messages[1]['content']}"}]):
        try:
            return tokenizer.apply_chat_template(candidate, enable_thinking=False, **kwargs)
        except TypeError:
            try:
                return tokenizer.apply_chat_template(candidate, **kwargs)
            except Exception:
                continue
        except Exception:
            continue
    raise ValueError("No usable chat template for this tokenizer")


def label_token_ids(tokenizer, prompt: str, labels: list[str]) -> list[int]:
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    ids = []
    for label in labels:
        full_ids = tokenizer(prompt + label, add_special_tokens=False)["input_ids"]
        if full_ids[: len(prompt_ids)] != prompt_ids or len(full_ids) != len(prompt_ids) + 1:
            raise ValueError(f"Label {label!r} is not a clean single-token continuation")
        ids.append(full_ids[-1])
    return ids


@torch.inference_mode()
def score(tokenizer, model, prompts: list[str], labels: list[str], batch_size: int) -> list[dict[str, float]]:
    tokenizer.padding_side = "right"
    ids = label_token_ids(tokenizer, prompts[0], labels)
    results = []
    for start in range(0, len(prompts), batch_size):
        chunk = prompts[start : start + batch_size]
        batch = tokenizer(chunk, add_special_tokens=False, padding=True, return_tensors="pt")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}
        logits = model(**batch, use_cache=False).logits
        for i in range(len(chunk)):
            final = logits[i, int(lengths[i]) - 1].float().log_softmax(-1)
            results.append({label: float(final[token_id]) for label, token_id in zip(labels, ids)})
        if start % (batch_size * 50) == 0:
            print(json.dumps({"scored": start + len(chunk), "total": len(prompts)}), flush=True)
    return results


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
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    labels = list(config["candidate_answers"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    prompts = [format_chat(tokenizer, row["prompt_text"]) for row in rows]
    scores = score(tokenizer, model, prompts, labels, int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "n_rows": len(rows), "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for row, value in zip(rows, scores):
            gold = row.get("gold_option", row.get("target_option"))
            other = row.get("other_option", row.get("distractor_option"))
            margin = value[gold] - value[other]
            handle.write(json.dumps({
                "record_type": "example",
                **{key: item for key, item in row.items() if key != "prompt_text"},
                "label_scores": value, "referent_margin": margin,
                "correct": bool(margin > 0),
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows)}))


if __name__ == "__main__":
    main()
