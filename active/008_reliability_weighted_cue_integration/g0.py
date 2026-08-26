#!/usr/bin/env python3
"""Generate simple multimodal cue-integration stimuli and score predictions.

No LLM judge. The visual cue is an SVG marker on a 0-100 ruler; the text cue is
provided in the manifest/prompt. Normative fusion uses inverse-variance weights.

Generate:
  python g0.py generate --out-dir stimuli --manifest manifest.jsonl

Score a runner-produced JSONL with {"id": ..., "prediction": <number>}:
  python g0.py score --manifest manifest.jsonl --predictions predictions.jsonl
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path


def optimal_image_weight(sigma_image: float, sigma_text: float) -> float:
    pi = 1.0 / (sigma_image * sigma_image)
    pt = 1.0 / (sigma_text * sigma_text)
    return pi / (pi + pt)


def fused(image_cue: float, text_cue: float, sigma_image: float, sigma_text: float) -> float:
    w = optimal_image_weight(sigma_image, sigma_text)
    return w * image_cue + (1.0 - w) * text_cue


def svg_ruler(marker: float, path: Path):
    # 0..100 maps to x=40..440. Intentionally plain: no decorative confounds.
    x = 40 + 4 * marker
    ticks = []
    labels = []
    for v in range(0, 101, 10):
        tx = 40 + 4 * v
        ticks.append(f'<line x1="{tx}" y1="85" x2="{tx}" y2="95" stroke="black"/>')
        labels.append(f'<text x="{tx}" y="115" text-anchor="middle" font-size="12">{v}</text>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="480" height="140">
<rect width="100%" height="100%" fill="white"/>
<line x1="40" y1="90" x2="440" y2="90" stroke="black" stroke-width="2"/>
{''.join(ticks)}
{''.join(labels)}
<circle cx="{x:.2f}" cy="60" r="7" fill="black"/>
<line x1="{x:.2f}" y1="67" x2="{x:.2f}" y2="90" stroke="black" stroke-width="2"/>
</svg>'''
    path.write_text(svg)


def generate(out_dir: Path, manifest: Path, seed: int, n_per_condition: int):
    rng = random.Random(seed)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    idx = 0
    # Includes image-better, balanced, and text-better regimes.
    for sigma_image, sigma_text in ((2.0, 10.0), (5.0, 10.0), (8.0, 8.0), (10.0, 5.0), (10.0, 2.0)):
        for _ in range(n_per_condition):
            target = rng.uniform(20, 80)
            image = min(100, max(0, rng.gauss(target, sigma_image)))
            text = min(100, max(0, rng.gauss(target, sigma_text)))
            # Very small cue disagreements make inferred weights unstable; resample once.
            if abs(image - text) < 3:
                text = min(100, max(0, rng.gauss(target, sigma_text) + (4 if text <= image else -4)))
            w_img = optimal_image_weight(sigma_image, sigma_text)
            gold = fused(image, text, sigma_image, sigma_text)
            sid = f"cue-{idx:04d}"
            image_path = out_dir / f"{sid}.svg"
            svg_ruler(image, image_path)
            rows.append({
                "id": sid,
                "target": target,
                "image_cue": image,
                "text_cue": text,
                "sigma_image": sigma_image,
                "sigma_text": sigma_text,
                "optimal_image_weight": w_img,
                "optimal_fused_estimate": gold,
                "image_path": str(image_path),
                "prompt": (
                    f"The image shows one noisy measurement of an unknown value on a 0-100 ruler. "
                    f"A second independent sensor reports {text:.1f}. "
                    f"The image sensor has standard deviation {sigma_image:.1f}; the text sensor has "
                    f"standard deviation {sigma_text:.1f}. Estimate the underlying value. Answer only one number."
                ),
            })
            idx += 1
    manifest.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    print(json.dumps({"n": len(rows), "manifest": str(manifest), "stimuli": str(out_dir)}, indent=2))


def load_jsonl(path: Path):
    return [json.loads(x) for x in path.read_text().splitlines() if x.strip()]


def score(manifest: Path, predictions: Path):
    cases = {r["id"]: r for r in load_jsonl(manifest)}
    preds = {r["id"]: r for r in load_jsonl(predictions)}
    rows = []
    for sid, c in cases.items():
        if sid not in preds:
            continue
        try:
            y = float(preds[sid]["prediction"])
        except (KeyError, TypeError, ValueError):
            continue
        denom = c["image_cue"] - c["text_cue"]
        if abs(denom) < 1e-9:
            continue
        w_obs = (y - c["text_cue"]) / denom
        rows.append({
            "id": sid,
            "prediction": y,
            "observed_image_weight": w_obs,
            "optimal_image_weight": c["optimal_image_weight"],
            "weight_abs_error": abs(w_obs - c["optimal_image_weight"]),
            "prediction_abs_error_vs_optimal": abs(y - c["optimal_fused_estimate"]),
            "sigma_image": c["sigma_image"],
            "sigma_text": c["sigma_text"],
        })
    if not rows:
        print(json.dumps({"n": 0}, indent=2))
        return

    by_cond = {}
    for si, st in sorted({(r["sigma_image"], r["sigma_text"]) for r in rows}):
        rr = [r for r in rows if r["sigma_image"] == si and r["sigma_text"] == st]
        by_cond[f"img{si:g}_txt{st:g}"] = {
            "n": len(rr),
            "mean_observed_image_weight": sum(r["observed_image_weight"] for r in rr) / len(rr),
            "optimal_image_weight": rr[0]["optimal_image_weight"],
            "mean_weight_abs_error": sum(r["weight_abs_error"] for r in rr) / len(rr),
        }
    summary = {
        "n": len(rows),
        "mean_weight_abs_error": sum(r["weight_abs_error"] for r in rows) / len(rows),
        "mean_prediction_abs_error_vs_optimal": sum(r["prediction_abs_error_vs_optimal"] for r in rows) / len(rows),
        "conditions": by_cond,
    }
    print(json.dumps(summary, indent=2))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate")
    g.add_argument("--out-dir", default="stimuli")
    g.add_argument("--manifest", default="manifest.jsonl")
    g.add_argument("--seed", type=int, default=0)
    g.add_argument("--n-per-condition", type=int, default=20)
    s = sub.add_parser("score")
    s.add_argument("--manifest", default="manifest.jsonl")
    s.add_argument("--predictions", required=True)
    args = ap.parse_args()

    if args.cmd == "generate":
        generate(Path(args.out_dir), Path(args.manifest), args.seed, args.n_per_condition)
    else:
        score(Path(args.manifest), Path(args.predictions))


if __name__ == "__main__":
    main()
