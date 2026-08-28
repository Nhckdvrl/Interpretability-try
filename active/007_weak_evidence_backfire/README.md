# 007 — Weak-Evidence Backfire

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r2 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model correctly recognize a piece of evidence as genuinely supporting a hypothesis, yet update **away** from that hypothesis relative to an otherwise matched no-evidence baseline?

The target contradiction is not merely weak updating:

```text
model judges E supports H
but
P(H | E) < P(H | no evidence)
```

The r2 contract is deliberately bidirectional. Each base scenario carries one weak cue supporting TARGET and one weak cue supporting OTHER. If the effect is genuine, the sign must flip with evidence direction: target-support evidence should lower TARGET, while other-support evidence should raise TARGET. A generic reaction to the word or concept “weak” therefore cannot pass.

## Evidence-direction contract

For `direction ∈ {supports_target, supports_other}` define:

```text
raw_update = P(target | weak evidence) - P(target | matched no-evidence baseline)
signed_update = raw_update                       if supports_target
              = - raw_update                     if supports_other
backfire = - signed_update
```

Normative positive evidence gives `signed_update > 0`. The phenotype requires `signed_update < 0`, i.e. `backfire > 0`.

The same signed convention is applied separately to a belief readout and a consequential action readout.

## What must be true before a case counts

The model must pass support recognition for the weak cue itself, recognize the weak cue's likelihood-ratio direction, still recognize it under the pragmatic-completeness protocol, and respond in the expected direction to a stronger cue of the same polarity. Thus a case in which the model simply thinks the weak cue is anti-evidence is not diagnostic.

D0 also freezes calibrated relations:

```text
1 < weak_target_lr < strong_target_lr
0 < strong_other_lr < weak_other_lr < 1
neutral_lr == 1
```

The core weak-evidence wording may not call itself “weak”, “slight”, “limited”, etc. Strength is supplied by the audited likelihood relation, not by a lexical instruction that could itself induce pessimism.

## Controls that rule out cheap explanations

Each direction is measured under exact matched protocols:

- `no_evidence` vs `weak` — primary contrast;
- `no_evidence_complete` vs `weak_complete` — both arms explicitly state that the record is complete, so “if stronger evidence existed it would have been shown” cannot explain a residual sign reversal;
- `no_evidence_length` vs `weak_length` — matched extra text/length on both arms;
- `neutral` — an LR=1 mention control;
- `strong` — capability control showing that sufficiently strong evidence of the same direction moves belief/action normatively.

Every weak score is paired to the exact baseline with the same readout template and the same A/B label order. The harness never compares an averaged weak condition to a differently worded or differently ordered baseline.

## Formal D0 record

```json
{
  "scenario_id": "diagnosis:17",
  "domain": "diagnosis",
  "background": "...natural base record...",
  "calibration_text": "...audited source-specific rates or other natural likelihood calibration...",
  "target_hypothesis": "...",
  "other_hypothesis": "...",
  "target_action": "...consequential action favoring TARGET...",
  "other_action": "...consequential action favoring OTHER...",
  "weak_target_evidence": "...positive but weak TARGET evidence; wording does not say weak...",
  "weak_other_evidence": "...positive but weak OTHER evidence...",
  "strong_target_evidence": "...",
  "strong_other_evidence": "...",
  "neutral_evidence": "...",
  "pragmatic_completeness_text": "The record below is complete; no additional evidence is being withheld.",
  "matched_length_control_text": "...matched non-evidential text...",
  "weak_target_lr": 1.2,
  "strong_target_lr": 4.0,
  "weak_other_lr": 0.83,
  "strong_other_lr": 0.25,
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
  "core_wording_does_not_label_strength_gold": true,
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

Formal G0 rejects custom-only rows. The calibrated weak relation may be an audited transformation over public natural records, but the base task, likelihood relation/gold, and provenance must be independently anchored.

## Promotion signature

A strong **direction** requires:

- all support/likelihood recognition gates pass;
- strong evidence moves both belief and action normatively;
- weak evidence gives positive backfire on both belief and action;
- the sign reversal survives the completeness protocol and the matched-length protocol;
- neutral mention movement is small relative to the reversal;
- the direction is stable across two natural belief phrasings, two action phrasings, and both answer orders.

A strong **scenario pair** requires both `supports_target` and `supports_other` directions to satisfy that contract. This bidirectional pair is the main protection against generic skepticism, confidence shrinkage, lexical “weakness”, and one-sided answer bias.

## Hard kills / holds

- The model does not reliably judge the weak cues as positive evidence, or strong same-direction evidence does not work → `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`.
- Gated paired cases have no positive backfire → `HARD-KILL-NO-BACKFIRE`.
- Primary reversal disappears under the completeness-matched comparison → `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`.
- Reversal appears only in verbal belief but not consequential action → `HOLD-READOUT-ONLY`.
- Neutral/matched mention causes comparable movement → `HOLD-GENERIC-MENTION-ARTIFACT`.

If a positive result depends on wording that explicitly announces evidence weakness, a selected weak model, or an asymmetric TARGET-only stimulus set, it does not satisfy this contract.

## No model call before authorization

`run` raises `PermissionError` while the frozen config has `validation_authorized: false`. Do not change that flag merely because the harness exists. Formal execution begins only after an independent N0 reviewer and D0 reviewer have signed the authoritative registry.

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[run,dev]'
pytest -q

# Safe preflight: validates D0 structure and calibrated relations only.
weak-evidence-run validate-data --data data/frozen_d0.jsonl

# Formal model execution remains blocked until authorization.
weak-evidence-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B --family Qwen --size-b 8 \
  --revision <exact-revision> \
  --out results/qwen3_8b.jsonl
```
