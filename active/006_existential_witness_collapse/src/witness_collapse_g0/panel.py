from __future__ import annotations
from pathlib import Path
import json
DEFAULT_REQUIRED_FAMILIES=("Qwen","Gemma","Phi","Llama","Mistral")
def evaluate_panel(summary_paths:list[str],*,smoke_min_families:int=2,generality_min_families:int=3,generality_panel_size:int=5,required_distinct_sizes_in_one_family:int=3,required_families:tuple[str,...]=DEFAULT_REQUIRED_FAMILIES)->dict:
    rows=[json.loads(Path(p).read_text(encoding="utf-8")) for p in summary_paths];families={};seen=set()
    for row in rows:
        family,model,size=row.get("family"),row.get("model"),row.get("size_b")
        if not family or not model or size is None:raise ValueError("each summary must contain family, model and size_b")
        key=(str(family),str(model),float(size))
        if key in seen:raise ValueError(f"duplicate model summary={key}")
        seen.add(key);families.setdefault(str(family),[]).append(row)
    required=set(required_families);passed=lambda r:bool(r.get("model_pass")) and r.get("verdict")=="PASS-TO-PANEL";pf={f for f in required if any(passed(r) for r in families.get(f,[]))};sizes={f:sorted({float(r["size_b"]) for r in families.get(f,[]) if passed(r)}) for f in required_families};three=sorted(f for f,v in sizes.items() if len(v)>=required_distinct_sizes_in_one_family);full=required.issubset(families) and len(required)>=generality_panel_size
    return {"required_families":list(required_families),"independent_families":sorted(families),"missing_required_families":sorted(required-set(families)),"passed_families":sorted(pf),"passed_sizes_b_by_family":sizes,"three_size_families":three,"smoke_cross_family_pass":len(pf)>=smoke_min_families,"generality_pass":full and len(pf)>=generality_min_families and bool(three),"note":"Only model_pass=true with verdict PASS-TO-PANEL counts; capability-floor and artifact failures never count."}
