from cross_modal_inertia.build_bank import gold_index, strip_label


def test_source_answer_mapping_and_label_stripping():
    row = {"id": 1, "options": ["A.Yes.", "B. No."], "answer": "B. No."}
    assert gold_index(row) == 1
    assert strip_label("A.Yes.") == "Yes."
    assert strip_label("B. No.") == "No."
