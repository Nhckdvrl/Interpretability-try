# 005 — Inadmissible-Evidence Persistence

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r3 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #5**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
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

A target case therefore requires both a real admitted update and a positive residual after exclusion; otherwise it is not evidence of failed counterfactual undo.

## Why r3 exists

r3 closes the remaining logic holes in the earlier harness:

- the polarity-recognition question now explicitly defines the **TARGET** and **OTHER** verdicts. Previously the probe asked which side the evidence favored without actually telling the model what those labels denoted;
- D0 must freeze not only exclusion status but also the admitted condition, evidence polarity, exclusion scope, never-seen baseline, neutral-control matching and neutral-ruling matching;
- the primary verdict behavior is measured with **two neutral natural phrasings**, while the explicit “apply the rule” wording remains a rescue diagnostic;
- a case/model cannot pass because one answer order or one natural wording drives the entire result: residual direction is audited separately for every natural-template × answer-order cell;
- the generality panel is locked to **Qwen, Gemma, Phi, Llama, Mistral**; arbitrary extra family names do not count toward the repository’s 3/5 contract.

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

  "admitted_gold": true,
  "struck_gold": true,
  "must_ignore_for_verdict_gold": true,
  "evidence_polarity_gold": true,
  "exclusion_scope_gold": true,
  "baseline_excludes_evidence_gold": true,
  "neutral_evidence_gold": true,
  "neutral_control_matched_gold": true,
  "neutral_ruling_matched_gold": true,

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

Interpretation of the additional D0 gold:

- `admitted_gold`: the evidence is genuinely usable in the admitted world;
- `evidence_polarity_gold`: an independent audit verifies the evidence favors the stated target/other side;
- `exclusion_scope_gold`: the exclusion really applies to the verdict being scored;
- `baseline_excludes_evidence_gold`: the never-seen condition contains none of the disputed evidence or a semantic duplicate;
- `neutral_control_matched_gold`: the neutral evidence is matched closely enough in presentation/salience to diagnose generic context effects;
- `neutral_ruling_matched_gold`: the neutral struck ruling has equivalent exclusion force/scope rather than being a weaker instruction.

Formal G0 rejects custom-only provenance. Both `supports_target` and `supports_other` must be represented.

## What the harness tests

### Recognition gate

The model must separately recognize:

- the evidence is excluded from the verdict;
- the supplied exclusion scope applies to the verdict question;
- ignoring admissibility, the evidence favors the D0-audited side.

TARGET and OTHER verdicts are printed explicitly in this probe. Each binary probe uses both A/B label orders.

### Natural three-world behavior

Two neutral natural verdict questions are run over `never_seen`, `admitted`, `struck` and `neutral_struck`. Both answer-label orders are used.

The admitted condition is a sensitivity gate: if admitted evidence does not move the model in the audited direction, the example cannot diagnose whether striking evidence successfully undoes an update.

For every natural-template × answer-order cell, the struck residual is retained. Strong cases and model pass require a high fraction of those cells to move in the same target direction, preventing one prompt/label slice from creating a pooled false positive.

### Explicit-rule rescue

A separate template explicitly tells the model to apply the evidentiary ruling first. Its residual is not mixed into the primary phenotype. `rule_reminder_rescue` asks whether explicit rule salience restores the counterfactual undo behavior.

### Neutral struck control

A matched neutral piece of excluded material is required. If neutral struck material produces comparable movement away from the never-seen state, the result is better explained as generic context/salience persistence.

### Polarity symmetry

Supports-target and supports-other cases are aggregated separately. Formal model pass requires sufficient gated examples and a positive mean residual in **both** directions. One-sided persistence becomes `HOLD-POLARITY-ASYMMETRY`, not a pooled pass.

## Commands

```bash
cd active/005_inadmissible_evidence_persistence
python -m pip install -e '.[run,dev]'
pytest -q

inadmissible-evidence-run run \
  --data data/frozen_d0.jsonl \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --revision <exact-revision-if-available> \
  --out results/qwen3_8b.jsonl

inadmissible-evidence-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json
```

Formal dispatch remains controlled by `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`. Exploratory local results must not be relabeled `READY-TO-SMOKE` without independent N0 + D0 sign-off.

## Kill / hold interpretation

Kill/route if the residual vanishes after recognition gating, admitted evidence has no directional effect, neutral struck material moves the verdict comparably, or the behavior does not survive cross-family validation. Hold rather than pass when only one evidence polarity survives or when the effect depends on one natural wording/answer order. No probe/patching/SAE sweep should precede the behavioral/generalization gates.
