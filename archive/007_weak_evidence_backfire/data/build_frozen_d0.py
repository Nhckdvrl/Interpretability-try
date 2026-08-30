from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import math

import numpy as np
from sklearn.datasets import load_breast_cancer, load_wine

SEED = 20260829
CAL_FRACTION = 0.60
ALPHA = 0.5

BREAST_FEATURES = [
    "mean radius", "mean texture", "mean smoothness", "mean compactness", "mean concavity",
    "mean concave points", "mean symmetry", "radius error", "perimeter error", "area error",
    "compactness error", "concavity error", "concave points error", "worst radius", "worst texture",
    "worst smoothness", "worst compactness", "worst concavity", "worst concave points", "worst symmetry",
]
WINE_FEATURES = [
    "alcohol", "ash", "alcalinity_of_ash", "magnesium", "total_phenols", "flavanoids",
    "proanthocyanins", "color_intensity", "od280/od315_of_diluted_wines", "proline",
]


def _array_sha(x: np.ndarray, y: np.ndarray) -> str:
    h = hashlib.sha256()
    h.update(np.ascontiguousarray(x).tobytes())
    h.update(np.ascontiguousarray(y).tobytes())
    return h.hexdigest()


def _split(y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(SEED)
    cal: list[int] = []
    val: list[int] = []
    for cls in sorted(np.unique(y).tolist()):
        ids = np.flatnonzero(y == cls).copy()
        rng.shuffle(ids)
        n_cal = int(round(CAL_FRACTION * len(ids)))
        cal.extend(ids[:n_cal].tolist())
        val.extend(ids[n_cal:].tolist())
    return np.asarray(cal, dtype=int), np.asarray(val, dtype=int)


def _smoothed_lr(counts: list[int]) -> float:
    et, nt, eo, no = counts
    return ((et + ALPHA) / (nt + 2 * ALPHA)) / ((eo + ALPHA) / (no + 2 * ALPHA))


def _evaluate(x: np.ndarray, y: np.ndarray, ids: np.ndarray, j: int, op: str, threshold: float):
    values = x[ids, j]
    labels = y[ids]
    event = values >= threshold if op == ">=" else values <= threshold
    target = labels == 0
    other = labels == 1
    counts = [int(np.sum(event & target)), int(np.sum(target)), int(np.sum(event & other)), int(np.sum(other))]
    return _smoothed_lr(counts), counts


def _candidates(x, y, cal, val, j):
    out = []
    for op in (">=", "<="):
        for threshold in np.unique(x[cal, j]):
            t = float(threshold)
            lr_c, cnt_c = _evaluate(x, y, cal, j, op, t)
            lr_v, cnt_v = _evaluate(x, y, val, j, op, t)
            p_c = (cnt_c[0] + cnt_c[2]) / (cnt_c[1] + cnt_c[3])
            p_v = (cnt_v[0] + cnt_v[2]) / (cnt_v[1] + cnt_v[3])
            if 0.08 <= p_c <= 0.92 and 0.05 <= p_v <= 0.95:
                out.append({"threshold": t, "op": op, "lr_cal": lr_c, "lr_val": lr_v,
                            "counts_cal": cnt_c, "counts_val": cnt_v, "p_cal": p_c, "p_val": p_v})
    return out


def _choose_pairs(x, y, cal, val, j):
    c = _candidates(x, y, cal, val, j)
    weak_t = [z for z in c if 1.12 <= z["lr_cal"] <= 1.65 and z["lr_val"] > 1.05]
    strong_t = [z for z in c if 2.0 <= z["lr_cal"] <= 8.0 and z["lr_val"] > 1.4]
    weak_o = [z for z in c if 0.60 <= z["lr_cal"] <= 0.90 and z["lr_val"] < 0.95]
    strong_o = [z for z in c if 0.12 <= z["lr_cal"] <= 0.50 and z["lr_val"] < 0.70]

    target_pairs = []
    for weak in weak_t:
        for strong in strong_t:
            if weak["op"] != strong["op"]:
                continue
            nested = strong["threshold"] >= weak["threshold"] if weak["op"] == ">=" else strong["threshold"] <= weak["threshold"]
            if nested and strong["lr_cal"] > weak["lr_cal"] * 1.20 and strong["lr_val"] > weak["lr_val"] * 1.20:
                score = abs(math.log(weak["lr_cal"]) - math.log(1.3)) + abs(math.log(strong["lr_cal"]) - math.log(3.5))
                target_pairs.append((score, weak, strong))
    other_pairs = []
    for weak in weak_o:
        for strong in strong_o:
            if weak["op"] != strong["op"]:
                continue
            nested = strong["threshold"] >= weak["threshold"] if weak["op"] == ">=" else strong["threshold"] <= weak["threshold"]
            if nested and strong["lr_cal"] < weak["lr_cal"] / 1.20 and strong["lr_val"] < weak["lr_val"] / 1.20:
                score = abs(math.log(weak["lr_cal"]) - math.log(1 / 1.3)) + abs(math.log(strong["lr_cal"]) - math.log(1 / 3.5))
                other_pairs.append((score, weak, strong))
    if not target_pairs or not other_pairs:
        raise RuntimeError("feature failed frozen weak/strong selection contract")
    _, wt, st = min(target_pairs, key=lambda z: z[0])
    _, wo, so = min(other_pairs, key=lambda z: z[0])
    return wt, st, wo, so


def _find_neutral(x, y, cal, val, feature_names, *, preferred_feature: str, preferred_op: str, preferred_threshold: float):
    j = list(feature_names).index(preferred_feature)
    lr_c, cnt_c = _evaluate(x, y, cal, j, preferred_op, preferred_threshold)
    lr_v, cnt_v = _evaluate(x, y, val, j, preferred_op, preferred_threshold)
    if not (0.90 <= lr_c <= 1.10 and 0.90 <= lr_v <= 1.10):
        raise RuntimeError(f"frozen neutral cue is not stable: {preferred_feature} {lr_c=} {lr_v=}")
    return {"threshold": float(preferred_threshold), "op": preferred_op, "lr_cal": lr_c,
            "lr_val": lr_v, "counts_cal": cnt_c, "counts_val": cnt_v}


def _fmt_threshold(x: float) -> str:
    return repr(float(x))


def _evidence(feature: str, spec: dict) -> str:
    phrase = "at least" if spec["op"] == ">=" else "at most"
    return f"the recorded {feature} value is {phrase} {_fmt_threshold(spec['threshold'])}."


def _count_text(evidence: str, counts: list[int], target_name: str, other_name: str) -> str:
    et, nt, eo, no = counts
    return f"'{evidence[:-1]}' occurred in {et}/{nt} {target_name} calibration cases and {eo}/{no} {other_name} calibration cases"


def _source_payload(name: str):
    if name == "breast":
        d = load_breast_cancer()
        return {
            "x": np.asarray(d.data), "y": np.asarray(d.target), "feature_names": list(d.feature_names),
            "dataset": "Breast Cancer Wisconsin (Diagnostic)", "doi": "10.24432/C5DW2B",
            "url": "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic",
            "domain": "breast-cytology", "target_name": "malignant", "other_name": "benign",
            "target_h": "the specimen is malignant", "other_h": "the specimen is benign",
            "target_action": "route the specimen to the malignant-case review queue",
            "other_action": "route the specimen to the benign-case review queue",
            "background": "A new fine-needle-aspiration specimen comes from the same diagnostic population as the calibration records and is known, for this binary routing decision, to be either malignant or benign.",
            "features": BREAST_FEATURES,
            "neutral": ("mean fractal dimension", "<=", 0.06246),
        }
    if name == "wine":
        d = load_wine()
        keep = np.asarray(d.target) < 2
        return {
            "x": np.asarray(d.data)[keep], "y": np.asarray(d.target)[keep], "feature_names": list(d.feature_names),
            "dataset": "Wine", "doi": "10.24432/C5PC7J",
            "url": "https://archive.ics.uci.edu/dataset/109/wine",
            "domain": "wine-cultivar", "target_name": "cultivar-1", "other_name": "cultivar-2",
            "target_h": "the sample comes from cultivar 1", "other_h": "the sample comes from cultivar 2",
            "target_action": "route the sample to the cultivar-1 provenance queue",
            "other_action": "route the sample to the cultivar-2 provenance queue",
            "background": "A new wine sample comes from the same chemical-analysis population as the calibration records and, within this frozen binary subset, is known to come from cultivar 1 or cultivar 2.",
            "features": WINE_FEATURES,
            "neutral": ("hue", "<=", 1.09),
        }
    raise ValueError(name)


def _make_row(source_name: str, index: int, feature: str) -> dict:
    meta = _source_payload(source_name)
    x, y, feature_names = meta["x"], meta["y"], meta["feature_names"]
    cal, val = _split(y)
    j = feature_names.index(feature)
    wt, st, wo, so = _choose_pairs(x, y, cal, val, j)
    nf, nop, nth = meta["neutral"]
    neutral = _find_neutral(x, y, cal, val, feature_names, preferred_feature=nf, preferred_op=nop, preferred_threshold=nth)

    wt_text = _evidence(feature, wt); st_text = _evidence(feature, st)
    wo_text = _evidence(feature, wo); so_text = _evidence(feature, so)
    n_text = _evidence(nf, neutral)
    calibration = (
        "A fixed 60% class-stratified calibration partition was frozen before any model run. "
        + "; ".join([
            _count_text(wt_text, wt["counts_cal"], meta["target_name"], meta["other_name"]),
            _count_text(st_text, st["counts_cal"], meta["target_name"], meta["other_name"]),
            _count_text(wo_text, wo["counts_cal"], meta["target_name"], meta["other_name"]),
            _count_text(so_text, so["counts_cal"], meta["target_name"], meta["other_name"]),
            _count_text(n_text, neutral["counts_cal"], meta["target_name"], meta["other_name"]),
        ]) + "."
    )
    cue_specs = {
        "weak_target": {"feature": feature, **wt}, "strong_target": {"feature": feature, **st},
        "weak_other": {"feature": feature, **wo}, "strong_other": {"feature": feature, **so},
        "neutral": {"feature": nf, **neutral},
    }
    source = {
        "dataset": meta["dataset"],
        "record_id": f"feature={feature};seed={SEED};calibration=60%;validation=40%",
        "license": "CC BY 4.0", "split": "derived-calibration/validation", "provenance": "external-derived",
        "url": meta["url"], "doi": meta["doi"], "derivation_seed": SEED,
        "calibration_fraction": CAL_FRACTION, "validation_fraction": 1 - CAL_FRACTION,
        "feature": feature, "neutral_feature": nf, "loader": "scikit-learn packaged UCI dataset copy",
        "source_array_sha256": _array_sha(x, y), "lr_estimator": "Jeffreys 0.5-cell smoothing",
        "cue_specs": cue_specs,
        "weak_target_lr_validation": wt["lr_val"], "strong_target_lr_validation": st["lr_val"],
        "weak_other_lr_validation": wo["lr_val"], "strong_other_lr_validation": so["lr_val"],
        "neutral_lr_validation": neutral["lr_val"],
        "weak_target_counts_validation": wt["counts_val"], "strong_target_counts_validation": st["counts_val"],
        "weak_other_counts_validation": wo["counts_val"], "strong_other_counts_validation": so["counts_val"],
        "neutral_counts_validation": neutral["counts_val"],
    }
    flags = {
        "calibration_valid_gold": True, "weak_target_support_gold": True, "weak_other_support_gold": True,
        "strong_target_support_gold": True, "strong_other_support_gold": True, "neutral_gold": True,
        "pragmatic_completeness_gold": True, "matched_length_control_gold": True, "actions_symmetric_gold": True,
        "hypotheses_exclusive_gold": True, "hypotheses_exhaustive_gold": True, "binary_choice_well_defined_gold": True,
        "core_wording_does_not_label_strength_gold": True, "direction_pair_matched_gold": True,
        "strong_weak_relation_comparable_gold": True, "neutral_control_matched_gold": True,
        "baseline_contains_no_case_specific_evidence_gold": True, "natural_setting_gold": True,
    }
    return {
        "scenario_id": f"{source_name}:{index:02d}:{feature.replace(' ', '_')}", "domain": meta["domain"],
        "background": meta["background"], "calibration_text": calibration,
        "target_hypothesis": meta["target_h"], "other_hypothesis": meta["other_h"],
        "target_action": meta["target_action"], "other_action": meta["other_action"],
        "weak_target_evidence": wt_text, "weak_other_evidence": wo_text,
        "strong_target_evidence": st_text, "strong_other_evidence": so_text, "neutral_evidence": n_text,
        "pragmatic_completeness_text": "The reporting protocol always displays the preselected measurement condition for the case. It does not choose which measurement to report based on whether a stronger unreported measurement exists, so omission of other measurements conveys no information.",
        "matched_length_control_text": "The reporting protocol uses the same fixed standardized field and placement for every case. The field format itself carries no information about which of the two hypotheses is correct.",
        "weak_target_lr": wt["lr_cal"], "weak_other_lr": wo["lr_cal"],
        "strong_target_lr": st["lr_cal"], "strong_other_lr": so["lr_cal"], "neutral_lr": neutral["lr_cal"],
        "source": source, **flags,
    }


def build_rows() -> list[dict]:
    rows = []
    for i, feature in enumerate(BREAST_FEATURES, 1):
        rows.append(_make_row("breast", i, feature))
    for i, feature in enumerate(WINE_FEATURES, 1):
        rows.append(_make_row("wine", i, feature))
    if len(rows) != 30 or len({r["scenario_id"] for r in rows}) != 30:
        raise RuntimeError("frozen D0 must contain exactly 30 unique scenarios")
    return rows


def render(rows: list[dict]) -> bytes:
    return "".join(json.dumps(r, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for r in rows).encode("utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).with_name("frozen_d0.jsonl")))
    args = ap.parse_args()
    raw = render(build_rows())
    Path(args.out).write_bytes(raw)
    print(json.dumps({"items": 30, "sha256": hashlib.sha256(raw).hexdigest(), "out": args.out}, indent=2))


if __name__ == "__main__":
    main()
