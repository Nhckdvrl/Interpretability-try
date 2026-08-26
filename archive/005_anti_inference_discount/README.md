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

This G0 deliberately separates two claims that the earlier draft conflated:

1. **Natural anti-inference behavior:** direct evidence is used more strongly than one-step inferential evidence in an ordinary downstream judgment.
2. **Post-comprehension residual:** after the model itself is already high-confidence that the critical inferred fact is true, continuing the same conversation still shows a direct-over-inferred discount.

The project is promoted only if **both** claims survive. A natural effect alone could simply be inference failure/effort; a bridged effect alone would not establish a naturally occurring behavioral failure.

## Logic-review corrections

The first draft had two serious confounds and one claim/gate mismatch.

1. The direct condition originally contained the inference condition plus an extra explicit conclusion. Any advantage could therefore be caused by extra text, repetition, or lexical overlap.
2. The original comprehension check and downstream judgment were unrelated fresh prompts, so success on one did not prove that the compared judgment started from an acknowledged fact.
3. A later version measured both natural and same-history paths but promoted on the natural path alone while the README/title claimed "after successful comprehension." That mismatch is now removed.

## Frozen matched evidence

The generator creates 96 scenarios: 32 each for legal/compliance timing, medical screening, and numerical eligibility.

For every scenario:

- `direct`: an authoritative record directly classifies the critical relation;
- `inference`: an equally authoritative record gives numerical facts from which the same relation follows in one trivial comparison;
- neither evidence string contains the other;
- neither repeats the exact critical-fact query verbatim;
- the context explicitly states that direct classifications and listed numerical values are equally authoritative and accurate;
- both routes logically entail the same downstream gold conclusion.

All gold structure is programmatic.

## Stage 1 — comprehension gate

For two semantically equivalent templates, score `Yes` vs `No` for the same critical fact under both evidence modes.

A scenario is eligible only if **every** comprehension template satisfies:

- minimum direct `p_yes >= .80`;
- minimum inference `p_yes >= .80`;
- maximum matched direct/inference confidence gap `<= .10`.

Thus any same-history analysis is restricted to cases where `Yes` is already the model's own deterministic preferred answer in both conditions.

## Stage 2A — natural downstream judgment

A fresh ordinary judgment prompt receives either the direct or inferential evidence and asks for the warranted conclusion. Two judgment templates and both A/B label orders are scored.

For matched presentation variants:

```text
natural_discount = p_target_direct - p_target_inference
```

This is the behavioral prerequisite corresponding to "one extra inferential step makes equally decisive evidence count less."

A strong natural scenario requires the comprehension gate, direct target probability `>= .70`, mean natural discount `>= .12`, and positive discount in at least 75% of matched natural variants.

## Stage 2B — same-history post-comprehension judgment

For the same gated scenarios we also continue the exact comprehension history:

```text
user: [context + evidence + critical-fact question]
assistant: Yes
user: [which downstream conclusion follows? A/B]
```

Because gated cases already have `Yes` as the model's high-confidence preferred response, this continuation conditions the downstream decision on the model's own acknowledged critical fact rather than using an unrelated comprehension probe.

Both direct and inference variants receive the identical acknowledgement structure. The residual quantity is:

```text
bridged_discount = p_target_direct - p_target_inference
```

If the natural effect disappears here, the data support "inference formation/effort" rather than the stronger claim that an already acknowledged inferred fact is still downweighted.

## Frozen model-level pass rule

A model is promoted only if **both** sub-gates pass.

Natural gate:

- at least 60/96 scenarios pass comprehension;
- mean natural discount `>= +.05`;
- paired bootstrap 95% CI lower bound `> +.01`;
- at least 2/3 families are positive with at least 16 gated items each;
- at least 10 strong scenarios, spread across at least 2 families;
- at least 60% of gated scenarios have positive natural discount.

Same-history residual gate:

- mean bridged discount `>= +.03`;
- paired bootstrap 95% CI lower bound `> 0`;
- at least 2/3 sufficiently populated families have positive bridged discount;
- at least 55% of gated scenarios have positive bridged discount.

At least two open-weight models must independently pass both gates. Do not weaken thresholds, cherry-pick families, add harder inference chains, or switch to weaker models after observing a null result.

## Interpretation

- Comprehension gate fails → ordinary inference failure; do not call it anti-inference-after-comprehension.
- Natural gate fails → no stable external phenomenon; kill.
- Natural passes but bridged fails → interesting inference-cost/formation effect, but **kill the stronger current mother question** or rename/re-scope before mechanism work.
- Both pass → mechanism work is justified: weakened inferred representation vs provenance-dependent weighting vs late arbitration become genuinely separable explanations.

## Usage

```bash
cd active/005_anti_inference_discount
python -m pip install -e '.[test]'
pytest -q

antiinf-generate --out data/scenarios.jsonl
antiinf-run --model Qwen/Qwen3-8B --data data/scenarios.jsonl --out results/qwen3_8b_g0.jsonl
antiinf-summarize --data data/scenarios.jsonl --results results/qwen3_8b_g0.jsonl --config configs/g0.json --out results/qwen3_8b_g0_summary.json
```
