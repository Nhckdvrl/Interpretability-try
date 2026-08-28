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

Can a model correctly understand two independent existential facts, yet later behave as though they identify **one shared witness**?

The logical contract is deliberately weaker than “the witnesses are different”:

```text
∃x P(x)
∃y Q(y)
```

does **not** license:

```text
∃z (P(z) ∧ Q(z))
```

The two witnesses may in fact be the same person; the error is claiming or acting as if sameness has already been established when the record leaves identity unresolved.

This distinction is essential. A scorer that marks “one witness” false because it assumes the witnesses must be distinct would itself contain the scientific bug this project is designed to study.

## Frozen behavioral contract

A case contributes to the phenotype only when all of the following are true for the same model and scenario:

1. It recognizes that at least one `P` witness exists.
2. It recognizes that at least one `Q` witness exists.
3. It correctly says the two existential statements do not entail a shared witness.
4. It correctly says witness identity is underdetermined.
5. In downstream staffing/resource/planning use, it nevertheless prefers `ESTABLISHED` for a requirement that needs one entity satisfying both properties.
6. It still handles explicit-identity controls correctly: `same_explicit → established`, `distinct_explicit → not established`.

The primary failure therefore has the form:

```text
local relation understanding correct
+ explicit identity controls correct
+ identity-unknown downstream world
→ fused/shared-witness action
```

The wrong destination is not “any wrong answer”; it is specifically the fused-entity decision.

## Formal D0 schema

Formal G0 data must be externally anchored or externally derived. Custom-only templates are rejected by the loader.

```json
{
  "scenario_id": "staffing:record-17",
  "domain": "staffing",
  "premise_p": "At least one technician ...",
  "premise_q": "At least one technician ...",
  "premise_paraphrase": "A natural paraphrase preserving both independent existentials ...",
  "p_property": "...",
  "q_property": "...",
  "shared_requirement": "A requirement needing one individual with both properties ...",
  "decision_context": "A natural downstream reason the record must be used ...",
  "same_witness_addendum": "External/audited wording that explicitly establishes identity ...",
  "distinct_witness_addendum": "External/audited wording that explicitly establishes different recorded witnesses ...",
  "neutral_addendum": "Matched extra context that does not change identity information ...",
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

D0 must manually audit at least 20 random source-derived cases for naturalness, identity underdetermination, and downstream gold before authorization. Toy first-order-logic strings can be used only as unit tests, not as formal behavioral evidence.

## Prompt and scoring design

The harness uses local Hugging Face causal LMs and exact continuation log-probabilities; there is no API dependency and no LLM judge.

Recognition probes and downstream choices are each evaluated under both `A/B` label orders. Downstream behavior is tested across two natural phrasings. The same scorer instance holds a lifetime cache so duplicate prompt/candidate requests are bit-stable across batches.

Primary downstream conditions:

```text
unknown           two independent existential facts; identity unresolved
paraphrase        same relation in a natural surface-form control
same_explicit     same witness explicitly established
distinct_explicit recorded witnesses explicitly different
neutral_control   matched extra context with no identity information
relation_reminder explicit logical reminder; diagnostic rescue only
```

The reminder condition can diagnose a late use/write failure but is never allowed to define the primary phenomenon.

## Metrics

For each gate-correct case:

```text
p_unknown      = P(ESTABLISHED | identity unknown)
illegal_margin = p_unknown - 0.5

unknown_vs_distinct =
    P(ESTABLISHED | identity unknown)
  - P(ESTABLISHED | explicit distinct)
```

A strong case requires the model to pass the recognition and explicit-identity controls, prefer the illegal fused decision in both the original and paraphrased unknown worlds, remain stable under a neutral-context control, and show the effect across most natural wording/order variants.

Model summaries preserve every case, every recognition probability, the fused wrong destination, neutral-control shift, explicit-identity controls, and relation-reminder rescue. Bootstrap uncertainty is over scenarios, not prompt variants.

## Hard kills / holds

- `HARD-KILL-QUANTIFIER-CAPABILITY-FLOOR`: the model cannot reliably state the local existential/identity relation, so downstream failure is ordinary quantifier reasoning error.
- `HARD-KILL-NO-ILLEGAL-JOIN`: enough gate-correct cases exist but the identity-unknown world does not systematically prefer the fused witness.
- `HOLD-WORDING-ARTIFACT`: the original wording moves toward fusion but the natural paraphrase does not.
- `HOLD-GENERIC-CONTEXT-ARTIFACT`: comparable movement appears after neutral matched context.
- Formal discovery is also killed if a natural external D0 cannot be built and the effect requires toy FOL templates.

## Mechanism forks reserved for later

Only after behavior, N1, cross-family generality, and the strong-model kill test pass should mechanism work begin. The current behavior is compatible with at least three separable hypotheses:

1. **Early referent fusion:** two anonymous existential referents collapse into one entity representation before downstream use.
2. **Join/reducer error:** local referents remain distinct/unknown, but a downstream planner incorrectly reuses one variable when combining requirements.
3. **Late answer-policy fusion:** internal relation is intact, but the final decision writer compresses “there is a P” + “there is a Q” into “there is a P∧Q”.

These predict different locations for probing/patching and different effects of a relation reminder, so the behavioral contract leaves a real interpretability opening rather than naming a mechanism in advance.

## Commands

Data validation is allowed before model authorization:

```bash
cd active/006_existential_witness_collapse
python -m pip install -e '.[run,dev]'
pytest -q
existential-witness-run validate-data --data data/frozen_d0.jsonl
```

Formal inference is deliberately blocked while `validation_authorized` is false:

```bash
existential-witness-run run \
  --data data/frozen_d0.jsonl \
  --config configs/frozen_g0.json \
  --model Qwen/Qwen3-8B \
  --family Qwen \
  --size-b 8 \
  --revision <exact-revision> \
  --out results/qwen3_8b.jsonl
```

Do not override this gate locally. The authoritative registry must first contain independent `N0-PASS`, `D0-PASS`, and `validation_authorized: true`.
