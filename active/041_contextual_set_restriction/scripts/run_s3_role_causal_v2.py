"""Causal test v2: true per-token projection replacement, scaled, with a shuffled-label control.

v1 had two defects. It added a fixed vector to every edited token instead of *replacing* that
token's component along the role direction with the opposite class mean, so the edit was not a
counterfactual and its size did not adapt to the token; and a single class-mean step is tiny
relative to clean referent margins of +4 to +29 logits, so the readout was saturated at 1.000
accuracy in both directions. Here the edit is

    h' = h + alpha * (mu_opposite - (h . d)) * d

with alpha frozen at 1, 2 and 4 before running, both intervention directions tested
(restricting -> non-restricting and the reverse), a shuffled-label direction added to the
random control, and a held-out surface form included so the causal claim is not tied to the
wording the direction was estimated on.
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
sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_s1_role_vs_uniqueness import format_chat, label_token_ids, modifier_positions  # noqa: E402
from run_s2_role_causal import TEST_FAMILIES, TRAIN_FAMILIES  # noqa: E402

ALPHAS = [1.0, 2.0, 4.0]


def decoder_layers(model):
    """Gemma-3 wraps the decoder one level deeper than Llama/Qwen/Phi/Mistral do."""
    for path in (("model", "layers"), ("model", "language_model", "layers"),
                 ("language_model", "model", "layers"), ("transformer", "h")):
        node = model
        for attribute in path:
            node = getattr(node, attribute, None)
            if node is None:
                break
        if node is not None:
            return node
    raise ValueError("Could not locate decoder layers on this model")


def training_states(s1_path: Path, gate_fractions: list[float]):
    lines = [json.loads(line) for line in s1_path.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    rows = [row for row in lines if row["record_type"] == "example"]
    bundle = np.load(s1_path.with_name(metadata["states_file"]))
    keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
    fractions = list(metadata["depth_fractions"])
    layers = [int(value) for value in bundle["residual_layers"]]
    entries = []
    for row in rows:
        if (row["description_condition"] != "full" or row["mapping_index"] != 0
                or row["surface_form"] != "np" or row["family"] not in TRAIN_FAMILIES):
            continue
        for slot in ["dim1", "dim2"]:
            key = f"{row['state_key']}|{slot}"
            if key in keys:
                entries.append((keys[key], int(slot == row["restricting_dimension"]), row["family"]))
    indices = np.array([entry[0] for entry in entries])
    labels = np.array([entry[1] for entry in entries])
    families = np.array([entry[2] for entry in entries])
    return bundle["states"], indices, labels, families, fractions, layers


def build_directions(states, indices, labels, families, fractions, layers,
                     gate_fractions: list[float], seed: int) -> dict[str, dict]:
    rng = np.random.default_rng(seed)
    shuffled = labels.copy()
    for family in np.unique(families):
        mask = families == family
        shuffled[mask] = rng.permutation(shuffled[mask])
    result = {}
    for fraction in gate_fractions:
        position = fractions.index(fraction)
        features = states[indices, position, :].astype(np.float32)

        def axis(values):
            positive, negative = features[values == 1].mean(0), features[values == 0].mean(0)
            vector = positive - negative
            vector = vector / max(float(np.linalg.norm(vector)), 1e-9)
            return vector, float(positive @ vector), float(negative @ vector)

        role_direction, role_positive, role_negative = axis(labels)
        shuffled_direction, shuffled_positive, shuffled_negative = axis(shuffled)
        random_direction = rng.standard_normal(features.shape[1]).astype("float32")
        random_direction = random_direction / np.linalg.norm(random_direction)
        projections = features @ random_direction
        result[f"{fraction:g}"] = {
            "residual_layer": layers[position], "block_index": layers[position] - 1,
            "role": {"direction": role_direction, "restricting": role_positive,
                     "non_restricting": role_negative},
            "shuffled": {"direction": shuffled_direction, "restricting": shuffled_positive,
                         "non_restricting": shuffled_negative},
            "random": {"direction": random_direction,
                       "restricting": float(np.quantile(projections, 0.75)),
                       "non_restricting": float(np.quantile(projections, 0.25))},
            "n_training_states": len(indices),
        }
    return result


@torch.inference_mode()
def score(tokenizer, model, rows, positions, label_ids, labels, batch_size,
          block_index=None, direction=None, mu=None, alpha=0.0):
    results = []
    device_direction = None if direction is None else torch.from_numpy(direction).to(model.device)
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        chunk_positions = positions[start : start + batch_size]
        batch = tokenizer([row["prompt"] for row in chunk], add_special_tokens=False,
                          padding=True, return_tensors="pt")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}
        handle = None
        if block_index is not None:
            def hook(_module, _inputs, output):
                hidden = output[0] if isinstance(output, tuple) else output
                changed = hidden.clone()
                for row_index, position in enumerate(chunk_positions):
                    if position is None:
                        continue
                    vector = changed[row_index, position].to(torch.float32)
                    projection = float(vector @ device_direction.to(torch.float32))
                    delta = alpha * (mu - projection)
                    changed[row_index, position] = (
                        vector + delta * device_direction.to(torch.float32)).to(changed.dtype)
                return (changed, *output[1:]) if isinstance(output, tuple) else changed
            handle = decoder_layers(model)[block_index].register_forward_hook(hook)
        try:
            logits = model(**batch, use_cache=False).logits
        finally:
            if handle is not None:
                handle.remove()
        for i in range(len(chunk)):
            final = logits[i, int(lengths[i]) - 1].float().log_softmax(-1)
            results.append({label: float(final[token_id]) for label, token_id in zip(labels, label_ids)})
    return results


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--s1-results", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=None,
                        help="Override the frozen batch size; larger checkpoints need a smaller one.")
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    gate_fractions = [float(value) for value in config["gate_depth_fractions"]]
    states, indices, labels, families, fractions, layers = training_states(args.s1_results, gate_fractions)
    directions = build_directions(states, indices, labels, families, fractions, layers,
                                  gate_fractions, int(config["seed"]))
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    rows = [row for row in rows if row["family"] in TEST_FAMILIES and row["mapping_index"] == 0]
    candidates = list(config["candidate_answers"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    tokenizer.padding_side = "right"
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    label_ids = label_token_ids(tokenizer, rows[0]["prompt"], candidates)
    slot_positions = {slot: [] for slot in ["dim1", "dim2"]}
    for row in rows:
        found = modifier_positions(tokenizer, row["prompt"], row["description_phrase"],
                                   {slot: row[f"modifier_{slot}"] for slot in ["dim1", "dim2"]})
        for slot in ["dim1", "dim2"]:
            slot_positions[slot].append(found.get(slot))

    batch_size = args.batch_size or int(config["batch_size"])
    clean = score(tokenizer, model, rows, [None] * len(rows), label_ids, candidates, batch_size)
    outputs = {}
    for fraction, entry in directions.items():
        per_depth = {}
        for kind in ["role", "shuffled", "random"]:
            axis = entry[kind]
            for target_role, mu in [("to_non_restricting", axis["non_restricting"]),
                                    ("to_restricting", axis["restricting"])]:
                for slot in ["dim1", "dim2"]:
                    for alpha in ALPHAS:
                        name = f"{kind}|{target_role}|{slot}|a{alpha:g}"
                        per_depth[name] = score(
                            tokenizer, model, rows, slot_positions[slot], label_ids, candidates,
                            batch_size, block_index=entry["block_index"],
                            direction=axis["direction"], mu=mu, alpha=alpha)
        outputs[fraction] = per_depth
        print(json.dumps({"depth_completed": fraction, "conditions": len(per_depth)}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": "s3_role_causal_v2",
            "model_checkpoint": checkpoint, "model_revision": revision,
            "train_families": TRAIN_FAMILIES, "test_families": TEST_FAMILIES,
            "gate_depth_fractions": config["gate_depth_fractions"], "alphas": ALPHAS,
            "depths": {fraction: {"residual_layer": entry["residual_layer"],
                                  "block_index": entry["block_index"],
                                  "n_training_states": entry["n_training_states"],
                                  "projections": {kind: {"restricting": entry[kind]["restricting"],
                                                         "non_restricting": entry[kind]["non_restricting"]}
                                                  for kind in ["role", "shuffled", "random"]}}
                       for fraction, entry in directions.items()},
            "n_rows": len(rows), "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for i, row in enumerate(rows):
            handle.write(json.dumps({
                "record_type": "example",
                **{key: value for key, value in row.items() if key not in {"prompt", "prompt_text"}},
                "clean_scores": clean[i],
                "edited_by_depth": {fraction: {name: values[i] for name, values in per_depth.items()}
                                    for fraction, per_depth in outputs.items()},
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows), "depths": list(outputs)}))


if __name__ == "__main__":
    main()
