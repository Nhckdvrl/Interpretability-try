# Generic generalization licensing — prevalence / diagnosticity / principled-causal relation

Date: 2026-09-01  
Former project: `037_generic_generalization_licensing`  
Verdict: **KILL-NOVELTY / DEREGISTER**

## Semantic aliases

- generic licensing statistics vs concepts
- prevalence vs cue validity vs causal/principled generic
- why low-prevalence generics are accepted
- statistical vs conceptual generic representation
- generic characteristicness mechanism
- principled vs statistical properties in LLMs

## Natural question

Why are statements such as `Birds lay eggs` or `Mosquitoes carry malaria` acceptable despite many exceptions? Does acceptance track prevalence, diagnosticity/cue validity, or a principled/causal relationship between the kind and property?

The question is natural and paper-scale. The project is killed for novelty, not scale.

## Decisive new collision

A July 2026 paper found during the v2.1 re-audit directly occupies the central conceptual axis:

**Zhimin Hu, Jeroen van Paridon, Gary Lupyan (2026), `Failures and Successes to Learn a Core Conceptual Distinction from the Statistics of Language`, arXiv:2607.04523 / Evolang XV.**

The paper constructs **208 generic statements** and obtains human item-level judgments for:

1. bare generic truth;
2. `by virtue of` / principled truth;
3. prevalence;
4. cue validity.

It then explicitly asks whether language models distinguish **principled** kind-property relations from **merely statistical** relations while controlling prevalence and cue validity. Its central result is that ordinary distributional models largely lose the distinction after prevalence is controlled, while GPT-4 retains it much more strongly. The Discussion explicitly contrasts statistical co-occurrence with richer causal/world-model representations.

This overlaps the former 037 headline at the level that matters for N2:

> prevalence / cue-validity statistics vs a principled/causal conceptual relation as the basis of generic knowledge.

037 added modern open models, striking/danger/developmental manipulations, and causal activation interventions. Those are valuable experimental extensions, but after this collision the most natural description becomes:

> prior work established and behaviorally factorized the statistical-vs-principled distinction in language models; we causally mechanize it in open LMs.

Under the authoritative v2.1 N2 rule, that is not enough to retain a fresh PASS-REGISTER slot.

## Why the extra `danger / developmental / striking` cells do not save it

They broaden the human-theory battery, but do not create a sufficiently independent new object. The former project's H3 was explicitly `conceptual / causal licensing beyond prevalence and cue validity`, which is already a direct extension of the principled-vs-statistical object tested by Hu et al. The project would need a new headline to escape the collision, which would violate story/scope discipline.

## Nearest-neighbor warning

Do not resurrect by:

- replacing GPT-4 with Qwen/Llama/Mistral;
- changing `principled` to `causal`, `characteristic`, `essential`, or `conceptual`;
- adding activation patching / SAE / probing;
- focusing only on striking generics or only on cue validity while keeping the same statistics-vs-conceptual headline;
- using the Cimpian novel-kind stimuli as a new dataset.

These are experimental/method changes, not a clean concept-level novelty delta.

## Resurrection condition

Only reopen if a **different, independently natural generic phenomenon** is identified whose headline is not statistics-vs-principled/causal licensing—for example a genuinely orthogonal property of generic interpretation with its own scientific literature and natural cross-cells—and the current generics datasets become merely measurement windows.

## Provenance

The former full PASS contract remains recoverable in Git history from commit `3acc545386a7735769e185f014d2ddd1aa916a05`. It was deregistered immediately after the fatal 2026 collision was found; no GPU evidence was used to rescue or redefine the question.
