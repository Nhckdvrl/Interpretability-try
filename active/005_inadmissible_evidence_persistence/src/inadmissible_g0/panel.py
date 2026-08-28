from __future__ import annotations
from pathlib import Path
import json

def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3) -> dict:
    rows = [json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]
    fam = {}
    for row in rows:
        family = row.get("family")
        if not family:
            raise ValueError("each summary must be annotated with top-level 'family'")
        fam.setdefault(family, []).append(row)
    passed = {f for f, rs in fam.items() if any(bool(r.get("model_pass")) for r in rs)}
    return {
        "independent_families": sorted(fam),
        "passed_families": sorted(passed),
        "smoke_cross_family_pass": len(passed) >= smoke_min_families,
        "generality_pass": len(passed) >= generality_min_families,
        "note": "Both evidence polarities and every failed family remain reportable; do not subset after seeing results.",
    }
