from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "reconstruct_v0.py"
SPEC = spec_from_file_location("reconstruct_v0", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def test_normalize_answer_uses_final_yes_no() -> None:
    assert MODULE.normalize_answer("Reasoning... final answer: Yes.") == "Yes"
    assert MODULE.normalize_answer("NO!!!") == "No"
    assert MODULE.normalize_answer("unknown") is None


def test_graph_truth_for_positive_and_reverse_queries() -> None:
    connected = {"linked_list": ["A", "B", "C"], "broken_edges": []}
    broken = {"linked_list": ["A", "B", "C"], "broken_edges": ["B -> C"]}
    followup = {"linked_list": ["A", "B", "C"], "edges": ["A -> B"]}

    assert MODULE.graph_facts(connected, False)["expected_answer"] == "Yes"
    assert MODULE.graph_facts(broken, False)["expected_answer"] == "No"
    assert MODULE.graph_facts(broken, True)["expected_answer"] == "Yes"
    assert MODULE.graph_facts(followup, False)["reachable"] is False


def test_event_cells() -> None:
    assert MODULE.event_cell(False, True) == "mother_deceptive"
    assert MODULE.event_cell(True, False) == "hard_truthful"
    assert MODULE.event_cell(False, False) == "both_wrong"
