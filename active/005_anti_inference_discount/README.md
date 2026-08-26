# 005 — Anti-inference discount after successful comprehension

**Status: PRE-CANDIDATE — frozen behavioral G0 only.**  
**Do not start mechanism work before this G0 passes.**

## Mother question

> When a model has already correctly inferred a fact, does it still give that inferred fact less weight than an equally authoritative direct statement of the same fact?

The target phenomenon is not merely that inference is harder than reading. We require a stronger dissociation: both conditions establish the same critical fact; the model recognizes that fact with high confidence in both; yet downstream judgment still discounts the inferred route.

## Logic-review correction

The first draft had two serious confounds.

1. The direct condition literally contained the entire inference condition plus an extra explicit conclusion. Any advantage could therefore be caused by extra text/repetition/lexical overlap rather than provenance.
2. Comprehension and judgment were separate prompts. Success on one prompt did not guarantee that the compared judgment computation actually started from an acknowledged inferred fact.

Both are removed.

## Frozen matched evidence

The generator creates 96 scenarios: 32 each for legal/compliance timing, medical screening, and numerical eligibility.

For every scenario:

- `direct`: one authoritative record directly classifies the critical relation;
- `inference`: an equally authoritative record gives numerical facts from which that same relation follows in one trivial comparison;
- neither evidence string contains the other;
- neither repeats the exact critical-fact query verbatim;
- the context explicitly states that direct classification and listed numerical values are equally authoritative and accurate.

All gold structure is programmatic.

## Stage 1 — comprehension gate

For two semantically equivalent templates, score `Yes` vs `No` for the same critical fact under both evidence modes.

A scenario is eligible only if **every comprehension template** satisfies the high-confidence requirement and the matched direct/inference confidence gap remains small:

- minimum direct `p_yes >= .80`;
- minimum inference `p_yes >= .80`;
- maximum template-matched absolute direct/inference gap `<= .10`.

This prevents a single averaged easy template from hiding an inference failure.

## Stage 2 — same-history downstream judgment

Judgment is not a fresh prompt. It extends the exact same comprehension history:

```text
user: [context + evidence + critical-fact question]
assistant: Yes
user: [which downstream conclusion follows? A/B]
```

Thus the measured judgment is explicitly conditioned on the model having acknowledged the critical fact in that same conversation history. Both direct and inference variants receive the identical `assistant: Yes` bridge.

For every comprehension template, judgment template, and A/B label order we compute the matched difference:

```text
judgment_discount = p_target_direct - p_target_inference
```

Primary scenario score is the mean of these matched variant-level differences, not the difference between two unrelated averages.

A strong scenario requires the comprehension gate, direct target probability `>= .70`, mean discount `>= .12`, and positive discount in at least 75% of matched presentation variants.

## Frozen model-level pass rule

A model passes only if:

- at least 60/96 scenarios pass the comprehension gate;
- mean judgment discount among gated scenarios `>= +.05`;
- paired bootstrap 95% CI lower bound `> +.01`;
- at least 2/3 families have positive mean discount;
- at least 10 gated scenarios are strong;
- at least 60% of gated scenarios have positive mean discount.

At least two open-weight models must pass. Do not weaken gates, remove the Yes bridge, add harder inference chains, cherry-pick one family, or switch to weaker models after observing a null result.

## Interpretation

If comprehension fails, this is simply an inference failure and does not support the topic. If comprehension passes but downstream discount is near zero, kill the stronger anti-inference hypothesis. Only a stable pass justifies mechanism work on weakened inferred representations vs provenance-dependent weighting vs late arbitration.

## Usage

```bash
cd active/005_anti_inference_discount
python -m pip install -e '.[test]'
pytest -q

antiinf-generate --out data/scenarios.jsonl
antiinf-run --model Qwen/Qwen3-8B --data data/scenarios.jsonl --out results/qwen3_8b_g0.jsonl
antiinf-summarize --data data/scenarios.jsonl --results results/qwen3_8b_g0.jsonl --config configs/g0.json --out results/qwen3_8b_g0_summary.json
```
