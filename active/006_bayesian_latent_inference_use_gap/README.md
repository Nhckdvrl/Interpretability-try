# 006 — Bayesian latent inference → downstream-use gap

**Status:** `ACTIVE-MECHANISM / BEHAVIORAL G0 PASSED`
**Validated:** 2026-08-27

## Mother question

> Why can a model report a sufficiently accurate latent-state posterior, yet fail to apply that same posterior to a minimal downstream policy decision?

This is deliberately narrower than generic Bayesian reasoning. The target is the transition from a represented/reportable posterior to its use by a downstream computation.

## Corrected decisive G0

The original scaffold had two invalid shortcuts: posterior error could cross the decision threshold, and raw `INVEST/HOLD` candidates introduced a large lexical prior. The corrected G0 therefore:

- scores the full `0.00…1.00` posterior candidate set and uses its normalized expectation;
- calls inference-good only when the reported posterior itself implies the Bayes-optimal action;
- excludes threshold-boundary cases;
- uses the minimal rule `P(A|evidence) > threshold → ACT, else WAIT`, removing expected-value arithmetic;
- counterbalances ACT/WAIT over neutral A/B answer labels;
- compares natural action choice with a matched bridge that explicitly supplies the correct posterior.

A bridge rescue is now interpretable: the model can perform the policy comparison when the posterior is made available, but does not reliably carry/use the posterior from the evidence itself.

## G0 results

| Model | Posterior MAE | Eligible cases | Direct error | Bridged error | Rescues | Mean Δp(gold) |
|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-14B-Instruct | 0.105 | 42 | 33.3% | 0.0% | 14/14 | +0.327 |
| Gemma3-12B-IT | 0.255 | 29 | 3.4% | 0.0% | 1/1 | +0.382 |
| Qwen3-8B | 0.253 | 14 | 50.0% | 42.9% | 2/7 | +0.0002 |

The anchor phenotype is Qwen2.5-14B: good posterior reporting, substantial unassisted use failure, and complete bridge rescue. Qwen3-8B instead fails mainly at posterior formation; Gemma usually selects the right action but its confidence remains strongly bridge-sensitive. This cross-model dissociation is useful rather than disqualifying: inference quality and routing quality do not improve in lockstep.

## Mechanism opening and paper scope

- representation: where and how the posterior becomes linearly/causally available;
- routing: whether posterior-bearing states reach the policy-token computation;
- readout: whether the information reaches the decision but is lost at label selection.

The conference-sized claim should remain one controlled transition—latent posterior to downstream use—tested in the closed-form task and then confirmed on one official BayesBench environment. It should not expand into a general theory of Bayesian reasoning.

## Files

- `g0.py` — deterministic generator, HF teacher-forced runner, and scorer;
- `data/cases.jsonl` — 72 policy cases over 24 unique evidence states;
- `results/*_g0.jsonl` and summaries — complete corrected runs;
- `tests/test_006_g0.py` — posterior, parsing, threshold-consistency, and label-mapping tests.

## Next step

Proceed to causal localization on Qwen2.5-14B, retaining Qwen3-8B as a representation-failure comparison. Before a paper-level claim, reproduce the same inference→use transition on the official BayesBench recommender or triage environment.
