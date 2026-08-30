from abstention_hysteresis.build_bank import answer_leaks, normalize


def test_normalize_matches_qa_evaluation_style():
    assert normalize("Miquette_Giraudy!") == "miquette giraudy"


def test_answer_leak_is_word_bounded():
    paragraphs = [{"text": "A cartoon concerns images."}]
    assert not answer_leaks("art", [], paragraphs)
    assert answer_leaks("cartoon", [], paragraphs)
