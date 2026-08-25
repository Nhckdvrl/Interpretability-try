from binding_probe.classify import binding_eligible_pairs, diagnose, literal_occurrences, parse_tool_call
from binding_probe.infer_hf import _load_ids


def sample():
    test = {
        "id": "x",
        "question": [[{"role": "user", "content": "Get directions from Tokyo to Osaka."}]],
        "function": [{
            "name": "route",
            "description": "route",
            "parameters": {
                "type": "dict",
                "properties": {
                    "origin": {"type": "string"},
                    "destination": {"type": "string"},
                },
                "required": ["origin", "destination"],
            },
        }],
    }
    ans = {"id": "x", "ground_truth": [{"route": {"origin": ["Tokyo"], "destination": ["Osaka"]}}]}
    return test, ans


def test_parse_qwen_tool_call():
    raw = '<tool_call>\n{"name":"route","arguments":{"origin":"Tokyo","destination":"Osaka"}}\n</tool_call>'
    assert parse_tool_call(raw)["arguments"]["origin"] == "Tokyo"



def test_parse_bfcl_pythonish_call():
    raw = '[route.estimate_time(start_location="San Francisco", end_location="Los Angeles", stops=["Santa Barbara"])]'
    parsed = parse_tool_call(raw)
    assert parsed["name"] == "route.estimate_time"
    assert parsed["arguments"]["end_location"] == "Los Angeles"


def test_literal_occurrence_has_boundaries():
    assert literal_occurrences("US", "region is Australia") == 0
    assert literal_occurrences(1, "values 10 and 1") == 1


def test_eligibility_is_strict_and_direct_copy():
    test, ans = sample()
    pairs = binding_eligible_pairs(test, ans)
    assert len(pairs) == 1
    assert {pairs[0]["key_a"], pairs[0]["key_b"]} == {"origin", "destination"}


def test_correct():
    test, ans = sample()
    raw = '<tool_call>{"name":"route","arguments":{"origin":"Tokyo","destination":"Osaka"}}</tool_call>'
    d = diagnose(test, ans, raw)
    assert d["label"] == "correct"
    assert not d["strict_natural_binding"]


def test_pure_swap_is_strict_natural_binding():
    test, ans = sample()
    raw = '<tool_call>{"name":"route","arguments":{"origin":"Osaka","destination":"Tokyo"}}</tool_call>'
    d = diagnose(test, ans, raw)
    assert d["label"] == "pure_binding_permutation"
    assert d["reassignment"]["origin"] == "destination"
    assert d["strict_natural_binding"]


def test_wrong_value_not_binding():
    test, ans = sample()
    raw = '<tool_call>{"name":"route","arguments":{"origin":"Nagoya","destination":"Osaka"}}</tool_call>'
    assert diagnose(test, ans, raw)["label"] == "value_error"


def test_different_types_are_not_strict_binding():
    test, ans = sample()
    test["function"][0]["parameters"]["properties"]["destination"]["type"] = "integer"
    raw = '<tool_call>{"name":"route","arguments":{"origin":"Osaka","destination":"Tokyo"}}</tool_call>'
    d = diagnose(test, ans, raw)
    assert d["label"] == "pure_binding_permutation"
    assert not d["strict_natural_binding"]


def test_load_ids_accepts_jsonl(tmp_path):
    p = tmp_path / "ids.jsonl"
    p.write_text('{"id":"a","pairs":[]}\n{"id":"b","pairs":[]}\n', encoding="utf-8")
    assert _load_ids(str(p)) == {"a", "b"}
