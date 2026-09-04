"""Fit the frozen ClearRef direction and matched controls on discovery items only."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def semantic_split(value: str) -> str:
    bucket = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) % 10
    return "train" if bucket < 6 else "validation" if bucket < 8 else "test"


def positions(row: dict) -> dict[str, int]:
    listed = [x.strip() for x in row["conversation"][0]["content"].split("following:", 1)[1].split(",")]
    return {candidate: index for index, candidate in enumerate(listed)}


def raw_unit_direction(pipeline) -> np.ndarray:
    scaler = pipeline.named_steps["standardscaler"]
    classifier = pipeline.named_steps["logisticregression"]
    direction = classifier.coef_[0] / scaler.scale_
    return direction / np.linalg.norm(direction)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--activations", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    archive = np.load(args.activations, allow_pickle=False)
    x = archive["activations"].astype(np.float32)
    activation_meta = json.loads(str(archive["metadata"]))
    if activation_meta["item_ids"] != [row["item_id"] for row in rows]:
        raise ValueError("Activation/stimulus mismatch")
    layer = int(config["hidden_state_layer"])
    indices = [i for i, row in enumerate(rows) if row["split"] == "clear_ref" and semantic_split(row["semantic_id"]) == "train"]
    labels = np.array([positions(rows[i])[rows[i]["positive_candidates"][0]] for i in indices])
    train_x = x[indices, layer]
    pipeline = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=float(config["probe_C"]), class_weight="balanced", max_iter=2000, random_state=config["seed"]),
    )
    pipeline.fit(train_x, labels)
    direction = raw_unit_direction(pipeline)
    projection_sd = float(np.std(train_x @ direction, ddof=1))

    rng = np.random.default_rng(config["seed"])
    random_direction = rng.normal(size=direction.shape).astype(np.float32)
    random_direction -= random_direction.dot(direction) * direction
    random_direction /= np.linalg.norm(random_direction)

    shuffled_labels = labels.copy()
    rng.shuffle(shuffled_labels)
    shuffled_pipeline = make_pipeline(
        StandardScaler(),
        LogisticRegression(C=float(config["probe_C"]), class_weight="balanced", max_iter=2000, random_state=config["seed"]),
    )
    shuffled_pipeline.fit(train_x, shuffled_labels)
    shuffled_direction = raw_unit_direction(shuffled_pipeline)
    metadata = {
        "model_checkpoint": activation_meta["model_checkpoint"],
        "model_revision": activation_meta["model_revision"],
        "hidden_state_layer": layer,
        "transformer_block": int(config["transformer_block"]),
        "n_discovery_rows": len(indices),
        "class_counts": {str(label): int((labels == label).sum()) for label in [0, 1]},
        "projection_sd": projection_sd,
        "strength_multiplier": float(config["intervention_strength_projection_sd"]),
        "semantic_split": "sha256 modulo 10; train buckets 0-5 only",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez(
        args.output,
        direction=direction.astype(np.float32),
        random_direction=random_direction,
        shuffled_direction=shuffled_direction.astype(np.float32),
        metadata=np.array(json.dumps(metadata)),
    )
    print(json.dumps({**metadata, "output": str(args.output)}, indent=2))


if __name__ == "__main__":
    main()
