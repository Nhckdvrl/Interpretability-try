# Rejection — Linguistic Convergence: Automatic Alignment vs Audience Design

Date: 2026-09-01  
Verdict: **KILL-NOVELTY / KILL-DATA**

## Semantic aliases

- linguistic accommodation mechanism
- automatic interactive alignment vs audience design
- priming vs partner-specific adaptation
- stylistic convergence mechanism
- local style imitation vs recipient design
- conversational entrainment vs strategic audience adaptation
- speaker-role adaptation vs recency priming

## Natural question considered

> When an LLM converges to a conversational partner's linguistic style, is the adaptation primarily automatic local alignment/priming, or does the model maintain a partner-specific audience representation and choose forms conditionally on that representation?

This question is natural and grounded in psycholinguistics / sociolinguistics, but the current LLM substrate does not leave a sufficiently clean, unoccupied, experiment-ready delta.

## Scientific lineage

The candidate was motivated by two genuine human-language accounts:

- Interactive Alignment / structural priming: convergence can emerge from largely automatic repetition and alignment across representational levels.
- Communication Accommodation / Audience Design: speakers adapt to interlocutors in socially and communicatively conditioned ways, including partner-specific recipient design.

The distinction predates LLMs and passes benchmark removal in isolation.

## Decisive kill evidence

### 1. The strongest EACL 2026 mother already advances a mechanism interpretation

Blevins, Schmalwieser & Roth, EACL 2026 Main, `Do language models accommodate their users? A study of linguistic convergence`, does more than establish aggregate convergence.

It:

- evaluates sixteen models across three dialogue corpora;
- performs a stepwise analysis separating immediately recent turns from earlier turns and speaker roles;
- reports strong recency for exact lexical/proper-noun overlap;
- finds sensitivity to the speaker role the model is replacing;
- explicitly contrasts human communicative accommodation with LM behavior;
- hypothesizes that LM convergence instead follows from the pretraining objective's pressure for stylistic consistency and connects it to structural priming / semantic leakage;
- states that future work should examine the underlying causes of LM convergence.

Thus a paper framed simply as `the mother found convergence; we causally test priming/style consistency versus human-like accommodation` is perilously close to mechanizing the mother's own Discussion and future-work interpretation.

### 2. The released measurement window lacks a decisive audience-design cross-cell

The EACL artifact is valuable and public, but its core setup completes fixed pre-existing dialogues. Alternating prior turns permit recency and speaker-role analyses, but **speaker role is not equivalent to a manipulated audience model**.

A theory-diagnostic test of automatic alignment versus audience design would need already-established cells such as:

- same recent linguistic prime with different partner identity/beliefs;
- partner switch while preserving local lexical/syntactic history;
- same partner representation with controlled recent prime removal;
- audience-relevant vs audience-irrelevant style changes.

Those cross-cells are not central gold in the mother artifact.

ACL 2025 Short `LLMs syntactically adapt their language use to their conversational partner` builds GPT-4o/Llama-3 agent-agent dialogues and establishes syntactic adaptation, but likewise does not supply the frozen partner-switch × local-prime factorization needed to adjudicate the two mechanisms without first creating new behavioral conditions.

## Gate audit

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
scientific_lineage: PASS
N0_object_ownership: crowded
N1_causal_occupancy: not_fully_occupied
N2_delta_width: unsafe
reason_N2: mother already proposes pretraining/priming-style consistency as the likely cause and explicitly leaves underlying-cause analysis as future work
exact_public_artifact: PASS
modern_open_behavior: PASS
frozen_theory_diagnostic_cross_cells: FAIL
requires_new_behavior_discovery: true
verdict: KILL-NOVELTY / KILL-DATA
```

## Nearest-neighbor warning

Also treat the following as nearby ownership:

- ACL 2025 syntactic partner adaptation;
- structural priming in LMs;
- semantic leakage/contextual entrainment work;
- 2026 studies of socially conditioned register modulation / observer identity.

Do not revive by renaming local priming as `automatic alignment`, or by calling speaker-role sensitivity an `audience model` without an actual audience-manipulation control.

## Resurrection condition

Only reconsider if an existing public modern-open-model artifact already contains a theory-diagnostic **partner identity/audience state × recent linguistic prime** factorization with stable effects on at least two genuinely different open families, and strongest-neighbor search confirms that the causal distinction has not already been studied. The project must not depend on constructing the factorization and running models first to see whether the phenomenon exists.
