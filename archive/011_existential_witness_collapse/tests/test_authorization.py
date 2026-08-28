import json
import pytest
from witness_collapse_g0.run import _require_authorized


def test_frozen_config_blocks_model_calls(tmp_path):
    p = tmp_path / "config.json"
    p.write_text(json.dumps({"validation_authorized": False}), encoding="utf-8")
    with pytest.raises(PermissionError, match="not authorized"):
        _require_authorized(str(p))
