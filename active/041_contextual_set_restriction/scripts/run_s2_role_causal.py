"""Causal specificity test: attenuate the restriction-role component at one modifier token.

The direction is estimated from S1 states on *training* property families only and applied to
held-out families, at three depths frozen before the causal test was run. The intervention sets
the component along the role direction to the non-restricting class mean at that token, leaving
the input text, the world and every other token untouched.

Frozen prediction: doing this to the modifier that actually restricts costs more referent margin
than doing it to the same lexical modifier in the paired world where it does not restrict, while
a matched-norm random direction does not, and while raw property knowledge survives.
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

TRAIN_FAMILIES = ["size_color", "texture_color", "fill_height"]
TEST_FAMILIES = ["material_color", "pattern_length", "color_curvature"]


def estimate_directions(s1_path: Path, gate_fractions: list[float]) -> dict[str, dict]:
    lines = [json.loads(line) for line in s1_path.read_text().splitlines() if line]
    metadata = next(row for row in lines if row["record_type"] == "metadata")
    rows = [row for row in lines if row["record_type"] == "example"]
    bundle = np.load(s1_path.with_name(metadata["states_file"]))
    states, layers = bundle["states"], [int(v) for v in bundle["residual_layers"]]
    keys = {str(value): index for index, value in enumerate(bundle["state_keys"])}
    fractions = list(metadata["depth_fractions"])
    entries = []
    for row in rows:
        if (row["description_condition"] != "full" or row["mapping_index"] != 0
                or row["surface_form"] != "np" or row["family"] not in TRAIN_FAMILIES):
            continue
        for slot in ["dim1", "dim2"]:
            key = f"{row['state_key']}|{slot}"
            if key in keys:
                entries.append((keys[key], int(slot == row["restricting_dimension"])))
    indices = np.array([entry[0] for entry in entries])
    labels = np.array([entry[1] for entry in entries])
    result = {}
    for fraction in gate_fractions:
        position = fractions.index(fraction)
        features = states[indices, position, :].astype(np.float32)
        positive, negative = features[labels == 1].mean(0), features[labels == 0].mean(0)
        direction = positive - negative
        direction = direction / max(float(np.linalg.norm(direction)), 1e-9)
        result[f"{fraction:g}"] = {
            "residual_layer": layers[position],
            "block_index": layers[position] - 1,
            "direction": direction,
            "non_restricting_projection": float(negative @ direction),
            "restricting_projection": float(positive @ direction),
            "n_training_states": len(entries),
        }
    return result


@torch.inference_mode()
def score_with_edit(tokenizer, model, rows: list[dict], positions: list[int | None],
                    vectors: torch.Tensor | None, block_index: int | None,
                    label_ids: list[int], labels: list[str], batch_size: int) -> list[dict[str, float]]:
    results = []
    for start in range(0, len(rows), batch_size):
        chunk = rows[start : start + batch_size]
        chunk_positions = positions[start : start + batch_size]
        batch = tokenizer([row["prompt"] for row in chunk], add_special_tokens=False,
                          padding=True, return_tensors="pt")
        lengths = batch["attention_mask"].sum(-1).tolist()
        batch = {key: value.to(model.device) for key, value in batch.items()}
        handle = None
        if block_index is not None:
            edits = vectors[start : start + batch_size].to(model.device, dtype=model.dtype)

            def hook(_module, _inputs, output):
                hidden = output[0] if isinstance(output, tuple) else output
                changed = hidden.clone()
                for row_index, position in enumerate(chunk_positions):
                    if position is not None:
                        changed[row_index, position] = changed[row_index, position] + edits[row_index]
                return (changed, *output[1:]) if isinstance(output, tuple) else changed

            handle = model.model.layers[block_index].register_forward_hook(hook)
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
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    gate_fractions = [float(value) for value in config["gate_depth_fractions"]]
    directions = estimate_directions(args.s1_results, gate_fractions)
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]
    rows = [row for row in rows if row["family"] in TEST_FAMILIES]
    labels = list(config["candidate_answers"])
    tokenizer, model = load_model(args.model_path, config["dtype"])
    tokenizer.padding_side = "right"
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    label_ids = label_token_ids(tokenizer, rows[0]["prompt"], labels)
    slot_positions = {slot: [] for slot in ["dim1", "dim2"]}
    for row in rows:
        found = modifier_positions(tokenizer, row["prompt"], row["description_phrase"],
                                   {slot: row[f"modifier_{slot}"] for slot in ["dim1", "dim2"]})
        for slot in ["dim1", "dim2"]:
            slot_positions[slot].append(found.get(slot))

    batch_size = int(config["batch_size"])
    clean = score_with_edit(tokenizer, model, rows, [None] * len(rows), None, None,
                            label_ids, labels, batch_size)
    rng = np.random.default_rng(int(config["seed"]))
    outputs = {}
    for fraction, entry in directions.items():
        direction = torch.from_numpy(entry["direction"])
        shift = entry["non_restricting_projection"] - entry["restricting_projection"]
        random_direction = torch.from_numpy(
            rng.standard_normal(direction.shape[0]).astype("float32"))
        random_direction = random_direction / random_direction.norm().clamp_min(1e-12)
        per_slot = {}
        for slot in ["dim1", "dim2"]:
            role_edit = torch.stack([direction * shift for _ in rows])
            random_edit = torch.stack([random_direction * abs(shift) for _ in rows])
            per_slot[f"role_{slot}"] = score_with_edit(
                tokenizer, model, rows, slot_positions[slot], role_edit,
                entry["block_index"], label_ids, labels, batch_size)
            per_slot[f"random_{slot}"] = score_with_edit(
                tokenizer, model, rows, slot_positions[slot], random_edit,
                entry["block_index"], label_ids, labels, batch_size)
        outputs[fraction] = per_slot
        print(json.dumps({"depth_completed": fraction, "block": entry["block_index"]}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "train_families": TRAIN_FAMILIES, "test_families": TEST_FAMILIES,
            "gate_depth_fractions": config["gate_depth_fractions"],
            "depths": {fraction: {key: value for key, value in entry.items() if key != "direction"}
                       for fraction, entry in directions.items()},
            "n_rows": len(rows), "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for i, row in enumerate(rows):
            handle.write(json.dumps({
                "record_type": "example",
                **{key: value for key, value in row.items() if key not in {"prompt", "prompt_text"}},
                "clean_scores": clean[i],
                "edited_by_depth": {fraction: {name: values[i] for name, values in per_slot.items()}
                                    for fraction, per_slot in outputs.items()},
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "depths": list(outputs)}))


if __name__ == "__main__":
    main()
