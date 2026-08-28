from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import hashlib
import json


def _builder():
    path = Path(__file__).parents[1] / "data" / "build_frozen_d0.py"
    spec = spec_from_file_location("build_frozen_d0", path)
    assert spec and spec.loader
    mod = module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_frozen_d0_builder_is_deterministic_and_has_40_external_rows():
    mod = _builder()
    text = mod.render()
    rows = [json.loads(line) for line in text.splitlines() if line.strip()]
    assert len(rows) == 40
    assert len({r["scenario_id"] for r in rows}) == 40
    assert {r["source"]["provenance"] for r in rows} == {"external-derived-redacted-identity"}
    assert all(r["source"]["url"].startswith("https://") for r in rows)
    assert hashlib.sha256(text.encode("utf-8")).hexdigest() == mod.EXPECTED_SHA256


def test_unknown_records_do_not_expose_hidden_source_club():
    mod = _builder()
    rows = [json.loads(line) for line in mod.render().splitlines() if line.strip()]
    for row in rows:
        club = row["source"]["source_club"]
        assert club not in row["premise_p"]
        assert club not in row["premise_q"]
        assert club not in row["premise_paraphrase"]
