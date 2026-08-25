from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd

PAIRWISE_RENAMES = {
    "prompt_template_expects_higher_entity": "prompt_expects_larger_entity",
    "llm_pairwise_response": "response",
    "llm_pairwise_perplexity": "perplexity",
    "llm_pairwise_predicted_entity": "predicted_entity",
    "entity1_llm_numerical_extraction_value_lowest_perplexity": "entity1_predicted_value",
    "entity2_llm_numerical_extraction_value_lowest_perplexity": "entity2_predicted_value",
}
POINTWISE_RENAMES = {
    "prompt_template": "prompt",
    "llm_numerical_extraction_response": "response",
    "messages": "full_response",
    "llm_numerical_extraction_perplexity": "perplexity",
    "llm_numerical_extraction_value": "predicted_value",
}

REQUIRED_PAIRWISE_COLUMNS = {
    "entity1_qid", "entity1_name", "entity1_value",
    "entity2_qid", "entity2_name", "entity2_value",
    "prompt_expects_larger_entity", "predicted_entity",
}
REQUIRED_POINTWISE_COLUMNS = {"qid", "predicted_value", "perplexity"}


@dataclass(frozen=True)
class GateConfig:
    min_total_eligible: int = 500
    min_total_strict_failures: int = 50
    min_group_failures: int = 10
    min_group_failure_rate: float = 0.02
    min_passing_groups: int = 2


@dataclass(frozen=True)
class GateResult:
    verdict: str
    reason: str
    total_eligible: int
    total_strict_failures: int
    passing_groups: int
    config: GateConfig


def _normalise_name(x: object) -> str:
    return str(x).strip().casefold()


def _check_columns(df: pd.DataFrame, required: set[str], source: Path) -> None:
    missing = sorted(required - set(df.columns))
    if missing:
        raise ValueError(f"{source}: missing required columns: {missing}")


def _load_pointwise_best(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path).rename(columns=POINTWISE_RENAMES)
    _check_columns(df, REQUIRED_POINTWISE_COLUMNS, path)
    df = df.copy()
    df["qid"] = df["qid"].astype(str)
    df["predicted_value"] = pd.to_numeric(df["predicted_value"], errors="coerce")
    df["perplexity"] = pd.to_numeric(df["perplexity"], errors="coerce")
    df = df[df["predicted_value"].notna() & df["perplexity"].notna()]
    if df.empty:
        return pd.DataFrame(columns=["qid", "predicted_value"])
    df = df.sort_values(["qid", "perplexity"], ascending=[True, True])
    return df.drop_duplicates("qid", keep="first")[["qid", "predicted_value"]]


def load_merged_dataset(pairwise_path: Path, pointwise_path: Path) -> pd.DataFrame:
    """Load one upstream pairwise CSV and merge pointwise numeric predictions.

    The merge mirrors the upstream repository's
    PointwiseResult.best_numeric_by_lowest_perplexity rule without importing
    the upstream package and its large dependency set.
    """
    pair = pd.read_csv(pairwise_path).rename(columns=PAIRWISE_RENAMES)
    _check_columns(pair, REQUIRED_PAIRWISE_COLUMNS, pairwise_path)
    pair = pair.copy()
    pair["entity1_qid"] = pair["entity1_qid"].astype(str)
    pair["entity2_qid"] = pair["entity2_qid"].astype(str)

    has_merged = {"entity1_predicted_value", "entity2_predicted_value"}.issubset(pair.columns)
    if not has_merged:
        best = _load_pointwise_best(pointwise_path)
        qid_to_pred = dict(zip(best["qid"], best["predicted_value"], strict=False))
        pair["entity1_predicted_value"] = pair["entity1_qid"].map(qid_to_pred)
        pair["entity2_predicted_value"] = pair["entity2_qid"].map(qid_to_pred)

    for col in (
        "entity1_value", "entity2_value",
        "entity1_predicted_value", "entity2_predicted_value",
        "entity1_qrank", "entity2_qrank",
        "entity1_cosine_similarity", "entity2_cosine_similarity",
    ):
        if col in pair.columns:
            pair[col] = pd.to_numeric(pair[col], errors="coerce")
    return pair


def _right_entity(df: pd.DataFrame, value1_col: str, value2_col: str) -> pd.Series:
    e1_larger = df[value1_col] > df[value2_col]
    expects_larger = df["prompt_expects_larger_entity"].astype(bool)
    entity1_is_right = e1_larger == expects_larger
    return pd.Series(
        [e1 if use_e1 else e2 for e1, e2, use_e1 in zip(
            df["entity1_name"], df["entity2_name"], entity1_is_right, strict=False
        )],
        index=df.index,
        dtype="object",
    )


def _relative_gap(a: pd.Series, b: pd.Series) -> pd.Series:
    denom = pd.concat([a.abs(), b.abs()], axis=1).max(axis=1)
    denom = denom.where(denom > 0, 1.0)
    return (a - b).abs() / denom


def classify_cases(df: pd.DataFrame) -> pd.DataFrame:
    """Classify natural facts-available-but-comparison-wrong cases.

    A strict failure requires:
      1. both pointwise numerical predictions are finite and non-tied;
      2. their implied comparison agrees with factual ground truth;
      3. pairwise output is a definite choice between the two entities;
      4. pairwise choice is nevertheless wrong.

    No synthetic perturbation is used to create failures.
    """
    out = df.copy()
    for col in ("entity1_value", "entity2_value", "entity1_predicted_value", "entity2_predicted_value"):
        if col not in out.columns:
            raise ValueError(f"missing required numeric column: {col}")

    pred_norm = out["predicted_entity"].map(_normalise_name)
    e1_norm = out["entity1_name"].map(_normalise_name)
    e2_norm = out["entity2_name"].map(_normalise_name)

    out["definite_pairwise_prediction"] = (pred_norm == e1_norm) | (pred_norm == e2_norm)
    out["gt_non_tie"] = (
        out["entity1_value"].notna() & out["entity2_value"].notna()
        & (out["entity1_value"] != out["entity2_value"])
    )
    out["numex_non_tie"] = (
        out["entity1_predicted_value"].notna() & out["entity2_predicted_value"].notna()
        & (out["entity1_predicted_value"] != out["entity2_predicted_value"])
    )
    out["eligible"] = out["definite_pairwise_prediction"] & out["gt_non_tie"] & out["numex_non_tie"]

    out["gt_right_entity"] = _right_entity(out, "entity1_value", "entity2_value")
    out["numex_right_entity"] = _right_entity(out, "entity1_predicted_value", "entity2_predicted_value")
    out["pairwise_correct"] = pred_norm == out["gt_right_entity"].map(_normalise_name)
    out["pairwise_consistent_with_numex"] = pred_norm == out["numex_right_entity"].map(_normalise_name)
    out["numex_direction_correct"] = (
        out["numex_right_entity"].map(_normalise_name)
        == out["gt_right_entity"].map(_normalise_name)
    )
    out["facts_available"] = out["eligible"] & out["numex_direction_correct"]
    out["strict_failure"] = out["facts_available"] & ~out["pairwise_correct"]

    out["gt_relative_gap"] = _relative_gap(out["entity1_value"], out["entity2_value"])
    out["numex_relative_gap"] = _relative_gap(out["entity1_predicted_value"], out["entity2_predicted_value"])

    # Shortcut alignment is descriptive only at G0; it is not part of the
    # strict-failure definition and does not establish a mechanism.
    out["predicted_first_entity"] = pred_norm == e1_norm
    if {"entity1_qrank", "entity2_qrank"}.issubset(out.columns):
        q1, q2 = out["entity1_qrank"], out["entity2_qrank"]
        popular_entity = pd.Series([
            e1 if a > b else e2 if b > a else None
            for e1, e2, a, b in zip(out["entity1_name"], out["entity2_name"], q1, q2, strict=False)
        ], index=out.index, dtype="object")
        pop_match = (pred_norm == popular_entity.map(_normalise_name)).astype("boolean")
        pop_match.loc[popular_entity.isna()] = pd.NA
        out["predicted_more_popular"] = pop_match
    else:
        out["predicted_more_popular"] = pd.NA

    if {"entity1_cosine_similarity", "entity2_cosine_similarity"}.issubset(out.columns):
        c1, c2 = out["entity1_cosine_similarity"], out["entity2_cosine_similarity"]
        cooccur_entity = pd.Series([
            e1 if a > b else e2 if b > a else None
            for e1, e2, a, b in zip(out["entity1_name"], out["entity2_name"], c1, c2, strict=False)
        ], index=out.index, dtype="object")
        cooccur_match = (pred_norm == cooccur_entity.map(_normalise_name)).astype("boolean")
        cooccur_match.loc[cooccur_entity.isna()] = pd.NA
        out["predicted_higher_cooccurrence"] = cooccur_match
    else:
        out["predicted_higher_cooccurrence"] = pd.NA
    return out


def wilson_interval(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n <= 0:
        return (math.nan, math.nan)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt((p * (1 - p) + z * z / (4 * n)) / n) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def summarise_group(df: pd.DataFrame, model: str, dataset: str) -> dict[str, object]:
    eligible = df[df["eligible"]]
    facts = df[df["facts_available"]]
    failures = df[df["strict_failure"]]
    n_facts, n_fail = len(facts), len(failures)
    lo, hi = wilson_interval(n_fail, n_facts)
    record: dict[str, object] = {
        "model": model,
        "dataset": dataset,
        "rows": len(df),
        "eligible": len(eligible),
        "facts_available": n_facts,
        "strict_failures": n_fail,
        "strict_failure_rate_given_facts": n_fail / n_facts if n_facts else math.nan,
        "strict_failure_rate_ci95_low": lo,
        "strict_failure_rate_ci95_high": hi,
        "pairwise_accuracy_eligible": eligible["pairwise_correct"].mean() if len(eligible) else math.nan,
        "numex_direction_accuracy_eligible": eligible["numex_direction_correct"].mean() if len(eligible) else math.nan,
    }
    if n_fail:
        record["failure_predicted_first_rate"] = failures["predicted_first_entity"].mean()
        record["failure_predicted_more_popular_rate"] = (
            failures["predicted_more_popular"].astype("boolean").mean()
            if failures["predicted_more_popular"].notna().any() else math.nan
        )
        record["failure_predicted_higher_cooccurrence_rate"] = (
            failures["predicted_higher_cooccurrence"].astype("boolean").mean()
            if failures["predicted_higher_cooccurrence"].notna().any() else math.nan
        )
    else:
        record.update({
            "failure_predicted_first_rate": math.nan,
            "failure_predicted_more_popular_rate": math.nan,
            "failure_predicted_higher_cooccurrence_rate": math.nan,
        })
    return record


def sensitivity_rows(
    df: pd.DataFrame,
    model: str,
    dataset: str,
    thresholds: Iterable[float] = (0.0, 0.05, 0.1, 0.2),
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for threshold in thresholds:
        sub = df[
            df["facts_available"]
            & (df["gt_relative_gap"] >= threshold)
            & (df["numex_relative_gap"] >= threshold)
        ]
        n, k = len(sub), int(sub["strict_failure"].sum())
        lo, hi = wilson_interval(k, n)
        rows.append({
            "model": model,
            "dataset": dataset,
            "min_relative_gap": threshold,
            "facts_available": n,
            "strict_failures": k,
            "failure_rate": k / n if n else math.nan,
            "ci95_low": lo,
            "ci95_high": hi,
        })
    return rows


def evaluate_gate(summary: pd.DataFrame, config: GateConfig) -> GateResult:
    total_eligible = int(summary["facts_available"].sum()) if len(summary) else 0
    total_failures = int(summary["strict_failures"].sum()) if len(summary) else 0
    passing = summary[
        (summary["strict_failures"] >= config.min_group_failures)
        & (summary["strict_failure_rate_given_facts"] >= config.min_group_failure_rate)
    ] if len(summary) else summary
    passing_groups = len(passing)

    if total_eligible < config.min_total_eligible:
        verdict = "HOLD_INSUFFICIENT_FACT_AVAILABLE_CASES"
        reason = "Too few natural fact-available cases to judge the phenomenon robustly."
    elif total_failures < config.min_total_strict_failures:
        verdict = "STOP_TOO_FEW_NATURAL_FAILURES"
        reason = "The target natural failure is too rare; do not manufacture synthetic failures to continue."
    elif passing_groups < config.min_passing_groups:
        verdict = "STOP_NOT_REPLICATED_ACROSS_GROUPS"
        reason = "The target failure does not replicate in enough model-dataset groups."
    else:
        verdict = "PASS_BEHAVIOR_G0"
        reason = "Natural facts-available-but-comparison-wrong failures are frequent and replicated enough to justify mechanism work."

    return GateResult(verdict, reason, total_eligible, total_failures, passing_groups, config)


def discover_result_pairs(results_dir: Path) -> list[tuple[str, str, Path, Path]]:
    pairs: list[tuple[str, str, Path, Path]] = []
    for model_dir in sorted(p for p in results_dir.iterdir() if p.is_dir()):
        pairwise_dir, pointwise_dir = model_dir / "pairwise", model_dir / "pointwise"
        if not pairwise_dir.is_dir() or not pointwise_dir.is_dir():
            continue
        for pairwise_path in sorted(pairwise_dir.glob("*.csv")):
            pointwise_path = pointwise_dir / pairwise_path.name
            if pointwise_path.exists():
                pairs.append((model_dir.name, pairwise_path.stem, pairwise_path, pointwise_path))
    return pairs


def run_preflight(results_dir: Path, output_dir: Path, gate: GateConfig | None = None) -> GateResult:
    gate = gate or GateConfig()
    result_pairs = discover_result_pairs(results_dir)
    if not result_pairs:
        raise ValueError(
            f"No matching pointwise/pairwise result CSVs found under {results_dir}. "
            "Expected <results>/<model>/pointwise/*.csv and pairwise/*.csv."
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict[str, object]] = []
    sensitivity: list[dict[str, object]] = []
    strict_case_frames: list[pd.DataFrame] = []

    for model, dataset, pairwise_path, pointwise_path in result_pairs:
        merged = load_merged_dataset(pairwise_path, pointwise_path)
        classified = classify_cases(merged)
        classified.insert(0, "model", model)
        classified.insert(1, "dataset", dataset)
        summaries.append(summarise_group(classified, model, dataset))
        sensitivity.extend(sensitivity_rows(classified, model, dataset))
        strict = classified[classified["strict_failure"]].copy()
        if len(strict):
            strict_case_frames.append(strict)

    summary_df = pd.DataFrame(summaries).sort_values(["model", "dataset"])
    sensitivity_df = pd.DataFrame(sensitivity).sort_values(["model", "dataset", "min_relative_gap"])
    cases_df = pd.concat(strict_case_frames, ignore_index=True) if strict_case_frames else pd.DataFrame()

    summary_df.to_csv(output_dir / "summary.csv", index=False)
    sensitivity_df.to_csv(output_dir / "sensitivity.csv", index=False)
    cases_df.to_csv(output_dir / "strict_natural_cases.csv", index=False)

    verdict = evaluate_gate(summary_df, gate)
    with (output_dir / "verdict.json").open("w", encoding="utf-8") as f:
        json.dump({
            "verdict": verdict.verdict,
            "reason": verdict.reason,
            "total_fact_available_cases": verdict.total_eligible,
            "total_strict_failures": verdict.total_strict_failures,
            "passing_groups": verdict.passing_groups,
            "gate_config": asdict(verdict.config),
        }, f, indent=2, ensure_ascii=False)
    return verdict
