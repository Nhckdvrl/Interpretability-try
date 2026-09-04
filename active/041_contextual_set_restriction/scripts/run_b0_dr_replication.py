"""Score B0: Davies & Richardson (2021) materials, reading time replaced by window surprisal.

Raw text, no chat template: the measure is the LM analogue of self-paced reading time, so the
vignette is scored as plain running text exactly as their participants read it. Two windows, theirs:
the noun phrase (adjective + noun) and the following wrap-up phrase.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "phenomenon_miner"))
from model_scoring import load_model, resolve_snapshot  # noqa: E402
from span_scoring import score_spans  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--stimuli", type=Path, required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--model-path", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--batch-size", type=int, default=None)
    args = parser.parse_args()

    config = json.loads(args.config.read_text())
    if args.model not in config["models"]:
        raise ValueError("Model is not frozen in config")
    rows = [json.loads(line) for line in args.stimuli.read_text().splitlines() if line]

    texts, spans = [], []
    for row in rows:
        text = row["full_text"]
        np_start = len(row["prefix"])
        np_end = np_start + len(row["critical_window"])
        texts.append(text)
        spans.append([(np_start, np_end), (np_end, np_end + len(row["wrapup_window"]))])

    tokenizer, model = load_model(args.model_path, config["dtype"])
    scored = score_spans(tokenizer, model, texts, spans,
                         args.batch_size or int(config["batch_size"]))
    checkpoint, revision = resolve_snapshot(args.model)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w") as handle:
        handle.write(json.dumps({
            "record_type": "metadata", "experiment_version": config["experiment_version"],
            "model_checkpoint": checkpoint, "model_revision": revision, "n_rows": len(rows),
            "seed": config["seed"],
            "commit_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
        }) + "\n")
        for row, (np_window, wrapup_window) in zip(rows, scored):
            handle.write(json.dumps({
                "record_type": "example",
                **{key: value for key, value in row.items() if key != "full_text"},
                "np_window": np_window, "wrapup_window": wrapup_window,
                "np_surprisal": -np_window["mean_logprob"],
                "wrapup_surprisal": -wrapup_window["mean_logprob"],
            }, ensure_ascii=False) + "\n")
    print(json.dumps({"output": str(args.output), "rows": len(rows)}))


if __name__ == "__main__":
    main()
