from __future__ import annotations

from collections import defaultdict
import json
import math
from pathlib import Path
import random
from statistics import mean
from typing import Any, Iterable

from .dataset import CARD_PERMUTATIONS, FORMS, load_wason, pair_official_items
from .prompts import TEMPLATES


def _read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows = []
    with Path(path).open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                raise ValueError(f"invalid JSONL line {lineno}") from e
    return rows


def _bootstrap_ci(values: list[float], seed: int = 0, n_boot: int = 5000) -> tuple[float, float]:
    if not values:
        return (math.nan, math.nan)
    rng = random.Random(seed)
    n = len(values)
    draws = sorted(mean(values[rng.randrange(n)] for _ in range(n)) for _ in range(n_boot))
    lo = draws[int(0.025 * (n_boot - 1))]
    hi = draws[int(0.975 * (n_boot - 1))]
    return lo, hi


def _aggregate_items(result_rows: Iterable[dict[str, Any]], expected_item_ids: set[int]) -> dict[int, dict[str, Any]]:
    grouped: dict[int, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[int, int, int]] = set()
    for row in result_rows:
        item_id = int(row["item_id"])
        if item_id not in expected_item_ids:
            raise ValueError(f"unknown result item_id={item_id}")
        key = (item_id, int(row["perm_id"]), int(row["template_id"]))
        if key in seen:
            raise ValueError(f"duplicate result variant {key}")
        seen.add(key)
        grouped[item_id].append(row)

    missing = expected_item_ids - set(grouped)
    if missing:
        raise ValueError(f"missing results for {len(missing)} items; first={sorted(missing)[:5]}")

    expected_variants = len(CARD_PERMUTATIONS) * len(TEMPLATES)
    out: dict[int, dict[str, Any]] = {}
    for item_id, rows in grouped.items():
        if len(rows) != expected_variants:
            raise ValueError(f"item {item_id}: expected {expected_variants} variants, found {len(rows)}")
        if len({r["modal"] for r in rows}) != 1 or len({r["form"] for r in rows}) != 1:
            raise ValueError(f"inconsistent metadata for item {item_id}")
        out[item_id] = {
            "item_id": item_id,
            "modal": rows[0]["modal"],
            "form": rows[0]["form"],
            "accuracy": mean(float(bool(r["correct"])) for r in rows),
            "p_gold": mean(float(r["p_gold"]) for r in rows),
        }
    return out


def summarize(*, data_path: str | Path, results_path: str | Path, config_path: str | Path, out_path: str | Path | None = None) -> dict[str, Any]:
    items = load_wason(data_path, strict_official=True)
    item_stats = _aggregate_items(_read_jsonl(results_path), {x.item_id for x in items})
    pairs = pair_official_items(items)
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    strong_cfg = cfg["strong_pair"]
    pass_cfg = cfg["model_pass"]

    paired_rows = []
    for pair in pairs:
        e = item_stats[pair.epistemic.item_id]
        d = item_stats[pair.deontic.item_id]
        delta_acc = d["accuracy"] - e["accuracy"]
        delta_p = d["p_gold"] - e["p_gold"]
        strong = d["accuracy"] >= strong_cfg["deontic_accuracy_min"] and e["accuracy"] <= strong_cfg["epistemic_accuracy_max"] and delta_p >= strong_cfg["delta_p_gold_min"]
        paired_rows.append({
            "pair_key": pair.pair_key,
            "form": pair.form,
            "epistemic_id": pair.epistemic.item_id,
            "deontic_id": pair.deontic.item_id,
            "epistemic_accuracy": e["accuracy"],
            "deontic_accuracy": d["accuracy"],
            "delta_accuracy": delta_acc,
            "epistemic_p_gold": e["p_gold"],
            "deontic_p_gold": d["p_gold"],
            "delta_p_gold": delta_p,
            "strong": strong,
        })

    delta_ps = [x["delta_p_gold"] for x in paired_rows]
    ci_lo, ci_hi = _bootstrap_ci(delta_ps)
    by_form = {}
    for form in FORMS:
        subset = [x for x in paired_rows if x["form"] == form]
        by_form[form] = {
            "n_pairs": len(subset),
            "mean_delta_accuracy": mean(x["delta_accuracy"] for x in subset),
            "mean_delta_p_gold": mean(x["delta_p_gold"] for x in subset),
            "strong_pairs": sum(bool(x["strong"]) for x in subset),
        }

    paired = {
        "n_pairs": len(paired_rows),
        "mean_delta_accuracy": mean(x["delta_accuracy"] for x in paired_rows),
        "mean_delta_p_gold": mean(delta_ps),
        "bootstrap_95_ci_delta_p_gold": [ci_lo, ci_hi],
        "positive_forms": sum(by_form[f]["mean_delta_p_gold"] > 0 for f in FORMS),
        "strong_pairs": sum(bool(x["strong"]) for x in paired_rows),
    }
    model_pass = paired["mean_delta_accuracy"] >= pass_cfg["mean_delta_accuracy_min"] and paired["mean_delta_p_gold"] >= pass_cfg["mean_delta_p_gold_min"] and ci_lo > pass_cfg["bootstrap_ci_lower_min"] and paired["positive_forms"] >= pass_cfg["positive_forms_min"] and paired["strong_pairs"] >= pass_cfg["strong_pairs_min"]
    summary = {"model_pass": model_pass, "paired": paired, "by_form": by_form, "item_stats": [item_stats[k] for k in sorted(item_stats)], "paired_rows": paired_rows}
    if out_path is not None:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
