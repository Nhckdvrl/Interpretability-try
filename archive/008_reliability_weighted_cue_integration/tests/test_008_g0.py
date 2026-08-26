import importlib.util
import json
from pathlib import Path


spec = importlib.util.spec_from_file_location("g0_008", Path(__file__).parents[1] / "g0.py")
g0 = importlib.util.module_from_spec(spec); spec.loader.exec_module(g0)


def test_inverse_variance_weight():
    assert abs(g0.optimal_image_weight(2, 8) - 16/17) < 1e-12
    assert abs(g0.optimal_image_weight(8, 2) - 1/17) < 1e-12
    assert g0.parse_number("work: 12 + 14; final answer: 13") == 13


def test_generator_hides_sigma_and_keeps_cue_means_separated(tmp_path):
    rows = g0.generate(tmp_path / "images", tmp_path / "manifest.jsonl", seed=0, n_per_condition=2)
    assert len(rows) == 10
    assert all(abs(x["image_sample_mean"] - x["text_sample_mean"]) >= 4 for x in rows)
    assert all("standard deviation" not in p.lower() for x in rows for p in g0.prompts(x).values())


def test_oracle_like_predictions_score_as_reliability_sensitive(tmp_path):
    rows = g0.generate(tmp_path / "images", tmp_path / "manifest.jsonl", seed=2, n_per_condition=2)
    preds = []
    for x in rows:
        preds.append({"id": x["id"], "image_only": x["image_sample_mean"], "text_only": x["text_sample_mean"], "combined": x["optimal_fused_estimate"]})
    pred_path = tmp_path / "pred.jsonl"
    pred_path.write_text("\n".join(json.dumps(x) for x in preds) + "\n")
    summary = g0.score(tmp_path / "manifest.jsonl", pred_path)
    assert summary["mean_abs_weight_error"] < 1e-10
    assert summary["reliability_weight_correlation"] > .999
