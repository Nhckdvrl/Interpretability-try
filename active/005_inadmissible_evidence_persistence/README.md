# 005 — Inadmissible-Evidence Persistence

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r4 / NOT READY-TO-SMOKE`

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

The original UDH-11 contract adds an essential causal check: the **same base case** must be paired with inadmissible evidence that is content-swapped from supporting TARGET to supporting OTHER. If struck content still causally votes, the final verdict should move with that swap despite the admissibility mask.

## r4 fixes

- TARGET and OTHER are explicitly defined in the polarity-recognition prompt.
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

The recognition gate checks inadmissibility, scope, and evidence polarity with reversed labels. The admitted world is a sensitivity gate: if the evidence does not move the model in the audited direction when admissible, the example cannot diagnose failed undo.

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

The first confirms that the swapped content has real directional force when admissible. The second is the decisive UDH-11 operator: if it remains positive after both evidence items are correctly struck, inadmissible content is still influencing the verdict accumulator. Formal model pass requires enough gated matched pairs and a positive paired bootstrap lower bound.

Supports-target and supports-other cases are still audited separately. One-sided persistence is `HOLD-POLARITY-ASYMMETRY`. Comparable neutral movement is `HOLD-GENERIC-SALIENCE-ARTIFACT`. Failing the paired operator after enough pairs is `FAIL-PAIRED-CONTENT-SWAP`.

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

Formal dispatch remains controlled by `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`; exploratory local runs must not be relabeled formal G0 without independent N0 + D0 sign-off.
