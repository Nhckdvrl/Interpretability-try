# 005 — Anti-inference evidence discount

**Status: PRE-CANDIDATE / behavioral G0 only**

## Mother question

When two evidence channels are explicitly matched for end-to-end reliability, does a model discount the conclusion merely because one channel requires an inference step?

G0 is designed to separate two possibilities that a simple direct-vs-circumstantial comparison confounds:

1. the model failed to understand the inferential link;
2. the model understood the link, but still assigns less weight to the inferred conclusion.

Only (2) is the target phenomenon.

## Matched design

Programmatically generated cases span four domains: legal evidence, medical diagnosis, cybersecurity, and engineering fault diagnosis. Each family has three conditions with identical target proposition and explicitly matched end-to-end reliability `r`:

- **direct:** a calibrated source directly reports target H with reliability r;
- **inferred:** a calibrated pipeline observes E and a stated rule makes E imply H; the prompt explicitly states that the *end-to-end conclusion H* has reliability r;
- **inferred-explicit:** same as inferred, but includes the derived sentence `Therefore, H.`

Reliability levels: 80%, 90%, 95%. Prompt/order variants are deterministic.

### Understanding gate

Before the probability judgment, the model is separately scored on a yes/no structural check:

- direct: does the report assert H?
- inferred: according to the stated rule, does E imply H?

A family enters the primary analysis only when recognition probability is >= 0.80 in direct and inferred conditions and differs by <= 0.10. This prevents "it never performed the inference" from being counted as anti-inference weighting.

### Primary endpoint

The probability task offers the fixed candidates `50%, 60%, 70%, 80%, 90%, 95%, 99%`. We compute the expected stated probability under the candidate likelihood distribution.

For each gated family:

`discount = expected_probability(direct) - expected_probability(inferred)`.

The explicit-conclusion arm is a preregistered diagnostic: recovery there suggests inference execution/serialization burden rather than a stable source-type penalty.

### Frozen promotion rule

A model passes only if:

- >= 60 gated families overall;
- mean direct-minus-inferred discount >= **5 percentage points**;
- paired bootstrap 95% CI lower bound > **2 points**;
- >= 65% of gated families show positive discount;
- positive mean discount in >= 3/4 domains;
- direct arm calibration error from stated reliability <= 5 points on average.

Promote only if two open-weight models pass. Otherwise KILL without weakening reliability gates or adding hand-picked domains.

## Run

```bash
cd active/005_anti_inference
python g0.py generate --out data/scenarios.jsonl
python g0.py run --model Qwen/Qwen3-8B --data data/scenarios.jsonl --out results/qwen3_8b.jsonl
python g0.py summarize --data data/scenarios.jsonl --results results/qwen3_8b.jsonl --out results/qwen3_8b_summary.json
pytest -q test_g0.py
```

## STOP

If the discount disappears after the understanding gate, the target phenomenon is not established and mechanism work stops. A raw direct-vs-inferred difference alone is not enough.
