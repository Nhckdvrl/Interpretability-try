import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "analyze_v3_reachability.py"
SPEC = importlib.util.spec_from_file_location("analyze_v3_reachability", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_auroc_handles_order_and_ties():
    assert MODULE.auroc([False, True], [0.0, 1.0]) == 1.0
    assert MODULE.auroc([False, True], [1.0, 0.0]) == 0.0
    assert MODULE.auroc([False, True], [1.0, 1.0]) == 0.5


def test_semantic_direction_points_to_reachable_mean():
    states = np.asarray([[0.0, 1.0], [2.0, 1.0], [4.0, 1.0]])
    labels = np.asarray([False, True, True])
    direction = MODULE.semantic_direction(states, labels, np.ones(3, dtype=bool))
    assert np.allclose(direction, [1.0, 0.0])
