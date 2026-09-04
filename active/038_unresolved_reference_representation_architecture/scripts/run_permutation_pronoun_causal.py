"""Patch the unresolved-pronoun state between content-preserving mention permutations."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


def semantic_split(value: str) -> str:
    bucket = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) % 10
    return "train" if bucket < 6 else "validation" if bucket < 8 else "test"


def pronoun_position(tokenizer, row: dict) -> int:
    prompt = row["prompt"]
    question = row["conversation"][-1]["content"]
    question_start = prompt.rfind(question)
    if question_start < 0:
        raise ValueError(f"Final question missing from rendered prompt: {row['item_id']}")
    matches = list(re.finditer(r"\bit\b", question, flags=re.IGNORECASE))
    if len(matches) != 1:
        raise ValueError(f"Expected one unresolved 'it': {row['item_id']} / {question}")
    start = question_start + matches[0].start()
    end = question_start + matches[0].end()
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    candidates = [
        index for index, (token_start, token_end) in enumerate(encoded["offset_mapping"])
        if token_end > start and token_start < end
    ]
    if len(candidates) != 1:
        raise ValueError(f"Pronoun did not align to one token: {row['item_id']} / {candidates}")
    return candidates[0]


@torch.inference_mode()
def extract_states(tokenizer, model, rows: list[dict], positions: list[int], block_index: int,
                   batch_size: int) -> torch.Tensor:
    states = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        chunk_positions = positions[start : start + batch_size]
        batch = tokenizer([row["prompt"] for row in chunk], add_special_tokens=False, padding=True, return_tensors="pt")
        batch = {key: value.to(model.device) for key, value in batch.items()}
        selected = []

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            selected.append(torch.stack([hidden[i, position] for i, position in enumerate(chunk_positions)]).float().cpu())

        handle = model.model.layers[block_index].register_forward_hook(hook)
        try:
            model(**batch, use_cache=False)
        finally:
            handle.remove()
        states.append(selected[0])
    return torch.cat(states)


@torch.inference_mode()
def score_with_patch(tokenizer, model, rows: list[dict], positions: list[int], vectors: torch.Tensor,
                     block_index: int, batch_size: int) -> list[dict[str, float]]:
    flat = []
    for row_index, row in enumerate(rows):
        prompt_ids = tokenizer(row["prompt"], add_special_tokens=False)["input_ids"]
        for candidate in row["candidates"]:
            full_ids = tokenizer(row["prompt"] + candidate, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate changed prompt-boundary tokenization")
            flat.append((row_index, candidate, prompt_ids, full_ids, positions[row_index]))
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
        for batch_index, (row_index, candidate, prompt_ids, full_ids, _) in enumerate(chunk):
            continuation = full_ids[len(prompt_ids) :]
            token_logits = logits[batch_index, len(prompt_ids) - 1 : len(prompt_ids) - 1 + len(continuation)]
            target = torch.tensor(continuation, device=model.device)
            result[row_index][candidate] = float(token_logits.log_softmax(-1).gather(-1, target[:, None]).sum())
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--clean-results", type=Path, required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    lines = [json.loads(line) for line in args.clean_results.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    if metadata["model_checkpoint"] != config["model"] or metadata["model_revision"] != config["model_revision"]:
        raise ValueError("Clean result checkpoint differs from frozen causal checkpoint")
    clean = [
        row for row in lines
        if row["record_type"] == "example" and row["split"] == "shared_ref"
        and semantic_split(row["semantic_id"]) == "test"
    ]
    allowed = {permutation for pair in config["permutation_pairs"] for permutation in pair}
    clean = [row for row in clean if row["permutation"] in allowed]
    index = {(row["semantic_id"], row["permutation"]): i for i, row in enumerate(clean)}
    opposite = {left: right for left, right in config["permutation_pairs"]}
    opposite.update({right: left for left, right in config["permutation_pairs"]})
    if any((row["semantic_id"], opposite[row["permutation"]]) not in index for row in clean):
        raise ValueError("Incomplete content-preserving permutation pairs")

    tokenizer, model = load_model(args.model_path, config["dtype"])
    positions = [pronoun_position(tokenizer, row) for row in clean]
    states = extract_states(tokenizer, model, clean, positions, int(config["block_index"]), int(config["batch_size"]))

    by_permutation = defaultdict(list)
    for i, row in enumerate(clean):
        by_permutation[row["permutation"]].append(i)
    for values in by_permutation.values():
        values.sort(key=lambda i: clean[i]["semantic_id"])
    rng = np.random.default_rng(int(config["seed"]))
    real, shuffled, random, donor_indices, shuffled_base_indices = [], [], [], [], []
    for i, row in enumerate(clean):
        donor_i = index[(row["semantic_id"], opposite[row["permutation"]])]
        donor_indices.append(donor_i)
        delta = states[donor_i] - states[i]
        pool = [j for j in by_permutation[row["permutation"]] if clean[j]["semantic_id"] != row["semantic_id"]]
        other_i = pool[(i + int(row["row_index"])) % len(pool)]
        other_donor_i = index[(clean[other_i]["semantic_id"], opposite[row["permutation"]])]
        shuffled_base_indices.append(other_i)
        shuffled_delta = states[other_donor_i] - states[other_i]
        noise = torch.from_numpy(rng.standard_normal(states.shape[1]).astype("float32"))
        noise = noise / noise.norm().clamp_min(1e-12) * delta.norm()
        real.append(states[donor_i])
        shuffled.append(states[i] + shuffled_delta)
        random.append(states[i] + noise)
    modes = {
        "real_same_item_opposite_order": torch.stack(real),
        "shuffled_item_same_order_delta": torch.stack(shuffled),
        "random_matched_norm": torch.stack(random),
    }
    patched = {
        name: score_with_patch(tokenizer, model, clean, positions, vectors, int(config["block_index"]),
                               int(config["batch_size"]))
        for name, vectors in modes.items()
    }
    checkpoint, revision = resolve_snapshot(config["model"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "block_index": config["block_index"], "residual_layer": config["residual_layer"],
            "seed": config["seed"], "n_examples": len(clean),
            "semantic_items": len({row["semantic_id"] for row in clean}),
            "permutation_pairs": config["permutation_pairs"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for i, row in enumerate(clean):
            donor = clean[donor_indices[i]]
            out = {
                "record_type": "example", "item_id": row["item_id"], "semantic_id": row["semantic_id"],
                "permutation": row["permutation"], "opposite_permutation": donor["permutation"],
                "positive_candidates": row["positive_candidates"], "negative_candidate": row["negative_candidate"],
                "pronoun_token_index": positions[i], "clean_scores": {k: v["logprob"] for k, v in row["scores"].items()},
                "donor_clean_scores": {k: v["logprob"] for k, v in donor["scores"].items()},
                "shuffled_semantic_id": clean[shuffled_base_indices[i]]["semantic_id"], "patched_scores": {},
            }
            for name, values in patched.items():
                out["patched_scores"][name] = values[i]
            handle.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "examples": len(clean), "semantic_items": len({x['semantic_id'] for x in clean})}))


if __name__ == "__main__":
    main()
