# Rejection Record — Desire vs Intention Mental-State Representation

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish **wanting an outcome** from **having formed an intention/plan to bring it about**?

## Semantic aliases

- desire vs intention
- wanting vs intending
- goal preference vs committed plan
- wish vs action commitment
- BDI mental-state separation

## Why it looked promising

The distinction is elementary in philosophy of action, cognitive science and BDI agent theory. A person can strongly want an outcome without intending to pursue it, or form an intention despite weak intrinsic desire. It seemed potentially valuable for agentic LLMs because intention should have stronger prospective consequences for planning/action than desire.

## Decisive kill evidence

Findings ACL 2025 **`Beyond Words: Integrating Theory of Mind into Conversational Agents for Human-Like Belief, Desire, and Intention Alignment`** directly studies the proposed mental-state categories in open-source LLaMA models. The paper frames Theory of Mind specifically in terms of **beliefs, desires, and intentions**, asks whether LLM-powered agents can infer these states during conversation, and investigates whether open-source LLaMA models **represent and retain ToM-related constructs** and use those representations for coherent mental-state modeling.

The accompanying public repository `cruiseresearchgroup/ToM_and_Alignment` provides the implementation/artifacts.

Therefore a new project asking whether hidden states separate desire from intention would not introduce a fresh model property. The scientific categories and their internal representation are already explicit in the strongest modern-open LLM neighbor. Different probes, steering, or a more factorial vignette set would mainly deepen the mechanism of an already-owned object.

## Strongest-neighbor warning

Do not revive as:

- desire/intention directions;
- want-vs-plan steering;
- goal preference vs committed intention subspaces;
- BDI-state causal patching;
- intention commitment latent state;
- modern Qwen/Gemma replication of belief/desire/intention representation.

## Death code

`F2 / N0-N2 — belief/desire/intention are already explicit representational objects in modern open-LLaMA ToM work.`

## Resurrection condition

Only reconsider if a distinct action-control property is found that cannot be reduced to belief/desire/intention classification or retention, prospective memory, goal/subgoal status, or generic planning commitment, with an independent natural object and substrate.
