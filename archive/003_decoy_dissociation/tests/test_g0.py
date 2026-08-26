from decoy_g0.dataset import DOMAINS, dominates, generate_scenarios
from decoy_g0.metrics import G0Thresholds, aggregate, summarize_scenarios
from decoy_g0.prompts import build_choice_cases, build_dominance_cases
from decoy_g0.scoring import HFChoiceScorer


def test_all_generated_decoys_are_strictly_dominated():
    scenarios = generate_scenarios(strengths=(0.1,))
    assert len(scenarios) > 100
    for s in scenarios:
        target = s.a if s.target == "A" else s.b
        assert dominates(target, s.decoy)
        assert not dominates(s.decoy, target)
        assert not dominates(s.a, s.b)
        assert not dominates(s.b, s.a)


def test_prompt_permutations_are_complete_and_semantically_invariant():
    s = generate_scenarios(strengths=(0.1,), domains=(DOMAINS[0],))[0]
    choices = build_choice_cases(s)
    dom = build_dominance_cases(s)
    assert len(choices) == 3 * (2 + 6)
    assert len(dom) == 2
    for c in choices:
        expected = {"A", "B"} if c.kind == "binary" else {"A", "B", "C"}
        assert set(c.semantic_by_label.values()) == expected


def _row(sid, kind, semantic, probs, case_id):
    return {"scenario_id": sid, "kind": kind, "semantic_by_label": semantic, "probs": probs, "case_id": case_id}


def test_strong_reversal_requires_all_gates():
    s = generate_scenarios(strengths=(0.1,), domains=(DOMAINS[0],))[0]
    sid = s.scenario_id
    target = s.target
    competitor = "B" if target == "A" else "A"
    rows = [
        _row(sid, "dominance", {"A": "target", "B": "decoy"}, {"A": 0.95, "B": 0.05}, "d1"),
        _row(sid, "dominance", {"A": "decoy", "B": "target"}, {"A": 0.05, "B": 0.95}, "d2"),
    ]
    for i in range(6):
        rows.append(_row(sid, "binary", {"A": target, "B": competitor}, {"A": 0.25, "B": 0.75}, f"b{i}"))
    for i in range(18):
        rows.append(_row(sid, "ternary", {"A": target, "B": competitor, "C": "C"}, {"A": 0.72, "B": 0.23, "C": 0.05}, f"t{i}"))
    verdicts = summarize_scenarios(rows, {sid: s.to_dict()}, G0Thresholds())
    assert len(verdicts) == 1
    assert verdicts[0].strong_reversal
    assert aggregate(verdicts)["overall"]["n_strong_reversal"] == 1


def test_scorer_does_not_insert_space_before_exact_label():
    class Encoded:
        def __init__(self, ids):
            self.input_ids = ids

    class RecordingTokenizer:
        def __init__(self):
            self.seen = []

        def __call__(self, text, add_special_tokens=False):
            self.seen.append(text)
            table = {"prefix\n": [1], "prefix\nA": [1, 32]}
            return Encoded(table[text])

    scorer = object.__new__(HFChoiceScorer)
    scorer.tokenizer = RecordingTokenizer()
    scorer._chat_prefix = lambda prompt: "prefix\n"

    ids, prefix_len = scorer._encode_pair("ignored", "A")

    assert scorer.tokenizer.seen == ["prefix\n", "prefix\nA"]
    assert ids == [1, 32]
    assert prefix_len == 1
