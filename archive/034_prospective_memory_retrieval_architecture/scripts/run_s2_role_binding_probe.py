"""Run the cue-role binding probe: behavior plus cue-token residual states at fixed depths."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


def format_chat(tokenizer, text: str) -> str:
    messages = [
        {"role": "system",
         "content": "Answer the final multiple-choice question using only A, B, C, or D. Do not explain."},
        {"role": "user", "content": text},
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def critical_token_position(tokenizer, prompt: str, sentence: str) -> int:
    sentence_start = prompt.rfind(sentence)
    if sentence_start < 0:
        raise ValueError(f"Critical sentence missing from prompt: {sentence}")
    match = re.match(r"The ([^ ]+)", sentence)
    if not match:
        raise ValueError(f"Cannot locate critical word: {sentence}")
    word_start, word_end = sentence_start + match.start(1), sentence_start + match.end(1)
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    tokens = [index for index, (start, end) in enumerate(encoded["offset_mapping"])
              if end > word_start and start < word_end]
    if not tokens:
        raise ValueError(f"Critical word has no aligned token: {sentence}")
    return tokens[-1]


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
def forward_pass(tokenizer, model, rows: list[dict], residual_layers: list[int], labels: list[str],
                 batch_size: int) -> tuple[np.ndarray, list[dict[str, float]]]:
    tokenizer.padding_side = "right"
    states = np.zeros((len(rows), len(residual_layers), model.config.hidden_size), dtype=np.float32)
    scores: list[dict[str, float]] = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        prompts = [row["prompt"] for row in chunk]
        positions = [critical_token_position(tokenizer, row["prompt"], row["critical_sentence"])
                     for row in chunk]
        batch = tokenizer(prompts, add_special_tokens=False, padding=True, return_tensors="pt")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}
        output = model(**batch, output_hidden_states=True, use_cache=False)
        for layer_index, layer in enumerate(residual_layers):
            hidden = output.hidden_states[layer]
            picked = torch.stack([hidden[i, position] for i, position in enumerate(positions)])
            states[start : start + len(chunk), layer_index] = picked.float().cpu().numpy().astype(np.float32)
        for i, row in enumerate(chunk):
            ids = label_token_ids(tokenizer, row["prompt"], labels)
            final = output.logits[i, int(lengths[i]) - 1].float().log_softmax(-1)
            scores.append({label: float(final[token_id]) for label, token_id in zip(labels, ids)})
    return states, scores


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--states-output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    n_blocks = int(config["models"][args.model]["n_blocks"])
    residual_layers = sorted({int(round(fraction * n_blocks)) for fraction in config["depth_fractions"]})
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    labels = list(config["candidate_answers"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    if int(getattr(model.config, "num_hidden_layers", n_blocks)) != n_blocks:
        raise ValueError("Frozen block count does not match the loaded checkpoint")
    states, scores = forward_pass(tokenizer, model, rows, residual_layers, labels, int(config["batch_size"]))

    state_index: dict[str, int] = {}
    keep = []
    for i, row in enumerate(rows):
        if row["state_key"] not in state_index:
            state_index[row["state_key"]] = len(keep)
            keep.append(i)
    checkpoint, revision = resolve_snapshot(args.model)
    args.states_output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.states_output, states=states[keep],
                        state_keys=np.array([rows[i]["state_key"] for i in keep]),
                        residual_layers=np.array(residual_layers))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "n_blocks": n_blocks, "residual_layers": residual_layers,
            "depth_fractions": config["depth_fractions"], "n_rows": len(rows),
            "n_state_rows": len(keep), "seed": config["seed"],
            "states_file": args.states_output.name,
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for i, row in enumerate(rows):
            semantic_scores = {semantic: scores[i][label] for semantic, label in row["semantic_to_label"].items()}
            handle.write(json.dumps({
                "record_type": "example",
                **{key: value for key, value in row.items() if key not in {"prompt", "prompt_text"}},
                "label_scores": scores[i], "semantic_scores": semantic_scores,
                "predicted_semantic": max(semantic_scores, key=semantic_scores.get),
                "state_row": state_index[row["state_key"]],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "states": str(args.states_output),
                      "rows": len(rows), "state_rows": len(keep), "residual_layers": residual_layers}))


if __name__ == "__main__":
    main()
