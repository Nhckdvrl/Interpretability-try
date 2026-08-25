from __future__ import annotations

import argparse
import json
from pathlib import Path

from .bfcl import load_jsonl, openai_tools, single_turn_messages, write_jsonl


def _load_ids(path: str) -> set[str]:
    ids: set[str] = set()
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("{"):
            try:
                obj = json.loads(line)
                if "id" in obj:
                    ids.add(str(obj["id"]))
                    continue
            except json.JSONDecodeError:
                pass
        ids.add(line.split("\t", 1)[0])
    return ids


def run(model_name: str, data_path: str, out_path: str, ids_path: str | None, max_new_tokens: int) -> None:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    rows = load_jsonl(data_path)
    if ids_path:
        keep = _load_ids(ids_path)
        rows = [r for r in rows if r["id"] in keep]

    tok = AutoTokenizer.from_pretrained(model_name)
    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=dtype, device_map="auto")
    model.eval()
    outputs = []
    for i, entry in enumerate(rows, 1):
        messages = single_turn_messages(entry)
        tools = openai_tools(entry)
        kwargs = dict(
            conversation=messages,
            tools=tools,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",
        )
        # Some Qwen3 templates accept enable_thinking; other model templates do not.
        try:
            inputs = tok.apply_chat_template(**kwargs, enable_thinking=False)
        except TypeError:
            inputs = tok.apply_chat_template(**kwargs)
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        with torch.inference_mode():
            generated = model.generate(
                **inputs,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tok.pad_token_id or tok.eos_token_id,
            )
        prompt_len = inputs["input_ids"].shape[-1]
        text = tok.decode(generated[0, prompt_len:], skip_special_tokens=False)
        outputs.append({"id": entry["id"], "raw_output": text})
        if i % 25 == 0:
            write_jsonl(outputs, out_path)
            print(f"[{i}/{len(rows)}] checkpointed {out_path}", flush=True)
    write_jsonl(outputs, out_path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-4B-Instruct-2507")
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--ids", default=None, help="Optional text/TSV/JSONL file containing BFCL ids")
    ap.add_argument("--max-new-tokens", type=int, default=192)
    a = ap.parse_args()
    run(a.model, a.data, a.out, a.ids, a.max_new_tokens)


if __name__ == "__main__":
    main()
