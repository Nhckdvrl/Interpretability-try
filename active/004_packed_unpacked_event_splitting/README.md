# 004 — Packed–Unpacked Event Splitting

Status: `ACTIVE-PREFLIGHT / HARNESS-R2-READY / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #2**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

If a model explicitly recognizes that a packed event `E` and an unpacked mutually-exclusive, exhaustive partition `E1 ∨ ... ∨ Ek` denote the **same extension**, does its own probability or consequential decision valuation still change merely because the event was split into explicit branches?

The r2 harness deliberately does **not** put packed and unpacked descriptions side by side and ask which is larger. That direct comparison can measure explicit extensional-rule compliance instead of the model's underlying probability/value reader. Packed, unpacked and controls are therefore judged in isolated prompts under the same frozen information context, then compared offline.

## What must be true before an effect counts

The project only survives if the model first recognizes equivalence, mutual exclusivity and exhaustiveness under label reversal. A D0 record must also freeze a natural strict-subset description and, when provided, a repacked equivalent form. Public-derived transformations must retain provenance and an explicit derivation rule.

A packed/unpacked effect is not enough by itself. Ordinary packed paraphrases should remain near the packed score; a strict subset must not become more probable than the full event beyond tolerance; repacking should return near the packed value; threshold responses must be approximately monotone; and Yes/No label reversal must not explain the result.

## Isolated readout

Each description is presented independently with the same `information_context`. Two probability prompts ask whether the event probability exceeds a frozen threshold grid, and two consequential prompts ask whether a risk-neutral $100 event contract exceeds a frozen fair-price grid. Both Yes/No label orders are scored by exact local continuation log-probability.

The threshold survival curve is integrated into a normalized score. The decisive quantity is therefore

```text
core_unpacked_bias = isolated_score(unpacked) - isolated_score(packed)
```

reported separately for probability and fair-value readouts before pooling. This avoids an LLM judge and avoids treating an explicit comparison answer as the phenomenon itself.

## D0 schema

Formal G0 consumes external or transparently public-derived records:

```json
{
  "scenario_id": "forecast:...",
  "domain": "forecast",
  "information_context": "information available before resolution...",
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
    "partial_unpacked_text": "...",
    "disjoint_gold": true,
    "exhaustive_gold": true,
    "equivalent_gold": true,
    "partial_is_strict_subset": true,
    "repacked_text": "...",
    "repacked_equivalent_gold": true
  }]
}
```

For branch-count analysis, D0 should provide multiple valid `k` partitions of the **same scenario/event**. The summary computes `k` slopes within scenario rather than comparing unrelated easy/hard items.

An optional complement frame can be supplied with `alternative_packed_text`, `alternative_branches`, `alternative_unpacked_text` and frozen complement/equivalence gold. It measures the Support-Theory-style diagnostic of whether unpacking the alternative changes the focal event's isolated valuation. This diagnostic is reported separately and is not allowed to rescue a missing core packed→unpacked effect.

## Why each control exists

- relation probes establish that any later difference is not merely failure to understand the partition;
- packed paraphrase estimates ordinary wording sensitivity;
- strict-subset recognition plus probability monotonicity distinguishes a real extension relation from generic list/length confusion without assuming a strict probability gap when an omitted branch might have zero mass;
- repacking tests reversibility of the representation change;
- within-scenario branch-count trajectories test a structural prediction without cross-item difficulty confounding;
- probability vs fair-value readouts test whether the effect reaches a consequential decision surface rather than one particular verbal interface;
- threshold monotonicity and label reversal expose scorer/interface artifacts.

## Model-panel contract

Two independent families are enough only for the repository's cheap smoke. Generality requires the full five-family panel, at least `3/5` families passing the same frozen contract, at least one family with three passing sizes, and survival on at least one checkpoint of `>=24B`. Failed families and sizes remain part of the report.

## Commands

```bash
cd active/004_packed_unpacked_event_splitting
python -m pip install -e '.[run,dev]'
pytest -q

packed-unpacked-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --out results/qwen3_8b.jsonl

packed-unpacked-run summarize \
  --data data/frozen_d0.jsonl \
  --results results/qwen3_8b.jsonl \
  --config configs/frozen_g0.json \
  --out results/qwen3_8b.summary.json
```

Do not execute model inference until the authoritative registry has the required N0/D0 authorization. The harness being ready is not a novelty sign-off.

## Hard kill / hold logic

Kill or route the standalone claim if the isolated effect vanishes after relation gating, ordinary paraphrase or repacked controls explain it, subset monotonicity fails, the effect lives only in one prompt/label interface, or it does not reproduce across the required model families. If the only apparent branch-count trend is cross-item rather than within-event, it is not evidence for the structural signature. White-box probe/SAE/patching work remains forbidden before behavioral generality clears.
