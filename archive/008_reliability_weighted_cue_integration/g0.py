#!/usr/bin/env python3
"""Perceptual reliability-weighted cue-integration G0.

Reliability is encoded by the spread of repeated measurements and is never
stated numerically in the prompt.  Image-only and text-only probes establish
that each cue can be read; the multimodal response is then compared against
the model's own unimodal estimates and the inverse-variance optimum.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import re
from pathlib import Path


RELIABILITY_PAIRS = ((2.0, 8.0), (4.0, 8.0), (6.0, 6.0), (8.0, 4.0), (8.0, 2.0))


def optimal_image_weight(sigma_image: float, sigma_text: float) -> float:
    pi, pt = 1.0 / sigma_image**2, 1.0 / sigma_text**2
    return pi / (pi + pt)


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def draw_measurements(samples: list[float], path: Path) -> None:
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new("RGB", (640, 210), "white"); draw = ImageDraw.Draw(image)
    x0, x1, ruler_y = 55, 585, 165
    draw.line((x0, ruler_y, x1, ruler_y), fill="black", width=3)
    font = ImageFont.load_default()
    for value in range(0, 101, 10):
        x = x0 + (x1 - x0) * value / 100
        draw.line((x, ruler_y - 6, x, ruler_y + 7), fill="black", width=2)
        draw.text((x - 7, ruler_y + 10), str(value), fill="black", font=font)
    for idx, value in enumerate(samples):
        x = x0 + (x1 - x0) * value / 100
        y = 55 + (idx % 3) * 28
        draw.ellipse((x - 7, y - 7, x + 7, y + 7), fill="black")
        draw.line((x, y + 8, x, ruler_y - 8), fill=(180, 180, 180), width=1)
    draw.text((55, 18), "Nine independent noisy readings of one unknown value", fill="black", font=font)
    image.save(path)


def generate(out_dir: Path, manifest: Path, seed: int, n_per_condition: int) -> list[dict]:
    rng = random.Random(seed); out_dir.mkdir(parents=True, exist_ok=True); rows = []; idx = 0
    for sigma_image, sigma_text in RELIABILITY_PAIRS:
        made = 0
        while made < n_per_condition:
            target = rng.uniform(25, 75)
            image_samples = [min(100, max(0, rng.gauss(target, sigma_image))) for _ in range(9)]
            text_samples = [min(100, max(0, rng.gauss(target, sigma_text))) for _ in range(9)]
            image_mean, text_mean = _mean(image_samples), _mean(text_samples)
            # Observed weights are ill-conditioned when the realized cue means coincide.
            if abs(image_mean - text_mean) < 4.0:
                continue
            sid = f"cue-{idx:04d}"; image_path = out_dir / f"{sid}.png"; draw_measurements(image_samples, image_path)
            rows.append({
                "id": sid, "target": target, "image_samples": image_samples, "text_samples": text_samples,
                "image_sample_mean": image_mean, "text_sample_mean": text_mean,
                "sigma_image": sigma_image, "sigma_text": sigma_text,
                "optimal_image_weight": optimal_image_weight(sigma_image, sigma_text),
                "optimal_fused_estimate": optimal_image_weight(sigma_image, sigma_text) * image_mean + (1 - optimal_image_weight(sigma_image, sigma_text)) * text_mean,
                "image_path": str(image_path),
                "text_values": ", ".join(f"{x:.1f}" for x in text_samples),
            })
            made += 1; idx += 1
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text("\n".join(json.dumps(r) for r in rows) + "\n")
    return rows


def prompts(case: dict) -> dict[str, str]:
    common = "All readings are independent measurements of the same unknown value on a 0-100 scale. Estimate that value. Answer only one number."
    text_cue = f"The nine noisy readings are: {case['text_values']}. Their mean is {case['text_sample_mean']:.1f}."
    return {
        "image_only": "The image contains nine noisy readings. " + common,
        "text_only": text_cue + " " + common,
        "combined": "The image contains nine readings. The text sensor says: " + text_cue + " " + common,
    }


def parse_number(text: str) -> float | None:
    matches = re.findall(r"(?<![\d.])-?(?:\d+(?:\.\d*)?|\.\d+)(?![\d.])", text.replace(",", ""))
    if not matches:
        return None
    valid = [float(value) for value in matches if -20 <= float(value) <= 120]
    return valid[-1] if valid else None


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class VLMRunner:
    def __init__(self, model_name: str, dtype: str = "auto"):
        import torch
        from transformers import AutoModelForImageTextToText, AutoProcessor
        self.torch = torch; self.processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
        dtype_arg = dtype if dtype == "auto" else getattr(torch, dtype)
        self.model = AutoModelForImageTextToText.from_pretrained(model_name, device_map="auto", torch_dtype=dtype_arg, trust_remote_code=True)
        self.model.eval()

    def generate(self, prompt: str, image_path: str | None) -> str:
        content = []
        if image_path:
            from PIL import Image
            content.append({"type": "image", "image": Image.open(image_path).convert("RGB")})
        content.append({"type": "text", "text": prompt})
        messages = [
            {"role": "system", "content": [{"type": "text", "text": "Return exactly one numeric estimate and no explanation. Compute silently."}]},
            {"role": "user", "content": content},
        ]
        kwargs = dict(add_generation_prompt=True, tokenize=True, return_dict=True, return_tensors="pt")
        try:
            inputs = self.processor.apply_chat_template(messages, enable_thinking=False, **kwargs)
        except TypeError:
            inputs = self.processor.apply_chat_template(messages, **kwargs)
        device = next(self.model.parameters()).device; inputs = inputs.to(device)
        with self.torch.inference_mode():
            generated = self.model.generate(**inputs, max_new_tokens=192, do_sample=False)
        continuation = generated[0, inputs["input_ids"].shape[1]:]
        return self.processor.decode(continuation, skip_special_tokens=True).strip()


def run(model_name: str, manifest: Path, out: Path, dtype: str, shard_index: int, num_shards: int) -> dict:
    cases = [c for i, c in enumerate(load_jsonl(manifest)) if i % num_shards == shard_index]
    runner = VLMRunner(model_name, dtype=dtype); rows = []
    for case in cases:
        row = {"id": case["id"], "model": model_name}
        for condition, prompt in prompts(case).items():
            image_path = case["image_path"] if condition in ("image_only", "combined") else None
            raw = runner.generate(prompt, image_path); row[f"{condition}_raw"] = raw; row[condition] = parse_number(raw)
        rows.append(row)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n")
    return {"model": model_name, "n": len(rows), "parsed_all": sum(all(r[c] is not None for c in ("image_only", "text_only", "combined")) for r in rows)}


def _correlation(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 2: return None
    mx, my = _mean(xs), _mean(ys); dx = sum((x - mx) ** 2 for x in xs); dy = sum((y - my) ** 2 for y in ys)
    if dx == 0 or dy == 0: return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / math.sqrt(dx * dy)


def score(manifest: Path, predictions: Path) -> dict:
    cases = {r["id"]: r for r in load_jsonl(manifest)}; prediction_rows = load_jsonl(predictions); rows = []
    for pred in prediction_rows:
        if pred.get("id") not in cases or any(pred.get(c) is None for c in ("image_only", "text_only", "combined")): continue
        c = cases[pred["id"]]; denom = pred["image_only"] - pred["text_only"]
        if abs(denom) < 4.0: continue
        w_obs = (pred["combined"] - pred["text_only"]) / denom
        rows.append({**c, **pred, "observed_image_weight": w_obs, "weight_abs_error": abs(w_obs - c["optimal_image_weight"])})
    if not rows: return {"n_predictions": len(prediction_rows), "n_weight_analyzable": 0}
    conditions = {}
    for pair in RELIABILITY_PAIRS:
        rr = [r for r in rows if (r["sigma_image"], r["sigma_text"]) == pair]
        if rr:
            conditions[f"img{pair[0]:g}_txt{pair[1]:g}"] = {
                "n": len(rr), "optimal_image_weight": rr[0]["optimal_image_weight"],
                "mean_observed_image_weight": _mean([r["observed_image_weight"] for r in rr]),
                "mean_abs_weight_error": _mean([r["weight_abs_error"] for r in rr]),
            }
    cond_rows = list(conditions.values()); optimal = [x["optimal_image_weight"] for x in cond_rows]; observed = [x["mean_observed_image_weight"] for x in cond_rows]
    return {
        "n_predictions": len(prediction_rows), "n_weight_analyzable": len(rows),
        "image_readout_mae_vs_sample_mean": _mean([abs(r["image_only"] - r["image_sample_mean"]) for r in rows]),
        "text_readout_mae_vs_sample_mean": _mean([abs(r["text_only"] - r["text_sample_mean"]) for r in rows]),
        "combined_mae_vs_optimal": _mean([abs(r["combined"] - r["optimal_fused_estimate"]) for r in rows]),
        "mean_abs_weight_error": _mean([r["weight_abs_error"] for r in rows]),
        "reliability_weight_correlation": _correlation(optimal, observed),
        "extreme_weight_shift": observed[-1] - observed[0] if len(observed) == len(RELIABILITY_PAIRS) else None,
        "conditions": conditions,
    }


def main() -> None:
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("generate"); g.add_argument("--out-dir", default="stimuli"); g.add_argument("--manifest", default="data/manifest.jsonl"); g.add_argument("--seed", type=int, default=0); g.add_argument("--n-per-condition", type=int, default=12)
    r = sub.add_parser("run"); r.add_argument("--model", required=True); r.add_argument("--manifest", default="data/manifest.jsonl"); r.add_argument("--out", required=True); r.add_argument("--dtype", default="auto"); r.add_argument("--shard-index", type=int, default=0); r.add_argument("--num-shards", type=int, default=1)
    s = sub.add_parser("score"); s.add_argument("--manifest", default="data/manifest.jsonl"); s.add_argument("--predictions", required=True); s.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "generate":
        rows = generate(Path(args.out_dir), Path(args.manifest), args.seed, args.n_per_condition); result = {"n": len(rows), "manifest": args.manifest, "stimuli": args.out_dir}
    elif args.cmd == "run": result = run(args.model, Path(args.manifest), Path(args.out), args.dtype, args.shard_index, args.num_shards)
    else:
        result = score(Path(args.manifest), Path(args.predictions))
        if args.out: Path(args.out).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
