from __future__ import annotations
from pathlib import Path
import json

def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3) -> dict:
    rows = [json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]
    family_rows = {}
    for row in rows:
        family = row.get("family")
        if not family:
            raise ValueError("each model summary must be annotated with a top-level 'family'")
        family_rows.setdefault(family, []).append(row)
    passed = {f for f, rs in family_rows.items() if any(bool(r.get("model_pass")) for r in rs)}
    return {
        "independent_families": sorted(family_rows),
        "passed_families": sorted(passed),
        "smoke_cross_family_pass": len(passed) >= smoke_min_families,
        "generality_pass": len(passed) >= generality_min_families,
        "note": "No failed family is discarded; inspect all per-model summaries before promotion.",
    }
