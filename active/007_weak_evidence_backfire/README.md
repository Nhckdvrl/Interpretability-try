# 007 — Weak-Evidence Backfire

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #10**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model explicitly recognize that evidence `E` supports hypothesis `H`, yet move **away** from `H` after receiving `E` compared with receiving no evidence?

The core contradiction is a sign reversal:

```text
model says E favors H
but
preference(H | E) < preference(H | no evidence)
```

The harness never treats “the update is smaller than ideal” as backfire. The update must have the wrong sign.

## Why the validation is unusually strict

This candidate is easy to fake accidentally. A valid result must rule out at least four simpler stories:

1. the model never represented `E` as positive evidence in the first place;
2. adding any extra observation generically lowers confidence;
3. “only a weak cue was mentioned” pragmatically implies that stronger evidence was absent;
4. a target/first-option bias makes one evidence direction look negative.

The code therefore freezes support gates, a neutral cue, stronger positive evidence, a matched reporting-note control, an explicit pragmatic-completeness protocol, **both evidence directions**, two belief phrasings, two equal-cost action phrasings, and both label orders.

## Formal D0 relation

The normative sign must not depend on an annotator merely saying “this seems supportive.” Each formal case carries an externally audited calibration with likelihood-ratio direction. **That calibration is an audit/probe instrument, not part of the primary behavioral prompt**:

```text
weak_target_lr  > 1
strong_target_lr > weak_target_lr

0 < strong_other_lr < weak_other_lr < 1
neutral_lr ≈ 1
```

Here the LR is always `P(E | target) / P(E | other)`. Therefore target-supporting evidence must raise target odds, while other-supporting evidence must lower target odds. The two directions are later sign-coded into the same normative axis.

Core evidence wording is not allowed to label itself “weak evidence”, “weak cue”, etc.; evidence strength must come from the calibration rather than a lexical instruction.

## Formal D0 schema

```json
{
  "scenario_id": "diagnostic:record-12",
  "domain": "diagnostics",
  "background": "A natural two-hypothesis situation ...",
  "calibration_text": "Externally anchored cue frequencies/rates ...",
  "target_hypothesis": "...",
  "other_hypothesis": "...",
  "target_action": "An equal-cost follow-up tied to target ...",
  "other_action": "An equal-cost follow-up tied to other ...",
  "weak_target_evidence": "Observed target-favoring cue ...",
  "weak_other_evidence": "Observed other-favoring cue ...",
  "strong_target_evidence": "Observed stronger target-favoring cue ...",
  "strong_other_evidence": "Observed stronger other-favoring cue ...",
  "neutral_evidence": "Observed LR≈1 cue ...",
  "pragmatic_completeness_text": "A protocol stating that omitted stronger cues carry no information ...",
  "matched_length_control_text": "A length-matched reporting note without that semantic guarantee ...",
  "weak_target_lr": 1.4,
  "weak_other_lr": 0.72,
  "strong_target_lr": 4.0,
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

Custom-only data are rejected for formal G0. D0 must manually audit at least 20 random cases and verify that the calibration, action symmetry, support direction, neutral cue, reporting protocol, and source license are genuine.

## The paired experimental worlds

For each scenario, both a target-supporting cue and an other-supporting cue are tested. Each direction contains:

```text
no_evidence
weak
strong
neutral
no_evidence_complete
weak_complete
no_evidence_length
weak_length
```

The two protocol baselines are essential. Pragmatic robustness is **not** computed as `weak_complete - ordinary_no_evidence`; it is:

```text
weak_complete - no_evidence_complete
```

Likewise the matched-length comparison is:

```text
weak_length - no_evidence_length
```

This prevents the reporting sentence itself from being mistaken for a backfire effect.

The primary downstream worlds contain only the natural background and observation; they do not show the calibration table. The model is separately asked, in independent prompts, whether the cue naturally supports the focal hypothesis, whether its externally audited likelihood relation has the correct direction (this probe may show the calibration), and whether the cue still supports the focal hypothesis under the completeness protocol. The support probes therefore validate the premise without turning the main behavior test into an explicit Bayes worksheet or priming the downstream readout.

## Sign-coded metric

Let `p_target(c)` be the exact continuation probability of the target choice after averaging natural phrasings and both label orders.

```text
sign = +1  for target-supporting evidence
sign = -1  for other-supporting evidence

signed_update = sign * [p_target(evidence) - p_target(matched baseline)]
backfire      = -signed_update
```

Thus both directions mean the same thing:

```text
signed_update > 0  normative movement
signed_update < 0  true sign reversal
backfire > 0       weak-evidence backfire
```

The primary uncertainty estimate first averages the two evidence directions within each scenario and then bootstraps **scenarios**. It does not pretend the two directions from one base case are independent observations.

The no-evidence, neutral, protocol-only, and length-note-only prompts are direction-invariant. The official runner uses one lifetime-scoped scorer cache, and the summarizer rejects a run if those duplicated baselines are not bit-identical across directions. This catches batch nondeterminism or incorrectly assembled result files before statistics are trusted.

## Controls required before a case can count

A direction is capability-gated only if:

- the model says the weak cue supports the focal hypothesis;
- the model correctly reads the likelihood relation;
- it still says the cue supports the focal hypothesis under the completeness protocol;
- stronger evidence moves choice in the normatively correct direction for both belief and action readouts.

A strong case additionally requires real negative weak updates, persistence under completeness and matched-length controls, small neutral shift, natural-template consistency, and an action-level echo rather than only one verbal confidence phrasing.

## Hard kills / holds

- `HARD-KILL-E-NOT-REPRESENTED-AS-SUPPORT`: the support premise itself fails broadly; there is no positive-evidence sign reversal to explain.
- `HARD-KILL-NO-SIGN-REVERSAL`: enough gate-correct paired cases exist but weak evidence does not move belief in the wrong direction.
- `HARD-KILL-PRAGMATIC-IMPLICATURE`: ordinary backfire appears but disappears once stronger-evidence absence is made non-informative under a matched protocol baseline.
- `HOLD-DIRECTION-ASYMMETRY`: the sign-coded effect survives only for one evidence direction, consistent with target/option bias.
- `HOLD-GENERIC-CONTEXT-ARTIFACT`: neutral observations cause comparable movement.

## Mechanism forks reserved for later

If the behavior survives N1, 3/5 families, a three-size sequence, and strong-model testing, the frozen controls distinguish at least these mechanism hypotheses:

1. **Causal-slot/focusing failure:** mentioning one cue occupies an explanation slot and suppresses alternatives.
2. **Absolute-sufficiency mapping:** the model internally converts a relatively diagnostic but modest cue into “overall evidence is insufficient”, confusing likelihood ratio with absolute sufficiency.
3. **Late readout inversion:** internal evidence update is correct, but a downstream answer/action interface maps “modest support” to a negative stance.

Completeness controls, calibrated LR direction, belief/action divergence, and later representation/patching tests make different predictions under these explanations.

## Commands

```bash
cd active/007_weak_evidence_backfire
python -m pip install -e '.[run,dev]'
pytest -q
weak-evidence-run validate-data --data data/frozen_d0.jsonl
```

Formal model inference is blocked while the frozen config says `validation_authorized: false`:

```bash
weak-evidence-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --revision <exact-revision> \
  --out results/qwen3_8b.jsonl
```

Do not bypass that gate. Independent N0, formal D0, and the authoritative registry must authorize smoke first.
