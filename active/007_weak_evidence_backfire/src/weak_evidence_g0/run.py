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
    calibrated_context,
    natural_base_context,
    choice_prompt,
    condition_context,
    evidence_for_direction,
    support_prompt,
)
from .scoring import HFChoiceScorer

SUPPORT_PROBES = ("support", "likelihood_relation", "support_complete")


def _require_authorized(config_path: str) -> dict:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if cfg.get("validation_authorized") is not True:
        raise PermissionError(
            "Formal model calls are not authorized by this frozen config. "
            "Do not bypass the N0/D0 gate; update authorization only after the authoritative registry is signed."
        )
    return cfg


def _write_jsonl(path: str, rows: list[dict]) -> None:
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
        natural_base = natural_base_context(scenario.background)
        calibrated_base = calibrated_context(scenario.background, scenario.calibration_text)
        for direction in DIRECTIONS:
            weak, strong = evidence_for_direction(
                direction=direction,
                weak_target=scenario.weak_target_evidence,
                weak_other=scenario.weak_other_evidence,
                strong_target=scenario.strong_target_evidence,
                strong_other=scenario.strong_other_evidence,
            )
            focal = scenario.target_hypothesis if direction == "supports_target" else scenario.other_hypothesis
            alternative = scenario.other_hypothesis if direction == "supports_target" else scenario.target_hypothesis
            for probe in SUPPORT_PROBES:
                for order_id, mapping in enumerate(YES_NO_ORDERS):
                    prompt, correct_label = support_prompt(
                        base=calibrated_base if probe == "likelihood_relation" else natural_base,
                        evidence=weak,
                        focal_hypothesis=focal,
                        other_hypothesis=alternative,
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
                        "correct_label": correct_label,
                    })

            contexts = {
                condition: condition_context(
                    base=natural_base,
                    weak_evidence=weak,
                    strong_evidence=strong,
                    neutral_evidence=scenario.neutral_evidence,
                    pragmatic_text=scenario.pragmatic_completeness_text,
                    length_control_text=scenario.matched_length_control_text,
                    condition=condition,
                )
                for condition in CONDITIONS
            }
            for template_id, (template_kind, template) in enumerate(READOUT_TEMPLATES):
                for condition, context in contexts.items():
                    for order_id, mapping in enumerate(CHOICE_ORDERS):
                        prompt, target_label = choice_prompt(
                            context=context,
                            target_hypothesis=scenario.target_hypothesis,
                            other_hypothesis=scenario.other_hypothesis,
                            target_action=scenario.target_action,
                            other_action=scenario.other_action,
                            template_kind=template_kind,
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
                            "template_kind": template_kind,
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
    _write_jsonl(out_path, rows)
