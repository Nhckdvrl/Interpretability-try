import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_v2_population.py"
SPEC = importlib.util.spec_from_file_location("build_v2_population", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_graph_state_finds_missing_edge_and_components():
    problem = {
        "linked_list": ["A", "B", "C", "D"],
        "broken_edges": ["B -> C"],
    }
    state = MODULE.graph_state(problem)
    assert state["missing_edge"] == "B -> C"
    assert state["missing_edge_index"] == 1
    assert state["source_component"] == ["A", "B"]
    assert state["target_component"] == ["C", "D"]
    assert state["reachable"] is False
    assert state["correct_answer"] == "No"


def test_graph_state_honors_explicit_followup_edges():
    problem = {
        "linked_list": ["A", "B", "C"],
        "broken_edges": ["A -> B"],
        "edges": ["B -> C"],
    }
    state = MODULE.graph_state(problem)
    assert state["present_edges"] == ["B -> C"]
    assert state["source_component"] == ["A"]
