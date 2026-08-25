from pathlib import Path

import pandas as pd

from facts_shortcuts_g0.preflight import GateConfig, classify_cases, evaluate_gate, load_merged_dataset


def _row(**overrides):
    row = {
        "entity1_qid": "Q1",
        "entity1_name": "Alpha",
        "entity1_value": 100.0,
        "entity1_qrank": 10.0,
        "entity2_qid": "Q2",
        "entity2_name": "Beta",
        "entity2_value": 200.0,
        "entity2_qrank": 100.0,
        "prompt_expects_larger_entity": True,
        "predicted_entity": "Beta",
        "entity1_predicted_value": 110.0,
        "entity2_predicted_value": 190.0,
    }
    row.update(overrides)
    return row


def test_strict_failure_requires_correct_numex_direction_and_wrong_pairwise():
    df = pd.DataFrame([
        _row(predicted_entity="Alpha"),
        _row(predicted_entity="Beta"),
        _row(predicted_entity="Alpha", entity1_predicted_value=300.0, entity2_predicted_value=190.0),
    ])
    out = classify_cases(df)
    assert out["strict_failure"].tolist() == [True, False, False]
    assert out["facts_available"].tolist() == [True, True, False]


def test_prompt_polarity_is_respected():
    df = pd.DataFrame([
        _row(prompt_expects_larger_entity=False, predicted_entity="Beta"),
        _row(prompt_expects_larger_entity=False, predicted_entity="Alpha"),
    ])
    out = classify_cases(df)
    assert out["strict_failure"].tolist() == [True, False]


def test_unknown_and_ties_are_not_eligible():
    df = pd.DataFrame([
        _row(predicted_entity="Unknown"),
        _row(entity1_predicted_value=100.0, entity2_predicted_value=100.0),
        _row(entity1_value=100.0, entity2_value=100.0),
    ])
    out = classify_cases(df)
    assert out["eligible"].tolist() == [False, False, False]
    assert not out["strict_failure"].any()


def test_popularity_alignment_is_descriptive_not_part_of_failure_definition():
    df = pd.DataFrame([
        _row(predicted_entity="Alpha", entity1_qrank=500.0, entity2_qrank=10.0),
        _row(predicted_entity="Alpha", entity1_qrank=10.0, entity2_qrank=500.0),
    ])
    out = classify_cases(df)
    assert out["strict_failure"].tolist() == [True, True]
    assert out["predicted_more_popular"].tolist() == [True, False]


def test_load_merge_matches_lowest_perplexity_rule(tmp_path: Path):
    pairwise = pd.DataFrame([{
        "entity1_qid": "Q1", "entity1_name": "Alpha", "entity1_value": 100,
        "entity2_qid": "Q2", "entity2_name": "Beta", "entity2_value": 200,
        "prompt_expects_larger_entity": True, "predicted_entity": "Beta",
    }])
    pointwise = pd.DataFrame([
        {"qid": "Q1", "predicted_value": 120, "perplexity": 3.0},
        {"qid": "Q1", "predicted_value": 105, "perplexity": 1.0},
        {"qid": "Q2", "predicted_value": 210, "perplexity": 2.0},
        {"qid": "Q2", "predicted_value": None, "perplexity": 0.5},
    ])
    p1, p2 = tmp_path / "pair.csv", tmp_path / "point.csv"
    pairwise.to_csv(p1, index=False)
    pointwise.to_csv(p2, index=False)
    merged = load_merged_dataset(p1, p2)
    assert merged.loc[0, "entity1_predicted_value"] == 105
    assert merged.loc[0, "entity2_predicted_value"] == 210


def test_gate_stops_when_natural_failures_are_rare():
    summary = pd.DataFrame([
        {"facts_available": 400, "strict_failures": 3, "strict_failure_rate_given_facts": 3 / 400},
        {"facts_available": 400, "strict_failures": 4, "strict_failure_rate_given_facts": 4 / 400},
    ])
    assert evaluate_gate(summary, GateConfig()).verdict == "STOP_TOO_FEW_NATURAL_FAILURES"


def test_gate_passes_only_when_replicated():
    summary = pd.DataFrame([
        {"facts_available": 300, "strict_failures": 30, "strict_failure_rate_given_facts": 0.10},
        {"facts_available": 300, "strict_failures": 25, "strict_failure_rate_given_facts": 0.083},
    ])
    assert evaluate_gate(summary, GateConfig()).verdict == "PASS_BEHAVIOR_G0"
