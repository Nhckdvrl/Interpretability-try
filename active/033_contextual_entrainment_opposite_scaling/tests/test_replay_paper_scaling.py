from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "replay_paper_scaling.py"
SPEC = spec_from_file_location("replay_paper_scaling", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_replays_opposite_scaling_signs() -> None:
    result = MODULE.replay()
    assert result["semantic_negative"] is True
    assert result["nonsemantic_positive"] is True
    for condition in result["conditions"].values():
        assert condition["absolute_exponent_difference"] < 0.01
