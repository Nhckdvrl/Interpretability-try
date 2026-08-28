from __future__ import annotations
from pathlib import Path
from typing import Any
import json

from .data import load_scenarios
from .prompts import (
    LABEL_ORDERS, PROBABILITY_TEMPLATES, DECISION_TEMPLATES,
    recognition_prompt, comparison_prompt, partial_text,
)
from .scoring import HFChoiceScorer

def _write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def _semantic_probs(label_probs: dict[str, float], mapping: dict[str, str]) -> dict[str, float]:
    return {semantic: label_probs[label] for label, semantic in mapping.items()}

def run(*, data_path: str, out_path: str, model_name: str, family: str,
        revision: str | None = None, dtype: str = "auto",
        sequence_batch_size: int = 64) -> None:
    scenarios = load_scenarios(data_path, require_external_source=True)
    scorer = HFChoiceScorer(model_name, revision=revision, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []
    meta: list[dict[str, Any]] = []

    for s in scenarios:
        for p in s.partitions:
            for probe in ("equivalent", "disjoint", "exhaustive"):
                for order in (0, 1):
                    yes, no = (("A", "B") if order == 0 else ("B", "A"))
                    requests.append((recognition_prompt(s.packed_text, p.branches, probe, yes, no), ("A", "B")))
                    meta.append({
                        "kind": "recognition", "scenario_id": s.scenario_id, "domain": s.domain,
                        "partition_id": p.partition_id, "branch_count": p.branch_count,
                        "probe": probe, "label_order": order, "yes_label": yes,
                    })

            readouts = [
                ("probability", PROBABILITY_TEMPLATES),
                ("decision", DECISION_TEMPLATES),
            ]
            conditions = [
                ("core", s.packed_text, p.unpacked_text),
                ("paraphrase", s.packed_text, s.packed_paraphrase),
                ("partial_subset", s.packed_text, partial_text(p.branches)),
            ]
            if p.repacked_text:
                conditions.append(("repacked", s.packed_text, p.repacked_text))

            for readout, templates in readouts:
                for template_id, instruction in enumerate(templates):
                    for condition, left, right in conditions:
                        for order_id, mapping in enumerate(LABEL_ORDERS):
                            prompt = comparison_prompt(left, right, instruction, mapping)
                            requests.append((prompt, ("A", "B", "C")))
                            meta.append({
                                "kind": "judgment", "scenario_id": s.scenario_id, "domain": s.domain,
                                "partition_id": p.partition_id, "branch_count": p.branch_count,
                                "readout": readout, "template_id": template_id,
                                "condition": condition, "label_order": order_id,
                                "mapping": mapping,
                            })

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows: list[dict[str, Any]] = []
    for m, score in zip(meta, scores):
        row = dict(m)
        row["model"] = model_name
        row["family"] = family
        row["revision"] = revision
        row["label_probs"] = score.probs
        if m["kind"] == "recognition":
            row["p_correct"] = score.probs[m["yes_label"]]
        else:
            row.update({f"p_{k}": v for k, v in _semantic_probs(score.probs, m["mapping"]).items()})
        rows.append(row)
    _write_jsonl(out_path, rows)
