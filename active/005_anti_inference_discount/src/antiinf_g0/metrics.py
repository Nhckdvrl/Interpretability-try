from __future__ import annotations

from collections import defaultdict
import json
import math
from pathlib import Path
import random
from statistics import mean
from typing import Any

from .dataset import FAMILIES, load_scenarios
from .prompts import COMPREHENSION_TEMPLATES, JUDGMENT_TEMPLATES


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
    return draws[int(0.025 * (n_boot - 1))], draws[int(0.975 * (n_boot - 1))]


def _aggregate(results: list[dict[str, Any]], scenario_ids: set[str]) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[Any, ...]] = set()
    for row in results:
        sid = str(row["scenario_id"])
        if sid not in scenario_ids:
            raise ValueError(f"unknown scenario_id={sid}")
        kind = row["kind"]
        mode = row["mode"]
        if mode not in ("direct", "inference"):
            raise ValueError(f"unknown mode={mode!r}")
        if kind == "comprehension":
            key = (sid, kind, mode, int(row["template_id"]))
        elif kind == "judgment":
            key = (sid, kind, mode, int(row["template_id"]), int(row["label_order"]))
        else:
            raise ValueError(f"unknown kind={kind!r}")
        if key in seen:
            raise ValueError(f"duplicate result variant {key}")
        seen.add(key)
        grouped[sid].append(row)

    missing = scenario_ids - set(grouped)
    if missing:
        raise ValueError(f"missing results for {len(missing)} scenarios; first={sorted(missing)[:5]}")

    out: dict[str, dict[str, Any]] = {}
    expected_comp = len(COMPREHENSION_TEMPLATES)
    expected_judg = len(JUDGMENT_TEMPLATES) * 2
    for sid, rows in grouped.items():
        families = {r["family"] for r in rows}
        if len(families) != 1:
            raise ValueError(f"inconsistent family for {sid}")
        summary: dict[str, Any] = {"scenario_id": sid, "family": rows[0]["family"]}
        for mode in ("direct", "inference"):
            comp = [r for r in rows if r["kind"] == "comprehension" and r["mode"] == mode]
            judg = [r for r in rows if r["kind"] == "judgment" and r["mode"] == mode]
            if len(comp) != expected_comp:
                raise ValueError(f"{sid}/{mode}: expected {expected_comp} comprehension variants, found {len(comp)}")
            if len(judg) != expected_judg:
                raise ValueError(f"{sid}/{mode}: expected {expected_judg} judgment variants, found {len(judg)}")
            summary[f"p_yes_{mode}"] = mean(float(r["p_yes"]) for r in comp)
            summary[f"p_target_{mode}"] = mean(float(r["p_target"]) for r in judg)
        out[sid] = summary
    return out


def summarize(*, data_path: str | Path, results_path: str | Path, config_path: str | Path, out_path: str | Path | None = None) -> dict[str, Any]:
    scenarios = load_scenarios(data_path, strict=True)
    by_id = {s.scenario_id: s for s in scenarios}
    stats = _aggregate(_read_jsonl(results_path), set(by_id))
    cfg = json.loads(Path(config_path).read_text(encoding="utf-8"))
    gate_cfg = cfg["comprehension_gate"]
    strong_cfg = cfg["strong_scenario"]
    pass_cfg = cfg["model_pass"]

    rows = []
    for sid in sorted(stats):
        s = stats[sid]
        gap = abs(s["p_yes_direct"] - s["p_yes_inference"])
        gated = s["p_yes_direct"] >= gate_cfg["p_yes_direct_min"] and s["p_yes_inference"] >= gate_cfg["p_yes_inference_min"] and gap <= gate_cfg["max_abs_gap"]
        discount = s["p_target_direct"] - s["p_target_inference"]
        strong = gated and s["p_target_direct"] >= strong_cfg["p_target_direct_min"] and discount >= strong_cfg["judgment_discount_min"]
        rows.append({**s, "comprehension_gap": gap, "gated": gated, "judgment_discount": discount, "strong": strong})

    gated_rows = [r for r in rows if r["gated"]]
    discounts = [r["judgment_discount"] for r in gated_rows]
    ci_lo, ci_hi = _bootstrap_ci(discounts)
    by_family = {}
    for family in FAMILIES:
        subset = [r for r in gated_rows if r["family"] == family]
        by_family[family] = {
            "gated": len(subset),
            "mean_discount": mean(r["judgment_discount"] for r in subset) if subset else math.nan,
            "strong": sum(bool(r["strong"]) for r in subset),
        }

    aggregate = {
        "total_scenarios": len(rows),
        "gated_scenarios": len(gated_rows),
        "mean_judgment_discount": mean(discounts) if discounts else math.nan,
        "bootstrap_95_ci": [ci_lo, ci_hi],
        "positive_families": sum(bool(by_family[f]["gated"]) and by_family[f]["mean_discount"] > 0 for f in FAMILIES),
        "strong_scenarios": sum(bool(r["strong"]) for r in gated_rows),
        "positive_discount_fraction": (sum(r["judgment_discount"] > 0 for r in gated_rows) / len(gated_rows)) if gated_rows else 0.0,
    }
    model_pass = (
        aggregate["gated_scenarios"] >= pass_cfg["gated_scenarios_min"]
        and aggregate["mean_judgment_discount"] >= pass_cfg["mean_judgment_discount_min"]
        and ci_lo > pass_cfg["bootstrap_ci_lower_min"]
        and aggregate["positive_families"] >= pass_cfg["positive_families_min"]
        and aggregate["strong_scenarios"] >= pass_cfg["strong_scenarios_min"]
        and aggregate["positive_discount_fraction"] >= pass_cfg["positive_discount_fraction_min"]
    )
    summary = {"model_pass": model_pass, "aggregate": aggregate, "by_family": by_family, "scenarios": rows}
    if out_path is not None:
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    return summary
