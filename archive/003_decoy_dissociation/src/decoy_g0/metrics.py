from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, asdict
from statistics import mean

@dataclass(frozen=True)
class G0Thresholds:
    dominance_prob: float = 0.80
    max_decoy_prob: float = 0.10
    binary_competitor_prob: float = 0.60
    ternary_target_ab_prob: float = 0.60
    min_stable_fraction: float = 2 / 3

@dataclass(frozen=True)
class ScenarioVerdict:
    scenario_id: str
    domain: str
    target: str
    dominance_pass: bool
    decoy_pass: bool
    binary_competitor_mean: float
    ternary_target_ab_mean: float
    attraction_delta: float
    reversal_fraction: float
    strong_reversal: bool


def _semantic_prob(row: dict, semantic: str) -> float:
    return sum(float(row["probs"].get(label, 0.0)) for label, sem in row["semantic_by_label"].items() if sem == semantic)


def summarize_scenarios(rows: list[dict], scenario_meta: dict[str, dict], th: G0Thresholds) -> list[ScenarioVerdict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        grouped[r["scenario_id"]].append(r)
    out: list[ScenarioVerdict] = []
    for sid, rs in grouped.items():
        meta = scenario_meta[sid]
        target = meta["target"]
        competitor = "B" if target == "A" else "A"
        dom = [r for r in rs if r["kind"] == "dominance"]
        binary = [r for r in rs if r["kind"] == "binary"]
        ternary = [r for r in rs if r["kind"] == "ternary"]
        if not dom or not binary or not ternary:
            continue
        dom_probs = [_semantic_prob(r, "target") for r in dom]
        decoy_probs = [_semantic_prob(r, "C") for r in ternary]
        binary_comp = [_semantic_prob(r, competitor) for r in binary]
        binary_target = [_semantic_prob(r, target) for r in binary]
        ternary_target_ab = []
        for r in ternary:
            pt, pc = _semantic_prob(r, target), _semantic_prob(r, competitor)
            ternary_target_ab.append(pt / (pt + pc) if pt + pc > 0 else 0.5)
        binary_frac = sum(p >= th.binary_competitor_prob for p in binary_comp) / len(binary_comp)
        ternary_frac = sum(p >= th.ternary_target_ab_prob for p in ternary_target_ab) / len(ternary_target_ab)
        reversal_fraction = min(binary_frac, ternary_frac)
        dominance_pass = min(dom_probs) >= th.dominance_prob
        decoy_pass = max(decoy_probs) <= th.max_decoy_prob
        out.append(ScenarioVerdict(
            sid, meta["domain"], target, dominance_pass, decoy_pass,
            mean(binary_comp), mean(ternary_target_ab),
            mean(ternary_target_ab) - mean(binary_target), reversal_fraction,
            dominance_pass and decoy_pass and reversal_fraction >= th.min_stable_fraction,
        ))
    return out


def aggregate(verdicts: list[ScenarioVerdict]) -> dict:
    if not verdicts:
        return {"n": 0}
    by_domain: dict[str, list[ScenarioVerdict]] = defaultdict(list)
    for v in verdicts:
        by_domain[v.domain].append(v)
    def pack(xs: list[ScenarioVerdict]) -> dict:
        gated = [v for v in xs if v.dominance_pass and v.decoy_pass]
        strong = [v for v in gated if v.strong_reversal]
        return {
            "n_total": len(xs), "n_gated": len(gated), "n_strong_reversal": len(strong),
            "strong_reversal_rate_among_gated": len(strong) / len(gated) if gated else 0.0,
            "mean_attraction_delta_gated": mean(v.attraction_delta for v in gated) if gated else 0.0,
        }
    return {"overall": pack(verdicts), "by_domain": {k: pack(v) for k, v in sorted(by_domain.items())}}


def verdicts_to_dicts(verdicts: list[ScenarioVerdict]) -> list[dict]:
    return [asdict(v) for v in verdicts]
