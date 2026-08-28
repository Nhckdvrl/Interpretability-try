# 004 — Packed–Unpacked Event Splitting

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r4 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #2**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

If a model can explicitly recognize that a packed event `E` and an unpacked mutually-exclusive, exhaustive partition `E1 ∨ ... ∨ Ek` denote the **same extension**, does its probability or equal-payoff decision value still increase merely because the event is represented as explicit branches?

The target is not generic paraphrase sensitivity. A useful phenotype must survive relation/capability checks and must separate partition structure from position, labels, wording, list order, verbosity, non-exhaustive subsets and arbitrary taxonomies.

## Why r4 exists

The earlier harness was runnable but still allowed several alternative explanations. r4 closes the remaining important holes:

- the relation gate now checks the **focal partition, the complement partition, and the focal/complement pair**; focal-vs-alternative effects are not interpreted when the model fails those relations;
- each primary readout has **two neutral natural phrasings**; explicit extensional reminders remain rescue diagnostics and are never pooled into the natural phenotype;
- the same unpacking is tested with a **reordered branch list**, so branch-order sensitivity cannot masquerade as partition dependence;
- focal-vs-alternative unpacking is measured relative to a packed baseline and then corrected by **length/verbosity-matched equivalent controls**;
- branch-count evidence is only computed inside a frozen `branch_count_family`, i.e. a D0-audited refinement family for the same source scenario; unrelated taxonomies from the same question cannot create a fake `k` slope;
- the generality panel is locked to the repository’s five required families: **Qwen, Gemma, Phi, Llama, Mistral**. Extra family names cannot replace a missing required family.

## Formal D0 contract

Every row must be anchored to an external/public record. All relation/gold fields are frozen before model output is inspected.

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
    "reordered_unpacked_text": "...same branches, different order...",
    "repacked_text": "...",
    "partial_text": "...",

    "complement_text": "...",
    "complement_branches": ["...", "...", "..."],
    "complement_unpacked_text": "...",

    "focal_length_control_text": "...verbose but still packed/equivalent focal wording...",
    "complement_length_control_text": "...verbose but still packed/equivalent complement wording...",

    "branch_count_family": "stable-refinement-family-id",

    "disjoint_gold": true,
    "exhaustive_gold": true,
    "equivalent_gold": true,
    "partial_is_strict_subset": true,
    "partial_strictly_lower_probability_gold": true,
    "complement_gold": true,
    "complement_partition_gold": true,
    "reordered_equivalent_gold": true,
    "length_controls_equivalent_gold": true,
    "length_controls_matched_gold": true,
    "branch_count_comparable_gold": true
  }]
}
```

`partial_strictly_lower_probability_gold` is stronger than set inclusion: the omitted branch must have genuine positive probability/viability at the information state. `branch_count_comparable_gold` means different `k` values sharing the same `branch_count_family` are true refinements of the same underlying event/taxonomy rather than unrelated alternative decompositions.

For a formal D0, provide enough scenarios with at least two different `k` values in the same refinement family; the frozen model-level contract currently requires at least five matched branch-count groups before a panel pass is possible.

## What the harness tests

### Relation gate

Before the behavioral effect counts, the model must recognize:

- focal packed ↔ focal unpacked equivalence, focal disjointness and focal exhaustiveness;
- complement packed ↔ complement unpacked equivalence, complement disjointness and complement exhaustiveness;
- focal and complement are mutually exclusive and jointly exhaustive for the relevant outcome space.

Each binary probe uses both A/B label orders.

### Primary natural phenotype

Probability and equal-payoff decision value are primary. Each has two neutral natural question phrasings. Packed/unpacked forms are counterbalanced on LEFT/RIGHT and every A/B/C semantic assignment is run.

```text
core_unpacked_bias = P(unpacked judged higher) - P(packed judged higher)
```

Frequency remains a diagnostic readout rather than a substitute for failed probability/decision evidence.

### Artifact and structural controls

- **ordinary paraphrase:** should not reproduce the core effect;
- **strict subset:** a D0-audited lower-probability subset must be judged below the full event;
- **branch reorder:** reordering the same branch set should preserve the unpacking effect within tolerance;
- **repacking:** compressing the branch list back into a packed description should reduce the effect;
- **focal vs alternative:** compare packed baseline, focal-unpacked and alternative-unpacked judgments;
- **length-matched controls:** subtract the corresponding shifts from verbose-but-still-packed focal/complement controls before treating focal-vs-alternative movement as Support-Theory-like structure;
- **branch count:** estimate `k` slope only inside `(scenario_id, branch_count_family)` groups;
- **natural prompt robustness:** promotion requires the target direction across the natural template/readout cells, not one lucky wording;
- **explicit extensional reminder:** reported separately as a rescue diagnostic.

Scenario is the statistical unit. Multiple partitions from the same source scenario are not treated as independent bootstrap observations.

## Commands

```bash
cd active/004_packed_unpacked_event_splitting
python -m pip install -e '.[run,dev]'
pytest -q

packed-unpacked-run run \
  --data data/frozen_d0.jsonl \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --revision <exact-revision-if-available> \
  --out results/qwen3_8b.jsonl

packed-unpacked-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json
```

Formal dispatch remains controlled by `phenomenon_miner/candidate_pool/AUDIT_REGISTRY.md`. Do not relabel exploratory local results as `READY-TO-SMOKE` without independent N0 + D0 sign-off.

## Kill / hold interpretation

A positive pooled number is not enough. Generic wording/position/order/length effects, failure of focal/complement relations, missing repacking/focal-alternative structure, an unstructured branch-count pattern, prompt-slice dependence, or cross-family failure blocks promotion. White-box mechanism work remains downstream of the behavioral/generalization gates.
