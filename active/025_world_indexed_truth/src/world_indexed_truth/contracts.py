"""Load immutable contracts with explicit single-parent inheritance."""

from __future__ import annotations

import json
from pathlib import Path


def load_contract(path: Path) -> dict:
    child = json.loads(path.read_text())
    parent_name = child.get("parent_contract")
    if parent_name is None:
        return child
    parent = load_contract(path.parent / parent_name)
    return {**parent, **child}
