# Rejected Candidates — Factuality / Information Conflict

**Domain:** false premises, answerability, misinformation, source credibility, repetition, retractions, context–memory conflict.  
**Status:** breadth-first scan completed for the current round.  
**Rule:** these entries are negative knowledge; do not revive by swapping datasets, model families, or factual domains unless the resurrection condition is genuinely met.

---

## 1. “The model knows the premise is false but answers anyway”

**Natural question:** Why does a model answer a question whose premise is false even when it has enough knowledge to reject the premise?

**Why it initially looked good:** Very natural real failure; seemingly ideal dissociation between stored knowledge / premise detection and answer-generation policy; easy public G0 using false-premise QA.

**Kill evidence:** Earlier work already showed that models often possess the knowledge needed to rebut false premises and that elicitation matters (`Won't Get Fooled Again`, ACL 2023). More decisively, `Two Axes of LLM Abstention: Answer Correctness and Question Answerability` (2026) explicitly separates correctness from answerability, shows that hidden states carry false-premise / unanswerability information that ordinary confidence and verbal checks miss, and then uses that hidden-state signal to route a premise-check policy. This occupies both the decisive representation–behavior dissociation and the mechanism-informed method story.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as CREPE, false assumptions, unanswerable questions, presupposition failure, “knowledge present but not used,” or another QA domain.

**Resurrection condition:** Need a qualitatively different natural phenomenon beyond answerability detection—for example, the model correctly and stably represents a *specific corrected world model* yet a later causal computation overwrites it in a structured way not covered by abstention/routing.

**Key references:** https://aclanthology.org/2023.acl-long.633/ ; https://arxiv.org/abs/2607.08456

---

## 2. Repetition overrides source credibility

**Natural question:** Why can repeating a claim from a low-credibility source make the model prefer it over a conflicting claim from a more credible source?

**Why it initially looked good:** Concrete and socially important; striking because the model otherwise exhibits sensible source preferences; naturally invites competition between source-quality and repetition/frequency signals.

**Kill evidence:** `Whose Facts Win? LLM Source Preferences under Knowledge Conflicts` (ACL 2026) already establishes the exact behavior across 13 open-weight LLMs: institutionally corroborated information is normally preferred, but repetition of lower-credibility information can reverse the preference. It also provides a targeted mitigation that reduces repetition bias while preserving much of the original source preference. A new interpretability-only follow-up would struggle to satisfy the repository's method-closure requirement because the practical repair is already available without the mechanism.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** Repeating social-media claims, duplicated RAG passages, majority-vote sources, duplicated citations, or “frequency beats credibility” are the same mother question.

**Resurrection condition:** A new decisive contrast must force different interventions depending on the internal cause and outperform / explain failures of the existing repetition-bias mitigation; merely finding a repetition direction is insufficient.

**Key reference:** https://aclanthology.org/2026.acl-long.1357/

---

## 3. Generic continued influence after correction / retraction

**Natural question:** Why does corrected misinformation continue to influence later reasoning after the model has been told that it was wrong?

**Why it initially looked good:** Classic continued-influence effect in humans; extremely natural for deployed assistants; possible split between correction encoding, event-model updating, retrieval competition, and downstream inference.

**Kill evidence:** `Unraveling Misinformation Propagation in LLM Reasoning` (Findings of EMNLP 2025) already studies injected misinformation propagating through reasoning, including cases where models possess the correct knowledge yet fail to correct the reasoning chain; it evaluates explicit correction placement and synthetic early-correction training. This does not reproduce every classic retraction paradigm, but it occupies the central narrative “correct knowledge / correction is available, yet misinformation still drives later reasoning,” and already creates obvious mitigation paths. Recasting it as a narrative-event CIE would be a domain swap rather than a sufficiently new decisive contrast.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Retraction, correction memory, post-hoc fact checking, narrative misinformation, and “the model remembers the correction but still reasons from the old claim” require an actually new causal contrast, not just different surface stimuli.

**Resurrection condition:** Reopen only if a public/cheap paradigm exposes a structured dissociation absent from misinformation-propagation work—for example, correction changes explicit belief and local retrieval but leaves a separable causal event model unchanged, with mechanism-specific intervention predictions.

**Key reference:** https://aclanthology.org/2025.findings-emnlp.631/

---

# Current lessons from the domain

1. In 2026, generic “the model knows X internally but says/does Y” factuality stories are no longer novel by themselves.
2. False-premise detection is especially crowded because answerability has now been separated from correctness at the hidden-state level and used for routing.
3. Repetition/source-conflict is behaviorally attractive but already has an end-to-end mitigation, so mechanism work needs a stronger reason to exist.
4. Future candidates should seek a genuinely different *state-update computation* or causal object, not merely another context-vs-memory conflict.