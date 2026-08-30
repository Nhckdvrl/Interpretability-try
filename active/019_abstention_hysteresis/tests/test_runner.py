from abstention_hysteresis.run_model import answer_scores, extracted_answer, is_abstention


ITEM = {"answer": "Ada Lovelace", "answer_aliases": ["Lovelace"]}


def test_protocol_parser():
    assert is_abstention("ABSTAIN: not enough evidence")
    assert extracted_answer("ANSWER: Ada Lovelace") == "Ada Lovelace"
    assert answer_scores("ANSWER: Lovelace", ITEM)[2]
    assert not answer_scores("ANSWER: Ada", ITEM)[2]


def test_token_f1_accepts_common_dataset_alias_omission():
    item = {"answer": "Louis-Hector Berlioz", "answer_aliases": []}
    exact, f1, correct = answer_scores("Hector Berlioz", item)
    assert not exact and f1 == .8 and correct
