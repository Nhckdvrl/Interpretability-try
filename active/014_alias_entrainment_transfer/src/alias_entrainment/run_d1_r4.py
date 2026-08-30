"""Run the frozen D1 r4 ALIAS-versus-ASSOC construct validation.

Every matched ordered surface pair is evaluated.  Redirect surface type,
structure, entity type, direction, and capability are analysis factors; this
runner never filters them.  The scored continuation is always the target
surface, so within-item ALIAS/ASSOC contrasts have identical tokenization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import torch
import transformers

from alias_entrainment.run_phase1 import Scorer, build_prompt


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_items(path: str | Path, limit: int = 0) -> list[dict]:
    rows = [json.loads(line) for line in open(path, encoding="utf-8") if line.strip()]
    item_ids = [row["item_id"] for row in rows]
    if len(item_ids) != len(set(item_ids)):
        raise RuntimeError("D1 r4 bank contains duplicate item_id values")
    return rows[:limit] if limit else rows


def condition_mentions(item: dict) -> list[tuple[str, str]]:
    rows = [
        ("EXACT", item["target_form"]),
        ("ALIAS", item["seen_form"]),
        ("ASSOC_ANY", item["assoc_any"]),
    ]
    if item.get("assoc_sametype"):
        rows.append(("ASSOC_SAMETYPE", item["assoc_sametype"]))
    return rows


def make_main_jobs(items: list[dict]) -> tuple[list[tuple[str, str]], list[dict]]:
    jobs: list[tuple[str, str]] = []
    keys: list[dict] = []
    for item in items:
        continuation = " " + item["target_form"]
        # A neutral carrier keeps the target continuation grammatical while
        # avoiding factual content about either entity.
        question = "What name comes next?"
        jobs.append((build_prompt(None, question), continuation))
        keys.append({"item_id": item["item_id"], "condition": "NOCTX", "frame": "-"})
        for frame, template in sorted(item["frames"].items()):
            for condition, mention in condition_mentions(item):
                context = template.format(M=mention)
                jobs.append((build_prompt(context, question), continuation))
                keys.append({"item_id": item["item_id"], "condition": condition, "frame": frame})
    return jobs, keys


def make_probe_jobs(items: list[dict]) -> tuple[list[tuple[str, str]], list[dict]]:
    """Counterbalanced hard identity gate against the matched ASSOC foil."""
    jobs: list[tuple[str, str]] = []
    keys: list[dict] = []
    for item in items:
        target, foil = item["target_form"], item["identity_probe_foil"]
        for order, options in enumerate(((target, foil), (foil, target))):
            prompt = (
                f'Q: Which option is another name for "{item["seen_form"]}"?\n'
                f"Options: (A) {options[0]}  (B) {options[1]}\nA: ("
            )
            gold = "A" if order == 0 else "B"
            for letter in ("A", "B"):
                jobs.append((prompt, letter))
                keys.append({
                    "item_id": item["item_id"], "order": order,
                    "letter": letter, "gold": gold,
                })
    return jobs, keys


def write_rows(path: Path, keys: list[dict], scores: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for key, score in zip(keys, scores, strict=True):
            f.write(json.dumps({**key, **score}, sort_keys=True) + "\n")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--bank", default="data/frozen_d1_r4.jsonl")
    ap.add_argument("--out-dir", default="results/d1_r4")
    ap.add_argument("--device", default="cuda:0")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    items = load_items(args.bank, args.limit)
    if not items:
        raise RuntimeError("D1 r4 bank is empty")
    scorer = Scorer(args.model, device=args.device, batch_size=args.batch_size)
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    started = time.time()

    probe_jobs, probe_keys = make_probe_jobs(items)
    probe_scores = scorer.score(probe_jobs)
    write_rows(out / f"{args.tag}__probe.jsonl", probe_keys, probe_scores)

    main_jobs, main_keys = make_main_jobs(items)
    main_scores = scorer.score(main_jobs)
    write_rows(out / f"{args.tag}__main.jsonl", main_keys, main_scores)

    revision = getattr(scorer.model.config, "_commit_hash", None)
    metadata = {
        "status": "complete",
        "contract_id": "2026-08-29-d1-r4-scope-correction",
        "model": args.model,
        "model_label": args.tag,
        "model_revision": revision,
        "bank_sha256": sha256(args.bank),
        "items": len(items),
        "probe_records": len(probe_keys),
        "main_records": len(main_keys),
        "batch_size": args.batch_size,
        "device": args.device,
        "dtype": "bfloat16",
        "boundary_shifts": scorer.boundary_shifts,
        "elapsed_seconds": time.time() - started,
        "python": platform.python_version(),
        "torch_version": torch.__version__,
        "transformers_version": transformers.__version__,
    }
    (out / f"{args.tag}__metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(json.dumps(metadata, indent=2), flush=True)


if __name__ == "__main__":
    main()
