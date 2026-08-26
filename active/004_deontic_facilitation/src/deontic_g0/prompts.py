from __future__ import annotations

from dataclasses import dataclass
import itertools

from .dataset import WasonItem

CANDIDATES = tuple(f"{a},{b}" for a, b in itertools.combinations(range(1, 5), 2))

TEMPLATES = (
    "Rule: {rule}\n\nThe four visible cards are:\n1. {c1}\n2. {c2}\n3. {c3}\n4. {c4}\n\nWhich TWO cards must be turned over to determine whether the rule is violated? Answer with exactly one pair in ascending order, such as 1,4.",
    "Consider this conditional rule: {rule}\n\nCards:\n[1] {c1}\n[2] {c2}\n[3] {c3}\n[4] {c4}\n\nSelect exactly the two cards that need checking. Return only the two position numbers separated by a comma, in ascending order.",
)


def build_prompt(item: WasonItem, template_id: int) -> str:
    try:
        template = TEMPLATES[template_id]
    except IndexError as e:
        raise ValueError(f"unknown template_id={template_id}") from e
    return template.format(
        rule=item.rule,
        c1=item.cards[0],
        c2=item.cards[1],
        c3=item.cards[2],
        c4=item.cards[3],
    )
