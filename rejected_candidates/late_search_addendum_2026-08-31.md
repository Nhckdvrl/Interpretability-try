# Late Hamdi-Style Search Rejection Addendum — 2026-08-31

**Purpose:** freeze additional scientific-object deaths discovered during the final convergence pass of the 2026-08-31 search. This file is authoritative over earlier chat or domain-log wording that still lists one of these ideas as `under audit`.

---

# 1. Assertion ≠ Presupposition — S0 KILL

**Natural question:** Does a language model distinguish a proposition that a speaker directly asserts from the same proposition treated as background presupposed information?

**Why it initially looked good:**

- `John stopped smoking` asserts a current-state claim while presupposing that John smoked before; the distinction is foundational and natural;
- NOPE provides natural corpus sentences and human-authored / checked presupposition propositions;
- recent open models show behavioral sensitivity to presupposition, so the semantic capability itself is not exotic.

**Kill evidence:**

The required factorization substrate is not available. NOPE gives a source-grounded **presupposed proposition**, but it does not supply a large natural population in which the **same proposition p** is independently observed as asserted in one row and presupposed in another with matched external gold. Building the decisive population would therefore require researcher-written asserted counterparts or other synthetic rewrites. That violates the S0 rule that the central cross-cells of a factorization topic must already exist naturally and cannot be manufactured by the experimenter.

This is not rescued by the fact that presupposition projection itself is well studied: W13 already showed that a presupposition *failure-mechanism* based on negation/projection was not stable across open families, while the present factorization version fails for a different reason—the missing same-p / different-status natural population.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** Do not revive as `at-issue vs background`, `asserted vs accommodated`, `asserted vs presupposed proposition`, or by writing paraphrases / templated assertion controls ourselves.

**Resurrection condition:** a released natural corpus with independently validated proposition-level alignment in which the same content occurs at useful scale under asserted and presupposed discourse status, without researcher-created central examples.

---

# 2. Truth ≠ Popular / Human Belief — N1 KILL

**Natural question:** A claim can be objectively true even if many people disbelieve it, and false even if many people believe it. Does a language model distinguish world truth from what people believe to be true?

**Why it initially looked good:**

- the distinction is naturally orthogonal and extremely easy to explain;
- fact-checking studies can pair expert-grounded veracity with human perceived-accuracy ratings on the same headlines;
- the object superficially resembles Hamdi's successful `knowledge ≠ ontology` factorization.

**Kill evidence:**

The broad title-level object is already occupied by **Suzgun et al., Language models cannot reliably distinguish belief from knowledge and fact, Nature Machine Intelligence 2025**. The KaBLE benchmark contains 13,000 questions across 13 epistemic tasks and explicitly frames the scientific problem as separating factual truth from human belief/knowledge, including false-belief cases and Llama-family models.

Restricting the new proposal to **collective / popular belief** rather than individual belief would be exactly the prohibited anti-narrowing move: the title would survive only by adding an adjective to an already-owned `truth vs belief` scientific object.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as `truth vs perceived truth`, `fact vs popular belief`, `fact-checker truth vs crowd belief`, `objective truth vs social belief`, or by changing fact-checking datasets.

**Resurrection condition:** a genuinely different epistemic variable not reducible to belief/knowledge/fact distinctions, with an independent external definition and a new title-level scientific object.

**Reference:** https://www.nature.com/articles/s42256-025-01113-8

---

# 3. Plausible ≠ True — S0 / narrative KILL

**Natural question:** Something can sound very plausible and still be false, while a surprising fact can be true. Does a language model separately represent plausibility and truth?

**Why it initially looked good:**

- ordinary distinction with obvious cross-cells;
- plausibility has substantial psycholinguistic annotation literature;
- would potentially separate world-model likelihood from factual status.

**Kill evidence:**

No broad natural substrate was found in which the **same statements** have both independent factual-truth gold and high-quality human plausibility ratings at the scale required for MI. Existing plausibility corpora provide plausibility labels as their central target, not an independently sourced truth axis; combining them with a fact benchmark would create the central mapping ourselves. Meanwhile the surrounding representation space is already crowded by direct work on plausibility/content effects (including ACL 2026 representational analysis of logical validity vs plausibility) and broad truth-direction / factuality work.

Keeping the topic would therefore require either synthetic true/false sentence construction plus plausibility ratings, or narrowing to one controlled reasoning task. Both violate S0 / anti-narrowing.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** Do not revive as `believable vs true`, `plausible falsehoods`, `surprising truths`, or by joining a plausibility corpus to FEVER/TruthfulQA after the fact.

**Resurrection condition:** a large released natural statement corpus with independently sourced truth labels and independent human plausibility ratings on the same units, plus a fresh N1 audit showing the resulting object is not absorbed by truth/belief/plausibility representation work.

---

# 4. Human False Consensus Effect — S0 KILL under current rules

**Natural question:** After a model adopts a choice or opinion, does it overestimate how many other people would make the same choice?

**Why it initially looked good:**

- classic and immediately understandable cognitive bias;
- Findings NAACL 2025 explicitly reports false-consensus behavior in LLMs;
- it naturally suggests a mechanistic fork between population-prior retrieval and projection of the model's current self/choice state.

**Kill evidence:**

The published LLM evidence does not satisfy the repository's current failure-mechanism S0. The mother study uses GPT-4, Claude 3, LLaMA 2 70B, and Mixtral and is based on four classic hypothetical Ross et al. scenarios. Because models free-choose the options extremely one-sidedly, the main experiment **directly feeds each option as if the model had chosen it** in order to construct the two groups. Thus the central self-choice state is partly imposed by the protocol rather than arising as a broad modern open-model behavioral population.

Under the current S0 rules, an old-model / four-scenario cognitive transfer with an imposed-choice construction is not enough to register a new failure mechanism. It would require a fresh modern open-family existence screen before any MI work.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** Do not revive directly as `false consensus`, `models think others agree with them`, or `self-choice projection` merely because the NAACL behavior paper exists.

**Resurrection condition:** a new ordinary-prompt population with deterministic scoring showing a large self-choice-conditioned consensus shift on at least two of three current analyzable families (e.g. Qwen3, Gemma3, Llama3.x) without having to force the model's own choice. If that appears, treat it as a fresh P0/S0 candidate rather than inheriting the old paper's effect.

**Reference:** https://aclanthology.org/2025.findings-naacl.6/

---

# 5. Statistical Significance ≠ Replicability — do not promote from BEAR alone

**Natural question:** A result being statistically significant once does not mean it will replicate.

**Status:** `NOT REGISTERED / HIGH N0-S0 RISK`, not a formal standalone kill of the broad philosophical distinction.

**Reason not to promote:** SCORE/OSC/Many Labs provide excellent matched replication outcomes, but `replicability/credibility prediction` is already a major scientific object of SCORE, with human and machine assessments of thousands of claims. A mechanistic project would need a genuinely new object beyond `predict which claims replicate`. In addition, a failure-mechanism version would require stable open-model replication forecasts before registration. Do not mistake BEAR's clean matched rows for novelty.

**Nearest-neighbor warning:** `p<.05 ≠ replication`, `significance vs credibility`, and `original evidence vs replication outcome` should not enter active merely because SCORE makes them easy to measure.

---

## Current implication

The late search reinforces the main rule:

> **A beautiful two-axis dataset is not enough, and a published human-like bias is not enough. The title-level scientific object must survive S0 and N0/N1 independently.**
