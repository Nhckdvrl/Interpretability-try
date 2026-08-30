"""Materialize the complete MUCAR dual-ambiguity source population."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from .io import sha256, write_jsonl


def strip_label(option: str) -> str:
    return re.sub(r"^\s*[AB][.、:)\]]\s*", "", option).strip()


def gold_index(row: dict) -> int:
    answer = row["answer"].strip()
    exact = [i for i, option in enumerate(row["options"]) if option.strip() == answer]
    if len(exact) == 1:
        return exact[0]
    if answer[:1] in {"A", "B"}:
        index = ord(answer[0]) - ord("A")
        if index < len(row["options"]):
            return index
    raise ValueError(f"cannot map source answer for id={row.get('id')}: {answer!r}")


def image_lookup(root: Path) -> dict[str, Path]:
    lookup: dict[str, Path] = {}
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png", ".webp"}:
            continue
        rel = path.relative_to(root).with_suffix("").as_posix()
        candidates = {rel, rel.removeprefix("images/"), path.stem}
        for key in candidates:
            if key in lookup and lookup[key] != path:
                continue
            lookup[key] = path
    return lookup


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", default="data/mucar_source/data-all.json")
    ap.add_argument("--images", default="data/mucar_images")
    ap.add_argument("--out-dir", default="data/d0_v1")
    ap.add_argument("--audit-n", type=int, default=30)
    args = ap.parse_args()
    source = json.load(open(args.source, encoding="utf-8"))
    dual = [row for row in source if int(row["tags"]["category"]) == 7]
    images_root = Path(args.images).resolve()
    lookup = image_lookup(images_root)
    rows = []
    excluded = []
    for row in dual:
        image_id = str(row["image_id"])
        image = lookup.get(image_id) or lookup.get(Path(image_id).name)
        if image is None:
            stem = image_id.rsplit("/", 1)[-1]
            candidates = sorted(path.relative_to(images_root).as_posix() for path in images_root.rglob(f"{stem}-*.*"))
            excluded.append({
                "source_id": int(row["id"]),
                "image_id": image_id,
                "reason": "released image_id does not exactly identify one file",
                "candidate_files": candidates,
            })
            continue
        options = [strip_label(option) for option in row["options"]]
        if len(options) != 2 or not all(options):
            raise ValueError(f"non-binary/empty options at source id={row['id']}")
        rows.append({
            "item_id": f"mucar-dual-{int(row['id']):04d}",
            "source_id": int(row["id"]),
            "question_id": int(row["question_id"]),
            "pair_id": str(row["pair_id"]),
            "image_id": image_id,
            # Stable across machines; the runner resolves this path relative to --images.
            "image_path": image.relative_to(images_root).as_posix(),
            "image_sha256": sha256(image),
            "question": "\n".join(part.strip() for part in (
                row.get("context") or row.get("sentence"), row.get("question")
            ) if part and part.strip()),
            "options": options,
            "gold_index": gold_index(row),
            "language": int(row["tags"]["language"]),
            "source_category": row.get("category") or "Dual-Ambiguity",
        })
    ids = [row["item_id"] for row in rows]
    if len(rows) != 186 or len(excluded) != 186 or len(ids) != len(set(ids)):
        raise RuntimeError(
            f"expected release audit split 186 exact/186 defective, got "
            f"{len(rows)} exact/{len(excluded)} defective/{len(set(ids))} unique IDs"
        )
    out = Path(args.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    bank = out / "d0_bank.jsonl"
    write_jsonl(bank, rows)
    audit = sorted(rows, key=lambda row: hashlib.sha256(
        (row["item_id"] + "source-audit").encode()).hexdigest())[:args.audit_n]
    write_jsonl(out / "source_audit_sample.jsonl", audit)
    write_jsonl(out / "excluded_release_mapping_defects.jsonl", excluded)
    summary = {
        "contract_id": "017-d0-v1",
        "source_rows": len(source),
        "target_dual_rows": len(dual),
        "released_valid_rows": len(rows),
        "excluded_mapping_defects": len(excluded),
        "unique_pair_ids": len({row["pair_id"] for row in rows}),
        "languages": dict(sorted(Counter(row["language"] for row in rows).items())),
        "source_categories": dict(Counter(row["source_category"] for row in rows)),
        "unique_images": len({row["image_sha256"] for row in rows}),
        "bank_sha256": sha256(bank),
        "source_sha256": sha256(args.source),
        "source_commit": "930eb28610c9799ee0caf81c7c0b59ac33cb372c",
        "image_revision": "3a28f23644e54a58c6131b41fe762a04869ee7cc",
    }
    (out / "scope_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
