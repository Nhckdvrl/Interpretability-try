# Means vs Side Effect / Instrumental vs Incidental Harm — Terminal Collision

Date: 2026-09-01  
Verdict: **KILL-NOVELTY for the simple object; mechanism-resurrection not authorized**

## Natural question

> Does a language model distinguish a harmful outcome that is **used as a necessary means** to a goal from the same kind of harm that occurs only as a **foreseen side effect**, and does that distinction affect its judgment?

A possible stronger variant asked whether any LLM means/side-effect effect is mediated by a representation of **intentionality** versus a direct moral rule over causal structure.

## Semantic aliases

- means vs side effect
- means vs byproduct
- instrumental vs incidental harm
- necessary means vs foreseen consequence
- Doctrine of Double Effect
- causal role of harm
- instrumental dilemma vs incidental dilemma
- means principle
- intention-mediated moral judgment
- trolley means/side-effect

## Why it looked promising

The distinction is a mature object in moral cognition and philosophy, supported by a large human literature. Human work also offers an independent mechanistic debate: means/side-effect effects may be mediated by nonmoral intentional-attribution representations rather than by a domain-specific moral rule. Controlled matched scenarios and explicit causal graphs make the factor highly measurable.

## Decisive kill evidence for the simple Route-C version

The factor is already directly owned in LLM behavioral work.

1. **MoCa (2023/2024), `Measuring Human-Language Model Alignment on Causal and Moral Judgment Tasks`** explicitly annotates moral stories with `Causal Role: Means | Side Effect`, evaluates language models on these factors, and reports model-vs-human marginal effects.
2. **OffTheRails / `Procedural Dilemma Generation for Evaluating Moral Reasoning in Humans and Language Models` (2024)** generates causal-graph-controlled dilemmas and directly compares necessary-means versus side-effect harm; human participants and tested language models show corresponding permissibility/intention effects.
3. Later trolley/LLM evaluations continue to use switch/loop/footbridge and related instrumentality contrasts.

Therefore `do LLMs distinguish means from side effects?` is not fresh.

## Why the mechanism variant is not registered

Cushman (2011) provides an attractive independent human-theory question: direct moral-rule computation versus mediation through nonmoral intentional attribution. However, under the current protocol this would be a **Route-B** project, not permission to turn an occupied behavioral factor into a generic MI paper.

The current public evidence does not give a sufficiently clean, frozen, analyzable modern-open-model phenotype for the exact means/side-effect effect needed to causally adjudicate that debate. MoCa's older/open models do not provide a robust common side-effect preference, while the strongest clean procedural result is reported on closed GPT-4/Claude models. A GPU sweep to find an open checkpoint/subset that exhibits the desired effect would be behavior lottery.

## Strongest-neighbor warning

Do not revive this by treating OffTheRails/MoCa merely as `benchmarks`. Their experiments already **own the scientific factor**: causal role of harm as means versus side effect in LM moral judgment.

## Death code

```yaml
simple_object_N0: FAIL
simple_object_N2: FAIL
human_mechanism_debate: REAL
route_B_open_behavior_anchor: INSUFFICIENT
GPU_AUTHORIZED: false
verdict: KILL-NOVELTY / NO-MECHANISM-RESURRECTION-YET
```

## Resurrection condition

Only reopen the stronger theory question if a preregisterable public artifact establishes the **same theory-diagnostic means/side-effect effect on an analyzable modern open checkpoint**, with the major confounds (personal force, action/omission, outcome severity, inevitability) already controlled, so that intentionality-mediation versus direct moral-rule predictions can be frozen before MI.

## Do not revive by

- rerunning MoCa/OffTheRails on Llama/Qwen and calling the model change novelty;
- adding probes/SAEs/activation patching to the same behavior with no independent theory delta;
- using a different trolley vignette set;
- relabeling `means/side-effect` as `causal-role representation`;
- searching many open checkpoints/prompts until one exhibits the desired human-like effect.
