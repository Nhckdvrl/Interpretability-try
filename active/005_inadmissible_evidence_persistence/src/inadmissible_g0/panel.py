from __future__ import annotations
from pathlib import Path
import json

def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3, generality_panel_size: int = 5,
                   size_sequence_min: int = 3, strong_model_min_size_b: float = 24.0) -> dict:
    rows = [json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]
    if not rows:
        raise ValueError("summary_paths is empty")
    family_rows: dict[str, list[dict]] = {}
    for row in rows:
        family = row.get("family")
        if not family:
            raise ValueError("each model summary must contain top-level 'family'")
        size_b = row.get("size_b")
        if size_b is None or float(size_b) <= 0:
            raise ValueError("each model summary must contain positive top-level 'size_b'")
        family_rows.setdefault(family, []).append(row)
    passed_families = {f for f, rs in family_rows.items() if any(bool(r.get("model_pass")) for r in rs)}
    passed_sizes_by_family = {
        f: sorted({float(r["size_b"]) for r in rs if bool(r.get("model_pass"))})
        for f, rs in family_rows.items()
    }
    three_size_families = sorted(f for f, sizes in passed_sizes_by_family.items() if len(sizes) >= size_sequence_min)
    strong_model_passes = [
        {"model": r.get("model"), "family": r.get("family"), "size_b": float(r["size_b"])}
        for r in rows if bool(r.get("model_pass")) and float(r["size_b"]) >= strong_model_min_size_b
    ]
    smoke_pass = len(passed_families) >= smoke_min_families
    full_panel_covered = len(family_rows) >= generality_panel_size
    size_sequence_pass = bool(three_size_families)
    strong_model_pass = bool(strong_model_passes)
    generality_pass = (
        full_panel_covered and len(passed_families) >= generality_min_families
        and size_sequence_pass and strong_model_pass
    )
    return {
        "independent_families": sorted(family_rows),
        "passed_families": sorted(passed_families),
        "passed_sizes_by_family": passed_sizes_by_family,
        "three_size_families": three_size_families,
        "strong_model_passes": strong_model_passes,
        "smoke_cross_family_pass": smoke_pass,
        "full_panel_covered": full_panel_covered,
        "size_sequence_pass": size_sequence_pass,
        "strong_model_pass": strong_model_pass,
        "generality_pass": generality_pass,
        "note": "Generality requires >=3 passing families in a five-family panel, a passing three-size sequence in one family, and survival on at least one >=24B checkpoint.",
    }
