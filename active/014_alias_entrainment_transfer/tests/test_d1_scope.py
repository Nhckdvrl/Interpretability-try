"""Regression tests for the 2026-08-29 D1 r4 scope correction.

These tests are intentionally about the SCIENTIFIC POPULATION, not a particular
realized sample size.  They prevent a future builder edit from silently turning
the cross-surface question back into person-only / opaque-only / one-alias-only.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src" / "alias_entrainment"))

from build_d1_candidates import is_derivable, normu, structural_stratum


def test_compositional_surface_forms_are_retained_as_a_stratum():
    assert is_derivable("IBM", "International Business Machines")
    assert structural_stratum("IBM", "International Business Machines") == "compositional"
    assert is_derivable("Boeing", "Boeing Company")
    # A genuine opaque alias remains distinguishable from the compositional axis.
    assert not is_derivable("Katy Perry", "Katheryn Hudson")


def test_unicode_is_not_collapsed_to_the_old_ascii_only_population():
    assert normu("Beyoncé")
    assert normu("Beyoncé") != normu("Beyonce")
    assert normu("İstanbul")


def test_r4_contract_restores_broad_scope():
    text = (ROOT / "configs" / "contract_d1_r4.yaml").read_text()
    assert "entity_types: ALL" in text
    assert "directions: BOTH" in text
    assert "keep_multiple_surfaces_per_entity: true" in text
    assert "pageview_floor_for_construction: NONE" in text
    assert "ascii_only_filter: false" in text
    assert "compositional_filter: false" in text
    assert "primary_control: ASSOC_ANY" in text
    assert "construction_filter: false" in text  # hard identity gate is analysis-only


def test_candidate_builder_has_no_four_category_or_one_alias_gate():
    src = (ROOT / "src" / "alias_entrainment" / "build_d1_candidates.py").read_text()
    assert "PRIMARY_ALLOWED" not in src
    assert "exactly ONE redirect form per entity" not in src
    assert "is_compositional(s, target):" not in src
    assert "ASCII_OK.match" not in src


def test_final_bank_does_not_hardcode_the_old_person_strict_cell():
    src = (ROOT / "src" / "alias_entrainment" / "build_d1_bank.py").read_text()
    assert 'entity_type="person"' not in src
    assert 'stratum="opaque_strict"' not in src
    assert "alias_to_canonical" in src
    assert "canonical_to_alias" in src
    assert "ASSOC_SAMETYPE" in src or "assoc_sametype" in src


def test_stale_cooccurrence_cannot_be_consumed():
    src = (ROOT / "src" / "alias_entrainment" / "count_cooccurrence.py").read_text()
    bank = (ROOT / "src" / "alias_entrainment" / "build_d1_bank.py").read_text()
    assert 'COOC_VERSION = "d1-r4-cooc-v2"' in src
    assert "casefold" in src
    assert "old pre-fix shards are forbidden" in bank


def test_misleading_pre_r4_frozen_bank_is_gone():
    assert not (ROOT / "data" / "frozen_d1.jsonl").exists()
