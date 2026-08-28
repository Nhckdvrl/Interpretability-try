# 006 — Existential Witness Collapse

Status: `ACTIVE-PREFLIGHT / HARNESS-READY-r1 / NOT READY-TO-SMOKE`

Canonical shortlist mapping: **2026-08-28 adversarial N0 shortlist #4**.

```yaml
formal_n0_verdict: null
independent_auditor: null
d0_verdict: null
validation_authorized: false
```

## Mother question

When a model correctly understands two separate existential claims and explicitly knows that their witnesses need not be the same individual, does a downstream planning or resource decision nevertheless fuse those anonymous witnesses into one person/entity?

The forbidden inference is:

```text
exists x: P(x)
exists y: Q(y)
--------------------------------
NOT ENTAILED: exists z: P(z) and Q(z)
```

This does **not** assert that the witnesses are different. It asserts only that identity is underdetermined until the record supplies an identity link.

## Decisive dissociation

A case only counts after four recognition probes pass:

- the model accepts `exists P`;
- the model accepts `exists Q`;
- the model rejects that a shared witness is entailed;
- the model says witness identity is not determined.

The downstream task then asks whether a single-person/single-resource requirement is already established. The phenomenon is an `ESTABLISHED` preference in the identity-unknown world despite the recognition gate being correct.

## Identity controls

Every D0 scenario contains matched controls:

- `unknown`: the two existential claims only;
- `paraphrase`: equivalent natural wording;
- `same_explicit`: the record explicitly says the same witness satisfies both properties;
- `distinct_explicit`: the record explicitly says the witnesses are different;
- `neutral_control`: matched extra context that does not bear on identity;
- `relation_reminder`: diagnostic reminder that separate existentials do not establish witness identity.

The harness refuses to call an unknown-world error “witness collapse” unless the model also handles explicit-same and explicit-distinct controls correctly. This prevents ordinary quantifier incompetence from passing as the target phenotype.

## Formal D0 record

```json
{
  "scenario_id": "staff:17",
  "domain": "staffing",
  "premise_p": "At least one technician inspected the cooling system.",
  "premise_q": "At least one technician inspected the power system.",
  "premise_paraphrase": "...equivalent natural wording...",
  "p_property": "inspected the cooling system",
  "q_property": "inspected the power system",
  "shared_requirement": "The audit requires one technician who personally inspected both systems.",
  "decision_context": "A manager must decide whether that staffing fact is already confirmed.",
  "same_witness_addendum": "The same technician performed both inspections.",
  "distinct_witness_addendum": "Different technicians performed the two inspections.",
  "neutral_addendum": "Both records were filed the same afternoon.",
  "p_exists_gold": true,
  "q_exists_gold": true,
  "shared_witness_not_entailed_gold": true,
  "identity_underdetermined_gold": true,
  "same_explicit_establishes_gold": true,
  "distinct_explicit_does_not_establish_gold": true,
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

Formal G0 requires externally anchored scenarios. Synthetic rows are accepted only by unit tests with `require_external_source=False`; they cannot satisfy the formal loader.

## Primary metrics

For each gate-passing case:

```text
unknown_margin = P(established | unknown) - 0.5
paraphrase_margin = P(established | paraphrase) - 0.5
unknown_vs_distinct = P(established | unknown) - P(established | distinct_explicit)
reminder_rescue = P(established | unknown) - P(established | relation_reminder)
```

A strong case requires a positive unknown and paraphrase margin, explicit-same/explicit-distinct control success, small neutral shift, and consistency across two natural wordings and both answer orders.

## Hard kills / holds

- Recognition gate failure on enough cases → `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`.
- Gate-correct cases show no positive unknown-world join → `HARD-KILL-NO-ILLEGAL-JOIN`.
- Effect disappears under equivalent natural paraphrase → `HOLD-WORDING-ARTIFACT`.
- Matched neutral context moves decisions comparably → `HOLD-GENERIC-CONTEXT-ARTIFACT`.
- If the phenomenon only survives toy FOL templates and not natural staffing/resource/assignment records, kill at D0/N1.

## No model call before authorization

Unlike older harnesses, `run` reads the frozen config and raises `PermissionError` while `validation_authorized` is false. This is deliberate: registration and code completion do not bypass independent N0 + D0.

```bash
cd active/006_existential_witness_collapse
python -m pip install -e '.[run,dev]'
pytest -q

# Safe before authorization: validates D0 structure only.
existential-witness-run validate-data --data data/frozen_d0.jsonl

# Formal model execution remains blocked until the authoritative gate is signed.
existential-witness-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B --family Qwen --size-b 8 \
  --revision <exact-revision> \
  --out results/qwen3_8b.jsonl
```
