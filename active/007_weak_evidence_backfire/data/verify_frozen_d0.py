from __future__ import annotations

from pathlib import Path
import hashlib
import json

import importlib.util

_BUILDER_PATH = Path(__file__).with_name("build_frozen_d0.py")
_spec = importlib.util.spec_from_file_location("weak_evidence_build_frozen_d0", _BUILDER_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"cannot load D0 builder from {_BUILDER_PATH}")
_builder = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_builder)
build_rows = _builder.build_rows
render = _builder.render

EXPECTED_SHA256 = "d3ef047882a49b05993f3c00c222e9d922faface3339c4161016594016c4877a"
EXPECTED_ITEMS = 30


def verify(path: str | Path | None = None) -> dict[str, object]:
    path = Path(path) if path is not None else Path(__file__).with_name("frozen_d0.jsonl")
    committed = path.read_bytes()
    rebuilt = render(build_rows())
    committed_sha = hashlib.sha256(committed).hexdigest()
    rebuilt_sha = hashlib.sha256(rebuilt).hexdigest()
    if committed_sha != EXPECTED_SHA256:
        raise AssertionError(f"committed frozen D0 checksum mismatch: {committed_sha}")
    if rebuilt_sha != EXPECTED_SHA256:
        raise AssertionError(f"rebuilt D0 checksum mismatch: {rebuilt_sha}")
    if rebuilt != committed:
        raise AssertionError("frozen D0 bytes differ from deterministic source rebuild")
    rows = [json.loads(line) for line in committed.decode("utf-8").splitlines() if line.strip()]
    if len(rows) != EXPECTED_ITEMS:
        raise AssertionError(f"expected {EXPECTED_ITEMS} scenarios, got {len(rows)}")
    return {
        "verified_items": len(rows),
        "sha256": committed_sha,
        "datasets": sorted({r["source"]["dataset"] for r in rows}),
        "domains": sorted({r["domain"] for r in rows}),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2))
