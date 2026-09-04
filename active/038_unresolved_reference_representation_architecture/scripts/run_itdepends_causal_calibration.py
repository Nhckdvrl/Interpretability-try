"""Causally qualify the frozen ClearRef direction before unresolved-state use."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot  # noqa: E402
from extract_itdepends_activations import format_reference_prompt  # noqa: E402


def semantic_split(value: str) -> str:
    bucket = int(hashlib.sha256(value.encode()).hexdigest()[:8], 16) % 10
    return "train" if bucket < 6 else "validation" if bucket < 8 else "test"


def positions(row: dict) -> dict[str, int]:
    listed = [x.strip() for x in row["conversation"][0]["content"].split("following:", 1)[1].split(",")]
    return {candidate: index for index, candidate in enumerate(listed)}


@torch.inference_mode()
def score_with_edit(tokenizer, model, layer, prompts, candidate_lists, edit, batch_size):
    flat = []
    for row_index, (prompt, candidates) in enumerate(zip(prompts, candidate_lists)):
        prompt_ids = tokenizer(prompt, add_special_tokens=False)["input_ids"]
        for candidate in candidates:
            full_ids = tokenizer(prompt + candidate, add_special_tokens=False)["input_ids"]
            if full_ids[: len(prompt_ids)] != prompt_ids:
                raise ValueError("Candidate changed prompt-boundary tokenization")
            flat.append((row_index, candidate, prompt_ids, full_ids[len(prompt_ids) :], full_ids))
    result = [dict() for _ in prompts]
    pad = tokenizer.pad_token_id
    for start in range(0, len(flat), batch_size):
        batch = flat[start : start + batch_size]
        max_len = max(len(item[4]) for item in batch)
        ids = torch.tensor([item[4] + [pad] * (max_len - len(item[4])) for item in batch], device=model.device)
        mask = torch.tensor([[1] * len(item[4]) + [0] * (max_len - len(item[4])) for item in batch], device=model.device)
        vector = None if edit is None else torch.as_tensor(edit, device=model.device, dtype=model.dtype)

        def hook(_module, _inputs, output):
            hidden = output[0] if isinstance(output, tuple) else output
            changed = hidden.clone()
            for batch_index, item in enumerate(batch):
                changed[batch_index, len(item[2]) - 1] += vector
            return (changed, *output[1:]) if isinstance(output, tuple) else changed

        handle = layer.register_forward_hook(hook) if vector is not None else None
        try:
            logits = model(input_ids=ids, attention_mask=mask, use_cache=False).logits
        finally:
            if handle is not None:
                handle.remove()
        for batch_index, (row_index, candidate, prompt_ids, continuation, _) in enumerate(batch):
            token_logits = logits[batch_index, len(prompt_ids) - 1 : len(prompt_ids) - 1 + len(continuation)]
            target = torch.tensor(continuation, device=model.device)
            result[row_index][candidate] = float(token_logits.log_softmax(-1).gather(-1, target[:, None]).sum())
    return result


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--direction", type=Path, required=True)
    p.add_argument("--model-path", required=True)
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    rows_all = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    rows = []
    for row in rows_all:
        pos = positions(row)
        if row["split"] == "clear_ref" and semantic_split(row["semantic_id"]) == config["clearref_evaluation_split"]:
            rows.append(row)
        elif row["split"] == "shared_ref":
            if sorted(pos[candidate] for candidate in row["positive_candidates"]) == [0, 1] and pos[row["negative_candidate"]] == 2:
                rows.append(row)
    direction_file = np.load(args.direction, allow_pickle=False)
    direction_meta = json.loads(str(direction_file["metadata"]))
    tokenizer, model = load_model(args.model_path, "bfloat16")
    layer = model.model.layers[int(config["transformer_block"])]
    prompts = [format_reference_prompt(tokenizer, row["conversation"], row["candidates"]) for row in rows]
    candidates = [row["candidates"] for row in rows]
    alpha = direction_meta["projection_sd"] * float(config["intervention_strength_projection_sd"])
    conditions = {"baseline": None}
    for name in ["direction", "random_direction", "shuffled_direction"]:
        vector = direction_file[name]
        conditions[f"{name}_plus"] = alpha * vector
        conditions[f"{name}_minus"] = -alpha * vector
    scores = {}
    for name, edit in conditions.items():
        scores[name] = score_with_edit(tokenizer, model, layer, prompts, candidates, edit, int(config["batch_size"]))
        print(json.dumps({"condition_completed": name, "rows": len(rows)}), flush=True)
    checkpoint, revision = resolve_snapshot(config["model"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as f:
        f.write(json.dumps({
            "record_type": "metadata",
            "model_checkpoint": checkpoint,
            "model_revision": revision,
            "direction_metadata": direction_meta,
            "intervention_alpha": alpha,
            "n_rows": len(rows),
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for index, row in enumerate(rows):
            f.write(json.dumps({"record_type": "example", **row, "intervention_scores": {name: value[index] for name, value in scores.items()}}, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows)}))


if __name__ == "__main__":
    main()
