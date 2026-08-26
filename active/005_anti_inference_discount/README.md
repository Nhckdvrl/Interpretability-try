# 005 — Anti-inference discount after successful comprehension

**Status: PRE-CANDIDATE — frozen behavioral G0 only.**  
**Do not start mechanism work before this G0 passes.**

## Mother question

> When a model has already correctly inferred a fact, does it still give that inferred fact less weight than the same fact stated directly?

This is a stricter version of the anti-inference / direct-vs-circumstantial evidence question. A weak experiment would only show that inference is harder than reading a statement. That is not enough. The target phenomenon here is a dissociation:

1. direct and inferential conditions support the same critical fact;
2. the model recognizes that fact with high confidence in **both** conditions;
3. the recognition confidence is closely matched;
4. yet the downstream decision gives less weight to the inferentially obtained fact.

If that dissociation is not stable in modern open-weight models, kill the topic before interpretability analysis.

## Why this G0 is not just a benchmark accuracy comparison

The experiment separates two stages:

### Stage 1 — comprehension gate

Ask whether the evidence establishes the critical fact. Both direct and inferential variants have gold answer `Yes`.

A scenario is eligible only if:

- `p_yes_direct >= 0.80`;
- `p_yes_inference >= 0.80`;
- `abs(p_yes_direct - p_yes_inference) <= 0.10`.

This removes cases where the model simply failed to perform the required inference.

### Stage 2 — downstream judgment

Using the same evidence, ask which of two conclusions is better supported. The target conclusion is programmatically fixed by the rule and critical fact. We score complete `A`/`B` continuations under both label orders and two prompt templates.

Primary quantity for gated scenarios:

```text
judgment_discount = p_target_direct - p_target_inference
```

A positive value means the model understood the inferred fact but still used it less strongly downstream.

## Frozen scenario families

The generator creates 96 matched scenarios: 32 per family.

### legal / compliance timing

A rule says an event violates a deadline when it occurs after a cutoff.

- direct: the record explicitly says the event occurred after the deadline;
- inference: the record gives the deadline and timestamp, from which the same fact follows.

### medical screening

A screening rule says a test is positive when a measurement exceeds a cutoff.

- direct: the report explicitly says the measurement is above threshold;
- inference: the report provides the numerical cutoff and measured value.

### eligibility

A rule says an applicant qualifies when a numerical quantity is below a cutoff.

- direct: the record explicitly states the applicant is below the cutoff;
- inference: the record provides the cutoff and observed value.

All gold labels are programmatic. No human annotation is needed.

These families deliberately use simple one-step inferences. The goal is **not** to create difficult reasoning; it is to test whether the provenance "derived rather than stated" is discounted even after comprehension is matched.

## Frozen presentation controls

Every scenario uses:

- 2 semantically equivalent comprehension templates;
- 2 semantically equivalent judgment templates;
- both A/B label orders for judgment;
- deterministic teacher-forced likelihood over complete `Yes`/`No` or `A`/`B` strings;
- Qwen3 thinking disabled in the chat template.

Per scenario this is 12 prompt evaluations:

- 2 evidence modes × 2 comprehension templates = 4;
- 2 evidence modes × 2 judgment templates × 2 label orders = 8.

Total: 1,152 prompt evaluations per model.

## Frozen endpoints

For each scenario:

- `p_yes_direct`;
- `p_yes_inference`;
- comprehension gap;
- `p_target_direct` averaged over judgment templates/orders;
- `p_target_inference` averaged likewise;
- `judgment_discount`.

A **strong anti-inference scenario** requires:

- passes comprehension gate;
- `p_target_direct >= 0.70`;
- `judgment_discount >= 0.12`.

Primary aggregate endpoint among gated scenarios:

- mean `judgment_discount` with paired bootstrap 95% CI.

Secondary:

- gated count;
- strong count/rate;
- mean discount per family;
- fraction of scenarios with positive discount.

## Frozen model-level pass rule

A model passes only if:

- at least 60/96 scenarios pass the comprehension gate;
- mean judgment discount among gated scenarios `>= +0.05`;
- paired bootstrap 95% CI lower bound `> +0.01`;
- at least 2 of 3 families have positive mean discount;
- at least 10 gated scenarios are strong anti-inference cases;
- positive-discount fraction among gated scenarios `>= 0.60`.

Run in order:

1. `Qwen/Qwen3-8B`
2. `google/gemma-3-12b-it`
3. `Qwen/Qwen3-14B` only as confirmation

Promote only if at least **two models** independently pass. Do not lower the comprehension gate, add harder inference chains, cherry-pick one family, or move to weaker models after seeing a null result.

## Interpretation of outcomes

### G0 fails because inference comprehension is poor

This does **not** establish anti-inference discount. The model simply failed to infer the fact. Archive this project under the current mother question.

### G0 passes comprehension but judgment discount is near zero

The stronger dissociation does not exist. Kill before mechanism work.

### G0 passes

Only then distinguish mechanisms such as:

- inferred facts are represented less strongly even when decodable;
- direct and inferred facts are equally represented, but provenance tags alter evidence weighting;
- both are equally weighted until late answer arbitration.

Those possibilities predict different repairs, so only a passing G0 justifies causal interpretability.

## Usage

```bash
cd active/005_anti_inference_discount
python -m pip install -e '.[test]'
pytest -q

antiinf-generate --out data/scenarios.jsonl

antiinf-run \
  --model Qwen/Qwen3-8B \
  --data data/scenarios.jsonl \
  --out results/qwen3_8b_g0.jsonl

antiinf-summarize \
  --data data/scenarios.jsonl \
  --results results/qwen3_8b_g0.jsonl \
  --config configs/g0.json \
  --out results/qwen3_8b_g0_summary.json
```

## Integrity checks

The generator is deterministic and expected to produce exactly 96 unique scenarios with 32 in each family. The loader rejects duplicate IDs, unknown families, malformed gold structure, or incorrect family counts.

The summarizer rejects duplicate variants, missing variants, unknown scenario IDs, missing evidence conditions, and incomplete template/order coverage. No malformed row is silently dropped.
