# 007 — Weak-Evidence Backfire

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r4 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model correctly recognize a cue as **genuine positive evidence for a hypothesis**, yet integrate that cue with the wrong sign in downstream belief and action?

The canonical contradiction is:

```text
E supports H
but adding E makes H less preferred than the same no-evidence baseline
```

The harness does not call a merely small positive update “backfire”. A negative update is admissible only after the model itself passes the support relation and ordinary strong-evidence sensitivity gates.

The “belief” readout is an exact binary preference between matched hypotheses, not a calibrated absolute posterior. The consequential action readout is therefore co-primary: promotion requires the same sign reversal at both interfaces.

## Bidirectional operator

Every scenario contains matched evidence in both directions:

- `supports_target`: `LR(target / other) > 1`;
- `supports_other`: `LR(target / other) < 1`, equivalently positive evidence for OTHER.

Strong cues point in the same two directions and are more diagnostic; the neutral cue has LR `1`.

For readouts stored as normalized target preference:

```text
signed_update(target-support) =  p(target | E) - p(target | baseline)
signed_update(other-support)  = -[p(target | E) - p(target | baseline)]
backfire                       = -signed_update
```

A valid phenotype must therefore flip with evidence direction: a target-supporting cue lowers target preference, while an other-supporting cue raises it. This bidirectional requirement sharply separates the target phenomenon from generic caution, answer conservatism, or a one-sided target prior.

The two directions of one natural scenario are treated as **one statistical unit**. Bootstrap inference is performed over scenario-level bidirectional means, not over the two correlated directions as if they were independent samples.

## r4 fixes that prevent false positives

### 1. A no-evidence baseline contains no negative observation

The baseline is only background + calibration. It does **not** say “no cue was observed”. Such a sentence would itself be evidence and could manufacture a sign reversal.

### 2. Support is checked more deeply than a yes/no label

Each direction must pass, under both answer orders:

- weak cue is positive evidence for the focal hypothesis;
- the likelihood relation points toward that hypothesis;
- the cue stays positive under the pragmatic-completeness protocol;
- the strong cue is positive;
- the strong cue is more diagnostic than the weak cue;
- the neutral cue is non-diagnostic.

Strong evidence must also move both belief and action toward the focal hypothesis consistently across readout wordings/orders.

### 3. Pragmatic absence-of-stronger-evidence is directly attacked

The decisive control is a paired protocol comparison:

```text
no_evidence_complete = background + calibration + completeness protocol
weak_complete        = same text + weak-positive cue
```

The protocol states that unshown cues carry no information. If ordinary weak evidence backfires but this paired contrast does not, the discovery contract is killed as `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`.

A separate matched-length protocol guards against the possibility that the completeness prompt itself creates the effect. Every weak, weak-complete, and weak-length contrast is paired within the **same readout wording and answer order**; a favorable aggregate cannot hide variants with the opposite sign.

## Formal D0 record

```json
{
  "scenario_id": "machine:17",
  "domain": "diagnostics",
  "background": "...natural externally anchored case...",
  "calibration_text": "...externally anchored conditional frequencies / likelihood relation...",
  "target_hypothesis": "cooling fault",
  "other_hypothesis": "power fault",
  "target_action": "run cooling follow-up",
  "other_action": "run power follow-up",
  "weak_target_evidence": "Cue T was observed.",
  "weak_other_evidence": "Cue O was observed.",
  "strong_target_evidence": "Marker T was observed.",
  "strong_other_evidence": "Marker O was observed.",
  "neutral_evidence": "Cue N was observed.",
  "pragmatic_completeness_text": "Only the scheduled cue is displayed; omission of other possible cues conveys no information.",
  "matched_length_control_text": "...matched semantically inert protocol text...",
  "weak_target_lr": 1.38,
  "weak_other_lr": 0.72,
  "strong_target_lr": 5.67,
  "strong_other_lr": 0.176,
  "neutral_lr": 1.0,
  "calibration_valid_gold": true,
  "weak_target_support_gold": true,
  "weak_other_support_gold": true,
  "strong_target_support_gold": true,
  "strong_other_support_gold": true,
  "neutral_gold": true,
  "pragmatic_completeness_gold": true,
  "matched_length_control_gold": true,
  "actions_symmetric_gold": true,
  "hypotheses_exclusive_gold": true,
  "hypotheses_exhaustive_gold": true,
  "binary_choice_well_defined_gold": true,
  "core_wording_does_not_label_strength_gold": true,
  "direction_pair_matched_gold": true,
  "strong_weak_relation_comparable_gold": true,
  "neutral_control_matched_gold": true,
  "baseline_contains_no_case_specific_evidence_gold": true,
  "natural_setting_gold": true,
  "source": {
    "dataset": "...",
    "record_id": "...",
    "split": "...",
    "license": "...",
    "url": "...",
    "provenance": "external-derived"
  }
}
```

Because the belief readout is a normalized two-choice probability, formal D0 also requires the two hypotheses to be mutually exclusive **and exhaustive**. Without exhaustiveness, a change in binary preference is not a clean stand-in for the posterior odds of the canonical `H` versus `not-H` comparison.

The loader enforces the directional inequalities

```text
1 < weak_target_lr < strong_target_lr
0 < strong_other_lr < weak_other_lr < 1
neutral_lr = 1
```

and the D0 auditor must verify that the prose calibration really corresponds to those stored relations. The core observation text may not simply announce “this is weak evidence”; evidence strength must come from the audited evidence relation, not an experimental label.

Formal G0 rejects custom-only provenance. Constructed transformations are acceptable only when the underlying case and likelihood relation are externally anchored and the D0 audit verifies the transformation.

## Readouts and promotion

The scorer is deterministic local exact-continuation log probability over `A/B`; there is no API and no LLM judge. Two belief phrasings and two consequential-action phrasings are answer-order counterbalanced.

A direction enters the denominator only after the support gate and strong-evidence capability gate pass. A strong direction then requires:

- negative weak update at both belief and action interfaces;
- survival under the completeness protocol;
- survival under the matched-length protocol;
- small neutral movement;
- at least 75% of wording/order variants having the backfire sign in the primary and control contrasts.

A scenario pair is strong only if **both evidence directions** are strong. Model-level inference bootstraps over gated scenario pairs and requires multiple natural domains before panel promotion.

## Hard kills / holds

- evidence direction / neutral relation / strong-vs-weak relation is not understood → `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`;
- gate-correct scenario pairs show no sign reversal → `HARD-KILL-NO-BACKFIRE`;
- completeness protocol removes the reversal → `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`;
- belief reverses but consequential action does not → `HOLD-READOUT-ONLY`;
- the effect is materially one-sided across target/other evidence → `HOLD-DIRECTION-ASYMMETRY`;
- neutral evidence moves similarly → `HOLD-GENERIC-MENTION-ARTIFACT`.

## Execution gate

`configs/frozen_g0.json` has `validation_authorized: false`. `weak-evidence-run run` checks this before model construction and refuses to run until the authoritative registry has independent N0 + D0 sign-off.

Safe pre-authorization work:

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[dev]'
pytest -q
weak-evidence-run validate-data --data data/frozen_d0.jsonl
```
