# 005 — Inadmissible-Evidence Persistence

Status: `ACTIVE-PREFLIGHT / HARNESS-R2-READY / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #5**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

When a model correctly recognizes that evidence has been ruled inadmissible / struck, understands that the exclusion applies to the verdict, and correctly knows which side the evidence favors, can it actually restore its verdict state toward the counterfactual in which that evidence was **never seen**?

The decisive contrast is:

```text
A. never_seen
B. same evidence + admitted
C. same evidence + struck / excluded
```

The phenomenon is not “the model does not know hearsay/admissibility rules.” A case enters the persistence analysis only after the model passes same-context admissibility, scope and evidence-polarity gates.

## Same-context dissociation

The r2 harness constructs the struck context once and uses that exact context for both recognition probes and the final struck-verdict readout. `EXCLUSION SCOPE` is therefore not extra help that appears only in the capability probe. The polarity probe also names the concrete TARGET and OTHER verdicts before asking which one the evidence favors.

This matters because the intended claim is a genuine `knows the veto → still fails to undo` dissociation. If recognition and action see materially different information, the claim is not licensed.

## Core measurement

For each prompt template and both answer-label orders, the harness estimates `P(target)` under never-seen, admitted and struck worlds. If the evidence favors the target, the directional sign is positive; if it favors the other verdict, the sign is reversed. We compute:

```text
admitted_shift = sign(evidence) * [P(target | admitted) - P(target | never_seen)]
struck_residual = sign(evidence) * [P(target | struck) - P(target | never_seen)]
undo_ratio = struck_residual / admitted_shift
```

The admitted condition is a sensitivity/capability gate: if the evidence does not move the model in the expected direction when legally usable, absence of a struck effect tells us little. There is deliberately no requirement that the never-seen baseline be far from 50%; a balanced baseline can be an excellent case.

## D0 schema

Formal G0 consumes external or transparently public-derived records and freezes the legal/decision relation before model evaluation:

```json
{
  "scenario_id": "...",
  "domain": "legal",
  "case_facts": "...",
  "evidence_text": "...",
  "evidence_polarity": "supports_target",
  "polarity_gold": true,
  "target_verdict": "...",
  "other_verdict": "...",
  "admissible_ruling": "...",
  "struck_ruling": "...",
  "exclusion_scope": "...",
  "admitted_gold": true,
  "struck_gold": true,
  "exclusion_scope_gold": true,
  "must_ignore_for_verdict_gold": true,
  "neutral_evidence_text": "...",
  "neutral_struck_ruling": "...",
  "neutral_gold": true,
  "polarity_pair_id": "pair-001",
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

A `polarity_pair_id` links two rows with the same baseline case facts, verdict meanings and exclusion scope but opposite evidence directions. These matched pairs test whether persistence follows evidence content rather than one-sided target-label or base-rate preference. Formal model pass requires enough complete pairs; unpaired cases can still be retained as additional evidence.

Neutral controls must use their own matched `neutral_struck_ruling`. Reusing a core ruling that semantically refers to different evidence would create an artificial control.

## Why each validation exists

- inadmissibility recognition rules out simple legal-rule ignorance;
- scope recognition rules out misunderstanding of whether the exclusion applies to this verdict;
- polarity recognition rules out failure to understand what the evidence would imply if admitted;
- the admitted shift proves the case is behaviorally sensitive to the evidence;
- the struck residual measures failure to counterfactually undo that update;
- both evidence directions must show positive residuals, preventing one-sided label/base-rate effects from passing;
- matched opposite-polarity pairs ask whether the residual reverses with evidence content under the same baseline;
- neutral struck material tests generic salience/length/presentation persistence;
- two verdict templates and both label orders prevent one interface from carrying the claim.

The model-level pass requires minimum evidence on **both** `supports_target` and `supports_other`, both prompt templates, sufficient neutral-control coverage and matched polarity-pair consistency. A large aggregate mean cannot compensate for failure of one direction.

## Model-panel contract

Two independent families are enough only for cheap smoke. Generality requires the full five-family panel, at least `3/5` families passing, one family with three passing sizes, and at least one passing checkpoint of `>=24B`. Failed families and sizes remain reportable rather than being dropped after inspection.

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
  --out results/qwen3_8b.jsonl

inadmissible-evidence-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json
```

Do not run model inference until the authoritative registry has the required independent N0/D0 authorization. Harness readiness does not create that authorization.

## Hard kill / hold logic

Kill the standalone topic if persistence vanishes after same-context recognition gates, if admitted evidence itself has no usable effect, or if one evidence direction fails while the other drives the aggregate. Hold rather than promote when matched neutral material moves the verdict comparably, neutral coverage is too sparse, or matched polarity-pair structure is inadequate. Prompt-template or answer-label dependence also blocks promotion. No probe, SAE, activation patching or other white-box mechanism work is permitted before cross-family behavioral generality clears.
