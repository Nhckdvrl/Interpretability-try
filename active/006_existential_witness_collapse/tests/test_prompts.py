from witness_collapse_g0.prompts import (
    ACTION_ORDERS,
    SEMANTIC_ORDERS,
    downstream_prompt,
    recognition_prompt,
)


def _recognition(probe: str, mapping: dict[str, str]):
    return recognition_prompt(
        premise_p="At least one analyst reviewed file A.",
        premise_q="At least one analyst reviewed file B.",
        p_property="reviewed file A",
        q_property="reviewed file B",
        probe=probe,
        mapping=mapping,
    )


def test_recognition_uses_semantic_options_not_yes_no():
    for probe in ("p_exists", "q_exists", "shared_entailment", "identity_determined"):
        prompt, _ = _recognition(probe, SEMANTIC_ORDERS[0])
        assert "A. Yes" not in prompt
        assert "B. Yes" not in prompt
        assert "A. No" not in prompt
        assert "B. No" not in prompt


def test_gold_label_is_counterbalanced_for_semantic_options():
    labels = [_recognition("shared_entailment", mapping)[1] for mapping in SEMANTIC_ORDERS]
    assert labels == ["A", "B"]


def test_identity_probes_require_both_same_and_distinct_to_remain_unestablished():
    same_prompt, _ = _recognition("shared_entailment", SEMANTIC_ORDERS[0])
    distinct_prompt, _ = _recognition("identity_determined", SEMANTIC_ORDERS[0])
    assert "shared witness remains possible but unproven" in same_prompt
    assert "does not establish that the two witnesses are different individuals" in distinct_prompt
    assert "shared-witness world" in distinct_prompt and "distinct-witness world" in distinct_prompt


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
    assert "What does the record establish about a single shared witness?" not in prompt
