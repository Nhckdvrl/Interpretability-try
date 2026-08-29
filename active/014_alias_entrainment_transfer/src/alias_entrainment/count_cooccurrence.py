"""D1 r4 stage 4: surface co-occurrence on the pinned Wikipedia snapshot.

Counts BOTH ordered directions for every retained surface pair and every ASSOC
candidate.  This is deliberately a new output namespace/version: the committed
pre-r4 shards were produced before the initials sentence-splitting fix and MUST
not be consumed.

    S(X->B) = log((c(X,B)+1)/(c(X)+100))

Canonical contract: configs/contract_d1_r4.yaml
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import ahocorasick

COOC_VERSION = "d1-r4-cooc-v2"
SNAPSHOT = "wikimedia/wikipedia:20231101.en"

# Split conservatively, then re-join pieces ending in initials/common
# abbreviations.  Unlike the old lookahead, this does not require ASCII [A-Z]
# at the next sentence start, so non-English/diacritic names remain countable.
SENT = re.compile(r"(?<=[.!?])\s+")
_ABBR = re.compile(
    r"(?:\b[^\W_]\.|\b(?:Dr|Mr|Mrs|Ms|Jr|Sr|St|Prof|Rev|Hon|Gen|Col|Lt|Sgt|Capt|Mt|Ft|Co|Inc|Ltd|vs|etc|al|e\.g|i\.e)\.)$",
    re.IGNORECASE | re.UNICODE,
)


def split_sentences(text: str):
    """Sentence-ish windows that do not cut `P. Diddy` / `L. L. Zamenhof`."""
    parts, buf = [], []
    for piece in SENT.split(text or ""):
        buf.append(piece)
        if not _ABBR.search(piece.rstrip()):
            parts.append(" ".join(buf))
            buf = []
    if buf:
        parts.append(" ".join(buf))
    return parts


def is_word_char(ch: str) -> bool:
    return bool(ch) and (ch.isalnum() or ch == "_")


def build_automaton(patterns: list[str]):
    A = ahocorasick.Automaton()
    for i, p in enumerate(patterns):
        folded = p.casefold()
        if not folded:
            continue
        A.add_word(folded, (i, len(folded)))
    A.make_automaton()
    return A


def matches(A, sent_folded: str) -> set[int]:
    """Pattern ids occurring at Unicode-aware alphanumeric boundaries."""
    out = set()
    n = len(sent_folded)
    for end, (pid, plen) in A.iter(sent_folded):
        start = end - plen + 1
        before_ok = start == 0 or not is_word_char(sent_folded[start - 1])
        after_ok = end + 1 >= n or not is_word_char(sent_folded[end + 1])
        if before_ok and after_ok:
            out.add(pid)
    return out


def worker(shard_args):
    shard_id, n_shards, patterns, pairs_by_b, out_dir = shard_args
    from datasets import load_dataset
    ds = load_dataset("wikimedia/wikipedia", "20231101.en", split="train")
    ds = ds.shard(num_shards=n_shards, index=shard_id, contiguous=True)
    A = build_automaton(patterns)
    single, pair = Counter(), Counter()
    want = {int(b): set(xs) for b, xs in pairs_by_b.items()}
    for n, row in enumerate(ds):
        for sent in split_sentences(row["text"]):
            if len(sent) > 4000:
                sent = sent[:4000]
            hit = matches(A, sent.casefold())
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
    Path(out_dir, f"shard{shard_id}.json").write_text(json.dumps(dict(
        version=COOC_VERSION,
        snapshot=SNAPSHOT,
        single={str(k): v for k, v in single.items()},
        pair={f"{a}|{b}": v for (a, b), v in pair.items()},
    )))
    return shard_id


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--assoc", default="data/d1_assoc_candidates_r4.json")
    ap.add_argument("--out-dir", default="results/d1_build/cooc_r4")
    ap.add_argument("--workers", type=int, default=16)
    ap.add_argument("--overwrite", action="store_true")
    args = ap.parse_args()

    A = json.load(open(args.assoc))
    strings: dict[str, int] = {}

    def pid(s):
        if s not in strings:
            strings[s] = len(strings)
        return strings[s]

    pairs_by_b: dict[int, set[int]] = {}
    for v in A:
        alias, canon = v["seen_form"], v["target_form"]
        assoc_surfaces = [r["label"] for r in v.get("assoc", [])]
        # alias -> canonical
        b = pid(canon)
        pairs_by_b.setdefault(b, set()).update([pid(alias), *[pid(x) for x in assoc_surfaces]])
        # canonical -> alias
        b = pid(alias)
        pairs_by_b.setdefault(b, set()).update([pid(canon), *[pid(x) for x in assoc_surfaces]])

    patterns = [s for s, _ in sorted(strings.items(), key=lambda kv: kv[1])]
    out = Path(args.out_dir)
    if out.exists() and list(out.glob("shard*.json")) and not args.overwrite:
        raise RuntimeError(
            f"{out} already contains shards; refuse to mix runs. Use --overwrite only after deleting/archiving them."
        )
    out.mkdir(parents=True, exist_ok=True)
    if args.overwrite:
        for p in out.glob("shard*.json"):
            p.unlink()

    pattern_hash = hashlib.sha256("\0".join(patterns).encode("utf-8")).hexdigest()
    Path(out, "strings.json").write_text(json.dumps(dict(
        version=COOC_VERSION, snapshot=SNAPSHOT, patterns=patterns,
        patterns_sha256=pattern_hash,
    ), ensure_ascii=False))
    print(f"{len(patterns)} distinct surfaces; "
          f"{sum(len(v) for v in pairs_by_b.values())} ordered pairs to count")

    import multiprocessing as mp
    serial_pairs = {str(k): sorted(v) for k, v in pairs_by_b.items()}
    jobs = [(i, args.workers, patterns, serial_pairs, str(out))
            for i in range(args.workers)]
    with mp.get_context("spawn").Pool(args.workers) as pool:
        for sid in pool.imap_unordered(worker, jobs):
            print(f"shard {sid} done", flush=True)
    print(f"all shards done; version={COOC_VERSION}; pattern_sha={pattern_hash}")


if __name__ == "__main__":
    main()
