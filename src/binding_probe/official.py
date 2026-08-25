from __future__ import annotations

import argparse
import json
import urllib.request
from pathlib import Path

from .bfcl import write_jsonl

BFCL_RESULT_REPO = "HuanzhiMao/BFCL-Result"
BFCL_RESULT_COMMIT = "6830ed13035c0cfee9aa7a9a0ffed70f10b3dd50"
BFCL_RESULT_SNAPSHOT = "2025-12-16"
DEFAULT_MODEL_DIR = "Qwen_Qwen3-4B-Instruct-2507-FC"


def result_url(model_dir: str, category: str) -> str:
    return (
        f"https://raw.githubusercontent.com/{BFCL_RESULT_REPO}/{BFCL_RESULT_COMMIT}/"
        f"{BFCL_RESULT_SNAPSHOT}/result/{model_dir}/non_live/BFCL_v4_{category}_result.json"
    )


def fetch_official_results(out_path: str | Path, model_dir: str = DEFAULT_MODEL_DIR, category: str = "simple_python") -> None:
    url = result_url(model_dir, category)
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(out_path.suffix + ".download")
    urllib.request.urlretrieve(url, tmp)
    converted = []
    with tmp.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            converted.append({
                "id": row["id"],
                "raw_output": row.get("result", ""),
                "source": "official_bfcl_result",
                "input_token_count": row.get("input_token_count"),
                "output_token_count": row.get("output_token_count"),
                "latency": row.get("latency"),
            })
    tmp.unlink(missing_ok=True)
    write_jsonl(converted, out_path)
    print(f"Pinned BFCL-Result commit: {BFCL_RESULT_COMMIT}")
    print(f"Snapshot: {BFCL_RESULT_SNAPSHOT}; model: {model_dir}; category: {category}")
    print(out_path)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts/qwen3_4b_official.jsonl")
    ap.add_argument("--model-dir", default=DEFAULT_MODEL_DIR)
    ap.add_argument("--category", default="simple_python")
    a = ap.parse_args()
    fetch_official_results(a.out, a.model_dir, a.category)


if __name__ == "__main__":
    main()
