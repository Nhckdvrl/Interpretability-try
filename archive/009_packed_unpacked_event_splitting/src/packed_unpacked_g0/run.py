from __future__ import annotations
from pathlib import Path
from typing import Any
import json
from .data import load_scenarios
from .prompts import LABEL_ORDERS, READOUT_TEMPLATES, recognition_prompt, pair_relation_prompt, comparison_prompt
from .scoring import HFChoiceScorer, VLLMChoiceScorer


def _write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _semantic_probs(label_probs: dict[str, float], mapping: dict[str, str]) -> dict[str, float]:
    return {semantic: label_probs[label] for label, semantic in mapping.items()}


def run(*, data_path: str, out_path: str, model_name: str, family: str,
        revision: str | None = None, dtype: str = "auto", size_b: float | None = None,
        sequence_batch_size: int = 64, base_url: str | None = None, served_model: str | None = None) -> None:
    if size_b is None or size_b <= 0:
        raise ValueError("size_b must be explicitly provided and > 0")
    scenarios = load_scenarios(data_path, require_external_source=True)
    scorer = VLLMChoiceScorer(model_name, base_url=base_url, revision=revision, served_model=served_model) if base_url else HFChoiceScorer(model_name, revision=revision, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []; meta: list[dict[str, Any]] = []
    for s in scenarios:
        for p in s.partitions:
            rec_specs = []
            for prefix, packed, branches in (("focal", s.packed_text, p.branches), ("complement", p.complement_text, p.complement_branches)):
                for probe in ("equivalent", "disjoint", "exhaustive"):
                    rec_specs.append((f"{prefix}_{probe}", recognition_prompt, (packed, branches, probe)))
            for probe in ("disjoint", "exhaustive"):
                rec_specs.append((f"pair_{probe}", pair_relation_prompt, (s.packed_text, p.complement_text, probe)))
            for probe_name, fn, args in rec_specs:
                for order in (0, 1):
                    yes, no = (("A", "B") if order == 0 else ("B", "A"))
                    requests.append((fn(*args, yes, no), ("A", "B")))
                    meta.append({"kind":"recognition","scenario_id":s.scenario_id,"domain":s.domain,
                                 "partition_id":p.partition_id,"branch_count":p.branch_count,
                                 "branch_count_family":p.branch_count_family,"probe":probe_name,
                                 "label_order":order,"yes_label":yes})
            variants = {"core": p.unpacked_text, "reordered": p.reordered_unpacked_text,
                        "paraphrase": s.packed_paraphrase, "partial_subset": p.partial_text,
                        "repacked": p.repacked_text}
            focal_contexts = {"baseline": (s.packed_text, p.complement_text),
                              "focal_unpacked": (p.unpacked_text, p.complement_text),
                              "alternative_unpacked": (s.packed_text, p.complement_unpacked_text),
                              "focal_length_control": (p.focal_length_control_text, p.complement_text),
                              "alternative_length_control": (s.packed_text, p.complement_length_control_text)}
            for readout, templates in READOUT_TEMPLATES.items():
                for template_id, (template_kind, instruction) in enumerate(templates):
                    for condition, variant in variants.items():
                        for side_order in (0, 1):
                            left, right = ((s.packed_text, variant) if side_order == 0 else (variant, s.packed_text))
                            variant_side = "right" if side_order == 0 else "left"
                            for order_id, mapping in enumerate(LABEL_ORDERS):
                                requests.append((comparison_prompt(left, right, instruction, mapping, readout), ("A","B","C")))
                                meta.append({"kind":"judgment","scenario_id":s.scenario_id,"domain":s.domain,
                                    "partition_id":p.partition_id,"branch_count":p.branch_count,"branch_count_family":p.branch_count_family,
                                    "readout":readout,"template_id":template_id,"template_kind":template_kind,"condition":condition,
                                    "side_order":side_order,"variant_side":variant_side,"label_order":order_id,"mapping":mapping})
                    for condition, (focal_text, alternative_text) in focal_contexts.items():
                        for side_order in (0, 1):
                            left, right = ((focal_text, alternative_text) if side_order == 0 else (alternative_text, focal_text))
                            focal_side = "left" if side_order == 0 else "right"
                            for order_id, mapping in enumerate(LABEL_ORDERS):
                                requests.append((comparison_prompt(left, right, instruction, mapping, readout), ("A","B","C")))
                                meta.append({"kind":"focal_alternative","scenario_id":s.scenario_id,"domain":s.domain,
                                    "partition_id":p.partition_id,"branch_count":p.branch_count,"branch_count_family":p.branch_count_family,
                                    "readout":readout,"template_id":template_id,"template_kind":template_kind,"condition":condition,
                                    "side_order":side_order,"focal_side":focal_side,"label_order":order_id,"mapping":mapping})
    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows=[]
    for m, score in zip(meta, scores):
        row=dict(m); row.update({"model":model_name,"family":family,"revision":revision,"size_b":size_b,
                                 "requested_dtype":dtype,"label_probs":score.probs})
        if m["kind"]=="recognition": row["p_correct"]=score.probs[m["yes_label"]]
        else: row.update({f"p_{k}":v for k,v in _semantic_probs(score.probs,m["mapping"]).items()})
        rows.append(row)
    _write_jsonl(out_path, rows)
