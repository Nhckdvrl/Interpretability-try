"""Create deterministic scope, attrition, and source/control audits for D1 r4."""
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path


def sha256(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def stable_sample(rows: list[dict], n: int, key) -> list[dict]:
    return sorted(rows, key=lambda r: hashlib.sha256(key(r).encode()).hexdigest())[:n]


def count(rows: list[dict], key) -> dict:
    return dict(sorted(Counter(key(r) for r in rows).items(), key=lambda x: str(x[0])))


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", default="data/d1_surface_pairs_r4.json")
    ap.add_argument("--wikidata", default="data/d1_wikidata_r4.json")
    ap.add_argument("--assoc", default="data/d1_assoc_candidates_r4.json")
    ap.add_argument("--bank", default="data/frozen_d1_r4.jsonl")
    ap.add_argument("--out-dir", default="results/d1_build/audit_r4")
    ap.add_argument("--sample-n", type=int, default=20)
    args = ap.parse_args()

    surface = json.load(open(args.surface, encoding="utf-8"))
    wikidata = json.load(open(args.wikidata, encoding="utf-8"))
    assoc = json.load(open(args.assoc, encoding="utf-8"))
    bank = [json.loads(line) for line in open(args.bank, encoding="utf-8") if line.strip()]
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)

    survived_pairs = {r["pair_id"] for r in bank}
    unmatched = [r for r in assoc if r["pair_id"] not in survived_pairs]
    intended_bank = [r for r in bank if r["confirmatory_intended_surface"]]
    summary = {
        "contract_id": "2026-08-29-d1-r4-scope-correction",
        "source": "naist-nlp/RedirectQA v1.0.0",
        "corpus_snapshot": "wikimedia/wikipedia 20231101.en",
        "stages": {
            "raw_surface_pairs": len(surface),
            "raw_entities": len({r["subject_id"] for r in surface}),
            "intended_surface_pairs": sum(r["confirmatory_intended_surface"] for r in surface),
            "entities_with_usable_relation": sum(
                bool([k for k in v.get("ties", {}) if k != "different_from"])
                for v in wikidata.values()
            ),
            "pairs_with_assoc_any_candidate": sum(bool(r.get("assoc")) for r in assoc),
            "matched_ordered_items": len(bank),
            "matched_surface_pairs": len(survived_pairs),
            "matched_entities": len({r["entity_uri"] for r in bank}),
            "matched_intended_ordered_items": len(intended_bank),
            "matched_intended_entities": len({r["entity_uri"] for r in intended_bank}),
            "matched_intended_opaque_strict_entities": len({
                r["entity_uri"] for r in intended_bank
                if r["structural_stratum"] == "opaque_strict"
            }),
            "matched_with_assoc_sametype": sum(bool(r.get("assoc_sametype")) for r in bank),
        },
        "raw": {
            "structure": count(surface, lambda r: r["structural_stratum"]),
            "high_level_type": count(
                [dict(row=r, label=t) for r in surface
                 for t in (r["redirect_high_types"] or ["UNKNOWN"])],
                lambda x: x["label"],
            ),
        },
        "matched": {
            "direction": count(bank, lambda r: r["direction"]),
            "structure": count(bank, lambda r: r["structural_stratum"]),
            "entity_type": count(bank, lambda r: r["entity_type"]),
            "assoc_relation": count(bank, lambda r: r["assoc_any_relation"]),
        },
        "sha256": {name: sha256(path) for name, path in {
            "surface": args.surface, "wikidata": args.wikidata,
            "assoc": args.assoc, "bank": args.bank,
        }.items()},
        "scope_note": (
            "Raw scope is never replaced by matched survivors. Entity type, direction, surface "
            "structure, RedirectQA class, and capability are factors, not construction filters."
        ),
    }
    (out / "scope_attrition_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n"
    )
    n = args.sample_n
    write_jsonl(out / "source_sample.jsonl", stable_sample(
        surface, n, lambda r: r["pair_id"] + "source-audit"
    ))
    write_jsonl(out / "assoc_candidate_sample.jsonl", stable_sample(
        [r for r in assoc if r.get("assoc")], n,
        lambda r: r["pair_id"] + "assoc-audit",
    ))
    write_jsonl(out / "matched_control_sample.jsonl", stable_sample(
        bank, n, lambda r: r["item_id"] + "matched-audit"
    ))
    write_jsonl(out / "unmatched_source_sample.jsonl", stable_sample(
        unmatched, n, lambda r: r["pair_id"] + "attrition-audit"
    ))
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
