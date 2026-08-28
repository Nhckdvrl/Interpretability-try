from __future__ import annotations
from pathlib import Path
import json

DEFAULT_REQUIRED_FAMILIES = ("Qwen", "Gemma", "Phi", "Llama", "Mistral")
PASS_VERDICT = "PASS-TO-PANEL"

def evaluate_panel(summary_paths: list[str], *, smoke_min_families: int = 2,
                   generality_min_families: int = 3, generality_panel_size: int = 5,
                   required_distinct_sizes_in_one_family: int = 3,
                   required_families: tuple[str, ...] = DEFAULT_REQUIRED_FAMILIES) -> dict:
    rows=[json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths]; fam={}; seen=set()
    for row in rows:
        family=row.get("family"); model=row.get("model"); size=row.get("size_b")
        if not family or not model or size is None: raise ValueError("each model summary must have family, model and size_b")
        key=(family,model,float(size))
        if key in seen: raise ValueError(f"duplicate model summary: {key}")
        seen.add(key); fam.setdefault(family,[]).append(row)
    required=set(required_families)
    def passed_row(r): return bool(r.get("model_pass")) and r.get("verdict")==PASS_VERDICT
    passed={f for f in required if f in fam and any(passed_row(r) for r in fam[f])}
    models={f:sorted({str(r["model"]) for r in fam.get(f,[]) if passed_row(r)}) for f in required_families}
    sizes={f:sorted({float(r["size_b"]) for r in fam.get(f,[]) if passed_row(r)}) for f in required_families}
    three=sorted(f for f,s in sizes.items() if len(s)>=required_distinct_sizes_in_one_family)
    full=required.issubset(fam) and len(required)>=generality_panel_size
    return {"required_families":list(required_families),"independent_families":sorted(fam),
            "missing_required_families":sorted(required-set(fam)),"unexpected_families":sorted(set(fam)-required),"full_panel_attempted":full,
            "passed_families":sorted(passed),"passed_models_by_family":models,"passed_sizes_b_by_family":sizes,
            "three_size_families":three,"smoke_cross_family_pass":len(passed)>=smoke_min_families,
            "generality_pass":full and len(passed)>=generality_min_families and bool(three),
            "note":"Only frozen families with model_pass=true AND verdict=PASS-TO-PANEL count. HOLD/FAIL summaries never count as passing families."}
