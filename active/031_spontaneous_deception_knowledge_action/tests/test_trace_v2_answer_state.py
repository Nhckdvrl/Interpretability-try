import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "trace_v2_answer_state.py"
SPEC = importlib.util.spec_from_file_location("trace_v2_answer_state", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_layer_summary_groups_conditions():
    margins = np.asarray([[1.0, 2.0], [-1.0, 0.0], [3.0, 4.0]])
    summary = MODULE.layer_summary(margins, ["a", "b", "a"])
    assert summary["a"]["n"] == 2
    assert summary["a"]["mean_correct_minus_wrong"] == [2.0, 3.0]
    assert summary["b"]["fraction_correct_margin_positive"] == [0.0, 0.0]
