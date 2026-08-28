# 005 — Inadmissible-Evidence Persistence

Status: `ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #5**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

When a model correctly identifies that evidence has been ruled inadmissible / struck and understands the exclusion scope, can it actually restore the verdict state toward the **counterfactual in which that evidence was never seen**?

The decisive three-way contrast is frozen:

```text
A. never_seen
B. evidence_seen + admitted
C. same evidence_seen + explicitly struck / excluded
```

The phenomenon is not “the model does not know hearsay law.” A case is analyzed only after the model passes:

- admissibility recognition;
- exclusion-scope recognition;
- evidence-polarity recognition.

Then the key residual is measured in the direction of the excluded evidence:

```text
admitted_shift = sign(evidence) * [P(target | admitted) - P(target | never_seen)]
struck_residual = sign(evidence) * [P(target | struck) - P(target | never_seen)]
undo_ratio = struck_residual / admitted_shift
```

A true persistence phenotype requires the struck residual to remain positive even though the model can state that the evidence must not be used.

## D0 input contract

Formal G0 consumes external/public records only:

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
  "struck_gold": true,
  "must_ignore_for_verdict_gold": true,
  "neutral_evidence_text": "...",
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

Core D0 must contain **both polarities** (`supports_target` and `supports_other`). This prevents a one-sided label/base-rate artifact from masquerading as persistence. The loader rejects custom-only provenance for formal G0.

## What the harness measures

- **Recognition gate:** inadmissibility, scope, polarity; every probe uses A/B label reversal.
- **Three verdict worlds:** never-seen, admitted, struck.
- **Two verdict prompt templates × both answer-label orders.**
- **Admissible-evidence capability gate:** the evidence must actually move the model in the correct direction when admitted; otherwise “no struck effect” is uninformative.
- **Counterfactual undo ratio:** how much of the admissible update survives after exclusion.
- **Bidirectional polarity audit:** inculpatory-like and exculpatory-like evidence must be analyzed separately.
- **Neutral struck control:** optional but strongly recommended; comparable movement from neutral struck material flags generic salience/length artifacts.
- **Bootstrap CI, per-domain summaries and hard-kill verdicts.**
- **No LLM judge and no paid API requirement.**

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

Do not execute the model command until the authoritative registry has independent N0, D0 and `validation_authorized: true`.

## Frozen hard-kill conditions

Kill/route the standalone topic when any of these dominates:

- failures are concentrated in samples where admissibility or exclusion scope itself is misunderstood;
- admitted evidence does not reliably shift the verdict, so the case lacks sensitivity;
- the struck residual does not track evidence polarity;
- neutral struck material creates a comparable shift, reducing the result to generic distractor/salience persistence;
- the residual disappears under answer-label and prompt-template counterbalancing;
- cross-family replication fails;
- independent N0 finds the same `never_seen / admitted / struck` counterfactual operator already studied as the core behavior.

No probe, patching, SAE or activation intervention is permitted before cross-family G0 clears.
