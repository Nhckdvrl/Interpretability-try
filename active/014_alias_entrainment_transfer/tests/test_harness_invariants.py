"""Invariants that must hold for the 014 phase-1 result to mean anything."""
import json
import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from alias_entrainment.build_d0 import is_acronym, norm, orth_sim, stratum, strict_stratum
from alias_entrainment.run_phase1 import CONDITIONS, build_prompt, mention_for


@pytest.fixture(scope="module")
def items():
    return [json.loads(l) for l in (ROOT / "data" / "frozen_d0.jsonl").open()]


def test_target_string_never_appears_in_alias_condition(items):
    """The whole experiment rests on this: in ALIAS the scored string is absent."""
    for it in items:
        for c in it["carriers"]:
            for tpl in it["frames"].values():
                prompt = build_prompt(tpl.format(M=mention_for(it, "ALIAS")), c["question"])
                assert norm(it["target_form"]) not in norm(prompt), it["item_id"]


def test_exact_condition_does_contain_the_target(items):
    for it in items:
        tpl = next(iter(it["frames"].values()))
        prompt = build_prompt(tpl.format(M=mention_for(it, "EXACT")), it["carriers"][0]["question"])
        assert norm(it["target_form"]) in norm(prompt)


def test_controls_are_not_coreferent(items):
    for it in items:
        for cond in ("SEMREL", "UNREL"):
            m = mention_for(it, cond)
            assert norm(m) != norm(it["target_form"])
            assert norm(m) != norm(it["seen_form"])


def test_neither_form_contains_the_other(items):
    for it in items:
        a, b = norm(it["seen_form"]), norm(it["target_form"])
        assert a not in b and b not in a, it["item_id"]


def test_semrel_is_never_orthographically_closer_than_the_alias(items):
    """Otherwise SEMREL silently stops being a semantic control."""
    for it in items:
        assert it["orth_semrel_target"] <= max(it["orth_alias_target"], 0.25) + 1e-9


def test_opaque_strict_stratum_is_actually_strict(items):
    for it in items:
        if it["strict_stratum"] == "opaque_strict":
            assert it["orth_alias_target"] < 0.40
            assert not (set(it["seen_form"].lower().split()) & set(it["target_form"].lower().split()))


def test_carrier_gold_is_never_the_target(items):
    for it in items:
        for c in it["carriers"]:
            assert norm(c["gold"]) != norm(it["target_form"])


def test_acronym_and_stratum_logic():
    assert is_acronym("IBM", "International Business Machines")
    assert is_acronym("USA", "United States of America")
    assert not is_acronym("Mumbai", "Bombay")
    assert stratum("IBM", "International Business Machines") == "acronym"
    assert stratum("Charlie Chaplin", "Charles Chaplin") == "partial"
    assert stratum("Bombay", "Mumbai") == "opaque"
    # char-similar opaque pairs are deliberately NOT admitted to opaque_strict
    assert strict_stratum("Italia", "Italy") == "opaque"           # orth 0.73
    assert strict_stratum("Bombay", "Mumbai") == "opaque"          # orth 0.50
    assert strict_stratum("Katheryn Hudson", "Katy Perry") == "opaque"   # orth 0.52
    assert strict_stratum("CCCP", "Soviet Union") == "opaque_strict"       # orth 0.00
    assert strict_stratum("Mr Bean", "Rowan Atkinson") == "opaque_strict"  # orth 0.32
    assert orth_sim("Italia", "Italy") > orth_sim("Bombay", "Mumbai")


def test_every_item_has_all_conditions_and_a_baseline():
    res = ROOT / "results" / "phase1_r1" / "llama31_8b_it__main.jsonl"
    if not res.exists():
        pytest.skip("phase-1 results not present")
    seen = {}
    for line in res.open():
        r = json.loads(line)
        seen.setdefault(r["item_id"], set()).add(r["condition"])
    for iid, conds in seen.items():
        assert conds == {"NOCTX", *CONDITIONS}, iid
