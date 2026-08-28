# 005 — Inadmissible-Evidence Persistence

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r2 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #5**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

When a model correctly recognizes that a piece of evidence is excluded from the verdict, understands the exclusion scope, and can identify which side the evidence favors, can it actually restore its verdict state toward the **counterfactual in which that evidence was never seen**?

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

A persistence case requires an admitted update in the expected direction and a positive residual after exclusion, despite passing the rule/scope/polarity recognition gate.

## Why r2 exists

The first harness had three important logic problems. r2 fixes them:

- the scope-recognition probe and the actual struck-verdict prompt now contain the **same exclusion scope**; previously the model could pass a scope question using information absent from the decision context;
- the primary verdict question is now neutral/natural, while an explicit “apply the evidentiary ruling” prompt is a separate rescue diagnostic instead of being averaged into the effect;
- model pass now requires persistence in **both** evidence directions, not merely the presence of at least one gated case of each polarity. The old baseline-distance-from-0.5 gate is removed because a clean 50/50 counterfactual baseline is not a capability failure.

The neutral-struck control is also mandatory in formal D0 rather than optional.

## Formal D0 contract

```json
{
  "scenario_id": "...",
  "domain": "legal",
  "case_facts": "...",
  "evidence_text": "...",
  "evidence_polarity": "supports_target",
  "target_verdict": "...",
  "other_verdict": "...",
  "admissible_ruling": "...",
  "struck_ruling": "...",
  "exclusion_scope": "...",
  "neutral_evidence_text": "...",
  "neutral_struck_ruling": "...",
  "struck_gold": true,
  "must_ignore_for_verdict_gold": true,
  "neutral_evidence_gold": true,
  "source": {
    "dataset": "...",
    "record_id": "...",
    "split": "...",
    "license": "...",
    "url": "...",
    "provenance": "external"
  }
}
```

The core dataset must contain both `supports_target` and `supports_other`. `neutral_evidence_gold` means the neutral control is audited not to favor either verdict. Formal G0 rejects custom-only provenance.

## What is measured

### Recognition gate

The model must separately pass:

- evidence is excluded from the verdict;
- the supplied exclusion scope applies to the asked verdict;
- ignoring admissibility, the evidence favors the audited side.

Every probe uses reversed A/B labels.

### Natural three-world verdict readout

The primary template simply asks which outcome is better supported by the case record. The struck condition itself contains the ruling and the same exclusion scope used by the recognition probe. Both answer orders are run.

The admitted condition is a capability/sensitivity check: if the evidence does not move the model in its audited direction when admitted, that case cannot diagnose whether striking the evidence successfully undoes an update.

### Explicit-rule rescue

A second template explicitly says to apply the evidentiary ruling first. It is reported separately. If the residual disappears only under this reminder, that is a potentially useful access/use signature; it is not mixed into the primary natural phenotype.

### Neutral struck control

A matched neutral piece of excluded material is required. If adding neutral struck material moves the verdict by a comparable amount, the effect is more parsimoniously generic context/salience persistence than content-specific inadmissible-evidence persistence.

### Polarity symmetry

Supports-target and supports-other cases are aggregated separately. Formal model pass requires a minimum number of gated cases and a positive mean struck residual **in each direction**. A one-sided result is `HOLD-POLARITY-ASYMMETRY`, not a pass.

## Reproducibility

Raw rows record model, family, exact revision, explicit parameter size (`size_b`) and requested dtype. Scoring uses exact continuation probability; no LLM judge or paid API is used. The local execution log should additionally freeze torch/transformers and chat-template versions.

## Commands

```bash
cd active/005_inadmissible_evidence_persistence
python -m pip install -e '.[run,dev]'

inadmissible-evidence-run run \
  --data data/frozen_d0.jsonl \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --out results/qwen3_8b.jsonl

inadmissible-evidence-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json

pytest -q
```

The registry remains the authority for formal dispatch; exploratory local runs must not be mislabeled as formal G0 before independent N0/D0 sign-off.

## Kill / hold logic

Kill/route if the residual disappears after recognition gating, admitted evidence has no directional effect, neutral struck content moves the verdict comparably, or cross-family behavior fails. Hold rather than pass if persistence is one-sided across evidence polarity. A result surviving only under one answer order or one prompt template is not the target phenotype.

No probe/patching/SAE sweep should start before the behavioral phenotype clears the repository’s generality gates.
