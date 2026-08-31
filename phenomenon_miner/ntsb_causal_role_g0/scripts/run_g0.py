#!/usr/bin/env python3
"""Deterministic G0 panel runner (vLLM). Implements PREREGISTRATION.md sections 7-8, 10.

Conditions:
  relevance          Task A, narrative + finding
  role               Task B, narrative + finding                     (primary)
  role_paraphrase    Task B, fixed paraphrase                        (sec. 9)
  role_findingonly   Control 2, finding only, no narrative
  role_narrativeonly Control 3, narrative only, finding text removed

Usage: run_g0.py --family qwen [--conditions ...]
"""
from __future__ import annotations

import argparse, json, os, platform, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

FAMILIES = {
    "qwen":    "Qwen/Qwen3-8B",
    "gemma":   "google/gemma-3-12b-it",
    "llama":   "NousResearch/Meta-Llama-3.1-8B-Instruct",
    "mistral": "mistralai/Mistral-Small-24B-Instruct-2501",
    # Repo-standard 4th family (MODEL_PANEL.md). Used as the documented
    # substitute after Mistral-Small-24B hung on this host during KV-cache
    # profiling, both with and without CUDA-graph capture, on two GPUs.
    "phi": "microsoft/Phi-4-mini-instruct",
}

P_RELEVANCE = """You are given the factual description of an aviation accident and one investigation finding.

ACCIDENT:
{narrative}

FINDING:
{finding}

Question: Was this finding causally relevant to the accident according to the investigation?
Answer only YES or NO."""

P_ROLE = """You are given the factual description of an aviation accident and one finding that investigators considered causally relevant.

ACCIDENT:
{narrative}

FINDING:
{finding}

Question: Was this finding classified as a CAUSE or a CONTRIBUTING FACTOR?
Answer only CAUSE or CONTRIBUTING_FACTOR."""

P_ROLE_PARA = """Below is the factual description of an aviation accident, followed by one finding that
the investigation treated as causally relevant.

ACCIDENT:
{narrative}

FINDING:
{finding}

Did the investigators list this finding as a cause of the accident, or as a factor that
merely contributed to it?
Answer only CAUSE or CONTRIBUTING_FACTOR."""

P_ROLE_FINDING_ONLY = """You are given one finding from an aviation accident investigation that investigators considered causally relevant.

FINDING:
{finding}

Question: Was this finding classified as a CAUSE or a CONTRIBUTING FACTOR?
Answer only CAUSE or CONTRIBUTING_FACTOR."""

P_ROLE_NARRATIVE_ONLY = """You are given the factual description of an aviation accident and one finding that investigators considered causally relevant. The text of the finding has been withheld.

ACCIDENT:
{narrative}

FINDING:
(withheld)

Question: Was this finding classified as a CAUSE or a CONTRIBUTING FACTOR?
Answer only CAUSE or CONTRIBUTING_FACTOR."""

CONDITIONS = {
    "relevance":          ("g0_relevance.jsonl", P_RELEVANCE),
    "role":               ("g0_roles.jsonl",     P_ROLE),
    "role_paraphrase":    ("g0_roles.jsonl",     P_ROLE_PARA),
    "role_findingonly":   ("g0_roles.jsonl",     P_ROLE_FINDING_ONLY),
    "role_narrativeonly": ("g0_roles.jsonl",     P_ROLE_NARRATIVE_ONLY),
}


def load_jsonl(p: Path):
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=sorted(FAMILIES))
    ap.add_argument("--conditions", nargs="*", default=list(CONDITIONS))
    ap.add_argument("--tp", type=int, default=1)
    ap.add_argument("--max-model-len", type=int, default=8192)
    ap.add_argument("--eager", action="store_true",
                    help="disable CUDA-graph capture/compile (Mistral-24B hung there on this host)")
    args = ap.parse_args()

    from vllm import LLM, SamplingParams
    import torch, transformers, vllm
    from huggingface_hub import snapshot_download
    from transformers import AutoTokenizer

    model_id = FAMILIES[args.family]
    # Only the files vLLM actually loads. Without this, repos that also ship
    # Meta's original consolidated *.pth mirror re-download the weights twice.
    local = snapshot_download(
        model_id,
        ignore_patterns=["original/*", "*.pth", "*.gguf", "*.bin", "consolidated*"],
    )
    rev = Path(local).name  # HF snapshot dirs are named by commit sha

    events = {e["ev_id"]: e for e in load_jsonl(ROOT / "items" / "g0_events.jsonl")}
    tok = AutoTokenizer.from_pretrained(model_id)

    llm = LLM(model=model_id, tensor_parallel_size=args.tp, max_model_len=args.max_model_len,
              gpu_memory_utilization=0.85, dtype="bfloat16", enforce_eager=args.eager, seed=20260831)
    sp = SamplingParams(temperature=0.0, top_p=1.0, max_tokens=8, logprobs=20, seed=20260831)

    outdir = ROOT / "results" / args.family
    outdir.mkdir(parents=True, exist_ok=True)

    manifest = {
        "family": args.family, "model_id": model_id,
        "resolved_snapshot": str(local), "revision_or_snapshot": rev,
        "tokenizer_class": type(tok).__name__,
        "tokenizer_name_or_path": str(tok.name_or_path),
        "chat_template_sha1": __import__("hashlib").sha1(
            (tok.chat_template or "").encode()).hexdigest(),
        "vllm": vllm.__version__, "transformers": transformers.__version__,
        "torch": torch.__version__, "python": platform.python_version(),
        "cuda": torch.version.cuda,
        "gpu": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
        "decoding": {"temperature": 0.0, "top_p": 1.0, "max_tokens": 8, "seed": 20260831},
        "max_model_len": args.max_model_len, "enforce_eager": args.eager,
        "conditions_run": args.conditions,
        "items_sha256": json.loads(
            (ROOT / "items" / "sampling_manifest.json").read_text())["items_sha256"],
    }
    (outdir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    for cond in args.conditions:
        fname, template = CONDITIONS[cond]
        items = load_jsonl(ROOT / "items" / fname)
        prompts, metas = [], []
        for it in items:
            narrative = events[it["ev_id"]]["narrative"]
            body = template.format(narrative=narrative, finding=it["finding"])
            prompts.append(tok.apply_chat_template(
                [{"role": "user", "content": body}],
                tokenize=False, add_generation_prompt=True,
                **({"enable_thinking": False} if args.family == "qwen" else {})))
            metas.append(it)

        outs = llm.generate(prompts, sp, use_tqdm=False)
        path = outdir / f"raw_{cond}.jsonl"
        with path.open("w", encoding="utf-8") as fh:
            for it, o in zip(metas, outs):
                c = o.outputs[0]
                first = {}
                if c.logprobs:
                    first = {v.decoded_token: round(v.logprob, 6)
                             for v in c.logprobs[0].values()}
                fh.write(json.dumps({
                    "item_id": it["item_id"], "ev_id": it["ev_id"],
                    "aircraft_key": it["aircraft_key"], "condition": cond,
                    "gold": it["gold"], "raw": c.text,
                    "n_prompt_tokens": len(o.prompt_token_ids),
                    "first_token_logprobs": first,
                }, ensure_ascii=False) + "\n")
        print(f"[{args.family}/{cond}] {len(metas)} items -> {path}", flush=True)


if __name__ == "__main__":
    main()
