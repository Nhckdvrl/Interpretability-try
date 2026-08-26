from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .dataset import load_scenarios
from .prompts import COMPREHENSION_TEMPLATES, JUDGMENT_TEMPLATES, build_comprehension_prompt, build_judgment_prompt
from .scoring import HFChoiceScorer


def run_g0(
    *,
    model_name: str,
    data_path: str | Path,
    out_path: str | Path,
    limit: int | None = None,
    sequence_batch_size: int = 96,
    dtype: str = "auto",
) -> None:
    scenarios = load_scenarios(data_path, strict=limit is None)
    if limit is not None:
        if limit <= 0:
            raise ValueError("--limit must be positive")
        scenarios = scenarios[:limit]

    scorer = HFChoiceScorer(model_name=model_name, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []
    metadata: list[dict[str, Any]] = []

    for scenario in scenarios:
        for mode in ("direct", "inference"):
            for template_id in range(len(COMPREHENSION_TEMPLATES)):
                requests.append((build_comprehension_prompt(scenario, mode, template_id), ("Yes", "No")))
                metadata.append({
                    "kind": "comprehension",
                    "scenario_id": scenario.scenario_id,
                    "family": scenario.family,
                    "mode": mode,
                    "template_id": template_id,
                })
            for template_id in range(len(JUDGMENT_TEMPLATES)):
                for label_order in (0, 1):
                    prompt, target_label = build_judgment_prompt(scenario, mode, template_id, label_order)
                    requests.append((prompt, ("A", "B")))
                    metadata.append({
                        "kind": "judgment",
                        "scenario_id": scenario.scenario_id,
                        "family": scenario.family,
                        "mode": mode,
                        "template_id": template_id,
                        "label_order": label_order,
                        "target_label": target_label,
                    })

    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for meta, score in zip(metadata, scores, strict=True):
            row = {**meta, "model": model_name, "probs": score.probs, "logprobs": score.logprobs}
            if meta["kind"] == "comprehension":
                row["p_yes"] = score.probs["Yes"]
                row["pred"] = max(score.probs, key=score.probs.get)
            else:
                row["p_target"] = score.probs[meta["target_label"]]
                row["pred"] = max(score.probs, key=score.probs.get)
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
