"""Causally transplant the state induced by swapping two content-equivalent bindings."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from collections import defaultdict
from pathlib import Path

import numpy as np
import torch

from model_scoring import format_chat, load_model, resolve_snapshot


def stable_unit_interval(seed: int, frame: int) -> float:
    digest = hashlib.sha256(f"{seed}:frame:{frame}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def row_key(row: dict, include_order: bool = True) -> tuple:
    fields = ["source_row", "competitor_relation", "identity", "cue_family", "readout", "label_order"]
    if include_order:
        fields.append("object_order")
    return tuple(row[x] for x in fields)


def introduction_end(passage: str) -> int:
    marker = "episode code "
    first = passage.find(marker)
    second = passage.find(marker, first + len(marker))
    if first < 0 or second < 0:
        raise ValueError(f"Cannot locate two binding introductions: {passage}")
    end = passage.find(".", second)
    if end < 0:
        raise ValueError(f"Cannot locate second binding sentence end: {passage}")
    return end + 1


def prompt_and_boundary(tokenizer, row: dict) -> tuple[str, int]:
    user = f"Passage: {row['passage']}\nQuestion: {row['question']}"
    prompt = format_chat(tokenizer, user)
    intro = row["passage"][: introduction_end(row["passage"])]
    char_end = prompt.find(intro)
    if char_end < 0:
        raise ValueError("Rendered prompt does not contain introduction prefix")
    char_end += len(intro)
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    candidates = [i for i, (start, end) in enumerate(encoded["offset_mapping"]) if end <= char_end and end > start]
    if not candidates:
        raise ValueError("Cannot align binding boundary to tokens")
    return prompt, max(candidates)


@torch.inference_mode()
def extract_states(tokenizer, model, prompts: list[str], positions: list[int], block_index: int, batch_size: int) -> torch.Tensor:
    states = []
    for start in range(0, len(prompts), batch_size):
        chunk = prompts[start : start + batch_size]
        pos = positions[start : start + batch_size]
        batch = tokenizer(chunk, add_special_tokens=False, padding=True, return_tensors="pt")
        batch = {k: v.to(model.device) for k, v in batch.items()}
        captured = []

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            captured.append(hidden.detach())

        handle = model.model.layers[block_index].register_forward_hook(hook)
        try:
            model(**batch, use_cache=False)
        finally:
            handle.remove()
        hidden = captured[0]
        states.extend(hidden[i, p].float().cpu() for i, p in enumerate(pos))
    return torch.stack(states)


@torch.inference_mode()
def patched_scores(tokenizer, model, prompts: list[str], positions: list[int], patch_vectors: torch.Tensor,
                   labels: list[str], block_index: int, batch_size: int) -> list[dict[str, float]]:
    flat = []
    for row_index, (prompt, position) in enumerate(zip(prompts, positions)):
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        for label in labels:
            full_ids = tokenizer(prompt + label, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate tokenization changed prompt boundary")
            flat.append((row_index, label, prompt_ids, full_ids, position))
    result = [dict() for _ in prompts]
    pad_id = tokenizer.pad_token_id
    for start in range(0, len(flat), batch_size):
        chunk = flat[start : start + batch_size]
        max_len = max(len(x[3]) for x in chunk)
        ids = torch.tensor([x[3] + [pad_id] * (max_len - len(x[3])) for x in chunk], device=model.device)
        mask = torch.tensor([[1] * len(x[3]) + [0] * (max_len - len(x[3])) for x in chunk], device=model.device)
        vectors = torch.stack([patch_vectors[x[0]] for x in chunk]).to(model.device, dtype=model.dtype)
        positions_chunk = [x[4] for x in chunk]

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            changed = hidden.clone()
            for i, position in enumerate(positions_chunk):
                changed[i, position] = vectors[i]
            if isinstance(output, tuple):
                return (changed, *output[1:])
            return changed

        handle = model.model.layers[block_index].register_forward_hook(hook)
        try:
            logits = model(input_ids=ids, attention_mask=mask, use_cache=False).logits
        finally:
            handle.remove()
        for i, (row_index, label, prompt_ids, full_ids, _) in enumerate(chunk):
            continuation = full_ids[len(prompt_ids) :]
            token_logits = logits[i, len(prompt_ids) - 1 : len(prompt_ids) - 1 + len(continuation)]
            target = torch.tensor(continuation, device=model.device)
            score = token_logits.log_softmax(dim=-1).gather(-1, target[:, None]).sum().item()
            result[row_index][label] = score
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--clean-results", type=Path, required=True)
    p.add_argument("--model-path", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    clean_lines = [json.loads(x) for x in args.clean_results.read_text().splitlines() if x]
    clean_meta = next(x for x in clean_lines if x["record_type"] == "metadata")
    if clean_meta["model_checkpoint"] != config["model"] or clean_meta["model_revision"] != config["model_revision"]:
        raise ValueError("Clean result checkpoint differs from frozen S2 checkpoint")
    clean_rows = [x for x in clean_lines if x["record_type"] == "example"]
    stimulus_rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    if len(stimulus_rows) != len(clean_rows):
        raise ValueError("Stimulus and clean-result panels differ in size")
    test_frames = sorted({
        row["frame"] for row in clean_rows
        if stable_unit_interval(int(config["seed"]), int(row["frame"])) < float(config["test_fraction"])
    })
    if len(test_frames) < 4:
        raise ValueError(f"Held-out frame set unexpectedly small: {test_frames}")
    rows = [row for row in clean_rows if row["frame"] in set(test_frames)]
    tokenizer, model = load_model(args.model_path, config["dtype"])
    if len(model.model.layers) <= int(config["block_index"]):
        raise ValueError("Frozen block index is outside model")
    prompts, positions = zip(*(prompt_and_boundary(tokenizer, row) for row in rows))
    prompts, positions = list(prompts), list(positions)
    states = extract_states(tokenizer, model, prompts, positions, int(config["block_index"]), int(config["batch_size"]))
    index = {row_key(row): i for i, row in enumerate(rows)}

    by_match = defaultdict(list)
    for i, row in enumerate(rows):
        match = (row["state_change"], row["competitor_relation"], row["identity"], row["cue_family"], row["readout"], row["label_order"], row["object_order"])
        by_match[match].append(i)
    for values in by_match.values():
        values.sort(key=lambda i: (rows[i]["frame"], rows[i]["source_row"]))

    rng = np.random.default_rng(int(config["seed"]))
    real_vectors, shuffled_vectors, random_vectors, donor_indices, shuffled_indices = [], [], [], [], []
    for i, row in enumerate(rows):
        opposite = "beta_first" if row["object_order"] == "alpha_first" else "alpha_first"
        donor_key = (*row_key(row, include_order=False), opposite)
        donor_i = index[donor_key]
        donor_indices.append(donor_i)
        delta = states[donor_i] - states[i]
        match = (row["state_change"], row["competitor_relation"], row["identity"], row["cue_family"], row["readout"], row["label_order"], row["object_order"])
        pool = [j for j in by_match[match] if rows[j]["frame"] != row["frame"]]
        if not pool:
            raise ValueError(f"No shuffled donor pool for {match}")
        base_other = pool[(rows[i]["frame"] + i) % len(pool)]
        other_row = rows[base_other]
        other_opposite = "beta_first" if other_row["object_order"] == "alpha_first" else "alpha_first"
        other_donor = index[(*row_key(other_row, include_order=False), other_opposite)]
        shuffled_indices.append(other_donor)
        shuffled_delta = states[other_donor] - states[base_other]
        noise = torch.from_numpy(rng.standard_normal(states.shape[1]).astype("float32"))
        noise = noise / noise.norm().clamp_min(1e-12) * delta.norm()
        strength = float(config["patch_strength"])
        real_vectors.append(states[i] + strength * delta)
        shuffled_vectors.append(states[i] + strength * shuffled_delta)
        random_vectors.append(states[i] + strength * noise)
    labels = list(config["candidate_answers"])
    modes = {
        "real_opposite_order": torch.stack(real_vectors),
        "shuffled_opposite_order_delta": torch.stack(shuffled_vectors),
        "random_matched_norm": torch.stack(random_vectors),
    }
    patched = {
        mode: patched_scores(tokenizer, model, prompts, positions, vectors, labels,
                             int(config["block_index"]), int(config["batch_size"]))
        for mode, vectors in modes.items()
    }
    checkpoint, revision = resolve_snapshot(config["model"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision, "dtype": config["dtype"],
            "block_index": config["block_index"], "residual_layer": config["residual_layer"],
            "patch_strength": config["patch_strength"], "batch_size": config["batch_size"],
            "seed": config["seed"], "test_frames": test_frames, "n_examples": len(rows),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for i, row in enumerate(rows):
            donor = rows[donor_indices[i]]
            base_margin = row["target_margin"]
            donor_margin = donor["target_margin"]
            out = {
                "record_type": "example", **{k: row[k] for k in row if k not in {"prompt", "scores", "record_type"}},
                "boundary_token_index": positions[i], "clean_margin": base_margin,
                "opposite_order_clean_margin": donor_margin,
                "opposite_order": donor["object_order"],
                "shuffled_source_row": rows[shuffled_indices[i]]["source_row"],
                "patched": {},
            }
            for mode, values in patched.items():
                margin = values[i][row["target_label"]] - values[i][row["foil_label"]]
                out["patched"][mode] = {"scores": values[i], "target_margin": margin}
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "test_frames": test_frames, "examples": len(rows)}))


if __name__ == "__main__":
    main()
