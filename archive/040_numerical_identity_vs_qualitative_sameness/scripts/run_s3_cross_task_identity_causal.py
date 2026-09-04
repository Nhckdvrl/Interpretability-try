"""Learn identity cross-surface and test causal transfer to arbitrary history use."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import balanced_accuracy_score, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from model_scoring import load_model, resolve_snapshot


def stable_unit_interval(seed: int, frame: int) -> float:
    digest = hashlib.sha256(f"{seed}:frame:{frame}".encode()).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def raw_unit_direction(pipeline) -> np.ndarray:
    scaler = pipeline.named_steps["standardscaler"]
    classifier = pipeline.named_steps["logisticregression"]
    direction = classifier.coef_[0] / scaler.scale_
    return direction / np.linalg.norm(direction)


@torch.inference_mode()
def extract_final_states(tokenizer, model, prompts: list[str], block_index: int, batch_size: int) -> np.ndarray:
    chunks = []
    for start in range(0, len(prompts), batch_size):
        prompt_chunk = prompts[start : start + batch_size]
        batch = tokenizer(prompt_chunk, add_special_tokens=False, padding=True, return_tensors="pt")
        batch = {key: value.to(model.device) for key, value in batch.items()}
        final_positions = batch["attention_mask"].sum(dim=1) - 1
        selected = []

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            selected.append(torch.stack([hidden[i, final_positions[i]] for i in range(len(prompt_chunk))]).float().cpu())

        handle = model.model.layers[block_index].register_forward_hook(hook)
        try:
            model(**batch, use_cache=False)
        finally:
            handle.remove()
        chunks.append(selected[0].numpy())
    return np.concatenate(chunks)


@torch.inference_mode()
def score_with_edit(tokenizer, model, rows: list[dict], vector: np.ndarray | None, block_index: int,
                    batch_size: int) -> list[dict[str, float]]:
    flat = []
    for row_index, row in enumerate(rows):
        prompt_ids = tokenizer(row["prompt"], add_special_tokens=False)["input_ids"]
        for label in ["A", "B"]:
            full_ids = tokenizer(row["prompt"] + label, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate changed prompt-boundary tokenization")
            flat.append((row_index, label, prompt_ids, full_ids))
    result = [dict() for _ in rows]
    pad_id = tokenizer.pad_token_id
    edit = None if vector is None else torch.as_tensor(vector, device=model.device, dtype=model.dtype)
    for start in range(0, len(flat), batch_size):
        chunk = flat[start : start + batch_size]
        max_len = max(len(value[3]) for value in chunk)
        ids = torch.tensor([value[3] + [pad_id] * (max_len - len(value[3])) for value in chunk], device=model.device)
        mask = torch.tensor([[1] * len(value[3]) + [0] * (max_len - len(value[3])) for value in chunk], device=model.device)

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            changed = hidden.clone()
            for batch_index, value in enumerate(chunk):
                changed[batch_index, len(value[2]) - 1] += edit
            return (changed, *output[1:]) if isinstance(output, tuple) else changed

        handle = model.model.layers[block_index].register_forward_hook(hook) if edit is not None else None
        try:
            logits = model(input_ids=ids, attention_mask=mask, use_cache=False).logits
        finally:
            if handle is not None:
                handle.remove()
        for batch_index, (row_index, label, prompt_ids, full_ids) in enumerate(chunk):
            continuation = full_ids[len(prompt_ids) :]
            token_logits = logits[batch_index, len(prompt_ids) - 1 : len(prompt_ids) - 1 + len(continuation)]
            target = torch.tensor(continuation, device=model.device)
            result[row_index][label] = float(token_logits.log_softmax(-1).gather(-1, target[:, None]).sum())
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--identity-results", type=Path, required=True)
    parser.add_argument("--history-results", type=Path, required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text())
    identity_lines = [json.loads(line) for line in args.identity_results.read_text().splitlines() if line]
    history_lines = [json.loads(line) for line in args.history_results.read_text().splitlines() if line]
    for lines in [identity_lines, history_lines]:
        metadata = next(row for row in lines if row["record_type"] == "metadata")
        if metadata["model_checkpoint"] != config["model"] or metadata["model_revision"] != config["model_revision"]:
            raise ValueError("Behavior result checkpoint differs from frozen S3 checkpoint")
    identity_rows = [row for row in identity_lines if row["record_type"] == "example" and row["readout"] == "history_transfer"]
    test_frames = sorted({row["frame"] for row in identity_rows if stable_unit_interval(int(config["seed"]), int(row["frame"])) < float(config["test_fraction"])})
    train_rows = [row for row in identity_rows if row["frame"] not in set(test_frames) and row["cue_family"] == "released_determiner"]
    test_rows = [row for row in identity_rows if row["frame"] in set(test_frames) and row["cue_family"] == "continuity_description"]
    history_rows = [row for row in history_lines if row["record_type"] == "example" and row["frame"] in set(test_frames)]
    tokenizer, model = load_model(args.model_path, config["dtype"])
    train_x = extract_final_states(tokenizer, model, [row["prompt"] for row in train_rows], int(config["block_index"]), int(config["batch_size"]))
    test_x = extract_final_states(tokenizer, model, [row["prompt"] for row in test_rows], int(config["block_index"]), int(config["batch_size"]))
    train_y = np.array([row["identity"] == "same_token" for row in train_rows], dtype=int)
    test_y = np.array([row["identity"] == "same_token" for row in test_rows], dtype=int)
    pipeline = make_pipeline(StandardScaler(), LogisticRegression(
        C=float(config["probe_C"]), class_weight="balanced", max_iter=2000, random_state=int(config["seed"])
    ))
    pipeline.fit(train_x, train_y)
    direction = raw_unit_direction(pipeline).astype("float32")
    projection_sd = float(np.std(train_x @ direction, ddof=1))
    test_probability = pipeline.predict_proba(test_x)[:, 1]
    readout = {
        "train_rows": len(train_rows), "test_rows": len(test_rows),
        "test_cross_surface_auc": float(roc_auc_score(test_y, test_probability)),
        "test_cross_surface_balanced_accuracy": float(balanced_accuracy_score(test_y, pipeline.predict(test_x))),
        "class_counts_train": {"different": int((train_y == 0).sum()), "same": int((train_y == 1).sum())},
        "class_counts_test": {"different": int((test_y == 0).sum()), "same": int((test_y == 1).sum())},
        "projection_sd": projection_sd,
    }
    rng = np.random.default_rng(int(config["seed"]))
    random_direction = rng.standard_normal(direction.shape).astype("float32")
    random_direction -= random_direction.dot(direction) * direction
    random_direction /= np.linalg.norm(random_direction)
    shuffled_y = train_y.copy()
    rng.shuffle(shuffled_y)
    shuffled_pipeline = make_pipeline(StandardScaler(), LogisticRegression(
        C=float(config["probe_C"]), class_weight="balanced", max_iter=2000, random_state=int(config["seed"])
    ))
    shuffled_pipeline.fit(train_x, shuffled_y)
    shuffled_direction = raw_unit_direction(shuffled_pipeline).astype("float32")
    alpha = projection_sd * float(config["intervention_strength_projection_sd"])
    conditions = {"baseline": None}
    for name, value in {"identity": direction, "shuffled": shuffled_direction, "random": random_direction}.items():
        conditions[f"{name}_plus"] = alpha * value
        conditions[f"{name}_minus"] = -alpha * value
    scored = {}
    for name, edit in conditions.items():
        scored[name] = score_with_edit(tokenizer, model, history_rows, edit, int(config["block_index"]), int(config["batch_size"]))
        print(json.dumps({"condition_completed": name, "rows": len(history_rows)}), flush=True)
    checkpoint, revision = resolve_snapshot(config["model"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision,
            "block_index": config["block_index"], "residual_layer": config["residual_layer"],
            "intervention_alpha": alpha, "seed": config["seed"], "test_frames": test_frames,
            "identity_readout": readout, "n_history_rows": len(history_rows),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
            "exclusions": [],
        }) + "\n")
        for index, row in enumerate(history_rows):
            out = {
                "record_type": "example",
                **{key: value for key, value in row.items() if key not in {"record_type", "prompt", "scores"}},
                "intervention_scores": {name: values[index] for name, values in scored.items()},
            }
            handle.write(json.dumps(out, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "test_frames": test_frames, "history_rows": len(history_rows), **readout}))


if __name__ == "__main__":
    main()
