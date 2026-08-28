from __future__ import annotations

from pathlib import Path
import json

from .data import load_scenarios
from .prompts import (
    CHOICE_ORDERS, CONDITIONS, DELAYS, DIRECTIONS, MEMORY_PROBES, READOUT_TEMPLATES,
    SOURCE_ORDERS, SOURCES, SUPPORT_PROBES, YES_NO_ORDERS,
    memory_prompt, readout_prompt, support_prompt,
)
from .scoring import HFChoiceScorer


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
    meta: list[dict] = []

    for s in scenarios:
        for direction in DIRECTIONS:
            for probe in SUPPORT_PROBES:
                for order_id, mapping in enumerate(YES_NO_ORDERS):
                    prompt, correct = support_prompt(s, direction=direction, probe=probe, mapping=mapping)
                    requests.append((prompt, ("A", "B")))
                    meta.append({"kind": "support_probe", "scenario_id": s.scenario_id,
                                 "domain": s.domain, "direction": direction, "probe": probe,
                                 "label_order": order_id, "correct_label": correct})

            for source in SOURCES:
                for delay in ("short", "long"):
                    for probe in MEMORY_PROBES:
                        orders = SOURCE_ORDERS if probe == "source_identity" else CHOICE_ORDERS if probe == "message_direction" else YES_NO_ORDERS
                        for order_id, mapping in enumerate(orders):
                            prompt, correct = memory_prompt(
                                s, direction=direction, source=source, delay=delay,
                                probe=probe, order=mapping,
                            )
                            requests.append((prompt, ("A", "B")))
                            meta.append({"kind": "memory_probe", "scenario_id": s.scenario_id,
                                         "domain": s.domain, "direction": direction, "source": source,
                                         "delay": delay, "probe": probe, "label_order": order_id,
                                         "correct_label": correct})

            for template_id, (kind, template) in enumerate(READOUT_TEMPLATES):
                for condition in CONDITIONS:
                    for order_id, mapping in enumerate(CHOICE_ORDERS):
                        prompt, target_label = readout_prompt(
                            s, direction=direction, condition=condition, template=template,
                            kind=kind, mapping=mapping,
                        )
                        requests.append((prompt, ("A", "B")))
                        meta.append({"kind": "readout", "scenario_id": s.scenario_id,
                                     "domain": s.domain, "direction": direction,
                                     "condition": condition, "template_id": template_id,
                                     "template_kind": kind, "label_order": order_id,
                                     "target_label": target_label})

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows: list[dict] = []
    for m, score in zip(meta, scores):
        row = dict(m)
        row.update({"model": model_name, "family": family, "revision": revision,
                    "size_b": size_b, "requested_dtype": dtype,
                    "label_probs": score.probs, "label_logprobs": score.logprobs})
        if m["kind"] in {"support_probe", "memory_probe"}:
            row["p_correct"] = score.probs[m["correct_label"]]
        else:
            row["p_target"] = score.probs[m["target_label"]]
        rows.append(row)
    _write(out_path, rows)
