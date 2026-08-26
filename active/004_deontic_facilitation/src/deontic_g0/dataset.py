from __future__ import annotations

from dataclasses import asdict, dataclass, replace
import itertools
import json
from pathlib import Path
from typing import Iterable

MODALS = ("epistemic", "deontic")
FORMS = ("pos-pos", "pos-neg", "neg-pos", "neg-neg")
# Full counterbalancing: every ordering of the four visible cards is evaluated.
CARD_PERMUTATIONS: tuple[tuple[int, int, int, int], ...] = tuple(itertools.permutations(range(4)))
GOLD_BY_FORM = {
    "pos-pos": (1, 4),
    "pos-neg": (1, 3),
    "neg-pos": (2, 4),
    "neg-neg": (2, 3),
}
FRAMES = (
    ("badge", "the badge is blue", "the badge is not blue", "the employee", "enter Gate A", "enters Gate A"),
    ("signal", "the signal is red", "the signal is not red", "the operator", "stop the conveyor", "stops the conveyor"),
    ("door", "the door is open", "the door is not open", "the guard", "log the inspection", "logs the inspection"),
    ("flag", "the flag is raised", "the flag is not raised", "the runner", "start the race", "starts the race"),
    ("ticket", "the ticket is marked priority", "the ticket is not marked priority", "the clerk", "review the file manually", "reviews the file manually"),
    ("alarm", "the alarm is sounding", "the alarm is not sounding", "the technician", "call the supervisor", "calls the supervisor"),
    ("vehicle", "the vehicle is in Zone A", "the vehicle is not in Zone A", "the driver", "present the permit", "presents the permit"),
    ("package", "the package is marked fragile", "the package is not marked fragile", "the handler", "use the protective tray", "uses the protective tray"),
)


@dataclass(frozen=True)
class WasonItem:
    pair_id: str
    frame_id: str
    form: str
    modal: str
    rule: str
    cards: tuple[str, str, str, str]
    gold: tuple[int, int]

    @property
    def gold_label(self) -> str:
        return canonical_pair(self.gold)


def canonical_pair(indices: Iterable[int]) -> str:
    values = sorted(int(x) for x in indices)
    if len(values) != 2 or values[0] == values[1] or not all(1 <= x <= 4 for x in values):
        raise ValueError(f"invalid card pair: {values}")
    return f"{values[0]},{values[1]}"


def _rule(modal: str, form: str, condition_pos: str, condition_neg: str, actor: str, bare_action: str, present_action: str) -> str:
    cons_neg = form.endswith("neg")
    antecedent = condition_neg if form.startswith("neg-") else condition_pos
    if modal == "epistemic":
        consequent = f"{actor} does not {bare_action}" if cons_neg else f"{actor} {present_action}"
    elif modal == "deontic":
        consequent = f"{actor} must not {bare_action}" if cons_neg else f"{actor} must {bare_action}"
    else:
        raise ValueError(f"unknown modal {modal!r}")
    return f"If {antecedent}, then {consequent}."


def generate_items() -> list[WasonItem]:
    rows: list[WasonItem] = []
    for frame_id, condition_pos, condition_neg, actor, bare_action, present_action in FRAMES:
        subject = actor[0].upper() + actor[1:]
        cards = (
            condition_pos[0].upper() + condition_pos[1:],
            condition_neg[0].upper() + condition_neg[1:],
            f"{subject} {present_action}",
            f"{subject} does not {bare_action}",
        )
        for form in FORMS:
            pair_id = f"{frame_id}:{form}"
            for modal in MODALS:
                rows.append(WasonItem(pair_id, frame_id, form, modal, _rule(modal, form, condition_pos, condition_neg, actor, bare_action, present_action), cards, GOLD_BY_FORM[form]))
    return _validate_items(rows, strict=True)


def _validate_items(rows: Iterable[WasonItem], *, strict: bool) -> list[WasonItem]:
    rows = list(rows)
    keys = [(x.pair_id, x.modal) for x in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate pair/modal rows")
    for row in rows:
        if row.modal not in MODALS or row.form not in FORMS:
            raise ValueError(f"invalid metadata in {row.pair_id}")
        if row.gold != GOLD_BY_FORM[row.form]:
            raise ValueError(f"wrong gold for {row.pair_id}/{row.modal}: {row.gold}")
        canonical_pair(row.gold)
        if len(row.cards) != 4 or len(set(row.cards)) != 4:
            raise ValueError(f"invalid cards in {row.pair_id}")
    by_pair: dict[str, list[WasonItem]] = {}
    for row in rows:
        by_pair.setdefault(row.pair_id, []).append(row)
    for pair_id, pair in by_pair.items():
        if {x.modal for x in pair} != set(MODALS) or len(pair) != 2:
            raise ValueError(f"{pair_id}: expected exactly one row per modality")
        e = next(x for x in pair if x.modal == "epistemic")
        d = next(x for x in pair if x.modal == "deontic")
        if (e.frame_id, e.form, e.cards, e.gold) != (d.frame_id, d.form, d.cards, d.gold):
            raise ValueError(f"{pair_id}: modalities are not structurally matched")
        if e.rule == d.rule:
            raise ValueError(f"{pair_id}: modality manipulation did not change rule")
    if strict:
        if len(rows) != 64 or len(by_pair) != 32:
            raise ValueError(f"expected 64 rows / 32 matched pairs, found {len(rows)} / {len(by_pair)}")
        for form in FORMS:
            n = len({x.pair_id for x in rows if x.form == form})
            if n != 8:
                raise ValueError(f"expected 8 matched pairs for {form}, found {n}")
        if len(CARD_PERMUTATIONS) != 24 or len(set(CARD_PERMUTATIONS)) != 24:
            raise ValueError("card counterbalancing must contain all 24 permutations")
    return rows


def write_items(path: str | Path) -> list[WasonItem]:
    rows = generate_items()
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")
    return rows


def load_items(path: str | Path, *, strict: bool = True) -> list[WasonItem]:
    rows: list[WasonItem] = []
    with Path(path).open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
                obj["cards"] = tuple(obj["cards"])
                obj["gold"] = tuple(obj["gold"])
                rows.append(WasonItem(**obj))
            except (json.JSONDecodeError, TypeError, KeyError) as e:
                raise ValueError(f"malformed item line {lineno}") from e
    return _validate_items(rows, strict=strict)


def permute_item(item: WasonItem, permutation: tuple[int, int, int, int]) -> WasonItem:
    if tuple(sorted(permutation)) != (0, 1, 2, 3):
        raise ValueError(f"invalid permutation: {permutation}")
    cards = tuple(item.cards[i] for i in permutation)
    inverse = {orig + 1: shown + 1 for shown, orig in enumerate(permutation)}
    gold = tuple(sorted(inverse[g] for g in item.gold))
    return replace(item, cards=cards, gold=gold)
