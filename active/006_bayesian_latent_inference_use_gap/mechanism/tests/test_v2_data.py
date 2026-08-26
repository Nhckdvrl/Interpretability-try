from __future__ import annotations

import json
import math
import sys
from pathlib import Path


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from v2_behavior import summarize  # noqa: E402
from v2_data import (  # noqa: E402
    PRIMARY_CONDITIONS,
    action_for,
    build_families,
    make_factorial_rows,
    select_decompositions,
    validate_factorial,
)
from v2_freeze import audit_one_factor  # noqa: E402


CONFIG = {
    "split": "test",
    "seed": 6,
    "likelihood_regimes": [
        {"id": "sym75", "p_red_a": 0.75, "p_red_b": 0.25},
        {"id": "asym80_30", "p_red_a": 0.80, "p_red_b": 0.30},
    ],
    "count_pairs": [[1, 3], [3, 1], [2, 2], [1, 5], [5, 1], [2, 4]],
    "decompositions_per_target": 2,
    "prior_bounds": [0.01, 0.99],
    "decision_blocks": [
        {
            "threshold": 0.5,
            "evidence_targets": [0.35, 0.65],
            "external_pairs": [
                {"low": 0.326731, "high": 0.673269, "band": "far"}
            ],
        }
    ],
    "numeral_format": "decimal6",
    "action_vocabularies": {"natural": {"ACT": "ACT", "WAIT": "WAIT"}},
    "option_mappings": [["ACT", "WAIT"], ["WAIT", "ACT"]],
    "rule_forms": ["gt_high_first", "le_low_first"],
    "observation_orders": ["red_first"],
    "template_ids": ["record_v1"],
}


def test_decompositions_recover_exact_target() -> None:
    rows = select_decompositions(
        0.35,
        CONFIG["likelihood_regimes"],
        CONFIG["count_pairs"],
        2,
        6,
        (0.01, 0.99),
    )
    assert len(rows) == 2
    assert len({row["likelihood_id"] for row in rows}) == 2
    assert all(math.isclose(row["gold_p_a"], 0.35) for row in rows)


def test_factorial_is_complete_and_mapping_correct() -> None:
    families = build_families(CONFIG)
    rows = make_factorial_rows(CONFIG, families)
    validation = validate_factorial(rows)
    assert validation["n_families"] == 4
    assert validation["n_surfaces"] == 4
    assert validation["n_rows"] == 4 * 4 * 8
    assert set(validation["conditions"]) == set(PRIMARY_CONDITIONS)
    for row in rows:
        mapping = row["option_mapping"]
        expected = "A" if mapping[0] == row["condition_action"] else "B"
        assert row["expected_label"] == expected
        if row["mode"] == "use":
            assert row["condition_action"] == action_for(
                row["serialized_value"], row["threshold"]
            )
        else:
            assert row["condition_action"] == row["evidence_action"]


def test_family_first_estimand_subtracts_generic_authority() -> None:
    families = build_families(CONFIG)
    rows = make_factorial_rows(CONFIG, families[:1])
    for row in rows:
        row["inference_good"] = True
        row["condition_correct"] = True
        sign = 1.0 if row["value_side"] == "high" else -1.0
        if row["condition"] == "posterior_use":
            row["semantic_logit"] = 3.0 * sign
        elif row["condition"] == "generic_use":
            row["semantic_logit"] = 2.0 * sign
        else:
            row["semantic_logit"] = 0.0
    result = summarize(rows, bootstrap_draws=100, seed=6)
    effects = result["family_first_effects"]
    assert effects["G_posterior"]["mean"] == 6.0
    assert effects["G_generic_control"]["mean"] == 4.0
    assert effects["G_specific"]["mean"] == 2.0


def test_config_round_trip_is_json_serializable() -> None:
    assert json.loads(json.dumps(CONFIG))["split"] == "test"


def test_ood_wrapper_changes_only_registered_field() -> None:
    config = (
        Path(__file__).resolve().parents[1]
        / "configs/confirmatory/v2_d2_ood_template.json"
    )
    audit = audit_one_factor(config)
    assert audit["changed_field"] == "template_ids"
    assert audit["one_factor_only"]
