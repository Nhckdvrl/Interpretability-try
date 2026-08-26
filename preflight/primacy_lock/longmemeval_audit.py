#!/usr/bin/env python3
"""Deterministic LongMemEval knowledge-update stale-intrusion preflight.

The script consumes the official cleaned LongMemEval JSON directly.  It does
not use an LLM judge.  Its main ecological signal is deliberately conservative:
an incorrect generated answer is marked as a high-precision stale intrusion
only when the answer string occurs verbatim in an older evidence session and
the official gold answer occurs in a later evidence session.

This will miss paraphrastic stale answers; false negatives are acceptable for
this preflight.  Do not interpret its lexical exact-match rate as the official
LongMemEval QA score.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common import load_json, load_jsonl, post_chat_completion, write_jsonl


def normalize(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[`*_\"']", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .,:;!?()[]{}")


def is_knowledge_update(row: dict) -> bool:
    qtype = str(row.get("question_type", "")).replace("_", "-").lower()
    return qtype == "knowledge-update"


def chronological_sessions(row: dict) -> list[dict]:
    sessions = row.get("haystack_sessions", [])
    dates = row.get("haystack_dates", [None] * len(sessions))
    ids = row.get("haystack_session_ids", list(range(len(sessions))))
    triples = list(zip(dates, ids, sessions))
    triples.sort(key=lambda x: "" if x[0] is None else str(x[0]))
    answer_ids = set(row.get("answer_session_ids", []))
    out = []
    for date, session_id, turns in triples:
        text = "\n".join(f"{t.get('role', 'unknown')}: {t.get('content', '')}" for t in turns)
        out.append({
            "date": date,
            "session_id": session_id,
            "is_answer_session": session_id in answer_ids,
            "turns": turns,
            "text": text,
        })
    return out


def render_prompt(row: dict) -> str:
    chunks = [
        "Below is a chronological record of previous conversations. Answer the final question using the history.",
        "When information changed over time, use the state that is correct at the time of the final question.",
    ]
    for i, sess in enumerate(chronological_sessions(row), 1):
        chunks.append(f"\n[Session {i} | {sess['date']}]\n{sess['text']}")
    chunks.append(f"\n[Final question | {row.get('question_date')}]\n{row['question']}\nAnswer concisely with the answer only.")
    return "\n".join(chunks)


def deterministic_correct(hypothesis: str, answer: str) -> bool:
    h, a = normalize(hypothesis), normalize(answer)
    if not h or not a:
        return False
    return h == a or (len(a) >= 4 and a in h)


def occurrence_indices(text: str, sessions: list[dict]) -> list[int]:
    needle = normalize(text)
    if len(needle) < 3:
        return []
    return [i for i, sess in enumerate(sessions) if needle in normalize(sess["text"])]


def audit_prediction(row: dict, hypothesis: str) -> dict:
    sessions = chronological_sessions(row)
    gold = str(row.get("answer", ""))
    gold_occ = occurrence_indices(gold, sessions)
    hyp_occ = occurrence_indices(hypothesis, sessions)
    correct = deterministic_correct(hypothesis, gold)

    high_precision_stale = False
    stale_from = []
    if not correct and gold_occ and hyp_occ:
        last_gold = max(gold_occ)
        stale_from = [i for i in hyp_occ if i < last_gold]
        high_precision_stale = bool(stale_from) and normalize(hypothesis) != normalize(gold)

    answer_session_positions = [i for i, sess in enumerate(sessions) if sess["is_answer_session"]]
    return {
        "deterministic_correct": correct,
        "gold_occurrence_session_indices": gold_occ,
        "hypothesis_occurrence_session_indices": hyp_occ,
        "answer_session_indices": answer_session_positions,
        "stale_source_session_indices": stale_from,
        "high_precision_stale_intrusion": high_precision_stale,
    }


def prepare_rows(dataset: list[dict], limit: int | None = None) -> list[dict]:
    rows = [r for r in dataset if is_knowledge_update(r) and not str(r.get("question_id", "")).endswith("_abs")]
    if limit is not None:
        rows = rows[:limit]
    return rows


def run_rows(rows: list[dict], args) -> list[dict]:
    out = []
    for i, row in enumerate(rows, 1):
        prompt = render_prompt(row)
        hypothesis = post_chat_completion(
            args.endpoint,
            args.model,
            [{"role": "user", "content": prompt}],
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            timeout=args.timeout,
            api_key=args.api_key,
            extra_body={"seed": args.generation_seed} if args.generation_seed is not None else None,
        )
        result = {
            "question_id": row.get("question_id"),
            "question_type": row.get("question_type"),
            "question": row.get("question"),
            "answer": row.get("answer"),
            "question_date": row.get("question_date"),
            "model": args.model,
            "hypothesis": hypothesis,
            "audit": audit_prediction(row, hypothesis),
        }
        out.append(result)
        if args.verbose:
            tag = "STALE" if result["audit"]["high_precision_stale_intrusion"] else ""
            print(f"[{i}/{len(rows)}] {result['question_id']} correct={result['audit']['deterministic_correct']} {tag}")
    return out


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    if not n:
        return {"n": 0}
    correct = sum(bool(r["audit"]["deterministic_correct"]) for r in rows)
    wrong = n - correct
    stale = sum(bool(r["audit"]["high_precision_stale_intrusion"]) for r in rows)
    historical_match_wrong = sum(
        (not r["audit"]["deterministic_correct"]) and bool(r["audit"]["hypothesis_occurrence_session_indices"])
        for r in rows
    )
    return {
        "n": n,
        "deterministic_lexical_accuracy": correct / n,
        "n_deterministic_wrong": wrong,
        "n_high_precision_stale_intrusions": stale,
        "high_precision_stale_share_of_wrong": stale / wrong if wrong else None,
        "n_wrong_answers_verbatim_in_any_history_session": historical_match_wrong,
        "warning": "This is a conservative lexical stale-intrusion audit, not the official LongMemEval LLM-judge score.",
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("--dataset", required=True)
    r.add_argument("--endpoint", required=True)
    r.add_argument("--model", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--api-key", default="EMPTY")
    r.add_argument("--temperature", type=float, default=0.0)
    r.add_argument("--max-tokens", type=int, default=128)
    r.add_argument("--timeout", type=int, default=600)
    r.add_argument("--generation-seed", type=int, default=0)
    r.add_argument("--limit", type=int)
    r.add_argument("--verbose", action="store_true")

    s = sub.add_parser("summarize")
    s.add_argument("--results", required=True)
    s.add_argument("--out")

    args = ap.parse_args()
    if args.cmd == "run":
        dataset = load_json(args.dataset)
        rows = prepare_rows(dataset, args.limit)
        results = run_rows(rows, args)
        write_jsonl(args.out, results)
        result = summarize(results)
    else:
        result = summarize(load_jsonl(args.results))
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
