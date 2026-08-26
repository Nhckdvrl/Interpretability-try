from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from deontic_g0.dataset import CARD_PERMUTATIONS, FORMS, WasonItem, canonical_pair, load_wason, pair_official_items, permute_item
from deontic_g0.prompts import CANDIDATES, build_prompt


def _write_official_like(path: Path) -> None:
    fields = ["ID", "modal", "form", "rule", "card-1", "card-2", "card-3", "card-4", "gold1", "gold2"]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t")
        w.writeheader()
        i = 1
        for form in FORMS:
            for modal in ("epistemic", "deontic"):
                for j in range(20):
                    w.writerow({"ID": i, "modal": modal, "form": form, "rule": f"If P{i}, then Q{i}.", "card-1": "P", "card-2": "not P", "card-3": "Q", "card-4": "not Q", "gold1": 1, "gold2": 4})
                    i += 1


def test_candidates_are_all_six_unordered_pairs() -> None:
    assert CANDIDATES == ("1,2", "1,3", "1,4", "2,3", "2,4", "3,4")


def test_card_rotation_preserves_gold_semantics() -> None:
    item = WasonItem(1, "epistemic", "pos-pos", "If P then Q", ("P", "not P", "Q", "not Q"), (1, 4))
    seen_positions = {i: set() for i in range(1, 5)}
    for perm in CARD_PERMUTATIONS:
        shown = permute_item(item, perm)
        assert canonical_pair(shown.gold) in CANDIDATES
        for displayed, original_zero in enumerate(perm, start=1):
            seen_positions[original_zero + 1].add(displayed)
    assert all(v == {1, 2, 3, 4} for v in seen_positions.values())


def test_prompt_demands_exact_pair() -> None:
    item = WasonItem(1, "epistemic", "pos-pos", "If P then Q", ("P", "not P", "Q", "not Q"), (1, 4))
    p = build_prompt(item, 0)
    assert "exactly" in p.lower()
    assert "1. P" in p


def test_strict_loader_checks_full_balance(tmp_path: Path) -> None:
    path = tmp_path / "wason.tsv"
    _write_official_like(path)
    rows = load_wason(path, strict_official=True)
    assert len(rows) == 160
    assert len(pair_official_items(rows)) == 80


def test_loader_rejects_nonofficial_count(tmp_path: Path) -> None:
    path = tmp_path / "wason.tsv"
    _write_official_like(path)
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(lines[:-1]) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="expected 160"):
        load_wason(path, strict_official=True)
