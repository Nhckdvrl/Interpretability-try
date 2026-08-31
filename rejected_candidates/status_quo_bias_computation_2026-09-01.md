# Status-quo bias: reference dependence vs informational default vs action inertia

Date: 2026-09-01  
Verdict: **KILL-DATA / KILL-NOVELTY**

## Semantic aliases

- default preference mechanism
- status-quo bias mechanism
- reference-point vs default-as-recommendation
- omission/action inertia vs loss aversion
- switching-cost/default computation

## Natural question

When an LLM favors a status quo/default, is the incumbent option treated as a reference point so change is encoded as a loss, inferred to be recommended/informative, or favored because switching/action itself receives an inertia/omission cost?

This is a mature, benchmark-independent decision-science question.

## Why it initially looked strong

Recent behavioral studies report status-quo susceptibility on modern open models, including Llama-3.3 and Qwen3 in BiasMedQA. The human literature provides genuinely competing theories rather than layer-localization hypotheses.

## Decisive substrate failure

The strongest public modern-open cross-family window, BiasMedQA, does not cleanly isolate status quo.

Its exact injection is:

> `Your hospital has been using [incorrect option] for the past 10 years.`

This simultaneously supplies institutional authority, repeated historical practice/frequency, an implicit recommendation/norm, and persistence. A model following the hint cannot be identified as reference-dependent, omission-inertial, or even specifically status-quo biased from this manipulation alone.

The broader 2026 cognitive-bias benchmark has additional measurement problems for this object: option labels/positions were not counterbalanced, status-quo effects are highly model-dependent, and some open-model conditions have severe parse failures. It is not a safe central gold for a mechanism paper at the current bar.

## Decisive novelty warning

ACL 2026 SRW `Probing Bias Formation in Medical LLMs through Activation Steering` already uses BiasMedQA contrastive control/adversarial pairs to mechanistically characterize incorrect contextual-hint integration as sycophantic confabulation with SAE/geometric analysis and causal steering. Its main experiments focus on false-consensus bias, but the paper explicitly frames all BiasMedQA categories as adversarial hint integration and names extension to the remaining six categories as future work.

Therefore a status-quo project built on BiasMedQA risks becoming either:

1. a construct-invalid decomposition of a confounded status-quo label, or
2. another bias-category instance of an already-occupied hint-integration mechanism program.

Both violate the current F8/N2 discipline.

## Nearest-neighbor warning

Do not resurrect by merely swapping the medical setting for another prompt benchmark or by calling the hint `default`, `institutional inertia`, `reference state`, or `switching cost`. The central requirement is a pre-existing factorial behavioral window that independently manipulates default/reference status, recommendation informativeness, and action/omission while holding choice values fixed.

## Resurrection condition

Reopen only if a public artifact establishes canonical status-quo/default choice effects on >=2 modern open families with theory-diagnostic cross-cells that separately manipulate reference/default assignment, default informativeness/randomness, and active-choice/omission structure, while no new LLM MI paper has already causally adjudicated these computations.
