from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .dataset import CARD_PERMUTATIONS, load_items, permute_item
from .prompts import CANDIDATES, TEMPLATES, build_prompt
from .scoring import HFChoiceScorer


def run_g0(*, model_name: str, data_path: str | Path, out_path: str | Path, limit: int | None = None, sequence_batch_size: int = 96, dtype: str = "auto") -> None:
    items = load_items(data_path, strict=limit is None)
    if limit is not None:
        if limit <= 0:
            raise ValueError("--limit must be positive")
        items = items[:limit]
    scorer = HFChoiceScorer(model_name=model_name, dtype=dtype)
    requests: list[tuple[str, tuple[str, ...]]] = []
    metadata: list[dict[str, Any]] = []
    for item in items:
        for perm_id, perm in enumerate(CARD_PERMUTATIONS):
            shown = permute_item(item, perm)
            for template_id in range(len(TEMPLATES)):
                requests.append((build_prompt(shown, template_id), CANDIDATES))
                metadata.append({"pair_id": item.pair_id, "frame_id": item.frame_id, "modal": item.modal, "form": item.form, "perm_id": perm_id, "permutation": list(perm), "template_id": template_id, "gold": shown.gold_label})
    scores = scorer.score_batch(requests, sequence_batch_size=sequence_batch_size)
    out = Path(out_path); out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for meta, score in zip(metadata, scores, strict=True):
            pred = max(score.probs, key=score.probs.get)
            f.write(json.dumps({**meta, "model": model_name, "pred": pred, "correct": pred == meta["gold"], "p_gold": score.probs[meta["gold"]], "probs": score.probs, "logprobs": score.logprobs}, ensure_ascii=False) + "\n")
