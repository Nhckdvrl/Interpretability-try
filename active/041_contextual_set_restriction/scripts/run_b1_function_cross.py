"""Score B1: reference forced choice and explanation continuation likelihood.

Two readouts, two scoring conventions, both frozen:

  reference   -- chat template, deterministic single-token forced choice over A/B/C, matching the
                 convention every earlier 041 experiment uses.
  explanation -- raw text, no chat template: the measure is the length-normalised log probability of
                 a fixed continuation, which is a running-text quantity and runs unchanged on base
                 models. Wrapping it in an assistant turn would change what is being measured.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "phenomenon_miner"))
from model_scoring import load_model, resolve_snapshot  # noqa: E402
from span_scoring import score_spans  # noqa: E402

SYSTEM = "Answer the final multiple-choice question using only A, B or C. Do not explain."


def format_chat(tokenizer, text: str) -> str:
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]
    merged = [{"role": "user", "content": f"{SYSTEM}\n\n{text}"}]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    for candidate in (messages, merged):
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
def score_choices(tokenizer, model, prompts: list[str], labels: list[str],
                  batch_size: int) -> list[dict[str, float]]:
    tokenizer.padding_side = "right"
    ids = label_token_ids(tokenizer, prompts[0], labels)
    results = []
    for start in range(0, len(prompts), batch_size):
        chunk = prompts[start: start + batch_size]
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
    parser.add_argument("--readout", choices=["reference", "explanation"], required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    rows = [row for row in rows if row["readout"] == args.readout]
    if not rows:
        raise ValueError(f"No rows for readout {args.readout}")

    batch_size = args.batch_size or int(config["batch_size"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    checkpoint, revision = resolve_snapshot(args.model)
    metadata = {
        "record_type": "metadata", "experiment_version": config["experiment_version"],
        "readout": args.readout, "model_checkpoint": checkpoint, "model_revision": revision,
        "n_rows": len(rows), "seed": config["seed"],
        "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    }

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps(metadata) + "\n")

        if args.readout == "reference":
            labels = list(config["candidate_answers"])
            prompts = [format_chat(tokenizer, row["prompt_text"]) for row in rows]
            scores = score_choices(tokenizer, model, prompts, labels, batch_size)
            for row, value in zip(rows, scores):
                gold = row["gold_option"]
                distractors = [value[label] for label in labels if label != gold]
                margin = value[gold] - float(torch.logsumexp(torch.tensor(distractors), 0))
                handle.write(json.dumps({
                    "record_type": "example",
                    **{key: item for key, item in row.items() if key != "prompt_text"},
                    "label_scores": value, "referent_margin": margin,
                    "correct": bool(max(value, key=value.get) == gold),
                }, ensure_ascii=False) + "\n")
        else:
            texts = [row["prefix"] + row["continuation"] for row in rows]
            spans = [[(len(row["prefix"]), len(row["prefix"]) + len(row["continuation"]))]
                     for row in rows]
            scored = score_spans(tokenizer, model, texts, spans, batch_size)
            for row, (window,) in zip(rows, scored):
                handle.write(json.dumps({
                    "record_type": "example",
                    **{key: item for key, item in row.items() if key != "prefix"},
                    "continuation_window": window,
                    "explanation_support": window["mean_logprob"],
                }, ensure_ascii=False) + "\n")

    print(json.dumps({"output": str(args.output), "readout": args.readout, "rows": len(rows)}))


if __name__ == "__main__":
    main()
