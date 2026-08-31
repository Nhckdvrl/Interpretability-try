# Rejected Candidates — Risk / Uncertainty Factorization

**Domain:** probability, risk, uncertainty, harm and decision-related factorization topics considered under the Hamdi-style P0 → S0 → N0 → N1 funnel.  
**Status:** negative-memory ledger, 2026-08-31.

---

# 1. Likelihood ≠ Severity

**Natural question:** A rare catastrophe can be extremely severe, while a common event can be mild. Does a language model represent how likely an event is separately from how bad its consequences would be?

**Why it initially looked good:**

- probability and consequence severity are foundational, independently meaningful components of risk;
- ordinary examples immediately populate both axes;
- mechanistic forks are strong: one generic risk scalar vs independent probability/severity variables vs separate variables combined only at readout.

**Kill evidence:**

The exact internal decomposition is already substantially occupied. 2026 work on **Expected Harm** explicitly formulates harm as a combination of consequence severity and execution likelihood/cost, then probes internal language-model representations and reports strong severity/refusal-related signals but weak or missing execution-cost/likelihood sensitivity. This is already the scientific axis plus internal-representation analysis we would otherwise claim. Restricting the same question to ordinary accidents, medical risks, or non-jailbreak scenarios would be a domain swap rather than a new scientific object.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as probability-vs-severity, likelihood-vs-impact, risk-frequency-vs-harm, execution-likelihood-vs-consequence, or by switching from safety prompts to another hazard domain.

**Resurrection condition:** A genuinely different risk variable with independent external gold and a causal prediction not reducible to the likelihood × severity / expected-harm decomposition.

---

# 2. Epistemic Uncertainty ≠ Aleatoric Uncertainty

**Natural question:** Is the model uncertain because it lacks knowledge, or because the world itself is inherently variable or unpredictable?

**Why it initially looked good:**

- the distinction is foundational in statistics and decision theory;
- either answer is meaningful scientifically;
- the internal hypotheses naturally support causal representation tests.

**Kill evidence:**

This is a direct mechanistic collision. ICML 2024 **Distinguishing the Knowable from the Unknowable with Language Models** already uses hidden-state probes to distinguish epistemic and aleatoric uncertainty. ACL 2026 further studies internal/self-function-vector estimation of aleatoric uncertainty, and AAAI 2026 work explicitly decomposes uncertainty signals. The title-level internal factorization is therefore already occupied.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as knowable-vs-unknowable, model-ignorance-vs-world-randomness, reducible-vs-irreducible uncertainty, or by swapping uncertainty estimator / benchmark / model family.

**Resurrection condition:** A different uncertainty distinction whose variables and causal predictions are not reducible to epistemic/aleatoric decomposition.

---

# Cross-cutting lesson

Risk and uncertainty have many attractive textbook decompositions. Before treating one as a Hamdi-style orthogonal axis, search recent MI work aggressively: these dimensions are already common targets for probing and causal representation analysis. A classic conceptual distinction is not sufficient novelty by itself.
