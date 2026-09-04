"""B1: the functional-selectivity matrix, exactly as frozen in B1_PREANALYSIS_FREEZE.md.

Gates (denominators, not contributions):
    G1        ReferenceConsequence(P) larger under R+ than R-
    G2_E(P)   ES_p(E+) - ES_p(E-)  > 0        event-relevance manipulation check

Matrix (rows = manipulation, columns = which readout's omission consequence moves):
    dRR = mean[RC(P) | R+] - mean[RC(P) | R-]
    dRE = mean[EC(P) | R+] - mean[EC(P) | R-]
    dER = mean[RC(P) | E+] - mean[RC(P) | E-]
    dEE = [ES(full,E+) - ES(dropP,E+)] - [ES(full,E-) - ES(dropP,E-)]

Contrasts are formed within item and world; intervals are non-parametric bootstrap over the 12
items, 5,000 resamples. Surface form is a blocking factor: reference contrasts are formed within a
template before any aggregation. Absolute magnitudes are NOT comparable across the two columns —
one is a forced-choice log-odds difference, the other a continuation log-probability difference.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

import numpy as np

BOOTSTRAP = 5000
SEED = 20260904


def ci(values: np.ndarray, rng) -> tuple[float, float, float]:
    draws = rng.choice(values, size=(BOOTSTRAP, values.size), replace=True).mean(axis=1)
    return float(values.mean()), float(np.percentile(draws, 2.5)), float(np.percentile(draws, 97.5))


def fmt(values: np.ndarray, rng) -> str:
    mean, low, high = ci(values, rng)
    star = "*" if (low > 0) == (high > 0) else " "
    return f"{mean:+.3f} [{low:+.3f},{high:+.3f}]{star}"


def by_item(per_item: dict[str, list[float]]) -> np.ndarray:
    return np.array([float(np.mean(per_item[i])) for i in sorted(per_item)])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", type=Path, required=True)
    parser.add_argument("--explanation", type=Path, required=True)
    args = parser.parse_args()

    ref_rows = [json.loads(line) for line in args.reference.read_text().splitlines() if line]
    exp_rows = [json.loads(line) for line in args.explanation.read_text().splitlines() if line]
    model = ref_rows[0]["model_checkpoint"].split("/")[-1]

    # --- reference: omission consequences, formed within template ---
    margins = {}
    for row in ref_rows[1:]:
        key = (row["world_id"], row["e_condition"], row["surface_form"], row["cue_index"],
               row["mapping_index"], row["description_condition"])
        margins[key] = row["referent_margin"]
    rc_p = defaultdict(lambda: defaultdict(list))   # [r_cond][item] and [e_cond][item]
    rc_q = defaultdict(lambda: defaultdict(list))
    accuracy = defaultdict(list)
    meta = {}
    for row in ref_rows[1:]:
        meta[row["world_id"]] = (row["item_id"], row["r_condition"])
        if row["description_condition"] != "full":
            continue
        base = (row["world_id"], row["e_condition"], row["surface_form"], row["cue_index"],
                row["mapping_index"])
        full = margins[base + ("full",)]
        cell = (row["r_condition"], row["e_condition"], row["item_id"])
        rc_p[cell][0].append(full - margins[base + ("drop_p",)])
        rc_q[cell][0].append(full - margins[base + ("drop_q",)])
        accuracy[row["r_condition"]].append(row["correct"])

    # --- explanation: omission consequence of P on the fixed P continuation ---
    support = {}
    for row in exp_rows[1:]:
        key = (row["world_id"], row["e_condition"], row["cue_index"], row["continuation_label"],
               row["description_condition"])
        support[key] = row["explanation_support"]
    ec_p = defaultdict(lambda: defaultdict(list))
    es_full = defaultdict(lambda: defaultdict(list))
    for row in exp_rows[1:]:
        if row["description_condition"] != "full":
            continue
        base = (row["world_id"], row["e_condition"], row["cue_index"], row["continuation_label"])
        cell = (row["r_condition"], row["e_condition"], row["item_id"], row["continuation_label"])
        ec_p[cell][0].append(support[base + ("full",)] - support[base + ("drop_p",)])
        es_full[cell][0].append(support[base + ("full",)])

    def collect(store, r_filter=None, e_filter=None, label="p"):
        per_item = defaultdict(list)
        for key, values in store.items():
            if len(key) == 4:
                r_cond, e_cond, item, continuation = key
                if continuation != label:
                    continue
            else:
                r_cond, e_cond, item = key
            if r_filter and r_cond != r_filter:
                continue
            if e_filter and e_cond != e_filter:
                continue
            per_item[item].extend(values[0])
        return by_item(per_item)

    rng = np.random.default_rng(SEED)
    print(f"\n=== {model} ===")
    print(f"full-description accuracy: R+ {np.mean(accuracy['R_plus']):.3f}  "
          f"R- {np.mean(accuracy['R_minus']):.3f}")

    print("\ngates")
    print(f"  G1      RC(P) R+ minus R-   {fmt(collect(rc_p, r_filter='R_plus') - collect(rc_p, r_filter='R_minus'), rng)}")
    print(f"  G2_E    ES_p  E+ minus E-   {fmt(collect(es_full, e_filter='E_plus') - collect(es_full, e_filter='E_minus'), rng)}")

    print("\nfunctional-selectivity matrix (magnitudes NOT comparable across columns)")
    print(f"{'':<18}{'reference consequence':>30}{'explanation consequence':>30}")
    print(f"{'R manipulation':<18}"
          f"{fmt(collect(rc_p, r_filter='R_plus') - collect(rc_p, r_filter='R_minus'), rng):>30}"
          f"{fmt(collect(ec_p, r_filter='R_plus') - collect(ec_p, r_filter='R_minus'), rng):>30}")
    print(f"{'E manipulation':<18}"
          f"{fmt(collect(rc_p, e_filter='E_plus') - collect(rc_p, e_filter='E_minus'), rng):>30}"
          f"{fmt(collect(ec_p, e_filter='E_plus') - collect(ec_p, e_filter='E_minus'), rng):>30}")

    print("\ncontrol and exploratory")
    print(f"  RC(Q) R+ minus R-           {fmt(collect(rc_q, r_filter='R_plus') - collect(rc_q, r_filter='R_minus'), rng)}"
          "   (should be near zero if Q's role is held constant)")
    print(f"  ES_pbar E+ minus E-         {fmt(collect(es_full, e_filter='E_plus', label='p_contrast') - collect(es_full, e_filter='E_minus', label='p_contrast'), rng)}"
          "   (exploratory false-property control only)")
    print("\n* = bootstrap interval over the 12 items excludes zero")


if __name__ == "__main__":
    main()
