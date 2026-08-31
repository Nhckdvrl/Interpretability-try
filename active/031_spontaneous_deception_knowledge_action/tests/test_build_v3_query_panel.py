import importlib.util
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "scripts" / "build_v3_query_panel.py"
SPEC = importlib.util.spec_from_file_location("build_v3_query_panel", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_queries_hold_graph_fixed_and_vary_truth():
    problem = {
        "problem": "Old query\nFacts:\nA can contact B\nC can contact D",
        "linked_list": ["A", "B", "C", "D"],
        "broken_edges": ["B -> C"],
    }
    rows = MODULE.make_rows(problem, 7, "train")
    assert len(rows) == 6
    assert sum(row["reachable"] for row in rows) == 4
    assert sum(row["expected_answer"] == "Yes" for row in rows) == 3
    for query_type in MODULE.QUERY_TYPES:
        pair = [row for row in rows if row["query_type"] == query_type]
        assert pair[0]["reachable"] == pair[1]["reachable"]
        assert pair[0]["expected_answer"] != pair[1]["expected_answer"]
