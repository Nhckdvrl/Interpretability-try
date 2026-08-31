# Rejection — Depth-Charge Semantic Illusion Mechanism

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- depth-charge illusion
- polarity illusion
- shallow/superficial interpretation vs compositional semantics
- noisy-channel repair vs literal composition
- constructionalized depth-charge meaning
- semantic-pragmatic repair under multiple negation

## Natural question considered

> Why do language models sometimes accept the plausible intended meaning of expressions like `No head injury is too trivial to ignore` instead of their compositionally licensed meaning: shallow incremental processing, noisy-channel repair, or a stored/constructionalized pattern?

This is a real and unusually strong linguistic object, but the theory-level explanatory axis is already too directly owned by recent work.

## Strong behavioral substrate found

ACL 2026 Main `Comparing human and language models sentence processing difficulties on complex structures` evaluates depth-charge comprehension together with matched baselines across 31 models, including all Llama-3.2, Qwen-3 and Gemma-3 families, and releases code/data. Thus modern open-model behavior and exact data are not the problem.

## Decisive novelty collision

The scientific question itself is already explicitly occupied:

- Paape (2023), *The Role of Incremental and Superficial Processing in the Depth Charge Illusion*, experimentally/modelingly tests incremental and superficial processing, world knowledge and communicative interpretation.
- Zhang, Ryskin & Gibson, *A noisy-channel approach to depth-charge illusions*, directly proposes rational noisy-channel inference as a competing account.
- Earlier depth-charge work directly tests processing-overload vs grammaticalized/ambiguity accounts.
- **Paape (2026), `What can LLMs tell us about the mechanisms behind polarity illusions in humans? Experiments across model scales and training steps`** explicitly uses LMs to adjudicate explanatory accounts of both the NPI and depth-charge illusions. The paper argues that LLM results weaken the need for rational-inference repair and proposes a synthesis based on shallow/good-enough processing and partial grammaticalization/construction grammar.

Accordingly, a new project whose headline is `Which of shallow processing / noisy-channel repair / stored construction causes the LLM depth-charge illusion?` is not an omitted concept-level axis. It is an internal mechanization/refinement of a question already named and debated in the LLM-specific literature.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
modern_open_behavior: PASS
exact_artifact: PASS
N0_object_ownership: FAIL
N1_causal_occupancy: partially_open_but_insufficient
N2_delta_width: FAIL
reason: internal causal localization would answer an already-owned 'mechanisms behind polarity illusions in LMs' question
verdict: KILL-NOVELTY
```

## Nearest-neighbor warning

Do not revive by:

- switching from Paape stimuli to ACL-2026 comprehension items;
- using Llama/Qwen/Gemma instead of Pythia;
- renaming accounts as literal vs pragmatic pathways;
- using activation patching/SAE/path patching;
- focusing on negation tokens or `too`;
- making the headline `when does the illusion emerge internally?`.

These keep the concept-level question unchanged.

## Resurrection condition

Only reconsider if a genuinely independent semantic-theory axis is found that is not equivalent to shallow/compositional, noisy-channel/rational repair, or constructionalization, and that has theory-defined cross-cells in the released modern-open-model substrate.
