# Rejection — Belief-Bias Dual-Process Arbitration

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- belief bias in syllogistic reasoning
- logic vs plausibility arbitration
- System 1 belief heuristic vs System 2 logical reasoning
- belief override vs analytic correction
- content-independent reasoning vs world-knowledge contamination
- plausibility trap / semantic-content interference in logic

## Natural question considered

> When formal validity conflicts with prior semantic belief, does an LLM first follow a belief-based heuristic that must be overridden by an analytic process, or does logical structure and world knowledge interact within a single integrated computation?

The question is scientifically natural and has a mature cognitive lineage, but the LLM mechanistic axis is already occupied too directly.

## Decisive kill evidence

**Kim, Valentino & Freitas, Findings of ACL 2025 — `Reasoning Circuits in Language Models: A Mechanistic Interpretation of Syllogistic Inference`** already performs the relevant causal decomposition.

Paper: https://aclanthology.org/2025.findings-acl.525/

The paper:

- discovers a sufficient/necessary causal circuit for content-independent syllogistic inference;
- explicitly asks whether content-independent reasoning mechanisms are disentangled from world knowledge and belief biases (RQ2);
- studies concrete schemes instantiated with commonsense knowledge;
- reports partial contamination of the core reasoning circuit by additional attention heads encoding commonsense/contextual knowledge;
- tests transfer across schemes, sizes and architectures using activation patching and related mechanistic tools.

This is not merely a behavioral belief-bias mother. It already owns the key internal factorization `formal reasoning circuit vs world-knowledge/belief-bias contamination`.

SemEval-2026 Task 11 further makes `disentangling content and formal reasoning` an explicit shared-task object, and multiple systems frame the conflict as logic vs belief / System-1 vs System-2. This increases N2 crowding rather than providing a fresh omitted axis.

## N0 / N1 / N2 audit

```yaml
N0_object_ownership: unsafe
reason: content-independent formal reasoning vs belief/content contamination is already an explicit research question

N1_causal_occupancy: FAIL
reason: Findings ACL 2025 already uses causal circuit interventions and identifies world-knowledge heads contaminating the reasoning circuit

N2_delta_width: FAIL
reason: recasting the same factorization as dual-process arbitration/override does not create a sufficiently new concept-level scientific question
```

## Why terminology cannot rescue it

Do not revive by renaming the two sides as:

- heuristic vs analytic;
- System 1 vs System 2;
- belief module vs logic module;
- plausibility pathway vs validity pathway;
- conflict detector / override gate.

Unless a genuinely different external scientific axis is introduced with independently diagnostic natural cross-cells, these are descriptions of the already-studied reasoning-vs-knowledge entanglement.

## Nearest-neighbor warning

- Findings ACL 2025: mechanistic syllogistic reasoning + belief contamination.
- SemEval-2026 Task 11: `Disentangling Content and Formal Reasoning in Large Language Models`, with public validity × plausibility labels and many Qwen/Llama systems.
- SemEval 2026 `ModusPonens`: explicitly frames belief bias as calibration between System-1 heuristic and System-2 logical thinking.

## Resurrection condition

Only reconsider if the new project asks a **different theory-level question** that is not equivalent to separating formal logic from semantic/world knowledge, and if its key causal factorization is absent from the Findings 2025 circuit analysis and SemEval-2026 content-effect literature.
