"""D1 stage 4: sentence-level surface co-occurrence on the pinned Wikipedia dump.

Implements contract_d1.yaml amendment d1-r2 §2:

    S(X->B) = log( (c(X,B) + alpha) / (c(X) + beta) ),  alpha=1, beta=100

with sentence windows, casefolded word-boundary exact matching, on
`wikimedia/wikipedia` config `20231101.en`. That build carries only article
text, so redirect pages contribute nothing -- which is the point: a redirect
mechanically links an alias to its canonical page, and counting that would make
`alias -> canonical` and `Orlando Bloom -> Katy Perry` different statistical
objects. Link counts are forbidden by the contract for the same reason.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

import ahocorasick

# BUG FIX 2026-08-29: a plain `(?<=[.!?])\s+` splitter cuts personal names in
# half at their initials -- "P. Diddy", "L. L. Zamenhof", "Dr. Esperanto" -- so
# those surfaces counted ZERO occurrences across all of Wikipedia. Do not split
# after a single capital letter, a common title, or a lone initial.
SENT = re.compile(
    r"(?<=[.!?])\s+(?=[A-Z(\"'])"           # only before a new sentence start
    r"(?<!\b[A-Z]\.\s)"                     # not after a lone initial "P. "
)
_ABBR = re.compile(r"\b(?:[A-Z]|Dr|Mr|Mrs|Ms|Jr|Sr|St|Prof|Rev|Hon|Gen|Col|Lt"
                   r"|Sgt|Capt|Mt|Ft|Co|Inc|Ltd|vs|etc|al)\.$")


def split_sentences(text: str):
    """Sentence split that never cuts through `X. Y` initials or a title."""
    parts, buf = [], []
    for piece in SENT.split(text):
        buf.append(piece)
        if not _ABBR.search(piece.rstrip()):
            parts.append(" ".join(buf)); buf = []
    if buf:
        parts.append(" ".join(buf))
    return parts
WORDCH = re.compile(r"[0-9a-z]")


def build_automaton(patterns: list[str]):
    A = ahocorasick.Automaton()
    for i, p in enumerate(patterns):
        A.add_word(p.lower(), (i, len(p)))
    A.make_automaton()
    return A


def matches(A, sent_lower: str) -> set[int]:
    """pattern ids occurring in the sentence at word boundaries"""
    out = set()
    n = len(sent_lower)
    for end, (pid, plen) in A.iter(sent_lower):
        start = end - plen + 1
        before_ok = start == 0 or not WORDCH.match(sent_lower[start - 1])
        after_ok = end + 1 >= n or not WORDCH.match(sent_lower[end + 1])
        if before_ok and after_ok:
            out.add(pid)
    return out


def worker(shard_args):
    shard_id, n_shards, patterns, pairs_by_b, out_dir = shard_args
    from datasets import load_dataset
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train")
    ds = ds.shard(num_shards=n_shards, index=shard_id, contiguous=True)
    A = build_automaton(patterns)
    single = Counter()
    pair = Counter()
    want = {b: set(xs) for b, xs in pairs_by_b.items()}
    for n, row in enumerate(ds):
        for sent in split_sentences(row["text"]):
            if len(sent) > 4000:
                sent = sent[:4000]
            hit = matches(A, sent.lower())
            if not hit:
                continue
            single.update(hit)
            for b in hit:
                w = want.get(b)
                if w:
                    for x in hit & w:
                        if x != b:
                            pair[(x, b)] += 1
        if n and n % 200000 == 0:
            print(f"  shard {shard_id}: {n} articles", flush=True)
    Path(out_dir, f"shard{shard_id}.json").write_text(json.dumps(
        dict(single={str(k): v for k, v in single.items()},
             pair={f"{a}|{b}": v for (a, b), v in pair.items()})))
    return shard_id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assoc", default="data/d1_assoc_candidates.json")
    ap.add_argument("--out-dir", default="results/d1_build/cooc")
    ap.add_argument("--workers", type=int, default=16)
    args = ap.parse_args()

    A = json.load(open(args.assoc))
    strings: dict[str, int] = {}

    def pid(s):
        return strings.setdefault(s, len(strings))

    pairs_by_b: dict[int, list[int]] = {}
    for tgt, v in A.items():
        b = pid(v["target_form"])
        xs = [pid(v["seen_form"])] + [pid(r["label"]) for r in v["assoc"]]
        pairs_by_b.setdefault(b, [])
        pairs_by_b[b].extend(xs)
    patterns = [s for s, _ in sorted(strings.items(), key=lambda kv: kv[1])]
    print(f"{len(patterns)} distinct surface strings, "
          f"{sum(len(v) for v in pairs_by_b.values())} pairs to count")

    out = Path(args.out_dir); out.mkdir(parents=True, exist_ok=True)
    Path(out, "strings.json").write_text(json.dumps(patterns))

    import multiprocessing as mp
    jobs = [(i, args.workers, patterns, pairs_by_b, str(out))
            for i in range(args.workers)]
    with mp.get_context("spawn").Pool(args.workers) as pool:
        for sid in pool.imap_unordered(worker, jobs):
            print(f"shard {sid} done", flush=True)
    print("all shards done")


if __name__ == "__main__":
    main()
