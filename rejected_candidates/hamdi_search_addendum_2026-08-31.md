# Hamdi-Style Search Rejection Addendum — 2026-08-31

This file records cross-domain candidates from the 2026-08-31 Hamdi-style search that are easy to accidentally rediscover because an older domain log is stale, the topic resembles a successful scientific-object pattern, or a new 2026 paper makes the collision especially tempting.

**Authority rule:** entries here supersede older `under audit` / `survivor` wording for the same scientific object. Full experimental evidence for formal archive projects remains in `archive/` and `phenomenon_miner/FAILED_TOPICS.md`.

---

# 1. Deontic Facilitation in the Wason Selection Task — TERMINAL

**Natural question:** Why can the same conditional logic become easier when framed as a norm/permission rather than a descriptive rule?

**Why it initially looked good:**

- exceptionally natural human cognitive phenomenon;
- EACL 2026 reports a broad deontic-vs-epistemic/descriptive advantage;
- exact logical structure suggested a clean failure-mechanism path.

**Kill evidence:**

This topic is already a completed internal negative result in `archive/004_deontic_facilitation/`. The decisive test used **32 genuinely matched Wason pairs**, all 24 card permutations and two prompt templates. Qwen showed only a small residual advantage, Gemma was approximately null, and **0/32 pairs** met the preregistered strong-pair criterion. The mother paper’s aggregate deontic/descriptive rows were not matched versions of the same semantic item, so the broad dataset-level difference did not survive the causal phenotype we actually needed.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** Do not revive as deontic facilitation, normative framing helps logic, permission-vs-description Wason, or by changing NeuBAROCO subset/model/prompt. The matched phenotype failed on the analyzable open models.

**Resurrection condition:** Only genuinely new evidence of a large matched deontic-framing effect on multiple current open families under the same logical items, not another aggregate dataset comparison.

**Internal references:** `archive/004_deontic_facilitation/`, `archive/README.md`, `phenomenon_miner/FAILED_TOPICS.md`.

---

# 2. Motivated Reasoning: Evidence Representation ≠ Late Decision Bias

**Natural question:** When identity cues bias a model’s conclusion, does the model actually reinterpret the evidence, or does it understand the evidence correctly and bias only the final decision/readout?

**Why it initially looked good:**

- this is a real cognitive fork, not a generic “persona representation” question;
- Findings ACL 2026 reports strong identity-congruent motivated reasoning across multiple LLMs;
- the mechanistic hypotheses are naturally distinct: early evidence distortion vs intact evidence + late motivated readout.

**Kill evidence:**

The substrate and N1 jointly fail the current registration bar.

1. The striking numeric-scientific-evidence result in **Persona-Assigned Large Language Models Exhibit Human-Like Motivated Reasoning** is inherited from a very small fixed set of human-study scientific-evidence scenarios with repeated sampling, rather than a broad natural row-level population that could support the title-level factorization without protocol dependence.
2. Persona-driven reasoning is already mechanistically occupied: **Dissecting Persona-Driven Reasoning in Language Models via Activation Patching** (Findings EMNLP 2025) directly traces how persona information is transformed by early MLPs and middle attention layers and shapes objective-task outputs.
3. Recent motivated-reasoning activation-probing work further narrows the remaining mechanism space.

The surviving novelty would therefore require increasingly specific wording such as “evidence-vs-decision decomposition for political numeric-table motivated reasoning,” violating the anti-narrowing rule.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as motivated reasoning localization, persona-induced evidence distortion, identity-congruent evidence processing, early-vs-late political bias, or “persona exists → is it causal?” with another objective benchmark.

**Resurrection condition:** A broad natural/open dataset with objective evidence-level gold and a stable multi-family motivated-reasoning effect whose decisive scientific question cannot be reduced to generic persona-driven reasoning or existing activation-patching accounts.

**References:**

- https://aclanthology.org/2026.findings-acl.585/
- https://aclanthology.org/2025.findings-emnlp.1335/

---

# 3. Self-Attribution / Ownership Confidence Bias

**Natural question:** Why is a model more confident in an identical answer merely because the conversation marks that answer as “its own” rather than the user’s?

**Why it initially looked good:**

- extremely natural and surprising behavioral phenomenon;
- 2026 work reports the effect across six recent open-weight models, three benchmarks and three confidence elicitation methods, with confidence differences up to about 26%;
- it naturally invites a self/ownership-state mechanism question.

**Kill evidence:**

This is unusable as a new topic for two independent reasons.

1. **Large Language Models Are Overconfident in Their Own Responses** (Findings ACL 2026 / arXiv 2606.03437) already owns the behavioral headline and explicitly names the phenomenon **ownership bias**, studies post-training/chat-format causes, and proposes an inference-time mitigation.
2. Internally, this scientific object collides with archived `007_choice_supportive_ownership_bias`, which already tested choice/ownership-specific bias and terminated because Qwen and Gemma exhibited qualitatively different phenomena. A new confidence readout does not authorize resurrection of the same ownership/self-attribution family.

**Death code:** `INTERNAL_COLLISION`

**Nearest-neighbor warning:** Do not revive as my-answer-vs-user-answer confidence, self-attribution confidence, answer ownership, “model trusts itself more,” or by replacing confidence with calibration/Brier/uncertainty readout.

**Resurrection condition:** A genuinely different self-reference phenomenon with a new external scientific object, not another ownership-conditioned evaluation of an answer already present in context.

**References:**

- https://arxiv.org/abs/2606.03437
- `archive/007_choice_supportive_ownership_bias/`

---

# Search discipline added by this addendum

Before proposing any topic whose words include **deontic / normative framing**, **persona / motivated reasoning / identity-congruent**, or **own answer / self-attribution / ownership**, search this file and the referenced archive/domain log first. A different benchmark, model family, confidence interface, or MI technique is not a new scientific object.
