import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "run_v2_transplant_preflight.py"
SPEC = importlib.util.spec_from_file_location("run_v2_transplant_preflight", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_summarize_records_reports_rescue_and_delta():
    rows = [
        {"layer": 2, "intervention": "x", "base_margin": -2.0, "patched_margin": 1.0},
        {"layer": 2, "intervention": "x", "base_margin": -1.0, "patched_margin": -0.5},
    ]
    summary = MODULE.summarize_records(rows)["layer_2/x"]
    assert summary["rescue_rate"] == 0.5
    assert summary["mean_margin_delta"] == 1.75
