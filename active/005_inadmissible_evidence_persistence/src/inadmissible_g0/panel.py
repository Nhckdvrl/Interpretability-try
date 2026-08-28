from __future__ import annotations
from pathlib import Path
import json


def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3,
                   required_distinct_sizes_in_one_family: int = 3) -> dict:
    rows = [json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]
    family_rows: dict[str, list[dict]] = {}
    for row in rows:
        family = row.get("family")
        model = row.get("model")
        if not family or not model:
            raise ValueError("each model summary must have top-level family and model")
        family_rows.setdefault(family, []).append(row)

    passed_families = {
        family for family, rs in family_rows.items()
        if any(bool(r.get("model_pass")) for r in rs)
    }
    passed_models_by_family = {
        family: sorted({str(r["model"]) for r in rs if bool(r.get("model_pass"))})
        for family, rs in family_rows.items()
    }
    passed_sizes_by_family = {}
    for family, rs in family_rows.items():
        sizes = sorted({float(r["size_b"]) for r in rs if bool(r.get("model_pass")) and r.get("size_b") is not None})
        passed_sizes_by_family[family] = sizes
    three_size_families = sorted(
        family for family, sizes in passed_sizes_by_family.items()
        if len(sizes) >= required_distinct_sizes_in_one_family
    )
    return {
        "independent_families": sorted(family_rows),
        "passed_families": sorted(passed_families),
        "passed_models_by_family": passed_models_by_family,
        "passed_sizes_b_by_family": passed_sizes_by_family,
        "three_size_families": three_size_families,
        "smoke_cross_family_pass": len(passed_families) >= smoke_min_families,
        "generality_pass": (
            len(passed_families) >= generality_min_families
            and bool(three_size_families)
        ),
        "note": (
            "Generality requires >=3 passing independent families and >=3 distinct passing parameter sizes "
            "inside one family. size_b must be explicitly recorded; model names are never parsed as size evidence."
        ),
    }
