import json
from pathlib import Path

from mixed_status_attraction.prompts import build_messages, option_mapping


CONTRACT = json.loads((Path(__file__).parents[1] / "configs" / "d0_contract.json").read_text())
ROW = {
    "title": "Example",
    "target_local": "Sentence 1: They <TARGET_EVENT>left</TARGET_EVENT>.",
    "same_status_natural": "same",
    "same_status_reversed": "same reversed",
    "mixed_status_natural": "mixed",
    "mixed_status_reversed": "mixed reversed",
    "full_local_discourse": "full",
    "target_label": "CT+",
}


def test_options_reverse_without_changing_definitions():
    canonical, canonical_map = option_mapping(CONTRACT, "canonical")
    reversed_options, reversed_map = option_mapping(CONTRACT, "reversed")
    assert [label for _, label, _ in canonical] == list(reversed([label for _, label, _ in reversed_options]))
    assert canonical_map["CT+"] == "A"
    assert reversed_map["CT+"] == "E"


def test_prompt_never_exposes_annotation_codes():
    messages, mapping = build_messages(ROW, "target_local", "canonical", CONTRACT)
    text = "\n".join(message["content"] for message in messages)
    assert mapping["CT+"] == "A"
    for code in CONTRACT["label_order"]:
        assert code not in text
    assert "<TARGET_EVENT>left</TARGET_EVENT>" in text
