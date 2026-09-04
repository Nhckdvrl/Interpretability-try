"""Cache prespecified AmbiCoref hidden-state trajectories for calibration."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import torch

SHARED_040 = Path(__file__).resolve().parents[3] / "phenomenon_miner"
sys.path.insert(0, str(SHARED_040))
from model_scoring import load_model, resolve_snapshot  # noqa: E402


PRONOUN = re.compile(r"\b(?:he|she|him|her|his)\b", re.I)


def format_prompt(tokenizer, row: dict) -> str:
    messages = [
        {
            "role": "system",
            "content": "Resolve the reference and answer with exactly one candidate entity and no explanation.",
        },
        {
            "role": "user",
            "content": (
                f"Sentence: {row['sentence']}\nQuestion: {row['question']}\n"
                f"Candidate entities: {row['candidates'][0]} | {row['candidates'][1]}\n"
                "Answer with one exact candidate entity:"
            ),
        },
    ]
    kwargs = {"tokenize": False, "add_generation_prompt": True}
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def pronoun_character_span(prompt: str, sentence: str) -> tuple[int, int]:
    matches = list(PRONOUN.finditer(sentence))
    if not matches:
        raise ValueError(f"No target pronoun found in: {sentence}")
    match = matches[-1]
    sentence_start = prompt.index(sentence)
    return sentence_start + match.start(), sentence_start + match.end()


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
    tokenizer, model = load_model(args.model_path or args.model, "bfloat16")
    prompts = [format_prompt(tokenizer, row) for row in rows]

    cached_batches = []
    for start in range(0, len(rows), args.batch_size):
        batch_rows = rows[start : start + args.batch_size]
        batch_prompts = prompts[start : start + args.batch_size]
        encoded = tokenizer(
            batch_prompts,
            add_special_tokens=False,
            padding=True,
            return_offsets_mapping=True,
            return_tensors="pt",
        )
        offsets = encoded.pop("offset_mapping").tolist()
        encoded = {key: value.to(model.device) for key, value in encoded.items()}
        with torch.inference_mode():
            output = model(**encoded, output_hidden_states=True, use_cache=False)
        # [batch, readout(pronoun/final), layer, hidden]
        batch_cache = []
        for local_index, (row, prompt, token_offsets) in enumerate(zip(batch_rows, batch_prompts, offsets)):
            char_start, char_end = pronoun_character_span(prompt, row["sentence"])
            pronoun_tokens = [
                index
                for index, (left, right) in enumerate(token_offsets)
                if right > char_start and left < char_end
            ]
            if not pronoun_tokens:
                raise ValueError(f"Pronoun span did not map to tokens: {row['item_id']}")
            pronoun_index = pronoun_tokens[-1]
            final_index = int(encoded["attention_mask"][local_index].sum().item()) - 1
            per_readout = []
            for token_index in [pronoun_index, final_index]:
                per_readout.append(
                    torch.stack([hidden[local_index, token_index] for hidden in output.hidden_states])
                    .to(torch.float16)
                    .cpu()
                    .numpy()
                )
            batch_cache.append(np.stack(per_readout))
        cached_batches.append(np.stack(batch_cache))
        print(json.dumps({"completed": min(start + args.batch_size, len(rows)), "total": len(rows)}), flush=True)

    checkpoint, revision = resolve_snapshot(args.model)
    metadata = {
        "model_checkpoint": checkpoint,
        "model_revision": revision,
        "dtype": "bfloat16_compute_float16_storage",
        "readout_order": ["pronoun", "final_decision"],
        "item_ids": [row["item_id"] for row in rows],
        "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        "stimuli": str(args.stimuli),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output,
        activations=np.concatenate(cached_batches, axis=0),
        metadata=np.array(json.dumps(metadata)),
    )
    print(json.dumps({"output": str(args.output), "shape": list(np.concatenate(cached_batches, axis=0).shape)}))


if __name__ == "__main__":
    main()
