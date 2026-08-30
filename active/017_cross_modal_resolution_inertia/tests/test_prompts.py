from cross_modal_inertia.prompts import (
    displayed_gold, final_messages, original_index, question_text, text_only_messages,
)


ITEM = {
    "question": "Ambiguous question?",
    "options": ["sense zero", "sense one"],
    "gold_index": 1,
    "image_path": "/tmp/example.jpg",
}


def test_order_counterbalance_preserves_original_mapping():
    assert displayed_gold(ITEM, "canonical") == "B"
    assert displayed_gold(ITEM, "reversed") == "A"
    assert original_index("A", "canonical") == 0
    assert original_index("A", "reversed") == 1


def test_image_path_is_identical_in_all_image_conditions():
    conditions = ["simultaneous", "matched_history", "image_first",
                  "text_first_actual_label", "text_first_actual_ordinal", "text_first_masked"]
    for condition in conditions:
        messages = final_messages(ITEM, "canonical", condition, "B")
        assert str(messages).count("/tmp/example.jpg") == 1


def test_ordinal_commitment_has_no_exact_answer_letter():
    messages = final_messages(ITEM, "canonical", "text_first_actual_ordinal", "B")
    assistant = messages[1]["content"]
    assert assistant == "My provisional choice is the second option."
    assert " B" not in assistant and "(B" not in assistant


def test_text_prompt_has_only_two_displayed_options():
    text = question_text(ITEM, "reversed")
    assert "(A) sense one" in text and "(B) sense zero" in text


def test_text_only_has_no_image():
    messages = text_only_messages(ITEM, "canonical")
    assert len(messages) == 1 and "/tmp/example.jpg" not in str(messages)
