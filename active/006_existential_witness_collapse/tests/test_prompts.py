from witness_collapse_g0.prompts import ACTION_ORDERS, YES_NO_ORDERS, downstream_prompt, recognition_prompt


def test_shared_entailment_probe_gold_is_no_under_both_orders():
    labels = []
    for mapping in YES_NO_ORDERS:
        _, correct = recognition_prompt(
            premise_p="At least one analyst reviewed file A.",
            premise_q="At least one analyst reviewed file B.",
            p_property="reviewed A",
            q_property="reviewed B",
            probe="shared_entailment",
            mapping=mapping,
        )
        labels.append(correct)
    assert labels == ["B", "A"]


def test_downstream_is_action_use_not_duplicate_entailment_question():
    prompt, _ = downstream_prompt(
        context="RECORD:\nP\nQ",
        requirement="One analyst must have reviewed both files.",
        decision_context="A manager must decide whether to close the audit.",
        collapse_action="Close the audit as satisfied.",
        preserve_action="Keep it open pending identity evidence.",
        template="Which action is justified by the current record?",
        mapping=ACTION_ORDERS[0],
    )
    assert "Close the audit" in prompt and "Keep it open" in prompt
    assert "Do these two statements logically establish" not in prompt
