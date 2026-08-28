from __future__ import annotations
from pathlib import Path
from typing import Any
import json

from .data import load_scenarios
from .prompts import (
    BINARY_ORDERS, RECOGNITION_ORDERS, VERDICT_TEMPLATES,
    condition_text, verdict_prompt, recognition_prompt,
)
from .scoring import HFChoiceScorer

def _write(path: str | Path, rows: list[dict[str, Any]]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def run(*, data_path: str, out_path: str, model_name: str, family: str, size_b: float,
        revision: str | None = None, dtype: str = "auto",
        sequence_batch_size: int = 64) -> None:
    scenarios = load_scenarios(data_path, require_external_source=True)
    scorer = HFChoiceScorer(model_name, revision=revision, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []
    meta: list[dict[str, Any]] = []

    for s in scenarios:
        struck_context = condition_text(
            s.case_facts, s.evidence_text, s.struck_ruling, "struck",
            exclusion_scope=s.exclusion_scope,
        )
        for probe in ("inadmissible", "scope", "polarity"):
            for order_id, mapping in enumerate(RECOGNITION_ORDERS):
                prompt, correct = recognition_prompt(
                    struck_context, s.target_verdict, s.other_verdict,
                    probe, mapping, s.evidence_polarity,
                )
                requests.append((prompt, ("A", "B")))
                meta.append({
                    "kind": "recognition", "scenario_id": s.scenario_id, "domain": s.domain,
                    "probe": probe, "label_order": order_id, "correct_label": correct,
                    "polarity": s.evidence_polarity, "polarity_pair_id": s.polarity_pair_id,
                })

        conditions = [
            ("never_seen", condition_text(s.case_facts, s.evidence_text, None, "never_seen")),
            ("admitted", condition_text(s.case_facts, s.evidence_text, s.admissible_ruling, "admitted")),
            ("struck", struck_context),
        ]
        if s.neutral_evidence_text is not None:
            conditions.append((
                "neutral_struck",
                condition_text(
                    s.case_facts, s.neutral_evidence_text, s.neutral_struck_ruling,
                    "struck", exclusion_scope=s.exclusion_scope,
                ),
            ))

        for template_id, template in enumerate(VERDICT_TEMPLATES):
            for condition, context in conditions:
                for order_id, mapping in enumerate(BINARY_ORDERS):
                    prompt = verdict_prompt(context, s.target_verdict, s.other_verdict, template, mapping)
                    requests.append((prompt, ("A", "B")))
                    target_label = next(l for l, sem in mapping.items() if sem == "target")
                    meta.append({
                        "kind": "verdict", "scenario_id": s.scenario_id, "domain": s.domain,
                        "condition": condition, "template_id": template_id,
                        "label_order": order_id, "target_label": target_label,
                        "polarity": s.evidence_polarity, "polarity_pair_id": s.polarity_pair_id,
                    })

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows: list[dict[str, Any]] = []
    for m, sc in zip(meta, scores):
        row = dict(m)
        row["model"] = model_name
        row["family"] = family
        row["size_b"] = float(size_b)
        row["revision"] = revision
        row["label_probs"] = sc.probs
        if m["kind"] == "recognition":
            row["p_correct"] = sc.probs[m["correct_label"]]
        else:
            row["p_target"] = sc.probs[m["target_label"]]
        rows.append(row)
    _write(out_path, rows)
