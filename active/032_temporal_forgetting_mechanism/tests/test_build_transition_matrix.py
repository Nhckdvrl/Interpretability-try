from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "build_transition_matrix.py"
SPEC = spec_from_file_location("build_transition_matrix", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_builds_all_adjacent_transition_cells() -> None:
    rows = [
        {"item_id": "forget", "checkpoint_step": 32, "correct": True},
        {"item_id": "forget", "checkpoint_step": 64, "correct": False},
        {"item_id": "improve", "checkpoint_step": 32, "correct": False},
        {"item_id": "improve", "checkpoint_step": 64, "correct": True},
        {"item_id": "retain", "checkpoint_step": 32, "correct": True},
        {"item_id": "retain", "checkpoint_step": 64, "correct": True},
        {"item_id": "wrong", "checkpoint_step": 32, "correct": False},
        {"item_id": "wrong", "checkpoint_step": 64, "correct": False},
    ]
    result = MODULE.build(rows)
    assert result["adjacent_pairs"]["32->64"]["counts"] == {
        "C->C": 1, "C->W": 1, "W->C": 1, "W->W": 1
    }
