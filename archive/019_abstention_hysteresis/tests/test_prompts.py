from abstention_hysteresis.prompts import final_payload, messages


ITEM = {
    "question": "Who won?",
    "full_evidence": [{"title": "Full", "text": "Ada won."}],
    "incomplete_evidence": [{"title": "Other", "text": "The event occurred."}],
}


def test_final_payload_is_verbatim_across_histories():
    expected = final_payload(ITEM)
    for condition in ("direct_full", "self_abstention", "teacher_abstention",
                      "paraphrased_abstention", "neutral_same_context", "answered_history"):
        conversation = messages(ITEM, condition, "ABSTAIN: missing winner")
        assert conversation[-1]["content"] == expected


def test_self_history_preserves_generated_text():
    conversation = messages(ITEM, "self_abstention", "ABSTAIN: no winner")
    assert conversation[-2]["content"] == "ABSTAIN: no winner"
