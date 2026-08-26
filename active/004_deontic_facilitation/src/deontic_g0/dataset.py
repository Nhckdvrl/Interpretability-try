from __future__ import annotations

from dataclasses import dataclass, replace
import csv
from pathlib import Path
from typing import Iterable

MODALS = ("epistemic", "deontic")
FORMS = ("pos-pos", "pos-neg", "neg-pos", "neg-neg")
# Four cyclic rotations: each original card occupies each displayed position once.
CARD_PERMUTATIONS: tuple[tuple[int, int, int, int], ...] = (
    (0, 1, 2, 3),
    (1, 2, 3, 0),
    (2, 3, 0, 1),
    (3, 0, 1, 2),
)


@dataclass(frozen=True)
class WasonItem:
    item_id: int
    modal: str
    form: str
    rule: str
    cards: tuple[str, str, str, str]
    gold: tuple[int, int]  # 1-based displayed positions in canonical/original order

    @property
    def gold_label(self) -> str:
        return canonical_pair(self.gold)


@dataclass(frozen=True)
class PairedItems:
    pair_key: str
    form: str
    epistemic: WasonItem
    deontic: WasonItem


def canonical_pair(indices: Iterable[int]) -> str:
    values = sorted(int(x) for x in indices)
    if len(values) != 2 or values[0] == values[1] or not all(1 <= x <= 4 for x in values):
        raise ValueError(f"invalid card pair: {values}")
    return f"{values[0]},{values[1]}"


def load_wason(path: str | Path, *, strict_official: bool = True) -> list[WasonItem]:
    path = Path(path)
    rows: list[WasonItem] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        expected = {"ID", "modal", "form", "rule", "card-1", "card-2", "card-3", "card-4", "gold1", "gold2"}
        if set(reader.fieldnames or []) != expected:
            raise ValueError(f"unexpected TSV columns: {reader.fieldnames}")
        for row in reader:
            modal = row["modal"].strip()
            form = row["form"].strip()
            if modal not in MODALS:
                raise ValueError(f"unknown modal {modal!r}")
            if form not in FORMS:
                raise ValueError(f"unknown form {form!r}")
            item = WasonItem(
                item_id=int(row["ID"]),
                modal=modal,
                form=form,
                rule=row["rule"].strip(),
                cards=tuple(row[f"card-{i}"].strip() for i in range(1, 5)),  # type: ignore[arg-type]
                gold=tuple(sorted((int(row["gold1"]), int(row["gold2"])))),  # type: ignore[arg-type]
            )
            canonical_pair(item.gold)
            if any(not card for card in item.cards) or not item.rule:
                raise ValueError(f"empty text in item {item.item_id}")
            rows.append(item)

    ids = [x.item_id for x in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate IDs in Wason data")

    if strict_official:
        if len(rows) != 160:
            raise ValueError(f"expected 160 official EACL 2026 items, found {len(rows)}")
        for modal in MODALS:
            for form in FORMS:
                n = sum(x.modal == modal and x.form == form for x in rows)
                if n != 20:
                    raise ValueError(f"expected 20 items for {modal}/{form}, found {n}")
    return rows


def permute_item(item: WasonItem, permutation: tuple[int, int, int, int]) -> WasonItem:
    if tuple(sorted(permutation)) != (0, 1, 2, 3):
        raise ValueError(f"invalid permutation: {permutation}")
    cards = tuple(item.cards[i] for i in permutation)
    # original 1-based position -> displayed 1-based position
    inverse = {orig + 1: shown + 1 for shown, orig in enumerate(permutation)}
    gold = tuple(sorted(inverse[g] for g in item.gold))
    return replace(item, cards=cards, gold=gold)  # type: ignore[arg-type]


def pair_official_items(items: Iterable[WasonItem]) -> list[PairedItems]:
    """Pair official rows by polarity form and within-block ordinal.

    The EACL dataset contains 20 epistemic and 20 deontic rows for each logical
    form. They are not semantic minimal pairs, so pairing is used only for a
    balanced, form-stratified effect estimate—not as a claim of lexical matching.
    """
    items = list(items)
    pairs: list[PairedItems] = []
    for form in FORMS:
        epi = sorted((x for x in items if x.form == form and x.modal == "epistemic"), key=lambda x: x.item_id)
        deo = sorted((x for x in items if x.form == form and x.modal == "deontic"), key=lambda x: x.item_id)
        if len(epi) != len(deo):
            raise ValueError(f"unbalanced modal counts for {form}: {len(epi)} vs {len(deo)}")
        for ordinal, (e, d) in enumerate(zip(epi, deo), start=1):
            pairs.append(PairedItems(pair_key=f"{form}:{ordinal:02d}", form=form, epistemic=e, deontic=d))
    return pairs
