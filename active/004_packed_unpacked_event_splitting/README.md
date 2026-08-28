# 004 — Packed–Unpacked Event Splitting

Status: `ACTIVE-PREFLIGHT / HARNESS-READY / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #2**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

If a model explicitly recognizes that a packed event `E` and an unpacked, mutually-exclusive, exhaustive partition `E1 ∨ ... ∨ Ek` denote the **same extension**, does its probability or consequential decision weight still increase merely because the event was split into branches?

This project is not “prompt wording changes probability.” The standalone contract requires:

1. equivalence / disjointness / exhaustiveness recognition passes first;
2. `packed ↔ unpacked` changes only the event partition representation;
3. ordinary packed paraphrase does **not** reproduce the effect;
4. a genuinely non-exhaustive strict subset is distinguished correctly;
5. branch-count and repacking diagnostics are reported rather than cherry-picked.

If generic wording sensitivity explains the core effect, or the relation gate fails, kill the standalone topic.

## D0 input contract

Input is JSONL. Every row must be anchored to an external/public record and freeze the extensional relation before model evaluation:

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
    "unpacked_text": "(...) or (...) or (...) ",
    "repacked_text": "...",
    "disjoint_gold": true,
    "exhaustive_gold": true,
    "equivalent_gold": true,
    "partial_is_strict_subset": true
  }]
}
```

The loader rejects `synthetic/custom-only` provenance for formal G0. Synthetic examples are allowed only in unit tests.

## What the harness measures

- **Relation gate:** equivalence, mutual exclusivity, exhaustiveness, each with Yes/No label reversal.
- **Core probability readout:** packed vs unpacked, 2 natural prompt templates × all 6 A/B/C semantic label permutations.
- **Consequential readout:** equal-payoff contract/bet valuation, same counterbalancing.
- **Paraphrase control:** packed vs ordinary packed paraphrase.
- **Strict-subset control:** packed vs one-branch-omitted representation; the model must prefer the full packed event.
- **Repacking diagnostic:** when D0 provides a repacked form, the unpacking bias should shrink.
- **Branch-count curve:** effect is summarized by number of branches rather than only a pooled mean.
- **Bootstrap CI + hard-kill logic:** no hidden judge and no API dependency.

The semantic effect score is:

```text
core_unpacked_bias = P(unpacked higher) - P(packed higher)
```

after recognition gating. An “equal” response is not silently counted as support for either side.

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

Do not execute the model command until the authoritative registry has independent N0, D0 and `validation_authorized: true`.

## Frozen hard-kill conditions

Kill/route the standalone claim if any of the following is the dominant explanation:

- the model cannot reliably recognize equivalent/disjoint/exhaustive partitions;
- packed-vs-packed-paraphrase bias is of comparable size;
- the model fails the strict-subset control, indicating generic list/length confusion;
- the cross-family phenotype does not reproduce;
- the only surviving signal is an arbitrary prompt-template slice;
- independent N0 finds an existing LLM study with the same recognized-extensionality + partition manipulation + consequential readout contract.

White-box work is forbidden before the behavior clears the repository’s cross-family G0.
