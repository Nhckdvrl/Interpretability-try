from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "run_v1_replay.py"
SPEC = spec_from_file_location("run_v1_replay", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_stratified_selection_is_reproducible() -> None:
    rows = []
    for variant in MODULE.VARIANTS:
        for cell in MODULE.CELLS:
            for index in range(5):
                rows.append({
                    "item_id": f"{variant}/{cell}/{index}",
                    "variant": variant,
                    "cell": cell,
                    "model": "m",
                    "length": 10,
                })
    first = MODULE.select_matched_sample(rows, source_model="m", length=10, n_per_cell=2, seed=7)
    second = MODULE.select_matched_sample(rows, source_model="m", length=10, n_per_cell=2, seed=7)
    assert first == second
    assert len(first) == 12


def test_answer_and_cell_scoring() -> None:
    assert MODULE.normalize_answer("The answer is Yes.") == "Yes"
    assert MODULE.classify(False, True) == "mother_deceptive"
