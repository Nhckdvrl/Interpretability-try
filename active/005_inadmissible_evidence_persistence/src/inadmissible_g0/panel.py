from __future__ import annotations
from pathlib import Path
import json

DEFAULT_REQUIRED_FAMILIES = ("Qwen", "Gemma", "Phi", "Llama", "Mistral")

def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3, generality_panel_size: int = 5,
                   required_distinct_sizes_in_one_family: int = 3,
                   required_families: tuple[str, ...] = DEFAULT_REQUIRED_FAMILIES) -> dict:
    rows=[json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]; fam={}
    for row in rows:
        family=row.get("family"); model=row.get("model")
        if not family or not model: raise ValueError("each model summary must have top-level family and model")
        fam.setdefault(family,[]).append(row)
    required=set(required_families)
    passed={f for f in required if f in fam and any(bool(r.get("model_pass")) for r in fam[f])}
    models={f:sorted({str(r["model"]) for r in fam.get(f,[]) if bool(r.get("model_pass"))}) for f in required_families}
    sizes={f:sorted({float(r["size_b"]) for r in fam.get(f,[]) if bool(r.get("model_pass")) and r.get("size_b") is not None}) for f in required_families}
    three=sorted(f for f,s in sizes.items() if len(s)>=required_distinct_sizes_in_one_family)
    full=required.issubset(fam) and len(required)>=generality_panel_size
    return {"required_families":list(required_families),"independent_families":sorted(fam),
            "missing_required_families":sorted(required-set(fam)),"full_panel_attempted":full,
            "passed_families":sorted(passed),"passed_models_by_family":models,"passed_sizes_b_by_family":sizes,
            "three_size_families":three,"smoke_cross_family_pass":len(passed)>=smoke_min_families,
            "generality_pass":full and len(passed)>=generality_min_families and bool(three),
            "note":"Only the frozen Qwen/Gemma/Phi/Llama/Mistral panel counts toward 3/5 generality; extra family labels cannot replace a missing required family."}
