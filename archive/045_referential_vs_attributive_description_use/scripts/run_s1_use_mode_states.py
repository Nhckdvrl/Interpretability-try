"""Score v3 worlds and capture residual states at the last token of the critical description."""

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
from run_s0_use_mode_crossover import format_chat, label_token_ids  # noqa: E402


def description_token(tokenizer, prompt: str, description: str) -> int:
    start = prompt.rfind(description)
    if start < 0:
        raise ValueError(f"Description missing from prompt: {description}")
    end = start + len(description)
    encoded = tokenizer(prompt, add_special_tokens=False, return_offsets_mapping=True)
    tokens = [index for index, (span_start, span_end) in enumerate(encoded["offset_mapping"])
              if span_end > start and span_start < end]
    if not tokens:
        raise ValueError(f"Description has no aligned token: {description}")
    return tokens[-1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
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
    for row in rows:
        row["prompt"] = format_chat(tokenizer, row["prompt_text"])
    label_ids = label_token_ids(tokenizer, rows[0]["prompt"], labels)
    hidden_size = getattr(model.config, "hidden_size", None) or model.config.text_config.hidden_size

    wanted = {}
    for index, row in enumerate(rows):
        wanted.setdefault(row["state_key"], index)
    state_index = {key: position for position, key in enumerate(sorted(wanted))}
    states = np.zeros((len(state_index), len(residual_layers), hidden_size), dtype=np.float16)

    batch_size = int(config["batch_size"])
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
                if wanted.get(row["state_key"]) != start + i:
                    continue
                position = description_token(tokenizer, row["prompt"], row["critical_description"])
                destination = state_index[row["state_key"]]
                for layer_position, layer in enumerate(residual_layers):
                    states[destination, layer_position] = (
                        output.hidden_states[layer][i, position].float().cpu().numpy().astype(np.float16))
            if start % (batch_size * 50) == 0:
                print(json.dumps({"scored": start + len(chunk), "total": len(rows)}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    args.states_output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.states_output, states=states,
                        state_keys=np.array(sorted(state_index)),
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
                **{key: item for key, item in row.items() if key not in {"prompt", "prompt_text"}},
                "label_scores": value, "referent_margin": margin, "correct": bool(margin > 0),
                "state_row": state_index[row["state_key"]],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows),
                      "state_rows": len(state_index), "residual_layers": residual_layers}))


if __name__ == "__main__":
    main()
