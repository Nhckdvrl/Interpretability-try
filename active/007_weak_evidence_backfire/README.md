# 007 — Weak-Evidence Backfire

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r3 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model correctly recognize a piece of evidence as genuinely supporting a hypothesis, yet update **away** from that hypothesis relative to an otherwise matched no-evidence baseline?

```text
model judges E supports H
but
P(H | E) < P(H | no evidence)
```

The contract is deliberately bidirectional. Each base scenario carries one weak cue supporting TARGET and one weak cue supporting OTHER. A real backfire must reverse sign with evidence direction: target-support evidence lowers TARGET, while other-support evidence raises TARGET. Generic caution, answer bias, or a reaction to the concept of weakness cannot satisfy this symmetry.

## Evidence-direction contract

```text
raw_update = P(target | weak evidence) - P(target | matched no-evidence baseline)
signed_update = raw_update       if supports_target
              = -raw_update      if supports_other
backfire = -signed_update
```

Normative positive evidence gives `signed_update > 0`; the phenotype requires `signed_update < 0`. The same convention is applied independently to belief and consequential-action readouts.

## What must be true before a case counts

The model must recognize the weak cue as positive evidence, recognize its likelihood-ratio direction, retain that judgment under the completeness protocol, and move normatively under a stronger cue of the same polarity. A case where the model simply interprets the weak cue as anti-evidence is therefore excluded before the backfire metric is considered.

D0 freezes:

```text
1 < weak_target_lr < strong_target_lr
0 < strong_other_lr < weak_other_lr < 1
neutral_lr == 1
target_length_control_lr == 1
other_length_control_lr == 1
```

The core weak-evidence text may not explicitly call itself “weak”, “slight”, “limited”, etc. Evidence strength comes from independently audited calibration, not from an experimental adjective.

## Controls that rule out cheap explanations

- `no_evidence` vs `weak`: primary sign-reversal contrast.
- `no_evidence_complete` vs `weak_complete`: both arms use an explicit reporting rule under which omitted stronger cues convey no information. A surviving reversal cannot be explained merely by “if stronger evidence existed it would have been shown.”
- `length_control` vs `weak_length`: **direction-specific LR=1 filler observations** matched in surface length/token budget to the corresponding weak cue. This is a real length/mention baseline; simply adding the same paragraph to both arms is not accepted as a length control.
- `neutral`: a separate LR=1 mention control.
- `strong`: capability control showing that stronger evidence of the same direction moves both readouts normatively.

Every primary weak score is paired to the exact no-evidence request with the same readout template and A/B label order.

## Formal D0 record

```json
{
  "scenario_id": "diagnosis:17",
  "domain": "diagnosis",
  "background": "...natural base record...",
  "calibration_text": "...audited natural likelihood calibration...",
  "target_hypothesis": "...",
  "other_hypothesis": "...",
  "target_action": "...consequential action favoring TARGET...",
  "other_action": "...consequential action favoring OTHER...",
  "weak_target_evidence": "...positive TARGET evidence; wording does not say weak...",
  "weak_other_evidence": "...positive OTHER evidence...",
  "strong_target_evidence": "...",
  "strong_other_evidence": "...",
  "neutral_evidence": "...",
  "pragmatic_completeness_text": "The scheduled reporting protocol is complete; omission of unreported cues conveys no information.",
  "target_length_control_evidence": "...TARGET-side LR=1 filler matched to weak_target_evidence length...",
  "other_length_control_evidence": "...OTHER-side LR=1 filler matched to weak_other_evidence length...",
  "weak_target_lr": 1.2,
  "strong_target_lr": 4.0,
  "weak_other_lr": 0.83,
  "strong_other_lr": 0.25,
  "neutral_lr": 1.0,
  "target_length_control_lr": 1.0,
  "other_length_control_lr": 1.0,
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

Formal G0 rejects custom-only rows. The base task, calibration/gold and provenance must be externally anchored; an audited transformation may construct paired cues, but it cannot invent the underlying evidence relation.

## Promotion signature

A strong direction requires all support/likelihood gates, strong-evidence capability, positive backfire in both belief and action, survival under completeness and LR=1 length-matched controls, neutral separation, and consistency across two belief phrasings, two action phrasings and both answer orders. A strong scenario pair requires both evidence directions to satisfy that contract.

## Hard kills / holds

- weak support recognition or strong same-direction capability fails → `HARD-KILL-EVIDENCE-DIRECTION-CAPABILITY-FLOOR`;
- gated paired cases show no backfire → `HARD-KILL-NO-BACKFIRE`;
- reversal dies under completeness-matched comparison → `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`;
- only verbal belief reverses, not consequential action → `HOLD-READOUT-ONLY`;
- LR=1 neutral/length-matched mention moves comparably → `HOLD-GENERIC-MENTION-ARTIFACT`.

If a result needs explicit “weak” wording, only one evidence polarity, a selected weak model, or a non-neutral length filler, it does not satisfy the contract.

## No model call before authorization

`run` raises `PermissionError` while `validation_authorized: false`. Formal execution begins only after independent N0 and D0 sign-off in the authoritative registry.

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[run,dev]'
pytest -q
weak-evidence-run validate-data --data data/frozen_d0.jsonl

# Blocked until authorization.
weak-evidence-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B --family Qwen --size-b 8 \
  --revision <exact-revision> \
  --out results/qwen3_8b.jsonl
```
