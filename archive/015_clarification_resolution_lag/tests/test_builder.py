from clarification_lag.build_bank import (
    choose_matched_pairs,
    enumerate_pairs,
    flatten_source,
    stratified_smoke_sample,
)


def source_rows():
    return [
        {
            "id": "q1",
            "question": "Where is Springfield?",
            "ctxs": [],
            "properties": [
                {"condition": "The city in Illinois", "groundtruth": "Illinois, USA"},
                {"condition": "The city in Queensland", "groundtruth": "Queensland, Australia"},
                {"condition": "The fictional city", "groundtruth": "The Simpsons universe"},
            ],
        },
        {
            "id": "q2",
            "question": "Single interpretation",
            "ctxs": [],
            "properties": [{"condition": "Only", "groundtruth": "One"}],
        },
    ]


def test_preserves_raw_and_all_ordered_directions():
    questions, properties = flatten_source(source_rows())
    pairs = enumerate_pairs(properties)
    assert len(questions) == 2
    assert len(properties) == 4
    assert len(pairs) == 3 * 2
    assert {(p["target_property_index"], p["distractor_property_index"]) for p in pairs} == {
        (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1)
    }


def test_one_distractor_per_target_is_separate_matched_layer():
    _, properties = flatten_source(source_rows())
    pairs = enumerate_pairs(properties)
    matched = choose_matched_pairs(pairs)
    assert len(pairs) == 6
    assert len(matched) == 3
    assert {p["target_property_index"] for p in matched} == {0, 1, 2}


def test_containment_is_validity_exclusion_not_raw_deletion():
    rows = source_rows()
    rows[0]["properties"][1]["groundtruth"] = "Illinois, USA and nearby areas"
    _, properties = flatten_source(rows)
    pairs = enumerate_pairs(properties)
    assert len(pairs) == 6
    assert any("answer_string_containment" in p["validity_exclusion_reasons"] for p in pairs)


def test_smoke_sample_is_deterministic():
    _, properties = flatten_source(source_rows())
    matched = choose_matched_pairs(enumerate_pairs(properties))
    assert stratified_smoke_sample(matched, 2, 7) == stratified_smoke_sample(matched, 2, 7)
