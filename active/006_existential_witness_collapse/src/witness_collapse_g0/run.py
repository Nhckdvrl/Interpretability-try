from __future__ import annotations

from pathlib import Path
import json

from .data import load_scenarios
from .prompts import (
    CONDITIONS,
    DOWNSTREAM_TEMPLATES,
    OUTCOME_ORDERS,
    YES_NO_ORDERS,
    condition_text,
    downstream_prompt,
    recognition_prompt,
)
from .scoring import HFChoiceScorer

RECOGNITION_PROBES = ("p_exists", "q_exists", "shared_entailment", "identity_determined")


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
        for probe in RECOGNITION_PROBES:
            for order_id, mapping in enumerate(YES_NO_ORDERS):
                prompt, correct_label = recognition_prompt(
                    premise_p=scenario.premise_p,
                    premise_q=scenario.premise_q,
                    p_property=scenario.p_property,
                    q_property=scenario.q_property,
                    probe=probe,
                    mapping=mapping,
                )
                requests.append((prompt, ("A", "B")))
                metadata.append({
                    "kind": "recognition",
                    "scenario_id": scenario.scenario_id,
                    "domain": scenario.domain,
                    "probe": probe,
                    "label_order": order_id,
                    "correct_label": correct_label,
                })

        contexts = {
            condition: condition_text(
                premise_p=scenario.premise_p,
                premise_q=scenario.premise_q,
                premise_paraphrase=scenario.premise_paraphrase,
                same_addendum=scenario.same_witness_addendum,
                distinct_addendum=scenario.distinct_witness_addendum,
                neutral_addendum=scenario.neutral_addendum,
                condition=condition,
            )
            for condition in CONDITIONS
        }
        for template_id, template in enumerate(DOWNSTREAM_TEMPLATES):
            for condition, context in contexts.items():
                for order_id, mapping in enumerate(OUTCOME_ORDERS):
                    prompt, established_label = downstream_prompt(
                        context=context,
                        requirement=scenario.shared_requirement,
                        decision_context=scenario.decision_context,
                        template=template,
                        mapping=mapping,
                    )
                    requests.append((prompt, ("A", "B")))
                    metadata.append({
                        "kind": "downstream",
                        "scenario_id": scenario.scenario_id,
                        "domain": scenario.domain,
                        "condition": condition,
                        "template_id": template_id,
                        "label_order": order_id,
                        "established_label": established_label,
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
        if meta["kind"] == "recognition":
            row["p_correct"] = score.probs[meta["correct_label"]]
        else:
            row["p_established"] = score.probs[meta["established_label"]]
        rows.append(row)
    _write_jsonl(out_path, rows)
