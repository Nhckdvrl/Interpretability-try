from __future__ import annotations
from pathlib import Path
from typing import Any
import json

from .data import load_scenarios
from .prompts import (
    RECOGNITION_ORDERS,
    PROBABILITY_TEMPLATES,
    DECISION_TEMPLATES,
    recognition_prompt,
    threshold_prompt,
)
from .scoring import HFChoiceScorer

def _write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def run(*, data_path: str, config_path: str, out_path: str, model_name: str, family: str,
        size_b: float, revision: str | None = None, dtype: str = "auto",
        sequence_batch_size: int = 64) -> None:
    scenarios = load_scenarios(data_path, require_external_source=True)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    prob_thresholds = [float(x) for x in cfg["readout"]["probability_thresholds"]]
    decision_thresholds = [float(x) for x in cfg["readout"]["decision_thresholds"]]
    scorer = HFChoiceScorer(model_name, revision=revision, dtype=dtype)

    requests: list[tuple[str, tuple[str, ...]]] = []
    meta: list[dict[str, Any]] = []

    for s in scenarios:
        for p in s.partitions:
            for probe in ("equivalent", "disjoint", "exhaustive", "partial_strict_subset"):
                for order_id, mapping in enumerate(RECOGNITION_ORDERS):
                    prompt, correct = recognition_prompt(
                        s.packed_text, p.branches, probe, mapping,
                        partial_text=p.partial_unpacked_text,
                    )
                    requests.append((prompt, ("A", "B")))
                    meta.append({
                        "kind": "recognition", "scenario_id": s.scenario_id, "domain": s.domain,
                        "partition_id": p.partition_id, "branch_count": p.branch_count,
                        "scope": "focal", "probe": probe, "label_order": order_id,
                        "correct_label": correct,
                    })

            if p.alternative_packed_text is not None:
                for probe in ("equivalent", "disjoint", "exhaustive"):
                    for order_id, mapping in enumerate(RECOGNITION_ORDERS):
                        prompt, correct = recognition_prompt(
                            p.alternative_packed_text, p.alternative_branches, probe, mapping
                        )
                        requests.append((prompt, ("A", "B")))
                        meta.append({
                            "kind": "recognition", "scenario_id": s.scenario_id, "domain": s.domain,
                            "partition_id": p.partition_id, "branch_count": p.branch_count,
                            "scope": "alternative", "probe": probe, "label_order": order_id,
                            "correct_label": correct,
                        })

            conditions: list[tuple[str, str, str | None]] = [
                ("packed", s.packed_text, None),
                ("core_unpacked", p.unpacked_text, None),
                ("paraphrase", s.packed_paraphrase, None),
                ("partial_subset", p.partial_unpacked_text, None),
            ]
            if p.repacked_text is not None:
                conditions.append(("repacked", p.repacked_text, None))
            if p.alternative_packed_text is not None:
                conditions.extend([
                    ("alt_frame_packed", s.packed_text, p.alternative_packed_text),
                    ("alt_frame_unpacked", s.packed_text, p.alternative_unpacked_text),
                ])

            for readout, templates, thresholds in (
                ("probability", PROBABILITY_TEMPLATES, prob_thresholds),
                ("decision", DECISION_TEMPLATES, decision_thresholds),
            ):
                for template_id, template in enumerate(templates):
                    for condition, event_text, alternative_text in conditions:
                        for threshold in thresholds:
                            for order_id, mapping in enumerate(RECOGNITION_ORDERS):
                                prompt, correct = threshold_prompt(
                                    s.information_context, event_text, readout, threshold,
                                    template, mapping, alternative_text=alternative_text,
                                )
                                requests.append((prompt, ("A", "B")))
                                meta.append({
                                    "kind": "readout", "scenario_id": s.scenario_id,
                                    "domain": s.domain, "partition_id": p.partition_id,
                                    "branch_count": p.branch_count, "readout": readout,
                                    "template_id": template_id, "condition": condition,
                                    "threshold": threshold, "label_order": order_id,
                                    "yes_label": correct,
                                })

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows: list[dict[str, Any]] = []
    for m, score in zip(meta, scores):
        row = dict(m)
        row["model"] = model_name
        row["family"] = family
        row["size_b"] = float(size_b)
        row["revision"] = revision
        row["label_probs"] = score.probs
        if m["kind"] == "recognition":
            row["p_correct"] = score.probs[m["correct_label"]]
        else:
            row["p_yes"] = score.probs[m["yes_label"]]
        rows.append(row)
    _write_jsonl(out_path, rows)
