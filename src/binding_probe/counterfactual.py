from __future__ import annotations

from copy import deepcopy
from typing import Any

from .bfcl import single_turn_messages


def swap_literals_in_user_text(entry: dict[str, Any], value_a: Any, value_b: Any) -> dict[str, Any] | None:
    """Create a minimal filler-swap counterfactual only when each literal occurs exactly once.

    This is deliberately strict: if literal replacement is ambiguous, return None rather than
    manufacturing a questionable causal pair.
    """
    a, b = str(value_a), str(value_b)
    clone = deepcopy(entry)
    msgs = single_turn_messages(clone)
    hits_a = sum(str(m.get("content", "")).count(a) for m in msgs if m.get("role") == "user")
    hits_b = sum(str(m.get("content", "")).count(b) for m in msgs if m.get("role") == "user")
    if hits_a != 1 or hits_b != 1:
        return None
    marker_a, marker_b = "__BINDING_SWAP_A__", "__BINDING_SWAP_B__"
    for m in msgs:
        if m.get("role") != "user":
            continue
        text = str(m.get("content", ""))
        text = text.replace(a, marker_a).replace(b, marker_b)
        text = text.replace(marker_a, b).replace(marker_b, a)
        m["content"] = text
    return clone
