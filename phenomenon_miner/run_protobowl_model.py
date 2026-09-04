#!/usr/bin/env python3
"""Run one local chat model on all human-written Protobowl clue prefixes."""

import argparse
import json
import re
import unicodedata
from pathlib import Path

from datasets import Dataset, load_dataset
from transformers import AutoTokenizer
from vllm import LLM, SamplingParams


EVAL_ARROW = Path(
    "/home/xiang/.cache/huggingface/datasets/"
    "mgor___protobowl-11-13/progressive-clues/0.0.0/"
    "3dae05a66d3e0fd8c6b23ef8656ff6f4437bb1d4/"
    "protobowl-11-13-eval.arrow"
)


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


def is_correct(prediction: str, answers: list[str]) -> bool:
    pred = normalize(prediction)
    pred = re.sub(r"^(the answer is|answer)\s+", "", pred).strip()
    for answer in answers:
        gold = normalize(answer)
        if pred == gold or pred.startswith(gold + " ") or gold.startswith(pred + " "):
            return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--label", required=True)
    parser.add_argument(
        "--dataset", choices=["protobowl", "acf24"], default="protobowl"
    )
    parser.add_argument("--out-dir", default="phenomenon_miner/results/protobowl_current")
    parser.add_argument("--tensor-parallel-size", type=int, default=1)
    args = parser.parse_args()

    if args.dataset == "protobowl":
        data = [dict(row) for row in Dataset.from_file(str(EVAL_ARROW))]
    else:
        source = load_dataset("qanta-challenge/acf-co24-tossups", split="eval")
        data = []
        for row in source:
            for clue_index, (_, clue_end) in enumerate(row["clue_spans"], start=1):
                data.append(
                    {
                        "qc_id": f'{row["qid"]}_{clue_index}',
                        "clue_text": row["question"][:clue_end],
                        "clean_answers": row["clean_answers"],
                    }
                )
    tokenizer = AutoTokenizer.from_pretrained(args.model, local_files_only=True)
    prompts = []
    for row in data:
        messages = [
            {
                "role": "system",
                "content": (
                    "Answer the quiz question with only the answer entity or concept. "
                    "Do not explain and do not repeat the question."
                ),
            },
            {"role": "user", "content": row["clue_text"]},
        ]
        try:
            prompt = tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True,
                enable_thinking=False,
            )
        except TypeError:
            prompt = tokenizer.apply_chat_template(
                messages, tokenize=False, add_generation_prompt=True
            )
        prompts.append(prompt)

    llm = LLM(
        model=args.model,
        tensor_parallel_size=args.tensor_parallel_size,
        max_model_len=2048,
        gpu_memory_utilization=0.78,
        trust_remote_code=True,
    )
    outputs = llm.generate(
        prompts,
        SamplingParams(temperature=0.0, max_tokens=32, stop=["\n"]),
    )

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{args.dataset}__{args.label}.jsonl"
    correct = 0
    with out_path.open("w", encoding="utf-8") as handle:
        for row, output in zip(data, outputs):
            prediction = output.outputs[0].text.strip()
            score = is_correct(prediction, row["clean_answers"])
            correct += int(score)
            handle.write(
                json.dumps(
                    {
                        "qc_id": row["qc_id"],
                        "prediction": prediction,
                        "score": int(score),
                        "answers": row["clean_answers"],
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
    print(json.dumps({"model": args.label, "n": len(data), "accuracy": correct / len(data), "out": str(out_path)}))


if __name__ == "__main__":
    main()
