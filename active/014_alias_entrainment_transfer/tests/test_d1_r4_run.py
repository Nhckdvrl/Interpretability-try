import json
from pathlib import Path

from alias_entrainment.analyze_d1_r4 import entity_equal_boot
from alias_entrainment.run_d1_r4 import condition_mentions, make_main_jobs, make_probe_jobs


def item():
    return {
        "item_id": "Q1::p::alias_to_canonical",
        "target_form": "International Business Machines",
        "seen_form": "IBM",
        "assoc_any": "Microsoft",
        "assoc_sametype": "Apple",
        "identity_probe_foil": "General Electric",
        "frames": {"F1": "{M} was reported.", "F2": "News mentioned {M}."},
    }


def test_all_frozen_conditions_and_frames_are_materialized():
    jobs, keys = make_main_jobs([item()])
    assert len(jobs) == 9  # one NOCTX + four conditions x two frames
    assert {k["condition"] for k in keys} == {
        "NOCTX", "EXACT", "ALIAS", "ASSOC_ANY", "ASSOC_SAMETYPE"
    }
    assert {k["frame"] for k in keys if k["condition"] != "NOCTX"} == {"F1", "F2"}


def test_probe_is_counterbalanced_and_scores_both_letters():
    jobs, keys = make_probe_jobs([item()])
    assert len(jobs) == 4
    assert {(k["order"], k["letter"], k["gold"]) for k in keys} == {
        (0, "A", "A"), (0, "B", "A"), (1, "A", "B"), (1, "B", "B")
    }


def test_assoc_target_never_replaces_scored_continuation():
    jobs, _ = make_main_jobs([item()])
    assert all(cont == " International Business Machines" for _, cont in jobs)


def test_entity_equal_boot_does_not_overweight_many_aliases():
    result = entity_equal_boot({"Q1": [10.0, 10.0, 10.0], "Q2": [0.0]}, n_boot=100)
    assert result["estimate"] == 5.0
    assert result["n_entities"] == 2
    assert result["n_items"] == 4
