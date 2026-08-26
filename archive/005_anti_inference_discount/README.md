# 005 — Anti-inference discount after successful comprehension

**Status: KILLED / ARCHIVED.**
**Do not start mechanism work before this G0 passes.**

## Final G0 decision (2026-08-27)

The frozen 96-scenario G0 was run end-to-end on both primary models. All
scenarios passed the strict comprehension gate in both models, but the natural
and same-history discounts were effectively zero and no strong scenario was
observed.

| Model | Gated | Mean natural discount | Mean bridged discount | Strong | Natural pass | Bridged pass |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3-8B | 96 | 0.001324 | 4.79e-12 | 0 | no | no |
| Gemma3-12B-IT | 96 | 1.38e-05 | 9.94e-08 | 0 | no | no |

The frozen thresholds required natural discount `>= .05`, bridged discount
`>= .03`, at least ten strong scenarios, and two independently passing models.
Both primary models fail both sub-gates, so the remaining single confirmation
model cannot satisfy promotion. The project is killed before mechanism work;
no thresholds or scenario families were changed.

## Mother question

> Why can evidence that logically establishes the same fact be used less strongly merely because the model must infer that fact rather than read it directly — and does any discount remain after the model has explicitly acknowledged the inferred fact?

The project is promoted only if both a **natural direct-over-inference discount** and a **same-history residual after acknowledgement** survive.

## Logic-review corrections

The G0 now blocks four major confounds:

1. Direct evidence no longer contains the inference evidence plus an extra conclusion; the two evidence strings are non-nested.
2. The post-comprehension comparison continues the exact same conversation history through an `assistant: Yes` acknowledgement rather than using an unrelated fresh probe.
3. Promotion requires both the natural effect and the same-history residual; a natural inference-cost effect alone cannot support the stronger title claim.
4. The bank is now **outcome-symmetric**. Every domain contains equal numbers where the rule criterion is met and not met, so a fixed tendency toward `violation`, `positive`, or `qualifies` cannot masquerade as anti-inference.

## Frozen matched evidence

The generator creates 96 scenarios:

- 32 legal/compliance timing;
- 32 medical screening;
- 32 numerical eligibility;
- inside every family: 16 `criterion_met` and 16 `criterion_not_met`.

For every scenario:

- `direct`: an authoritative record directly states the relevant relation;
- `inference`: an equally authoritative record supplies numbers/timestamps from which the same relation follows by one trivial comparison;
- neither evidence string contains the other;
- neither repeats the exact critical-fact query verbatim;
- the context declares direct relations and listed numerical values equally authoritative and accurate;
- both routes entail the same gold conclusion.

When the criterion direction flips, the gold conclusion also flips (e.g. violated ↔ satisfied, positive ↔ negative, qualifies ↔ does not qualify).

## Stage 1 — comprehension gate

Two semantically equivalent templates score `Yes` vs `No` for the same critical fact under both evidence modes. A scenario is eligible only if every template satisfies:

- direct `p_yes >= .80`;
- inference `p_yes >= .80`;
- matched direct/inference gap `<= .10`.

## Stage 2A — natural downstream judgment

A fresh judgment prompt receives direct or inferential evidence and asks for the warranted conclusion. Two templates and both A/B label orders are scored.

```text
natural_discount = p_gold_direct - p_gold_inference
```

A strong natural scenario requires the comprehension gate, direct gold probability `>= .70`, mean discount `>= .12`, and positive discount in at least 75% of matched presentation variants.

## Stage 2B — same-history post-comprehension judgment

For the same gated scenarios, judgment continues from the exact comprehension history:

```text
user: [context + evidence + critical-fact question]
assistant: Yes
user: [which downstream conclusion follows? A/B]
```

```text
bridged_discount = p_gold_direct - p_gold_inference
```

Because `Yes` is already required to be a high-probability model-consistent continuation in both conditions, this tests whether a residual direct/inference asymmetry remains after the critical fact has been explicitly acknowledged.

## Frozen model-level pass rule

A model passes only if **both** sub-gates pass.

Natural gate:

- at least 60/96 scenarios pass comprehension;
- mean natural discount `>= +.05`;
- bootstrap 95% CI lower bound `> +.01`;
- at least 2/3 families are positive with sufficient gated support;
- **both criterion directions are positive**, each with at least 24 gated scenarios;
- at least 10 strong scenarios across at least 2 families;
- at least 60% of gated scenarios have positive discount.

Same-history gate:

- mean bridged discount `>= +.03`;
- bootstrap 95% CI lower bound `> 0`;
- at least 2/3 sufficiently populated families are positive;
- **both criterion directions are positive**;
- at least 55% of gated scenarios have positive bridged discount.

At least two open-weight models must independently pass both gates. Do not weaken thresholds, cherry-pick domains/outcomes, add harder inference chains, or switch to weaker models after a null result.

## Interpretation

- comprehension fails → ordinary inference failure; kill the stronger claim;
- natural gate fails → no stable external phenomenon; kill;
- natural passes but bridged fails → inference-cost/formation effect only; kill or rename the stronger current mother question;
- both pass across domains and both outcome directions → mechanism work is justified.

## Usage

```bash
cd active/005_anti_inference_discount
python -m pip install -e '.[test]'
pytest -q

antiinf-generate --out data/scenarios.jsonl
antiinf-run --model Qwen/Qwen3-8B --data data/scenarios.jsonl --out results/qwen3_8b_g0.jsonl
antiinf-summarize --data data/scenarios.jsonl --results results/qwen3_8b_g0.jsonl --config configs/g0.json --out results/qwen3_8b_g0_summary.json
```
