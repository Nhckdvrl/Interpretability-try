from witness_collapse_g0.metrics import bootstrap_ci, compute_case_features


def cfg():
    return {
        "recognition_gate": {
            "min_existence_probability": .8,
            "min_no_shared_entailment_probability": .8,
            "min_identity_underdetermined_probability": .75,
            "min_label_order_probability": .65,
        },
        "capability_gate": {
            "min_same_explicit_collapse_probability": .7,
            "max_distinct_explicit_collapse_probability": .3,
            "min_control_variant_success_fraction": .75,
        },
        "strong_case": {
            "min_unknown_collapse_probability": .55,
            "min_paraphrase_collapse_probability": .55,
            "min_unknown_minus_distinct": .15,
            "max_neutral_abs_shift": .05,
            "min_natural_variant_positive_fraction": .75,
        },
    }


def variants():
    return {
        "unknown": [.68, .72, .66, .74],
        "paraphrase": [.66, .70, .64, .72],
        "same_explicit": [.94, .96, .95, .97],
        "distinct_explicit": [.06, .10, .08, .08],
        "neutral_control": [.68, .70, .69, .69],
        "relation_reminder": [.18, .22, .20, .20],
    }


def test_illegal_join_requires_recognition_and_action_controls():
    features = compute_case_features(
        recognition={"p_exists": .95, "q_exists": .95, "shared_entailment": .9, "identity_determined": .9},
        recognition_min_variant=.85,
        p={"unknown": .70, "paraphrase": .68, "same_explicit": .95, "distinct_explicit": .08, "neutral_control": .69, "relation_reminder": .20},
        variants=variants(),
        cfg=cfg(),
    )
    assert features["capability_gate"]
    assert features["unknown_margin"] > 0
    assert features["reminder_rescue"] > 0
    assert features["strong"]


def test_quantifier_failure_cannot_count():
    features = compute_case_features(
        recognition={"p_exists": .95, "q_exists": .95, "shared_entailment": .2, "identity_determined": .2},
        recognition_min_variant=.2,
        p={"unknown": .85, "paraphrase": .85, "same_explicit": .95, "distinct_explicit": .05, "neutral_control": .85, "relation_reminder": .10},
        variants=variants(),
        cfg=cfg(),
    )
    assert not features["recognition_gate"]
    assert not features["strong"]


def test_position_unstable_explicit_controls_do_not_gate():
    v = variants()
    v["same_explicit"] = [.95, .95, .40, .40]
    features = compute_case_features(
        recognition={"p_exists": .95, "q_exists": .95, "shared_entailment": .9, "identity_determined": .9},
        recognition_min_variant=.85,
        p={"unknown": .70, "paraphrase": .68, "same_explicit": .80, "distinct_explicit": .08, "neutral_control": .69, "relation_reminder": .20},
        variants=v,
        cfg=cfg(),
    )
    assert not features["downstream_control_gate"]


def test_bootstrap_positive():
    lo, hi = bootstrap_ci([.05, .1, .15, .2], seed=7, n_boot=500)
    assert lo > 0 and hi >= lo
