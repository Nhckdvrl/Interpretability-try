"""Patch focal cue-token states into nonfocal PM recipients at fixed depth fractions."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

SHARED = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


def pair_key(row: dict, include_focality: bool = True) -> tuple:
    values = [row["semantic_id"], row["cue_type"], row["expectancy"], row["mapping_index"]]
    if include_focality:
        values.append(row["focality"])
    return tuple(values)


def critical_token_position(tokenizer, row: dict) -> int:
    prompt = row["prompt"]
    sentence = row["critical_sentence"]
    sentence_start = prompt.rfind(sentence)
    if sentence_start < 0:
        raise ValueError(f"Critical sentence missing: {row['item_id'] if 'item_id' in row else pair_key(row)}")
    match = re.match(r"The ([^ ]+)", sentence)
    if not match:
        raise ValueError(f"Cannot locate critical word: {sentence}")
    word_start = sentence_start + match.start(1)
    word_end = sentence_start + match.end(1)
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    tokens = [index for index, (start, end) in enumerate(encoded["offset_mapping"])
              if end > word_start and start < word_end]
    if not tokens:
        raise ValueError(f"Critical word has no aligned token: {sentence}")
    return tokens[-1]


@torch.inference_mode()
def extract_states(tokenizer, model, rows: list[dict], positions: list[int], residual_layers: list[int],
                   batch_size: int) -> dict[int, torch.Tensor]:
    captured = {layer: [] for layer in residual_layers}
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        chunk_positions = positions[start : start + batch_size]
        batch = tokenizer([row["prompt"] for row in chunk], add_special_tokens=False, padding=True, return_tensors="pt")
        batch = {key: value.to(model.device) for key, value in batch.items()}
        output = model(**batch, output_hidden_states=True, use_cache=False)
        for layer in residual_layers:
            chosen = torch.stack([output.hidden_states[layer][i, position]
                                  for i, position in enumerate(chunk_positions)]).float().cpu()
            captured[layer].append(chosen)
    return {layer: torch.cat(values) for layer, values in captured.items()}


@torch.inference_mode()
def score_with_patch(tokenizer, model, rows: list[dict], positions: list[int], vectors: torch.Tensor,
                     block_index: int, labels: list[str], batch_size: int) -> list[dict[str, float]]:
    flat = []
    for row_index, row in enumerate(rows):
        prompt_ids = tokenizer(row["prompt"], add_special_tokens=False)["input_ids"]
        for label in labels:
            full_ids = tokenizer(row["prompt"] + label, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate changed prompt-boundary tokenization")
            flat.append((row_index, label, prompt_ids, full_ids, positions[row_index]))
    result = [dict() for _ in rows]
    pad_id = tokenizer.pad_token_id
    for start in range(0, len(flat), batch_size):
        chunk = flat[start : start + batch_size]
        max_len = max(len(value[3]) for value in chunk)
        ids = torch.tensor([value[3] + [pad_id] * (max_len - len(value[3])) for value in chunk], device=model.device)
        mask = torch.tensor([[1] * len(value[3]) + [0] * (max_len - len(value[3])) for value in chunk], device=model.device)
        patch = torch.stack([vectors[value[0]] for value in chunk]).to(model.device, dtype=model.dtype)

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            changed = hidden.clone()
            for batch_index, value in enumerate(chunk):
                changed[batch_index, value[4]] = patch[batch_index]
            return (changed, *output[1:]) if isinstance(output, tuple) else changed

        handle = model.model.layers[block_index].register_forward_hook(hook)
        try:
            logits = model(input_ids=ids, attention_mask=mask, use_cache=False).logits
        finally:
            handle.remove()
        for batch_index, (row_index, label, prompt_ids, full_ids, _) in enumerate(chunk):
            continuation = full_ids[len(prompt_ids) :]
            token_logits = logits[batch_index, len(prompt_ids) - 1 : len(prompt_ids) - 1 + len(continuation)]
            target = torch.tensor(continuation, device=model.device)
            result[row_index][label] = float(token_logits.log_softmax(-1).gather(-1, target[:, None]).sum())
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--behavior-results", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    lines = [json.loads(line) for line in args.behavior_results.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    if metadata["model_checkpoint"] != args.model:
        raise ValueError("Behavior results belong to another checkpoint")
    all_rows = [row for row in lines if row["record_type"] == "example" and row["cue_type"] in {"other", "none"}]
    index = {pair_key(row): row for row in all_rows}
    base_rows = [row for row in all_rows if row["focality"] == "nonfocal"]
    donor_rows = [index[(*pair_key(row, include_focality=False), "focal")] for row in base_rows]
    combined = base_rows + donor_rows
    tokenizer, model = load_model(args.model_path, config["dtype"])
    combined_positions = [critical_token_position(tokenizer, row) for row in combined]
    block_indices = list(config["models"][args.model]["block_indices"])
    residual_layers = [block + 1 for block in block_indices]
    states = extract_states(tokenizer, model, combined, combined_positions, residual_layers, int(config["batch_size"]))
    n = len(base_rows)
    base_positions = combined_positions[:n]
    by_match = defaultdict(list)
    for i, row in enumerate(base_rows):
        by_match[(row["cue_type"], row["expectancy"], row["mapping_index"])].append(i)
    rng = np.random.default_rng(int(config["seed"]))
    output_by_layer = {}
    for block_index, residual_layer in zip(block_indices, residual_layers):
        layer_states = states[residual_layer]
        base_states, donor_states = layer_states[:n], layer_states[n:]
        real_vectors, shuffled_vectors, random_vectors = [], [], []
        for i, row in enumerate(base_rows):
            delta = donor_states[i] - base_states[i]
            pool = [other for other in by_match[(row["cue_type"], row["expectancy"], row["mapping_index"])]
                    if base_rows[other]["semantic_id"] != row["semantic_id"]]
            other = pool[(i + row["mapping_index"]) % len(pool)]
            shuffled_delta = donor_states[other] - base_states[other]
            noise = torch.from_numpy(rng.standard_normal(delta.shape[0]).astype("float32"))
            noise = noise / noise.norm().clamp_min(1e-12) * delta.norm()
            real_vectors.append(donor_states[i])
            shuffled_vectors.append(base_states[i] + shuffled_delta)
            random_vectors.append(base_states[i] + noise)
        modes = {
            "real_focal_state": torch.stack(real_vectors),
            "shuffled_item_focal_delta": torch.stack(shuffled_vectors),
            "random_matched_norm": torch.stack(random_vectors),
        }
        output_by_layer[str(residual_layer)] = {
            mode: score_with_patch(tokenizer, model, base_rows, base_positions, vectors, block_index,
                                   list(config["candidate_answers"]), int(config["batch_size"]))
            for mode, vectors in modes.items()
        }
        print(json.dumps({"residual_layer_completed": residual_layer, "rows": n}), flush=True)
    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "block_indices": block_indices, "residual_layers": residual_layers,
            "n_examples": n, "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for i, row in enumerate(base_rows):
            handle.write(json.dumps({
                "record_type": "example",
                **{key: value for key, value in row.items() if key not in {"record_type", "prompt", "scores"}},
                "critical_token_index": base_positions[i], "clean_semantic_scores": row["semantic_scores"],
                "patched_by_residual_layer": {
                    layer: {mode: values[i] for mode, values in modes.items()}
                    for layer, modes in output_by_layer.items()
                },
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": n, "residual_layers": residual_layers}))


if __name__ == "__main__":
    main()
