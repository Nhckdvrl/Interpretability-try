"""Score the decorrelated worlds and capture residual states at each modifier token.

States are stored in float32. float16 was enough for Llama, Qwen, Phi and Mistral but overflowed to
inf on Gemma-3-12B, whose residual stream exceeds 65504 in the middle third of the stack; that
silently produced NaN probe scores, which a balanced-accuracy readout reports as exactly 0.500.
"""

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


def modifier_positions(tokenizer, prompt: str, phrase: str, modifiers: dict[str, str | None]) -> dict[str, int]:
    phrase_start = prompt.rfind(phrase)
    if phrase_start < 0:
        raise ValueError(f"Description phrase missing from prompt: {phrase}")
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    offsets = encoded["offset_mapping"]
    positions = {}
    for slot, word in modifiers.items():
        if word is None:
            continue
        local = phrase.find(word)
        if local < 0:
            raise ValueError(f"Modifier {word!r} missing from phrase {phrase!r}")
        start, end = phrase_start + local, phrase_start + local + len(word)
        tokens = [index for index, (span_start, span_end) in enumerate(offsets)
                  if span_end > start and span_start < end]
        if not tokens:
            raise ValueError(f"Modifier {word!r} has no aligned token")
        positions[slot] = tokens[-1]
    return positions


def label_token_ids(tokenizer, prompt: str, labels: list[str]) -> list[int]:
    prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
    ids = []
    for label in labels:
        full_ids = tokenizer(prompt + label, add_special_tokens=False)["input_ids"]
        if full_ids[: len(prompt_ids)] != prompt_ids or len(full_ids) != len(prompt_ids) + 1:
            raise ValueError(f"Label {label!r} is not a clean single-token continuation")
        ids.append(full_ids[-1])
    return ids


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=None,
                        help="Override the frozen batch size; larger checkpoints need a smaller one.")
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
    tokenizer.padding_side = "right"
    reported = getattr(model.config, "num_hidden_layers", None)
    if reported is None:
        reported = getattr(getattr(model.config, "text_config", None), "num_hidden_layers", n_blocks)
    if int(reported) != n_blocks:
        raise ValueError("Frozen block count does not match the loaded checkpoint")
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    label_ids = label_token_ids(tokenizer, rows[0]["prompt"], labels)

    wanted = {}
    for index, row in enumerate(rows):
        for slot in ["dim1", "dim2"]:
            if row[f"modifier_{slot}"] is not None:
                wanted.setdefault((row["state_key"], slot), index)
    state_index = {key: position for position, key in enumerate(sorted(wanted))}
    hidden_size = getattr(model.config, "hidden_size", None)
    if hidden_size is None:  # Gemma-3 keeps it under text_config
        hidden_size = model.config.text_config.hidden_size
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
                scores.append({label: float(final[token_id]) for label, token_id in zip(labels, label_ids)})
                slots = {slot: row[f"modifier_{slot}"] for slot in ["dim1", "dim2"]}
                needed = {slot for slot in slots
                          if slots[slot] is not None
                          and wanted.get((row["state_key"], slot)) == start + i}
                if not needed:
                    continue
                positions = modifier_positions(tokenizer, row["prompt"], row["description_phrase"], slots)
                for slot in needed:
                    destination = state_index[(row["state_key"], slot)]
                    for layer_position, layer in enumerate(residual_layers):
                        states[destination, layer_position] = (
                            output.hidden_states[layer][i, positions[slot]].float().cpu().numpy().astype(np.float32))
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
            gold = row.get("gold_option", row.get("target_option"))
            other = row.get("other_option", row.get("distractor_option"))
            margin = value[gold] - value[other]
            handle.write(json.dumps({
                "record_type": "example",
                **{key: item for key, item in row.items() if key not in {"prompt", "prompt_text"}},
                "label_scores": value, "referent_margin": margin, "correct": bool(margin > 0),
                "state_rows": {slot: state_index[(row["state_key"], slot)]
                               for slot in ["dim1", "dim2"]
                               if (row["state_key"], slot) in state_index
                               and row[f"modifier_{slot}"] is not None},
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "state_rows": len(state_index),
                      "residual_layers": residual_layers}))


if __name__ == "__main__":
    main()
