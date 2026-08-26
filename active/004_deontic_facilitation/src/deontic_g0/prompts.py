from __future__ import annotations

import itertools

from .dataset import WasonItem

CANDIDATES = tuple(f"{a},{b}" for a, b in itertools.combinations(range(1, 5), 2))

# Keep the task instruction neutral with respect to modality. In particular, the
# control prompt must not inject "violation", "obligation", permission language,
# or a concrete answer example that could privilege one gold pair.
TEMPLATES = (
    "Conditional rule: {rule}\n\nEach card has a condition-side statement on one side and an outcome-side statement on the other. Exactly one side of each card is visible; turning a card reveals its hidden other side.\n\nThe four visible sides are:\n1. {c1}\n2. {c2}\n3. {c3}\n4. {c4}\n\nWhich TWO cards need to be turned over to determine whether the four cases satisfy the conditional rule? Return only the two position numbers separated by a comma, in ascending order.",
    "Consider the conditional rule below.\n{rule}\n\nEvery card pairs one condition-side value with one outcome-side value. One side is visible and the corresponding other side is hidden until the card is turned.\n\nVisible sides:\n[1] {c1}\n[2] {c2}\n[3] {c3}\n[4] {c4}\n\nSelect exactly the two cards whose hidden sides need checking to determine whether the four cases satisfy the rule. Return only the two position numbers separated by a comma, in ascending order.",
)


def build_prompt(item: WasonItem, template_id: int) -> str:
    try:
        template = TEMPLATES[template_id]
    except IndexError as e:
        raise ValueError(f"unknown template_id={template_id}") from e
    return template.format(rule=item.rule, c1=item.cards[0], c2=item.cards[1], c3=item.cards[2], c4=item.cards[3])
