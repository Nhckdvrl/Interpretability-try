# 005 — Inadmissible-Evidence Persistence

Status: `ARCHIVED / TERMINAL-HOLD-D0V3-CONTRACT`

The current operationalization was archived after the one-time r5 calibration.
The abstract scientific question is retained; no D0 v4/v5 repair is authorized.

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #5**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
behavioral_verdict: TERMINAL-HOLD-D0V3-CONTRACT
```

## Mother question

When a model correctly recognizes that evidence is excluded from the verdict, understands the exclusion scope, and correctly identifies which verdict the evidence favors, can it restore its decision state toward the **counterfactual in which that evidence was never seen**?

The decisive three-world comparison is:

```text
A. never_seen
B. same evidence seen + admitted
C. same evidence seen + struck/excluded
```

For evidence direction `s ∈ {+1,-1}`:

```text
admitted_shift = s * [P(target | admitted) - P(target | never_seen)]
struck_residual = s * [P(target | struck) - P(target | never_seen)]
undo_ratio = struck_residual / admitted_shift
```

The original UDH-11 contract adds an essential causal check: the **same base case** must be paired with inadmissible evidence that is content-swapped from supporting TARGET to supporting OTHER. If struck content still causally votes, the final verdict should move with that swap despite the admissibility mask.

## D0 v2 forensic verdict

D0 v2 is invalid for deciding UDH-11. Its polarity probe mapped pro-TARGET to
semantic Yes and pro-OTHER to semantic No, while `never_seen` retained a
reference to a missing “statement below.” Qwen had 11/20 pairs pass rule/scope
plus the admitted pair operator, but 8 were then killed only by the polarity
probe; Gemma had 8/20 and 3 such probe-induced failures. Both models still had
only one fully gated pair, and neutral salience remained an independent blocker.

## r5 final calibration fixes

- Polarity is a direct choice between the two real verdicts; TARGET/OTHER option
  order is counterbalanced. The asymmetric semantic Yes/No probe is deleted.
- Explicit polarity recognition is diagnostic. The paired admitted content-swap
  operator is the primary capability gate.
- `never_seen` case facts are validated against dangling “statement/evidence
  below” references.
- Exclusion reason is a registered factor:
  `procedural_truth_neutral` versus `reliability_based`.
- Core uncertainty is bootstrapped over `polarity_pair_id`, not over the two
  correlated case members.
- Formal D0 requires a `polarity_pair_id`; every pair contains exactly one `supports_target` and one `supports_other` record with the same base facts, verdict definitions, rulings, scope, and neutral control.
- Model promotion requires a paired content-swap signature, not merely positive pooled residuals from unrelated pro-target/pro-other cases.
- Neutral struck material must be small both absolutely and relative to the target residual, so a comparable generic context/salience shift cannot pass.
- Two neutral natural verdict phrasings and both answer orders remain primary robustness checks; explicit rule reminder remains diagnostic only.
- Panel promotion counts only frozen Qwen/Gemma/Phi/Llama/Mistral families and only summaries whose verdict is actually `PASS-TO-PANEL`.

## Formal D0 contract

```json
{
  "scenario_id": "case:17:pro-target",
  "polarity_pair_id": "case:17",
  "domain": "legal",
  "case_facts": "...same in both pair members...",
  "evidence_text": "...inadmissible content supporting TARGET...",
  "evidence_polarity": "supports_target",
  "target_verdict": "...",
  "other_verdict": "...",
  "admissible_ruling": "...same in both pair members...",
  "struck_ruling": "...same in both pair members...",
  "exclusion_scope": "...same in both pair members...",
  "neutral_evidence_text": "...same matched neutral content...",
  "neutral_struck_ruling": "...same...",
  "exclusion_reason_type": "procedural_truth_neutral | reliability_based",
  "admitted_gold": true,
  "struck_gold": true,
  "must_ignore_for_verdict_gold": true,
  "evidence_polarity_gold": true,
  "exclusion_scope_gold": true,
  "baseline_excludes_evidence_gold": true,
  "neutral_evidence_gold": true,
  "neutral_control_matched_gold": true,
  "neutral_ruling_matched_gold": true,
  "content_swap_gold": true,
  "matched_base_gold": true,
  "baseline_no_dangling_reference_gold": true,
  "exclusion_reason_gold": true,
  "polarity_options_symmetric_gold": true,
  "pair_statistical_unit_gold": true,
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

Each `polarity_pair_id` must occur exactly twice. The loader enforces matching base fields and opposite evidence polarity. The content swap may be an audited transformation derived from public data, but the underlying case/rule/gold must remain externally anchored.

## What the harness tests

The recognition gate checks inadmissibility and scope. Direct verdict-choice
polarity recognition is retained as a diagnostic. A pair enters the primary
analysis only when the target-support and other-support admitted worlds separate
in the audited direction across natural templates and answer orders.

Natural `never_seen / admitted / struck / neutral_struck` judgments are scored with exact continuation probability across two natural phrasings and both answer orders. Rule-reminder responses are kept separate as a rescue diagnostic.

For a matched polarity pair:

```text
admitted_polarity_delta =
    P(target | admitted, pro-target evidence)
  - P(target | admitted, pro-other evidence)

struck_polarity_delta =
    P(target | struck, pro-target evidence)
  - P(target | struck, pro-other evidence)
```

The first confirms that the swapped content has real directional force when
admissible. The second is the decisive UDH-11 operator: if it remains positive
after both evidence items are correctly struck, inadmissible content is still
influencing the verdict accumulator.

This r5 run is a one-time harness calibration, not a formal model pass. It
requires at least 80% pair capability, at least four gated pairs in each
exclusion-reason stratum, and neutral-artifact fraction at most 0.10 before any
phenotype statistic is interpretable.

The frozen stop rule is one Qwen3-8B plus Gemma3-12B calibration on 12 pairs.
Failure ends this operationalization; no v4/v5 repair loop is allowed. A clean
negative struck delta is recorded only as an inversion diagnostic and is not an
authorized pivot to a new phenotype.

## Commands

```bash
cd archive/010_inadmissible_evidence_persistence
python -m pip install -e '.[run,dev]'
pytest -q

inadmissible-evidence-run run \
  --data data/frozen_d0_v3_calibration.jsonl \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --revision <exact-revision-if-available> \
  --out results/qwen3_8b.jsonl

inadmissible-evidence-run summarize \
  --data data/frozen_d0_v3_calibration.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json
```

Formal dispatch remains controlled by `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`; exploratory local runs must not be relabeled formal G0 without independent N0 + D0 sign-off.
