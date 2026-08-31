#!/usr/bin/env python3
"""Frozen G0 runner/analyzer for the two unregistered mass frontiers.

No MI is performed here. Models are expected to be served one-at-a-time through
an OpenAI-compatible local multimodal endpoint (vLLM/SGLang/etc.).
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import mimetypes
import random
import re
import statistics
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

PROMPT = (
    "Estimate the mass of the main physical object in this image. "
    "Use only what is visible in this image and ordinary real-world knowledge. "
    "Return JSON only with mass_kg as one positive number and category as a "
    "short common-noun label."
)

MASS_RE = re.compile(r'[\"\']?mass_kg[\"\']?\s*[:=]\s*([0-9]+(?:\.[0-9]+)?)', re.I)


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            if line.strip():
                obj = json.loads(line)
                obj["_line"] = i
                rows.append(obj)
    return rows


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def post_json(url: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "Authorization": "Bearer EMPTY"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_fence(text: str) -> str:
    s = text.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
        s = re.sub(r"\s*```$", "", s)
    return s.strip()


def parse_mass(text: str) -> Tuple[Optional[float], Optional[str], str]:
    s = strip_fence(text)
    try:
        obj = json.loads(s)
        mass = float(obj["mass_kg"])
        if math.isfinite(mass) and mass > 0:
            cat = str(obj.get("category", "")).strip() or None
            return mass, cat, "json"
    except Exception:
        pass
    m = MASS_RE.search(s)
    if m:
        mass = float(m.group(1))
        if math.isfinite(mass) and mass > 0:
            return mass, None, "regex_mass_field"
    return None, None, "parse_fail"


def run(args: argparse.Namespace) -> None:
    manifest = read_jsonl(Path(args.manifest))
    out = Path(args.output)
    done = set()
    if out.exists() and args.resume:
        for row in read_jsonl(out):
            done.add(row.get("request_id"))

    endpoint = args.base_url.rstrip("/") + "/v1/chat/completions"
    for row in manifest:
        image = Path(row["image_path"])
        if not image.is_absolute():
            image = Path(args.image_root) / image
        key_payload = {
            "family": args.family,
            "model": args.model,
            "object_id": row["object_id"],
            "view_id": row["view_id"],
            "repeat_id": row.get("repeat_id", 0),
            "pipeline_variant": row.get("pipeline_variant", "original"),
            "image_path": str(row["image_path"]),
        }
        request_id = hashlib.sha256(
            json.dumps(key_payload, sort_keys=True).encode("utf-8")
        ).hexdigest()[:20]
        if request_id in done:
            continue

        payload = {
            "model": args.model,
            "temperature": 0,
            "top_p": 1,
            "max_tokens": args.max_tokens,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": PROMPT},
                        {"type": "image_url", "image_url": {"url": data_uri(image)}},
                    ],
                }
            ],
        }
        result: Dict[str, Any] = {**row, **key_payload, "request_id": request_id, "prompt": PROMPT}
        try:
            raw = post_json(endpoint, payload, timeout=args.timeout)
            text = raw["choices"][0]["message"]["content"]
            mass, category, parse_mode = parse_mass(text)
            result.update(
                {
                    "raw_text": text,
                    "pred_mass_kg": mass,
                    "pred_category": category,
                    "parse_mode": parse_mode,
                    "server_model": raw.get("model"),
                    "error": None,
                }
            )
        except Exception as e:
            result.update(
                {
                    "raw_text": None,
                    "pred_mass_kg": None,
                    "pred_category": None,
                    "parse_mode": "request_error",
                    "server_model": None,
                    "error": repr(e),
                }
            )
        append_jsonl(out, result)


def median(xs: Iterable[float]) -> Optional[float]:
    vals = list(xs)
    return statistics.median(vals) if vals else None


def quantile(xs: List[float], q: float) -> Optional[float]:
    if not xs:
        return None
    ys = sorted(xs)
    if len(ys) == 1:
        return ys[0]
    pos = q * (len(ys) - 1)
    lo, hi = int(math.floor(pos)), int(math.ceil(pos))
    if lo == hi:
        return ys[lo]
    w = pos - lo
    return ys[lo] * (1 - w) + ys[hi] * w


def norm_category(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    s = re.sub(r"[^a-z0-9 ]+", " ", s.lower())
    s = re.sub(r"\s+", " ", s).strip()
    return s or None


def original_base(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        r
        for r in rows
        if r.get("pipeline_variant", "original") == "original"
        and int(r.get("repeat_id", 0) or 0) == 0
    ]


def parsed(r: Dict[str, Any]) -> bool:
    x = r.get("pred_mass_kg")
    return isinstance(x, (int, float)) and math.isfinite(float(x)) and float(x) > 0


def same_view_repeat_diffs(rows: List[Dict[str, Any]]) -> List[float]:
    groups: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for r in rows:
        if r.get("pipeline_variant", "original") == "original" and parsed(r):
            groups[(str(r["object_id"]), str(r["view_id"]), str(r.get("image_path")))].append(r)
    diffs = []
    for rs in groups.values():
        base = [r for r in rs if int(r.get("repeat_id", 0) or 0) == 0]
        rep = [r for r in rs if int(r.get("repeat_id", 0) or 0) > 0]
        if not base:
            continue
        b = math.log(float(base[0]["pred_mass_kg"]))
        diffs.extend(abs(math.log(float(r["pred_mass_kg"])) - b) for r in rep)
    return diffs


def pipeline_control_diffs(rows: List[Dict[str, Any]]) -> List[float]:
    groups: Dict[Tuple[str, str], Dict[str, Dict[str, Any]]] = defaultdict(dict)
    for r in rows:
        if int(r.get("repeat_id", 0) or 0) != 0 or not parsed(r):
            continue
        groups[(str(r["object_id"]), str(r["view_id"]))][str(r.get("pipeline_variant", "original"))] = r
    diffs = []
    for variants in groups.values():
        if "original" not in variants:
            continue
        b = math.log(float(variants["original"]["pred_mass_kg"]))
        for name, r in variants.items():
            if name != "original":
                diffs.append(abs(math.log(float(r["pred_mass_kg"])) - b))
    return diffs


def per_object_view_stats(rows: List[Dict[str, Any]]) -> Tuple[Dict[str, Dict[str, float]], int, int]:
    source: Dict[str, int] = Counter(str(r["object_id"]) for r in original_base(rows))
    eligible_source = sum(v >= 4 for v in source.values())
    by: Dict[str, List[float]] = defaultdict(list)
    for r in original_base(rows):
        if parsed(r):
            by[str(r["object_id"])].append(math.log(float(r["pred_mass_kg"])))
    out = {}
    for obj, ys in by.items():
        if len(ys) < 4:
            continue
        rng = max(ys) - min(ys)
        out[obj] = {
            "n_views": len(ys),
            "view_log_range": rng,
            "view_ratio": math.exp(rng),
            "view_log_sd": statistics.pstdev(ys),
        }
    return out, eligible_source, len(out)


def category_modal_shares(rows: List[Dict[str, Any]]) -> List[float]:
    by: Dict[str, List[str]] = defaultdict(list)
    for r in original_base(rows):
        cat = norm_category(r.get("pred_category"))
        if cat:
            by[str(r["object_id"])].append(cat)
    vals = []
    for cats in by.values():
        if len(cats) >= 4:
            vals.append(Counter(cats).most_common(1)[0][1] / len(cats))
    return vals


def object_fe_components(rows: List[Dict[str, Any]]) -> Dict[str, Tuple[float, float]]:
    by: Dict[str, List[Tuple[float, float]]] = defaultdict(list)
    for r in original_base(rows):
        if not parsed(r):
            continue
        area = r.get("apparent_area_fraction")
        try:
            area = float(area)
        except Exception:
            continue
        if not (math.isfinite(area) and area > 0):
            continue
        by[str(r["object_id"])].append((math.log(area), math.log(float(r["pred_mass_kg"]))))
    comps = {}
    for obj, xy in by.items():
        if len(xy) < 4:
            continue
        mx = statistics.mean(x for x, _ in xy)
        my = statistics.mean(y for _, y in xy)
        num = sum((x - mx) * (y - my) for x, y in xy)
        den = sum((x - mx) ** 2 for x, _ in xy)
        if den > 0:
            comps[obj] = (num, den)
    return comps


def slope_from_components(comps: Dict[str, Tuple[float, float]], ids: Optional[List[str]] = None) -> Optional[float]:
    ids = ids if ids is not None else list(comps)
    num = sum(comps[i][0] for i in ids)
    den = sum(comps[i][1] for i in ids)
    return num / den if den > 0 else None


def bootstrap_ci(comps: Dict[str, Tuple[float, float]], seed: int, n: int) -> Tuple[Optional[float], Optional[float]]:
    ids = sorted(comps)
    if len(ids) < 2:
        return None, None
    rng = random.Random(seed)
    vals = []
    for _ in range(n):
        sample = [rng.choice(ids) for _ in ids]
        b = slope_from_components(comps, sample)
        if b is not None:
            vals.append(b)
    return quantile(vals, 0.025), quantile(vals, 0.975)


def leave_one_out_positive(comps: Dict[str, Tuple[float, float]]) -> Optional[float]:
    ids = sorted(comps)
    if len(ids) < 3:
        return None
    signs = []
    for drop in ids:
        b = slope_from_components(comps, [i for i in ids if i != drop])
        if b is not None:
            signs.append(b > 0)
    return sum(signs) / len(signs) if signs else None


def analyze_family(rows: List[Dict[str, Any]], seed: int, bootstrap_n: int) -> Dict[str, Any]:
    obj_stats, source_objs, eligible_objs = per_object_view_stats(rows)
    ratios = [x["view_ratio"] for x in obj_stats.values()]
    log_ranges = [x["view_log_range"] for x in obj_stats.values()]
    repeat = same_view_repeat_diffs(rows)
    pipeline = pipeline_control_diffs(rows)
    cats = category_modal_shares(rows)

    med_ratio = median(ratios)
    frac_ratio2 = (sum(x >= 2 for x in ratios) / len(ratios)) if ratios else None
    eligible_rate = eligible_objs / source_objs if source_objs else 0.0
    med_repeat = median(repeat)
    med_pipeline = median(pipeline)
    med_cross_range = median(log_ranges)
    med_cat = median(cats)

    repeat_ok = med_repeat is not None and med_repeat <= 0.05
    pipeline_ok = (
        med_pipeline is not None
        and med_cross_range is not None
        and med_pipeline <= 0.5 * med_cross_range
    )
    category_ok = med_cat is not None and med_cat >= 0.75

    cross_positive = bool(
        eligible_rate >= 0.80
        and med_ratio is not None and med_ratio >= 2.0
        and frac_ratio2 is not None and frac_ratio2 >= 0.50
        and repeat_ok and pipeline_ok and category_ok
    )

    comps = object_fe_components(rows)
    beta = slope_from_components(comps)
    ci_lo, ci_hi = bootstrap_ci(comps, seed=seed, n=bootstrap_n)
    loo = leave_one_out_positive(comps)
    size_positive = bool(
        beta is not None and beta >= 0.25
        and ci_lo is not None and ci_lo > 0
        and loo is not None and loo >= 0.90
        and repeat_ok and pipeline_ok
    )

    return {
        "source_objects_with_4plus_views": source_objs,
        "eligible_objects_with_4plus_parsed_views": eligible_objs,
        "eligible_object_rate": eligible_rate,
        "median_view_ratio": med_ratio,
        "fraction_objects_view_ratio_ge_2": frac_ratio2,
        "median_view_log_range": med_cross_range,
        "same_view_repeat_n": len(repeat),
        "same_view_repeat_median_abs_logdiff": med_repeat,
        "pipeline_control_n": len(pipeline),
        "pipeline_control_median_abs_logdiff": med_pipeline,
        "category_control_object_n": len(cats),
        "category_control_median_modal_share": med_cat,
        "cross_view_instability_positive": cross_positive,
        "size_fe_object_n": len(comps),
        "within_object_logmass_on_logarea_beta": beta,
        "cluster_bootstrap_95ci": [ci_lo, ci_hi],
        "leave_one_object_out_positive_fraction": loo,
        "visual_size_shortcut_positive": size_positive,
        "object_view_stats": obj_stats,
    }


def analyze(args: argparse.Namespace) -> None:
    families: Dict[str, List[Dict[str, Any]]] = {}
    for spec in args.inputs:
        if "=" not in spec:
            raise SystemExit("--inputs entries must be FAMILY=path.jsonl")
        family, path = spec.split("=", 1)
        families[family] = read_jsonl(Path(path))

    fam_summary = {
        f: analyze_family(rows, seed=args.seed, bootstrap_n=args.bootstrap)
        for f, rows in families.items()
    }
    cross_pos = sum(bool(x["cross_view_instability_positive"]) for x in fam_summary.values())
    size_pos = sum(bool(x["visual_size_shortcut_positive"]) for x in fam_summary.values())
    n_family = len(fam_summary)

    summary = {
        "contract_date": "2026-08-31",
        "families": fam_summary,
        "cross_view_positive_families": cross_pos,
        "visual_size_positive_families": size_pos,
        "family_count": n_family,
        "cross_view_verdict": (
            "PASS-TO-N0-N1 (STILL NOT REGISTERED)"
            if n_family >= 3 and cross_pos >= 2
            else "KILL-S0 / NO-BROAD-CURRENT-OPEN-FAMILY-CROSS-VIEW-MASS-INSTABILITY"
        ),
        "visual_size_verdict": (
            "PASS-TO-N0-N1 (STILL NOT REGISTERED)"
            if n_family >= 3 and size_pos >= 2
            else "KILL-S0 / NO-BROAD-CURRENT-OPEN-FAMILY-VISUAL-SIZE-MASS-SHORTCUT"
        ),
    }
    Path(args.output).write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "families"}, indent=2))


def main() -> None:
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("run")
    r.add_argument("--manifest", required=True)
    r.add_argument("--image-root", default=".")
    r.add_argument("--family", required=True)
    r.add_argument("--model", required=True)
    r.add_argument("--base-url", default="http://127.0.0.1:8000")
    r.add_argument("--output", required=True)
    r.add_argument("--max-tokens", type=int, default=64)
    r.add_argument("--timeout", type=int, default=180)
    r.add_argument("--resume", action="store_true")
    r.set_defaults(func=run)

    a = sub.add_parser("analyze")
    a.add_argument("--inputs", nargs="+", required=True, help="FAMILY=path.jsonl ...")
    a.add_argument("--output", required=True)
    a.add_argument("--seed", type=int, default=20260831)
    a.add_argument("--bootstrap", type=int, default=5000)
    a.set_defaults(func=analyze)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
