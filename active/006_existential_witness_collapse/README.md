# 006 — Existential Witness Collapse

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r2 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #4**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

Can a model explicitly understand that two existential witnesses are **not known to be the same individual**, yet still operationally reuse them as one person/resource when making a downstream staffing, assignment, compliance, or planning decision?

The forbidden inference is:

```text
exists x: P(x)
exists y: Q(y)
-----------------
NOT ENTAILED: exists z: P(z) and Q(z)
```

The contract does **not** assert that the two witnesses are different. A valid D0 item must make both worlds logically possible: one individual could satisfy both properties, and two distinct individuals could satisfy them. The record simply does not identify which world holds.

## Why r2 changes the downstream test

A direct question such as “do the premises entail one shared witness?” is useful only as a **recognition gate**. Asking essentially the same entailment question again with different wording would not establish a `knows-but-does-not-use` dissociation.

The primary downstream readout is therefore an action pair. Each item defines:

- a `collapse_action` that is justified only if one shared witness has actually been established;
- a `preserve_action` that keeps identity unresolved / obtains another resource / requests identity evidence.

The target phenotype is:

```text
recognition: shared witness is NOT entailed; identity is underdetermined
use:         choose collapse_action anyway
```

The predicted wrong destination is thus explicit: the model behaves as though the anonymous discourse referents had been joined.

## Matched identity worlds

Every item contains six conditions:

- `unknown`: only the two existential facts;
- `paraphrase`: the same facts in an independently audited natural paraphrase;
- `same_explicit`: explicit evidence that one and the same witness satisfies both;
- `distinct_explicit`: explicit evidence that different witnesses satisfy them;
- `neutral_control`: matched extra context that does not bear on identity;
- `relation_reminder`: a diagnostic reminder that separate existentials do not establish identity.

A case enters the denominator only if the model passes four recognition probes (`exists P`, `exists Q`, no shared-witness entailment, identity underdetermined) **and** handles the explicit-same and explicit-distinct action controls. The same/distinct controls must also be stable across both natural decision phrasings and both answer orders.

## Formal D0 contract

```json
{
  "scenario_id": "staff:17",
  "domain": "staffing",
  "premise_p": "At least one technician inspected the cooling system.",
  "premise_q": "At least one technician inspected the power system.",
  "premise_paraphrase": "...equivalent natural wording preserving two independent existential introductions...",
  "p_property": "inspected the cooling system",
  "q_property": "inspected the power system",
  "shared_requirement": "One technician must personally have inspected both systems before sign-off.",
  "decision_context": "A compliance manager must decide whether the requirement can be signed off now.",
  "collapse_action": "Sign off the single-technician requirement as already satisfied.",
  "preserve_action": "Keep the requirement unresolved until witness identity is established.",
  "same_witness_addendum": "The log explicitly states that the same technician performed both inspections.",
  "distinct_witness_addendum": "The log explicitly states that different technicians performed the two inspections.",
  "neutral_addendum": "Both entries were filed on the same afternoon.",
  "p_exists_gold": true,
  "q_exists_gold": true,
  "shared_witness_not_entailed_gold": true,
  "identity_underdetermined_gold": true,
  "joint_witness_possible_gold": true,
  "distinct_witness_possible_gold": true,
  "premises_do_not_identify_witnesses_gold": true,
  "same_explicit_authorizes_collapse_gold": true,
  "distinct_explicit_blocks_collapse_gold": true,
  "unknown_requires_identity_check_gold": true,
  "action_pair_matched_gold": true,
  "paraphrase_equivalent_gold": true,
  "neutral_control_equivalent_gold": true,
  "matched_base_gold": true,
  "natural_setting_gold": true,
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

The two `*_possible_gold` fields are not cosmetic. Without them, properties `P` and `Q` might be mutually incompatible or might logically force co-reference, in which case “identity unknown” would be false and the experiment would be invalid.

Formal G0 rejects custom-only provenance. An audited transformation may be derived from public data, but the underlying entities/events/requirements and gold relation must remain externally anchored, and D0 must archive at least 20 randomly sampled manual checks as required by `phenomenon_miner/PROCESS.md`.

## Metrics

The scorer uses local exact-continuation log probability over `A/B`; no API and no LLM judge are involved. Labels are reversed in every probe and decision.

For a recognition- and control-gated item, let `p_collapse(c)` be the normalized exact-choice preference for the collapse action under condition `c`:

```text
unknown_margin       = p_collapse(unknown) - 0.5
paraphrase_margin    = p_collapse(paraphrase) - 0.5
unknown_vs_distinct  = p_collapse(unknown) - p_collapse(distinct_explicit)
reminder_rescue      = p_collapse(unknown) - p_collapse(relation_reminder)
```

A strong case requires positive unknown and paraphrase margins, a large separation from explicit-distinct, stable explicit controls, small neutral-context movement, and consistency over both decision phrasings and both answer orders. `relation_reminder` is diagnostic only; it is not required for promotion.

## Hard kills / holds

- the model cannot reliably represent the two existentials / identity uncertainty → `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`;
- enough gate-correct cases reliably do **not** choose the collapse action → `HARD-KILL-NO-ILLEGAL-JOIN`;
- the collapse preference vanishes under the audited natural paraphrase → `HOLD-WORDING-ARTIFACT`;
- matched neutral context moves the downstream action comparably → `HOLD-GENERIC-CONTEXT-ARTIFACT`;
- if D0 can produce the effect only with toy FOL-style templates rather than natural staffing/resource/assignment records, kill at D0/N1.

## Execution gate

`configs/frozen_g0.json` deliberately has `validation_authorized: false`. `existential-witness-run run` reads that flag **before loading a model** and raises `PermissionError` while it is false. Code completion is not authorization.

Safe pre-authorization work:

```bash
cd active/006_existential_witness_collapse
python -m pip install -e '.[dev]'
pytest -q
existential-witness-run validate-data --data data/frozen_d0.jsonl
```

Formal model execution is permitted only after the authoritative registry records independent `N0-PASS`, `D0-PASS`, and `validation_authorized: true`.
