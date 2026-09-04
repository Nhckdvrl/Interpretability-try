"""Cache final-decision residual trajectories for the frozen ItDepends panel."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


def format_reference_prompt(tokenizer, conversation: list[dict], candidates: list[str]) -> str:
    messages = [
        {
            "role": "system",
            "content": (
                "This is a controlled reference experiment. Reply with exactly one entity from "
                "the candidate list and no explanation. Choose the entity that the final pronoun most naturally refers to."
            ),
        },
        *conversation,
        {
            "role": "user",
            "content": "Candidate entities: " + " | ".join(candidates) + "\nAnswer with one exact candidate entity:",
        },
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--stimuli", type=Path, required=True)
    p.add_argument("--model", required=True)
    p.add_argument("--model-path", default=None)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--batch-size", type=int, default=4)
    args = p.parse_args()
    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    rows = [json.loads(x) for x in args.stimuli.read_text().splitlines() if x]
    tokenizer, model = load_model(args.model_path or args.model, config["dtype"])
    prompts = [format_reference_prompt(tokenizer, row["conversation"], row["candidates"]) for row in rows]
    cached = []
    for start in range(0, len(rows), args.batch_size):
        prompts_batch = prompts[start : start + args.batch_size]
        encoded = tokenizer(prompts_batch, add_special_tokens=False, padding=True, return_tensors="pt")
        encoded = {key: value.to(model.device) for key, value in encoded.items()}
        with torch.inference_mode():
            output = model(**encoded, output_hidden_states=True, use_cache=False)
        final_indices = encoded["attention_mask"].sum(dim=1) - 1
        cached.append(
            torch.stack([
                torch.stack([hidden[i, final_indices[i]] for hidden in output.hidden_states])
                for i in range(len(prompts_batch))
            ]).to(torch.float16).cpu().numpy()
        )
        if start == 0 or start + args.batch_size >= len(rows) or (start + args.batch_size) % 100 == 0:
            print(json.dumps({"completed": min(start + args.batch_size, len(rows)), "total": len(rows)}), flush=True)
    activations = np.concatenate(cached, axis=0)
    checkpoint, revision = resolve_snapshot(args.model)
    metadata = {
        "model_checkpoint": checkpoint,
        "model_revision": revision,
        "readout": "final_decision",
        "item_ids": [row["item_id"] for row in rows],
        "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(args.output, activations=activations, metadata=np.array(json.dumps(metadata)))
    print(json.dumps({"output": str(args.output), "shape": list(activations.shape)}))


if __name__ == "__main__":
    main()
