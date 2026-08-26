import importlib.util
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[1]))
spec = importlib.util.spec_from_file_location("latitude_g0", Path(__file__).parents[1] / "latitude_g0.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_role_serialization_separates_ownership_only():
    case = {"stage1_prompt": "Question"}
    own = module.stage2_messages(case, "own", "A", "neutral")
    hidden = module.stage2_messages(case, "hidden", "A", "neutral")
    other = module.stage2_messages(case, "other", "A", "neutral")
    assert own[0] == hidden[0] == other[0]
    assert own[1]["content"].endswith("A")
    assert hidden[1]["content"].endswith("xx")
    assert "Another language model" in other[2]["content"]


def test_summary_reports_ownership_specific_not_visibility_only():
    row = {"gold": "A", "initial": "A"}
    for key, p in (("neutral_hidden", .5), ("neutral_own", .8), ("neutral_other", .55), ("opposing_hidden", .7), ("opposing_own", .3), ("opposing_other", .65)):
        row[f"{key}_probs"] = {"A": p if key.startswith("neutral") else 1-p, "B": 1-p if key.startswith("neutral") else p}
    summary = module.summarize([row])
    assert abs(summary["neutral_ownership_specific_boost_own_minus_other"] - .25) < 1e-12
    assert abs(summary["opposing_revision_resistance_hidden_minus_own"] - .4) < 1e-12
