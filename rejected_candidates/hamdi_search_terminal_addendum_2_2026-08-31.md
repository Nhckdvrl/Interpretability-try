# Hamdi-Style Search — Terminal Addendum II (2026-08-31)

This file freezes scientific objects rejected during the second half of the 2026-08-31 search. It exists to prevent attractive titles from being rediscovered after changing the dataset, model, language, or MI method.

**Authority rule:** if an item below conflicts with an older `under audit`, `lead`, or `HOLD` note for the same scientific object, this file is the newer adjudication. A dead object may only re-enter the funnel if its explicit resurrection condition is satisfied; a new probe/SAE/patching result is not itself a resurrection condition.

---

# 1. Assertion ≠ Presupposition — KILL-DATA

**Natural question:** Does a language model represent the same proposition differently when a speaker directly asserts it versus merely presupposes it as background information?

**Why it looked good:**

- `John stopped smoking` asserts a present change but presupposes prior smoking;
- propositional content and discourse status are genuinely different concepts;
- NOPE provides naturally occurring presupposition triggers and human-written presupposed propositions.

**Kill evidence:**

The decisive S0 population is missing. NOPE supplies the **presupposition side**, but no large natural artifact was found in which the **same proposition** independently occurs with source-grounded `asserted` versus `presupposed` status. Work that crosses assertion and presupposition for the same information does so by researcher-constructing cleft/dialogue stimuli. Using those constructed counterparts would make the central contrast synthetic, exactly what the S0 gate forbids for a factorization topic.

The issue is not that the contrast cannot be written. The issue is that the title-level object lacks a natural row-level two-status substrate at scale.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** do not revive as at-issue vs backgrounded content, asserted vs taken-for-granted information, proposition vs discourse status, or by generating assertion counterparts to NOPE rows.

**Resurrection condition:** a released natural corpus with independently validated proposition-level content and discourse-status gold, containing useful numbers of the same/sufficiently matched propositions in both asserted and presupposed status without researcher-created central examples.

---

# 2. Polysemy ≠ Homonymy — KILL-NOVELTY

**Natural question:** Does a model distinguish one word with several related senses from one surface form that happens to denote unrelated meanings?

**Why it looked good:**

- `paper`-style related senses and `bank`-style unrelated lexical entries are a classic lexical-semantic distinction;
- mechanistic hypotheses such as shared-core representation versus separate lexical entries are natural.

**Kill evidence:**

The title-level lexical-ambiguity object is already occupied. Recent work studies layer-wise homonym representations in Llama/Qwen-style contextual models, and 2026 lexicographic work explicitly operationalizes the homonymy/polysemy distinction in LLM retrieval. A new project whose novelty is “now use causal patching/SAEs” would be the prohibited `existing scientific object → stronger MI` shape.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** do not revive as related-vs-unrelated senses, shared lexical core vs separate entries, homonym/polyseme geometry, or by switching languages/dictionaries.

**Resurrection condition:** a different lexical phenomenon with an independently established behavioral anomaly and competing internal mechanisms not reducible to the already-studied homonymy/polysemy organization question.

---

# 3. Coreference ≠ Bridging Reference — KILL-N0

**Natural question:** Referring to the same entity is not the same as referring to a different but associated entity (`I bought a house. The roof leaks.`). Does a model internally separate identity reference from associative bridging?

**Why it looked good:**

- GUMBridge provides thousands of natural bridging cases across genres;
- GUM-style annotation distinguishes identity coreference from bridging links in the same discourse ecosystem;
- the linguistic distinction is real and easy to explain.

**Kill evidence:**

The mother/data line itself defines **identity coreference versus associative bridging** as the core discourse-reference distinction. Recent representation work also analyzes ordinary coreference and bridging together. The remaining contribution would therefore be “take the mother’s two relation types and do causal MI,” not a new scientific object.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as same-entity vs associated-entity reference, identity vs part/whole reference, coreference vs associative anaphora, or by restricting to one bridging relation subtype.

**Resurrection condition:** a separate natural discourse phenomenon whose headline is not the coreference/bridging taxonomy and whose decisive behavior cannot be reduced to identifying one of those existing relation classes.

---

# 4. Prevalence ≠ Diagnosticity / Cue Validity — KILL-DATA

**Natural question:** A feature being common in a category, `P(feature | category)`, is not the same as that feature being diagnostic of the category, `P(category | feature)`. Does a model distinguish these two directions?

**Why it looked good:**

- the two conditional quantities are genuinely different;
- generic-language phenomena such as `Mosquitoes carry malaria` make the distinction intuitively interesting;
- small human norm studies directly measure prevalence and cue validity for the same category-feature items.

**Kill evidence:**

The direct human double-gold substrate found during this search is too small for a broad MI paper. Larger concept-property norms such as CSLB provide feature production frequency and feature distinctiveness, but **production frequency is not real-world prevalence**. Substituting accessibility/production frequency for prevalence would change the headline variable to a proxy. No sufficiently large public natural item-level source was found that directly grounds both `P(feature|category)` prevalence and `P(category|feature)` diagnosticity without constructing or inferring one axis.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** do not revive by treating feature-production frequency, corpus co-occurrence, association strength, feature distinctiveness, or an LLM-estimated prevalence as the missing real-world prevalence gold.

**Resurrection condition:** a large released concept-feature norm with independently elicited or objectively derived prevalence and diagnosticity/cue-validity values for the same items, with enough natural low/high cross-cells for the title-level claim.

---

# 5. Statistical Significance / Evidence Strength ≠ Effect Magnitude — KILL-MI-FIT

**Natural question:** Strong evidence that an effect is non-zero does not mean that the effect is large or practically important. Does a model confuse statistical evidence with magnitude?

**Why it looked good:**

- significance/evidence and effect magnitude are mathematically distinct;
- real research artifacts are available at scale rather than requiring synthetic statistics;
- BEAR publicly aggregates SCORE, OSC, Many Labs and other empirical datasets. For SCORE, BEAR documents 274 matched original/replication claims (267 retained) and 1,946 retained claim-level statistics, deriving a unified evidence statistic from z/t/coefficient-SE/F/CI/p information.

**Kill evidence:**

The available substrate does not by itself create a compelling mechanistic scientific object. If the model is shown an effect estimate and a p-value/standard error, separating “magnitude” from “evidence” can collapse into parsing two explicit numeric quantities. No broad, independently established open-model failure was found in which capable models systematically treat smaller p-values as larger/practically more important effects under ordinary scientific reasoning. Without such a behavioral phenomenon, MI would be method decoration around a textbook statistical distinction.

This topic therefore fails the project’s `why interpretability?` / surprise test rather than data availability.

**Death code:** `LOW_SURPRISE`

**Nearest-neighbor warning:** do not revive as p-value vs Cohen's d, statistical vs practical significance, evidence strength vs effect size, or by creating synthetic `n,d,p` factorial questions. A benchmark showing that the two numbers are decodable is not a scientific mechanism result.

**Resurrection condition:** a large, stable, multi-open-family natural behavior showing systematic significance-as-magnitude conflation despite adequate basic statistical capability, with a causal mechanism question that cannot be explained as mere number parsing.

**Useful substrate if that behavior ever appears:** https://github.com/wwiecek/BEAR and https://github.com/wwiecek/BEAR_data .

---

# 6. Knowing the Answer ≠ Knowing What a Novice Would Know — KILL-N0

**Natural question:** A model can solve a question itself yet fail to predict that a novice or weaker student would struggle with it. Why does its own competence contaminate simulation of a less-informed mind?

**Why it looked good:**

- this is an intuitive LLM analogue of the human `curse of knowledge`;
- ACL 2026 reports systematic human–AI difficulty misalignment over 20+ models and several domains;
- a separate ACL 2026 student-simulation paper reports high-capacity LMs overestimating low-ability students, while low-capacity models underestimate high-ability students;
- 2026 query-simulation work finds answer-side knowledge intrusion across 77,004 queries and eight LLMs.

**Kill evidence:**

The strongest mother already owns the title-level object. `Can LLMs Estimate Student Struggles?` explicitly separates **intrinsic problem-solving capability** from **human difficulty perception**, tests proficiency simulation, names the observed divergence a **Curse of Knowledge**, and concludes that high capability impedes faithful simulation of student limitations. `One LLM Does Not Simulate All Students` likewise frames ability-dependent simulation bias as its main phenomenon. A new paper that asks which layers/heads/SAE features cause this effect is therefore a direct behavior→mechanism follow-up, not a new scientific object under the repository’s N0 rule.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as expert-vs-novice simulation, own competence vs other competence, knowledge leakage into weaker personas, ability-state binding, or “curse of knowledge circuit” merely by adding causal tracing.

**Resurrection condition:** a qualitatively different natural less-informed-perspective phenomenon with a title-level behavioral distinction not already covered by human-difficulty prediction, proficiency simulation, false-belief tracking, or answer-side intrusion.

---

# 7. Claim Content ≠ Claim Scope — KILL-N0

**Natural question:** Preserving what a scientific study found is not enough if a summary silently drops who, where, or under what conditions the finding applies.

**Why it looked good:**

- scientific overgeneralization is natural and consequential;
- a 2025 Royal Society Open Science study compares 4,900 LLM summaries to source research and reports broad overgeneralization in modern models, including LLaMA 3.3 70B;
- an internal story about proposition content versus applicability/scope binding is mechanistically appealing.

**Kill evidence:**

The mother paper’s scientific object is already **scope preservation / overgeneralization**. It explicitly defines generalized versus restricted conclusions, measures when summaries broaden claim scope, and even studies prompt/temperature moderators. Recasting the same error as `content × scope binding` and adding patching would be exactly `mother behavior → mechanism`. No independent new scientific variable was introduced.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** do not revive as population-scope binding, qualifier dropping, applicability-condition representation, source-claim vs summary-claim scope, or scientific generalization circuit unless a new external behavioral object exists beyond the mother’s overgeneralization phenomenon.

**Resurrection condition:** a different scope-sensitive phenomenon with independent source-grounded axes and a headline not equivalent to “LLMs overgeneralize / drop qualifiers when summarizing.”

---

## Search lesson added by this batch

Two tempting but invalid rescue patterns appeared repeatedly:

```text
strong natural mother failure
→ rename an obvious component of that failure as an “internal object”
→ claim novelty because prior work did not patch it
```

and

```text
two mathematically/linguistically distinct variables
→ find a dataset containing both
→ assume hidden-state separation is automatically interesting
```

Under the current rules, neither is sufficient. The candidate must either own a new title-level scientific object or start from a natural model behavior whose mechanism itself poses genuinely competing scientific explanations.
