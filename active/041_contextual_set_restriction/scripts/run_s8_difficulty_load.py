"""Score the load-graded worlds and capture residual states at every modifier token."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot  # noqa: E402
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_s1_role_vs_uniqueness import format_chat, label_token_ids  # noqa: E402


def modifier_positions(tokenizer, prompt: str, phrase: str, words: list[str]) -> list[int | None]:
    start = prompt.rfind(phrase)
    if start < 0:
        raise ValueError(f"Description phrase missing from prompt: {phrase}")
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    offsets = encoded["offset_mapping"]
    positions: list[int | None] = []
    cursor = 0
    for word in words:
        local = phrase.find(word, cursor)
        if local < 0:
            positions.append(None)
            continue
        cursor = local + len(word)
        begin, end = start + local, start + local + len(word)
        tokens = [index for index, (span_start, span_end) in enumerate(offsets)
                  if span_end > begin and span_start < end]
        positions.append(tokens[-1] if tokens else None)
    return positions


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--states-output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    n_blocks = int(config["models"][args.model]["n_blocks"])
    residual_layers = sorted({int(round(f * n_blocks)) for f in config["depth_fractions"]})
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    labels = list(config["candidate_answers"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    tokenizer.padding_side = "right"
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    label_ids = label_token_ids(tokenizer, rows[0]["prompt"], labels)
    hidden_size = getattr(model.config, "hidden_size", None) or model.config.text_config.hidden_size

    # states only for the full description, where every modifier is present
    wanted = {}
    for index, row in enumerate(rows):
        if row["dropped_slot"] is None:
            wanted.setdefault(row["state_key"], index)
    slots = {}
    for key, index in wanted.items():
        for slot in range(rows[index]["n_modifiers"]):
            slots[(key, slot)] = None
    state_index = {key: position for position, key in enumerate(sorted(slots))}
    states = np.zeros((len(state_index), len(residual_layers), hidden_size), dtype=np.float32)

    batch_size = args.batch_size or int(config["batch_size"])
    scores: list[dict[str, float]] = []
    with torch.inference_mode():
        for start in range(0, len(rows), batch_size):
            chunk = rows[start : start + batch_size]
            batch = tokenizer([row["prompt"] for row in chunk], add_special_tokens=False,
                              padding=True, return_tensors="pt")
            lengths = batch["attention_mask"].sum(-1).tolist()
            batch = {key: value.to(model.device) for key, value in batch.items()}
            output = model(**batch, output_hidden_states=True, use_cache=False)
            for i, row in enumerate(chunk):
                final = output.logits[i, int(lengths[i]) - 1].float().log_softmax(-1)
                scores.append({label: float(final[token_id])
                               for label, token_id in zip(labels, label_ids)})
                if wanted.get(row["state_key"]) != start + i:
                    continue
                found = modifier_positions(tokenizer, row["prompt"], row["description_phrase"],
                                           row["modifier_words"])
                for slot, position in enumerate(found):
                    if position is None:
                        continue
                    destination = state_index[(row["state_key"], slot)]
                    for layer_position, layer in enumerate(residual_layers):
                        states[destination, layer_position] = (
                            output.hidden_states[layer][i, position].float().cpu().numpy())
            if start % (batch_size * 50) == 0:
                print(json.dumps({"scored": start + len(chunk), "total": len(rows)}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    keys = sorted(state_index)
    args.states_output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.states_output, states=states,
                        state_keys=np.array([f"{key}|{slot}" for key, slot in keys]),
                        residual_layers=np.array(residual_layers))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "n_blocks": n_blocks, "residual_layers": residual_layers,
            "depth_fractions": config["depth_fractions"], "n_rows": len(rows),
            "n_state_rows": len(state_index), "seed": config["seed"],
            "states_file": args.states_output.name,
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for row, value in zip(rows, scores):
            margin = value[row["gold_option"]] - value[row["other_option"]]
            handle.write(json.dumps({
                "record_type": "example",
                **{k: v for k, v in row.items() if k not in {"prompt", "prompt_text"}},
                "label_scores": value, "referent_margin": margin, "correct": bool(margin > 0),
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "state_rows": len(state_index)}))


if __name__ == "__main__":
    main()
