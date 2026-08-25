from __future__ import annotations

import json
import urllib.request
from pathlib import Path
from typing import Any, Iterable

BFCL_REPO = "ShishirPatil/gorilla"
BFCL_COMMIT = "f7cf7359b7ac615a0b294831c5ba2bc95ee4a000"
BFCL_DATA_ROOT = (
    f"https://raw.githubusercontent.com/{BFCL_REPO}/{BFCL_COMMIT}/"
    "berkeley-function-call-leaderboard/bfcl_eval/data"
)


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_jsonl(rows: Iterable[dict[str, Any]], path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def download_category(category: str, out_dir: str | Path) -> tuple[Path, Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    prompt_url = f"{BFCL_DATA_ROOT}/BFCL_v4_{category}.json"
    answer_url = f"{BFCL_DATA_ROOT}/possible_answer/BFCL_v4_{category}.json"
    prompt_path = out_dir / f"BFCL_v4_{category}.json"
    answer_path = out_dir / f"BFCL_v4_{category}_answers.json"
    urllib.request.urlretrieve(prompt_url, prompt_path)
    urllib.request.urlretrieve(answer_url, answer_path)
    return prompt_path, answer_path


def index_by_id(rows: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in rows}


def single_turn_messages(entry: dict[str, Any]) -> list[dict[str, str]]:
    q = entry["question"]
    if not q or not isinstance(q, list):
        raise ValueError(f"Malformed BFCL question for {entry.get('id')}")
    # BFCL single-turn stores one conversation as question[0].
    if isinstance(q[0], list):
        return q[0]
    return q


def user_text(entry: dict[str, Any]) -> str:
    msgs = single_turn_messages(entry)
    return "\n".join(str(m.get("content", "")) for m in msgs if m.get("role") == "user")


def one_function(entry: dict[str, Any]) -> dict[str, Any]:
    funcs = entry.get("function", [])
    if len(funcs) != 1:
        raise ValueError(f"Expected exactly one function for {entry.get('id')}, got {len(funcs)}")
    return funcs[0]


def openai_tools(entry: dict[str, Any]) -> list[dict[str, Any]]:
    """Convert BFCL function docs to the OpenAI/Hermes tool schema used by Qwen."""
    return [{"type": "function", "function": fn} for fn in entry.get("function", [])]
