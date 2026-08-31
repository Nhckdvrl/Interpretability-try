import importlib.util
import sys
from pathlib import Path

import numpy as np


SCRIPT_DIR = Path(__file__).parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))
MODULE_PATH = SCRIPT_DIR / "analyze_v3_ridge_probe.py"
SPEC = importlib.util.spec_from_file_location("analyze_v3_ridge_probe", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_ridge_direction_generalizes_simple_signal():
    rng = np.random.default_rng(3)
    fit = rng.normal(size=(80, 5))
    validation = rng.normal(size=(40, 5))
    fit_labels = fit[:, 0] > 0
    validation_labels = validation[:, 0] > 0
    direction, alpha, validation_auc = MODULE.fit_ridge_direction(
        fit, fit_labels, validation, validation_labels
    )
    assert direction[0] > 0
    assert alpha in MODULE.ALPHAS
    assert validation_auc > 0.9
