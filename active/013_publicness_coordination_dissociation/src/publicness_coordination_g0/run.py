from __future__ import annotations

from pathlib import Path
import json

from .data import load_scenarios
from .prompts import ACTION_ORDERS, ACTION_TEMPLATES, CAPABILITY_PROBES, PARTICIPANTS, VERSIONS, YES_NO_ORDERS, action_prompt, capability_prompt
from .scoring import HFChoiceScorer


def _require_authorized(config_path: str) -> dict:
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    if cfg.get("validation_authorized") is not True:
        raise PermissionError(
            "Formal model calls are not authorized; independent N0 + D0 must sign the authoritative registry first."
        )
    return cfg


def _write(path: str, rows: list[dict]) -> None:
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run(*, data_path: str, out_path: str, config_path: str, model_name: str, family: str,
        revision: str | None = None, dtype: str = "auto", size_b: float | None = None,
        sequence_batch_size: int = 64) -> None:
    _require_authorized(config_path)
    if size_b is None or size_b <= 0:
        raise ValueError("size_b must be explicitly provided and > 0")
    scenarios = load_scenarios(data_path, require_external_source=True)
    scorer = HFChoiceScorer(model_name, revision=revision, dtype=dtype)
    requests = []; meta = []
    for s in scenarios:
        for who in PARTICIPANTS:
            for state in ("private", "public"):
                for probe in CAPABILITY_PROBES:
                    for order_id, mapping in enumerate(YES_NO_ORDERS):
                        prompt, correct = capability_prompt(s, who=who, state=state, probe=probe, mapping=mapping)
                        requests.append((prompt, ("A", "B")))
                        meta.append({"kind": "capability_probe", "scenario_id": s.scenario_id, "domain": s.domain,
                                     "participant": who, "state": state, "probe": probe, "label_order": order_id,
                                     "correct_label": correct})
            for version in VERSIONS:
                for state in ("private", "public", "explicit_ck"):
                    for template_id, template in enumerate(ACTION_TEMPLATES):
                        for order_id, mapping in enumerate(ACTION_ORDERS):
                            prompt, coordinate_label = action_prompt(s, who=who, state=state, version=version,
                                                                     template=template, mapping=mapping)
                            requests.append((prompt, ("A", "B")))
                            meta.append({"kind": "action_readout", "scenario_id": s.scenario_id, "domain": s.domain,
                                         "participant": who, "state": state, "version": version,
                                         "template_id": template_id, "label_order": order_id,
                                         "coordinate_label": coordinate_label})
    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    rows = []
    for m, score in zip(meta, scores):
        row = dict(m)
        row.update({"model": model_name, "family": family, "revision": revision, "size_b": size_b,
                    "requested_dtype": dtype, "label_probs": score.probs, "label_logprobs": score.logprobs})
        if m["kind"] == "capability_probe": row["p_correct"] = score.probs[m["correct_label"]]
        else: row["p_coordinate"] = score.probs[m["coordinate_label"]]
        rows.append(row)
    _write(out_path, rows)
