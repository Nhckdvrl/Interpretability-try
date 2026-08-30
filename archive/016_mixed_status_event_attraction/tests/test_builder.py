from mixed_status_attraction.build_bank import compact_pair, relation_index, render_sentences


def mention(mid, eid, label, sent):
    return {
        "doc_id": "d",
        "source_split": "train",
        "mention_id": mid,
        "event_id": eid,
        "event_type": "Test",
        "sent_id": sent,
        "factuality": label,
    }


def test_pair_is_directional():
    left = mention("m1", "e1", "CT+", 0)
    right = mention("m2", "e2", "PS+", 1)
    forward = compact_pair(left, right, [])
    backward = compact_pair(right, left, [])
    assert forward["direction"] == "CT+->PS+"
    assert backward["direction"] == "PS+->CT+"
    assert forward["pair_id"] != backward["pair_id"]


def test_relation_index_keeps_relation_types():
    doc = {
        "temporal_relations": {"BEFORE": [["EVENT_a", "EVENT_b"]]},
        "causal_relation": {"CAUSE": [["EVENT_a", "EVENT_b"]]},
        "subevent_relations": [],
    }
    relations = relation_index(doc)[frozenset(("EVENT_a", "EVENT_b"))]
    assert set(relations) == {"temporal:BEFORE", "causal:CAUSE"}


def test_sentence_rendering_marks_exact_offset():
    doc = {"tokens": [["They", "might", "leave", "."]]}
    text = render_sentences(doc, [0], {0: [(2, 3, "TARGET_EVENT")]})
    assert "<TARGET_EVENT> leave </TARGET_EVENT>" in text
