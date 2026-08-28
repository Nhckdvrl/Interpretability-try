# Pre-merge validation audit — active 006 / 007

Date: 2026-08-28  
Scope: `006_existential_witness_collapse` and `007_weak_evidence_backfire`  
Result: `HARNESS-READY / NOT READY-TO-SMOKE`

This audit reviews whether the frozen behavioral harnesses test the exact canonical shortlist contracts without silently replacing them with easier proxy tasks. It is a code/scientific-design audit, **not** an independent N0 sign-off, D0 sign-off, or model result.

## Cross-project invariants

Both harnesses now enforce the same repository-level safeguards:

- no API or LLM judge; primary scoring is exact local continuation log probability over counterbalanced `A/B` choices;
- repeated identical score requests are lifetime-cached;
- result coverage and run metadata are validated before aggregation;
- case-level structure is preserved rather than treating prompt variants as independent samples;
- panel promotion counts only `model_pass=true` **and** `verdict=PASS-TO-PANEL`;
- `run` checks the frozen `validation_authorized` flag before model construction, so the current `false` state is a hard execution barrier;
- custom-only provenance cannot satisfy formal D0/G0.

## 006 — Existential Witness Collapse

### Scientific bug found and fixed

An earlier downstream formulation was too close to the recognition question: asking whether a shared witness is entailed twice would only measure logical judgment twice, not the required `recognition correct -> downstream illegal join` dissociation.

The frozen harness now separates the interfaces. Recognition asks whether each existential holds, whether a shared witness is entailed, and whether identity is determined. Downstream evaluation instead asks for a consequential action where one option is justified only if a single shared witness has actually been established.

### D0 validity strengthened

Formal D0 must certify all of the following simultaneously:

- a P-witness exists and a Q-witness exists;
- a joint witness is logically possible;
- distinct witnesses are logically possible;
- the premises do not identify which world holds;
- explicit-same evidence authorizes the collapse action;
- explicit-distinct evidence blocks it;
- unknown identity requires preserving uncertainty / obtaining identity evidence;
- paraphrase and neutral controls preserve the intended relation;
- the setting and source are externally anchored.

The two possibility checks are essential: without them, incompatible properties could force distinctness or the source facts could force co-reference, invalidating the claimed underdetermination.

### Promotion / kill logic

A case cannot count unless recognition passes and the model handles the explicit-same and explicit-distinct action controls across both answer orders. The target error is positive preference for the collapse action in the identity-unknown world, stable under natural paraphrase and separated from a neutral-context shift.

Model-level no-effect behavior is explicitly classified `HARD-KILL-NO-ILLEGAL-JOIN`; failure of the basic quantifier/identity gate is `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR` rather than evidence for the phenomenon.

### Offline verification

`15` unit/integration tests pass. The suite includes full synthetic result-matrix tests showing that a deliberately injected illegal-join signature can reach `PASS-TO-PANEL`, while a gate-correct model that preserves witness uncertainty is classified `HARD-KILL-NO-ILLEGAL-JOIN`. These fixtures validate the scorer/aggregator logic only and are not behavioral evidence.

## 007 — Weak-Evidence Backfire

### Scientific bugs found and fixed

1. An earlier no-evidence baseline said that no case-specific cue was observed. That sentence is itself an observation and could be negative evidence. The baseline now contains only background and calibration, with no observation block.
2. Treating target-support and other-support directions as independent samples would pseudoreplicate one natural case. The statistical unit is now the scenario-level bidirectional pair.
3. Aggregate backfire could hide prompt variants with the normal sign. Primary, completeness, and length controls now require within-template/answer-order sign consistency.
4. A two-choice normalized probability can stand in for posterior odds only when the alternatives form a proper binary partition. Formal D0 therefore requires hypotheses to be both mutually exclusive **and exhaustive**, in addition to the binary-choice validity audit.

### Exact positive-evidence contract

Each scenario contains weak and strong evidence in both directions, plus neutral evidence. D0 stores externally audited likelihood-ratio relations:

```text
1 < weak_target_lr < strong_target_lr
0 < strong_other_lr < weak_other_lr < 1
neutral_lr = 1
```

Before a direction can enter the denominator, the model must itself recognize weak support, the likelihood direction, support under the completeness protocol, strong support, strong>weak diagnosticity, and neutral non-diagnosticity. Strong evidence must move both belief and consequential action in the normatively correct direction.

The target backfire is sign-coded symmetrically: target-support must lower target preference, and other-support must raise target preference. A scenario is strong only if both directions satisfy the sign reversal.

### Pragmatic and surface controls

The completeness contrast uses a matched baseline and explicitly states that omission of other possible cues conveys no information. If the ordinary reversal disappears there, the verdict is `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`. A separate matched-length protocol and neutral cue distinguish this from protocol length or generic mention effects.

### Offline verification

`15` unit/integration tests pass. Full synthetic result matrices verify three opposite paths: a deliberately injected bidirectional sign reversal can reach `PASS-TO-PANEL`; ordinary Bayesian-direction updates become `HARD-KILL-NO-BACKFIRE`; and a reversal that disappears under the completeness protocol becomes `HARD-KILL-PRAGMATIC-ABSENCE-IMPLICATURE`. These fixtures validate decision logic only and are not model evidence.

## What remains intentionally unverified

The harnesses are sufficient to test the **behavioral G0 contracts** once real D0 data exist. They do not and should not certify novelty, data validity, generality, or mechanism by themselves.

Before any formal model call, each project still needs an independent N0 reviewer, external data/license/gold resolution, the required random manual D0 audit, and an authoritative registry update. Mechanism experiments remain out of scope until smoke, N1, cross-family/scale, and strong-model gates survive.
