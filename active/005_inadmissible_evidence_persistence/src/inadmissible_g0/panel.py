from __future__ import annotations
from pathlib import Path
import json


def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3,
                   generality_panel_size: int = 5,
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
    full_panel_attempted = len(family_rows) >= generality_panel_size
    return {
        "independent_families": sorted(family_rows),
        "full_panel_attempted": full_panel_attempted,
        "passed_families": sorted(passed_families),
        "passed_models_by_family": passed_models_by_family,
        "passed_sizes_b_by_family": passed_sizes_by_family,
        "three_size_families": three_size_families,
        "smoke_cross_family_pass": len(passed_families) >= smoke_min_families,
        "generality_pass": (
            full_panel_attempted
            and len(passed_families) >= generality_min_families
            and bool(three_size_families)
        ),
        "note": (
            "Generality means 3/5 rather than merely 3 observed families: the configured full family panel must be attempted, "
            ">=3 independent families must pass, and one family must have >=3 distinct passing size_b values."
        ),
    }
