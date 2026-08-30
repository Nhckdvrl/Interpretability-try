import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alignment_arbitration.build_bank import build, payoff


def test_payoff_tables_match_published_rules():
    assert payoff("PD", "F", "J") == 10
    assert payoff("PD", "J", "F") == 0
    assert payoff("BoS", "F", "F") == 10
    assert payoff("BoS", "J", "J") == 7


def test_history_excludes_current_decision():
    rows = []
    for game in ["PD", "BoS"]:
        for _ in range(10):
            rows.append(
                {
                    "id": "1",
                    "game": game,
                    "action": "0",
                    "score": "5" if game == "PD" else "10",
                    "opponent": "Base",
                    "guess": "LLM",
                    "coordination": "1",
                }
            )
    bank = build(rows)
    pd = [row for row in bank if row["game"] == "PD"]
    assert [len(row["history"]) for row in pd] == list(range(10))
    assert pd[0]["human_action"] == "F"
    assert pd[-1]["history"][-1]["round"] == 9


def test_contract_has_four_strict_pairs():
    contract = json.loads((ROOT / "configs" / "d0_contract.json").read_text())
    assert set(contract["models"]) == {"qwen", "gemma", "llama", "mistral"}
    for pair in contract["models"].values():
        assert set(pair) == {"base", "aligned"}
        assert pair["base"] != pair["aligned"]
