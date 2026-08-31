# Decision-Choice Terminal Override (2026-08-31)

This file supersedes the stale `PRE-CANDIDATE / HIGH-PRIORITY SURVIVOR` status for **Description–Experience / Description–History Gap** in `rejected_candidates/decision_choice_anomalies.md`.

## Description–Experience (Description–History) Gap — KILL-N0

**Natural question:** Why does an LLM make different risky choices when the same underlying outcome distribution is given explicitly as probabilities versus shown through a history of outcomes?

**Why it looked good:**

- ACL 2026 `Mind the (DH) Gap!` reports a large description-history gap in conversational LLMs across 20 frontier/open models, with reasoning models behaving much more invariantly;
- code and processed model choice data are public;
- human decision science supplies several competing mechanistic explanations (sampling/probability inference, rare-event weighting, utility transformation, memory, policy/readout), making the internal causal question superficially excellent.

**Kill evidence under the current stricter handoff:**

The mother paper's **title-level scientific object is already the Description–History Gap itself**. It explicitly defines prospect representation (description versus experience/history), quantifies the behavioral gap, compares model classes, fits prospect-theoretic models, and links the model-class difference to mathematical-reasoning training. Therefore asking whether the gap arises in probability inference, value transformation, or decision policy is a direct `mother behavior → mechanism` follow-up. The fact that the mother has not yet used activation patching does not create a new scientific object under the repository's N0 rule.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as explicit-probability vs sampled-history representation, description-vs-experience pathway, rare-event weighting circuit, experience-policy routing, or reasoning-training collapses two pathways. These are mechanism decompositions of the mother's headline object.

**Resurrection condition:** a different risky-choice phenomenon with a title-level behavioral distinction not already defined by description/history representation, framing, order, explanation, or generic risk-policy differences, and with a natural modern-open-family existence substrate.

**References:**

- https://aclanthology.org/2026.acl-long.479/
- https://github.com/Yongyan-Zhang/mind-the-dh-gap

**Final status:** `KILL-N0 / TERMINAL`. 
