# 004 — Packed–Unpacked Event Splitting

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r2 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #2**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

If a model can explicitly recognize that a packed event `E` and an unpacked mutually-exclusive, exhaustive partition `E1 ∨ ... ∨ Ek` denote the **same extension**, does its probability or equal-payoff decision value still increase merely because that same event is represented as more branches?

This is not generic paraphrase sensitivity. Formal G0 asks whether a representation-only partition operator produces a directional judgment change **after** extensional recognition succeeds, while ordinary paraphrase, strict-subset, repacking, focal/alternative and position controls behave differently.

## Why r2 exists

The first harness was runnable but scientifically incomplete. r2 fixes four important problems:

- the core comparison is now left/right counterbalanced; A/B/C label permutation alone was not enough to rule out presentation-side bias;
- the primary readout is now a neutral natural question; explicit extensional reminders are a separate rescue diagnostic rather than being averaged into the phenotype;
- branch-count effects are estimated **within the same source scenario**, and bootstrap uncertainty is clustered at scenario level rather than treating multiple partitions from one record as independent;
- the D0 contract now includes focal-vs-alternative unpacking and a strict-subset control whose omitted mass is frozen as genuinely positive, so “strict subset” is not incorrectly assumed to imply strictly smaller probability by logic alone.

## Formal D0 contract

Every row must be anchored to an external/public record. Human/D0 audit must freeze the relation before any model output is inspected.

```json
{
  "scenario_id": "forecastqa:...",
  "domain": "forecast",
  "packed_text": "...",
  "packed_paraphrase": "...",
  "source": {
    "dataset": "...",
    "record_id": "...",
    "split": "...",
    "license": "...",
    "url": "...",
    "provenance": "external"
  },
  "partitions": [{
    "partition_id": "k3-a",
    "branches": ["...", "...", "..."],
    "unpacked_text": "...",
    "repacked_text": "...",
    "partial_text": "...",
    "complement_text": "...",
    "complement_branches": ["...", "...", "..."],
    "complement_unpacked_text": "...",
    "disjoint_gold": true,
    "exhaustive_gold": true,
    "equivalent_gold": true,
    "partial_is_strict_subset": true,
    "partial_strictly_lower_probability_gold": true,
    "complement_gold": true,
    "complement_partition_gold": true
  }]
}
```

`partial_strictly_lower_probability_gold` is deliberately stronger than set inclusion: the removed branch must have genuine positive probability/viability at the task information state. The loader rejects custom-only provenance for formal G0.

For the branch-count diagnostic, prefer at least two partitions with different `k` for the **same scenario**. Cross-scenario branch-count comparisons are not treated as evidence for the structural curve.

## What is measured

### Capability / relation gate

For every partition, equivalence, mutual exclusivity and exhaustiveness are checked independently, each with Yes/No label reversal. The core effect is interpreted only after this gate.

### Primary natural phenotype

Both probability and equal-payoff contract valuation use a neutral natural question. Packed and unpacked/controlled forms appear on both LEFT and RIGHT, and all six A/B/C semantic assignments are run. The directional score is always mapped back to the semantic variant, so position bias cancels rather than being mistaken for unpacking.

```text
core_unpacked_bias = P(unpacked judged higher) - P(packed judged higher)
```

The primary aggregate uses only `template_kind=natural`.

### Explicit extensional reminder

A second template explicitly reminds the model that logically equivalent events should have equal probability/value. This is **not** included in the primary mean. Its purpose is diagnostic: if the natural phenotype is rescued by an explicit invariant reminder, that tells us something about access/use rather than existence of the behavior.

### Controls and structural signatures

- **packed paraphrase:** a normal equivalent rewording should not reproduce the unpacking bias;
- **strict subset:** the audited lower-probability subset should be judged below the full event;
- **repacking:** converting the explicit branch list back to a compact description should shrink the core bias;
- **focal vs alternative unpacking:** for a matched focal/complement pair, unpacking the focal side should shift the focal-vs-complement judgment differently from unpacking the alternative side;
- **branch count:** slope is computed only from different `k` partitions of the same scenario;
- **readout consistency:** probability and consequential decision are reported separately and must point in the same direction for a strong case.

## Statistical unit

A source scenario may contribute multiple partitions. Those are correlated manipulations, not independent observations. Model-level mean, strong fraction and bootstrap CI therefore use equal-weight **scenario-level** aggregates. Partition-level rows are still retained for error-shape inspection.

## Reproducibility

Each raw row records model, family, exact revision, explicit parameter size (`size_b`) and requested dtype. Exact continuation log-probability is used; there is no LLM judge or paid API. The local execution log should additionally freeze the environment and chat-template versions used for the run.

## Commands

```bash
cd active/004_packed_unpacked_event_splitting
python -m pip install -e '.[run,dev]'

packed-unpacked-run run \
  --data data/frozen_d0.jsonl \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --out results/qwen3_8b.jsonl

packed-unpacked-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json

pytest -q
```

The repository registry still controls formal dispatch. Exploratory local runs must not be relabeled `READY-TO-SMOKE` without independent N0 and D0 sign-off.

## Kill / hold logic

Kill or route the standalone topic if the natural-readout effect vanishes after relation gating, ordinary paraphrase explains comparable movement, the strict-subset control fails, focal/alternative and repacking structure disappear, or cross-family replication fails. A signal surviving only under one prompt slice or one presentation side is an artifact, not the phenomenon.

White-box work remains downstream of behavioral/cross-family G0.
