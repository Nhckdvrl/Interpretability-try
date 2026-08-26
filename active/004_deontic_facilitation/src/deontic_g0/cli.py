from __future__ import annotations

import argparse
from pathlib import Path
import urllib.request

from .metrics import summarize
from .run import run_g0

PINNED_DATA_URL = (
    "https://raw.githubusercontent.com/kmineshima/NeuBAROCO/"
    "447929fdabe07bc3d13efae8e0c527fd458df177/eacl2026/wason.tsv"
)


def fetch_main() -> None:
    p = argparse.ArgumentParser(description="Fetch the pinned official EACL 2026 Wason dataset")
    p.add_argument("--out", default="data/wason.tsv")
    args = p.parse_args()
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(PINNED_DATA_URL, timeout=30) as r:
        data = r.read()
    out.write_bytes(data)
    print(f"wrote {len(data)} bytes to {out}")


def run_main() -> None:
    p = argparse.ArgumentParser(description="Run frozen deontic-facilitation G0")
    p.add_argument("--model", required=True)
    p.add_argument("--data", default="data/wason.tsv")
    p.add_argument("--out", required=True)
    p.add_argument("--limit", type=int)
    p.add_argument("--sequence-batch-size", type=int, default=96)
    p.add_argument("--dtype", default="auto")
    args = p.parse_args()
    run_g0(
        model_name=args.model,
        data_path=args.data,
        out_path=args.out,
        limit=args.limit,
        sequence_batch_size=args.sequence_batch_size,
        dtype=args.dtype,
    )


def summarize_main() -> None:
    p = argparse.ArgumentParser(description="Summarize frozen deontic-facilitation G0")
    p.add_argument("--data", default="data/wason.tsv")
    p.add_argument("--results", required=True)
    p.add_argument("--config", default="configs/g0.json")
    p.add_argument("--out", required=True)
    args = p.parse_args()
    summary = summarize(data_path=args.data, results_path=args.results, config_path=args.config, out_path=args.out)
    print(
        f"model_pass={summary['model_pass']} "
        f"delta_acc={summary['paired']['mean_delta_accuracy']:.4f} "
        f"delta_p={summary['paired']['mean_delta_p_gold']:.4f} "
        f"strong={summary['paired']['strong_pairs']}"
    )
