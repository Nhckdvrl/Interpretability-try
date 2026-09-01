# 038 Hard Re-Audit — 2026-09-01

Verdict: **PASS-REGISTER / GPU AUTHORIZED — HARD RE-AUDIT PASSED**

## Frozen question

> When reference remains genuinely unresolved, does the model maintain multiple candidate referents, a compact underspecified reference state, or prematurely commit to one candidate?

## Why this audit was necessary

After former 039 failed because its scientific object was already owned despite different neighboring paper headlines, 038 was re-audited using the same standard: search for object ownership inside experiments and interpretations, not merely exact title matches.

## Strongest modern neighbors checked

### `It Depends` — UncertaiNLP 2025

Tests DeepSeek v3, Qwen3-32B, Llama-3.1-8B and others on persistent referential ambiguity. It establishes behavior: models often commit to one interpretation or enumerate alternatives rather than appropriately preserve uncertainty / clarify.

Source: https://aclanthology.org/2025.uncertainlp-main.20/

**Occupies:** behavioral ambiguity handling.  
**Does not occupy:** internal representational format of a still-unresolved reference.

### `Correct-Detect` — EMNLP 2025 Main

Uses AmbiCoref and Llama-3.1-70B / GPT-4o. It establishes the correctness-versus-ambiguity-detection trade-off and shows models often answer ambiguous items as though one interpretation were licensed.

Source: https://aclanthology.org/2025.emnlp-main.1527/

**Occupies:** coreference ambiguity detection/resolution behavior.  
**Does not occupy:** parallel candidates vs underspecification vs early internal commitment.

### `When Agents Commit Too Soon` — 2026

Defines generic representational commitment in long-horizon agents as hidden-state convergence across runs and demonstrates signatures in Llama-3.1-70B, Qwen2.5-72B and Phi-3-14B.

Source: https://arxiv.org/abs/2606.22936

This is an important N2 warning because `premature commitment` is not itself a novel generic LLM phrase anymore.

**Occupies:** whether a reasoning trajectory has settled into a stable path.  
**Does not occupy:** the linguistic-reference object or whether unresolved reference is encoded as multiple candidate identities versus a single underspecified variable versus one selected antecedent.

### `Tug-of-war between idioms' figurative and literal interpretations in LLMs` — EACL 2026

Uses causal tracing to show competing literal and figurative pathways for idioms, with both readings remaining available.

Source: https://aclanthology.org/2026.eacl-long.135/

This is the closest mechanistic ambiguity neighbor.

**Occupies:** causal competition between two lexicalized idiom interpretations.  
**Does not occupy:** genuinely unresolved discourse reference or the explicit-alternatives-vs-underspecification factorization.

### `Divergent large language model predictions from convergent representations in ambiguous word pairs` — Aug 2026

Studies lexical ambiguity in GPT-2, Llama-3.2-3B and Qwen2.5-32B with layer analysis and activation patching.

Source: https://arxiv.org/abs/2608.01816

**Occupies:** internal representation of context-disambiguated lexical senses / prediction differences.  
**Does not occupy:** a reference that remains unresolved because context does not determine a unique antecedent.

### `How Language Models Prioritize Contextual Grammatical Cues?` — BlackboxNLP 2024

Uses BERT/GPT-2 and activation patching when multiple gender cues can each independently determine a target pronoun.

Source: https://aclanthology.org/2024.blackboxnlp-1.21/

**Occupies:** priority among redundant disambiguating grammatical cues.  
**Does not occupy:** unresolved two-candidate reference; every cue in its setup licenses a determinate pronoun prediction.

## N0 / N1 / N2 conclusion

The exact remaining scientific object is still unoccupied:

> **What representational format carries a linguistic reference before the available evidence licenses a unique antecedent?**

This is broader than explaining `Correct-Detect` behavior and distinct from generic hidden-state convergence, idiom competition, and already-disambiguated lexical senses.

The concept-level delta therefore survives the 039-style audit.

## Substrate / measurement conclusion

The substrate remains unusually strong:

- AmbiCoref: human-validated ambiguous/unambiguous minimal pairs;
- Correct-Detect: modern open Llama behavior on AmbiCoref;
- It Depends: Qwen/Llama/DeepSeek persistent-ambiguity behavior plus explicit row-level candidate sets and permutations;
- central candidate scoring can be deterministic and need not depend on an API LLM judge.

## Identifiability conclusion

Unlike the former 036 contract, 038 explicitly contains a hard H1-vs-H2 identifiability gate:

- candidate-specific causal coverage/selectivity must support explicit alternatives;
- a candidate-balanced shared ambiguity/underspecification state must be independently validated for the underspecified account;
- asymmetric candidate coverage plus prespecified order/semantic bias supports early commitment;
- if these signatures cannot robustly separate H1 from H2, the architecture claim terminates rather than shrinking to `ambiguity is represented somewhere`.

That is a legitimate falsifier rather than a post-hoc rescue path.

## Final verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
N0_object_ownership: PASS
N1_causal_occupancy: PASS
N2_delta_width: PASS
substrate: PASS
modern_open_model_premise: PASS
central_gold_without_llm_judge: PASS
causal_identifiability_contract: PASS_WITH_HARD_KILL
story_invariance: PASS
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

038 remains frozen. Do not broaden it into generic ambiguity processing, generic uncertainty, or generic premature commitment.
