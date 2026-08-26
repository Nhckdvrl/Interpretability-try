# 006 — Bayesian latent inference → downstream-use gap

**Status:** `PAUSED / EXTERNAL VALIDITY NOT ESTABLISHED`
**Last audited:** 2026-08-27

For the complete chronological record from topic registration through G0, exploratory mechanism runs, result audit, and the frozen V2 plan, see [`PROGRESS.md`](PROGRESS.md).

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

A bridge rescue shows that the model can perform the policy comparison when the posterior is made available. By itself it does not distinguish a direct prompt that never forms the posterior from one that forms but fails to route/use it; the mechanism plan tests those alternatives separately.

## Synthetic G0 results (development evidence only)

| Model | Posterior MAE | Eligible cases | Direct error | Bridged error | Rescues | Mean Δp(gold) |
|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-14B-Instruct | 0.105 | 42 | 33.3% | 0.0% | 14/14 | +0.327 |
| Gemma3-12B-IT | 0.255 | 29 | 3.4% | 0.0% | 1/1 | +0.382 |
| Qwen3-8B | 0.253 | 14 | 50.0% | 42.9% | 2/7 | +0.0002 |

On the custom closed-form prompts, Qwen2.5-14B has good posterior reporting, substantial unassisted use failure, and complete bridge rescue. Qwen3-8B and Gemma do not reproduce the same phenotype. These results are useful for debugging and mechanism development, but they do **not** establish a cross-model phenomenon: custom wording, label binding, task comprehension, and synthetic-distribution artifacts remain viable explanations.

The later cross-model meta-G0 smoke is invalid as scientific evidence. In particular, Qwen3-8B collapsed to one answer label across action rows, and Gemma showed weak mapping consistency. Those runs diagnose prompt/evaluation fragility rather than belief/use dissociation.

An external-validity audit also found that [BayesBench](https://arxiv.org/abs/2606.30850) already states the broad behavioral claim that stronger latent inference does not reliably transfer to downstream prediction across seven models. Its official implementation uses MovieLens, AITA, and medical-triage public datasets in addition to a synthetic coin task. Therefore neither our synthetic behavioral gap nor the broad report/use framing is currently a novel paper contribution.

## Current decision boundary

All new V2 mechanism runs are paused. Existing Qwen2.5 results remain labeled D0 exploratory and may be reused only if the phenotype transfers to an official task.

The project gets one bounded salvage test:

1. reproduce a latent-inference/downstream-use gap with the official BayesBench code on at least two public-data environments;
2. require the same open-weight anchor phenotype on more than one model or model size;
3. show that the existing Qwen2.5 mechanism prediction transfers without selecting prompts, layers, or strengths on the test data.

If (1) or (2) fails, archive 006. If behavior transfers but (3) fails, the current mechanism account is rejected; a new mechanism project would need to begin from the official task. Passing this test would support a narrower, potentially novel paper about the mechanism and selective repair of a phenomenon BayesBench already established—not a new behavioral-discovery claim.

## Files

- `g0.py` — deterministic generator, HF teacher-forced runner, and scorer;
- `data/cases.jsonl` — 72 policy cases over 24 unique evidence states;
- `results/*_g0.jsonl` and summaries — complete corrected runs;
- `tests/test_006_g0.py` — posterior, parsing, threshold-consistency, and label-mapping tests.

## Next step

Do not run the custom V2 matrix. First run a small, unmodified BayesBench reproduction on its MovieLens recommender and public medical-triage environments. Record this as external replication, not as our dataset. No further white-box work is approved until that check passes.

The complete study design is in [`INTERPRETABILITY_PLAN.md`](INTERPRETABILITY_PLAN.md). It treats query-gated posterior formation, posterior routing, comparator failure, and late option binding as competing hypotheses rather than presupposing a routing failure.

Mechanism experiments have started. The first Qwen2.5-14B representation and natural-interchange results are recorded in [`mechanism/MECHANISM_LOG.md`](mechanism/MECHANISM_LOG.md); the safe current finding is that replacing the complete eight-token serialized number is sufficient to transfer bridge actions in early layers, with source-site intervention efficacy decaying over layers 16–24.

The result-driven next design is frozen in [`INTERPRETABILITY_PLAN_V2.md`](INTERPRETABILITY_PLAN_V2.md). It treats role-gated transport as a hypothesis and adds subspan necessity, cross-format abstraction, receiver localization, direct diagnosis, and mechanism-predicted repair.
