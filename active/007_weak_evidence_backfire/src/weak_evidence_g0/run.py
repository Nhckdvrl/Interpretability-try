from __future__ import annotations

from pathlib import Path
import json

from .data import load_scenarios
from .prompts import (
    CHOICE_ORDERS,
    CONDITIONS,
    DIRECTIONS,
    READOUT_TEMPLATES,
    YES_NO_ORDERS,
    base_text,
    condition_text,
    evidence_for,
    readout_prompt,
    support_prompt,
)
from .scoring import HFChoiceScorer

SUPPORT_PROBES = (
    "support",
    "likelihood_relation",
    "support_complete",
    "strong_support",
    "strong_gt_weak",
    "neutral_non_support",
)


def _require_authorized(config_path: str) -> dict:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if cfg.get("validation_authorized") is not True:
        raise PermissionError(
            "Formal model calls are not authorized; independent N0 + D0 must sign the authoritative registry first."
        )
    return cfg


def _write(path: str, rows: list[dict]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(*, data_path: str, out_path: str, config_path: str, model_name: str, family: str,
        revision: str | None = None, dtype: str = "auto", size_b: float | None = None,
        sequence_batch_size: int = 64) -> None:
    _require_authorized(config_path)
    if size_b is None or size_b <= 0:
        raise ValueError("size_b must be explicitly provided and > 0")
    scenarios = load_scenarios(data_path, require_external_source=True)
    scorer = HFChoiceScorer(model_name, revision=revision, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []
    metadata: list[dict] = []

    for scenario in scenarios:
        base = base_text(scenario.background, scenario.calibration_text)
        for direction in DIRECTIONS:
            focal = scenario.target_hypothesis if direction == "supports_target" else scenario.other_hypothesis
            other = scenario.other_hypothesis if direction == "supports_target" else scenario.target_hypothesis
            weak = evidence_for(scenario, direction, "weak")
            strong = evidence_for(scenario, direction, "strong")
            for probe in SUPPORT_PROBES:
                for order_id, mapping in enumerate(YES_NO_ORDERS):
                    prompt, correct = support_prompt(
                        base=base,
                        weak_evidence=weak,
                        strong_evidence=strong,
                        neutral_evidence=scenario.neutral_evidence,
                        focal_hypothesis=focal,
                        other_hypothesis=other,
                        probe=probe,
                        mapping=mapping,
                        pragmatic_text=scenario.pragmatic_completeness_text,
                    )
                    requests.append((prompt, ("A", "B")))
                    metadata.append({
                        "kind": "support_probe",
                        "scenario_id": scenario.scenario_id,
                        "domain": scenario.domain,
                        "direction": direction,
                        "probe": probe,
                        "label_order": order_id,
                        "correct_label": correct,
                    })

            for template_id, (kind, template) in enumerate(READOUT_TEMPLATES):
                target_text = scenario.target_hypothesis if kind == "belief" else scenario.target_action
                other_text = scenario.other_hypothesis if kind == "belief" else scenario.other_action
                for condition in CONDITIONS:
                    context = condition_text(scenario, direction=direction, condition=condition)
                    for order_id, mapping in enumerate(CHOICE_ORDERS):
                        prompt, target_label = readout_prompt(
                            context=context,
                            target_text=target_text,
                            other_text=other_text,
                            template=template,
                            mapping=mapping,
                        )
                        requests.append((prompt, ("A", "B")))
                        metadata.append({
                            "kind": "readout",
                            "scenario_id": scenario.scenario_id,
                            "domain": scenario.domain,
                            "direction": direction,
                            "condition": condition,
                            "template_id": template_id,
                            "template_kind": kind,
                            "label_order": order_id,
                            "target_label": target_label,
                        })

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows: list[dict] = []
    for meta, score in zip(metadata, scores):
        row = dict(meta)
        row.update({
            "model": model_name,
            "family": family,
            "revision": revision,
            "size_b": size_b,
            "requested_dtype": dtype,
            "label_probs": score.probs,
            "label_logprobs": score.logprobs,
        })
        if meta["kind"] == "support_probe":
            row["p_correct"] = score.probs[meta["correct_label"]]
        else:
            row["p_target"] = score.probs[meta["target_label"]]
        rows.append(row)
    _write(out_path, rows)
