# Rejected Candidates — Semantic / Pragmatic Factorization

**Domain:** semantic, pragmatic, discourse, lexical-conceptual and referential factorization topics considered under the Hamdi-style natural-question → S0 → N0 → N1 funnel.  
**Status:** negative-memory ledger, 2026-08-31.  
**Rule:** these entries are scientific-object deaths, not merely dataset failures. Do not revive them by changing model, benchmark, language, prompt, or MI tool unless the stated resurrection condition is genuinely met.

---

# 1. Speaker Intent ≠ Listener Perception in Sarcasm

**Natural question:** A speaker can intend sarcasm without a listener recognizing it, and a listener can hear sarcasm where none was intended. Do language models internally separate communicative intention from perceived sarcastic force?

**Why it initially looked good:**

- the two variables are genuinely distinct in human communication;
- iSarcasm-style resources provide unusually clean author-side labels and observer-side perception judgments;
- the natural 2×2 contains both communication-failure directions rather than only aligned cases.

**Kill evidence:**

The scientific object itself is already a headline object in prior work. The 2025 IWCS paper **The Difficult Case of Intended and Perceived Sarcasm** directly studies intended sarcasm versus perceived sarcasm and reports that generative language models differ depending on speaker vs observer perspective. A new project that merely changes the measurement from behavior to hidden-state factorization would therefore be exactly the prohibited shape “existing object/behavior → we do mechanism.”

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as “speaker sarcasm vs observer sarcasm,” “intended vs detected irony,” “author intent vs reader interpretation,” or by restricting to one sarcasm subtype. The title-level object is already owned.

**Resurrection condition:** Only a different pragmatic variable, independently defined and not already part of the intended/perceived sarcasm literature, with its own natural cross-population and new scientific question.

---

# 2. Literal Meaning ≠ Intended / Figurative Meaning

**Natural question:** When a sentence has a literal interpretation and a figurative or intended interpretation, does a language model keep both meanings separately or overwrite one with the other?

**Why it initially looked good:**

- ordinary examples are immediate (idioms, sarcasm, metaphor);
- the competing mechanisms are natural: parallel interpretations, literal-first overwrite, contextual selector;
- author-provided paraphrases in sarcasm resources appeared to offer clean intended-meaning targets.

**Kill evidence:**

The mechanism arc is already occupied. EACL 2026 work on idiom processing uses causal tracing / intervention to study literal versus figurative pathways and reports parallel maintenance / competition between interpretations. ACL 2026 sarcasm-mechanism work also analyzes hidden-state geometry and causal intervention for organic vs synthetic sarcasm and pragmatic cues. The remaining novelty would have to narrow to a particular figurative subtype or author-rephrased corpus.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as literal-vs-figurative idioms, literal-vs-sarcastic meaning, metaphor-literal competition, or “which layer switches interpretation.” Those are direct mechanism-followup shapes.

**Resurrection condition:** A different meaning dimension with an independently grounded target and a decisive contrast not reducible to literal/figurative competition or contextual interpretation selection.

---

# 3. What Is Said ≠ What Is Implicated

**Natural question:** Does a model distinguish what a speaker literally says from what the listener is pragmatically expected to infer?

**Why it initially looked good:**

- this is a foundational semantic/pragmatic distinction independent of any benchmark;
- conversational implicature is naturally occurring;
- mechanistic forks are strong: literal proposition + separate implicature, implicature overwrite, or contextual readout.

**Kill evidence:**

S0 failed. Public natural conversational-implicature corpora provide human judgments about inferred implicatures, but not an equally reliable, row-aligned, independently authored **literal/what-is-said target** for the same natural units. Conversational implicature also exhibits substantial human interpretive variation. Repairing the substrate would require researcher-written literal paraphrases, controlled scalar templates, or LLM-generated central targets, reproducing the exact failure mode of 027 `Rhetorical Force ≠ Implied Assertion`.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** Do not revive as “literal content vs implicature,” “said vs meant,” “explicit vs implicit proposition,” scalar-implicature-only, or indirect-answer-only by generating the missing literal side ourselves.

**Resurrection condition:** A released natural corpus in which the same rows have independently validated source/human gold for both literal propositional content and implicated content at useful scale.

---

# 4. Emotion ≠ Emotion Cause

**Natural question:** Knowing what someone feels is not the same as knowing why they feel it. Does a language model encode affective state and causal attribution separately?

**Why it initially looked good:**

- the two variables are naturally distinct;
- emotion-cause corpora provide human labels;
- the mechanistic question could have separated affect state from causal-event binding.

**Kill evidence:**

Recent work already occupies the internal-factorization story. Findings ACL 2026 explicitly proposes disentangling emotion-oriented semantics and cause-oriented semantics into complementary representation spaces, while Findings ACL 2025 mechanistic work localizes emotion inference and causally manipulates appraisal concepts. A new LLM paper would be reduced to applying newer MI tools to an already explicit representation-separation object.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as emotion-vs-cause, affect-vs-trigger, appraisal-vs-feeling, or emotion-cause-pair “disentanglement” with a different corpus/model.

**Resurrection condition:** A distinct affective scientific object whose competing mechanisms make predictions not captured by emotion/cause semantic decoupling or appraisal-based emotion inference.

---

# 5. Communicative Act ≠ Affect

**Natural question:** What an utterance is doing in a conversation (question, request, inform, directive) is not the same as the speaker’s emotion. Does a language model keep dialogue function and affect separate?

**Why it initially looked good:**

- DailyDialog provides the same utterances with human dialogue-act and emotion labels;
- both dimensions are meaningful without the dataset;
- cross-cells occur naturally.

**Kill evidence:**

The object is too close to a long-standing joint-modeling problem. Dialogue-act + sentiment/emotion multi-task and shared-vs-task-specific representation work has existed since at least ACL-era pre-LLM neural dialogue modeling and continues in later joint architectures. The only obvious remaining claim is “pretrained LLM internals factorize the two and we causally patch them,” which fails N0 because the scientific object is inherited from the established joint task rather than newly identified.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as intent-vs-emotion, dialogue-function-vs-sentiment, speech-act-vs-affect, or by swapping DailyDialog for another dialogue corpus.

**Resurrection condition:** A natural discourse phenomenon where function and affect interact in a surprising way that is itself not the existing joint-label problem, and whose mechanism has competing causal explanations.

---

# 6. Definiteness ≠ Specificity

**Natural question:** “Can the hearer identify which referent I mean?” and “Do I, the speaker, have one particular referent in mind?” are different referential properties. Does a model separate definiteness from specificity?

**Why it initially looked good:**

- this is a classic linguistic distinction;
- BCCWJ-InfoSt publicly provides row-level natural Japanese NP annotations for both definiteness and specificity, avoiding English article-token shortcuts;
- annotator agreement is high.

**Kill evidence:**

S0 decisive cross-cells fail in the natural corpus. The published BCCWJ-InfoSt contingency counts are:

- definite + specific: **1120**
- indefinite + specific: **36**
- indefinite + non-specific: **749**
- definite + non-specific: **0**

The required 2×2 therefore does not naturally exist in this substrate. Filling the missing cell with constructed examples would convert a natural factorization question into a synthetic protocol and violate the S0 gate.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** Do not revive by generating definite-but-nonspecific examples, restricting to one determiner construction, switching only to English `a/the`, or replacing specificity with a proxy such as givenness.

**Resurrection condition:** A natural, accessible corpus with independent definiteness and specificity gold and nontrivial counts in all decisive cells, without hand-created central examples.

**Source artifact:** https://github.com/masayu-a/BCCWJ-Infostr

---

# 7. Taxonomic ≠ Thematic Semantic Relations

**Natural question:** `dog–wolf` are related because they are the same kind of thing; `dog–leash` are related because they belong in the same situation. Does a model organize these two kinds of semantic relatedness separately?

**Why it initially looked good:**

- the distinction is classic in human semantic memory;
- an unusually strong public norm contains the **same 659 word pairs** independently rated for taxonomic similarity and thematic relatedness, with individual human judgments;
- S0 substrate is substantially cleaner than most factorization candidates.

**Kill evidence:**

N1 / internal-history collision is too strong. Earlier contextual-embedding work has already asked whether taxonomic and thematic information occupy separable representational containers, and 2026 LLM semantic-relation work uses probes, SAEs and activation patching to causally analyze relation representations. The repository’s W41 already freezes the rule that “swap in another semantic relation inventory” is not enough after direct semantic-relation MI work. The remaining novelty would be essentially one special relation pair inside an occupied object family.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as category-vs-event relation, feature-based-vs-situation-based semantics, same-kind-vs-same-scene, or by changing the semantic norm/model family.

**Resurrection condition:** A semantic organization principle with a new external variable and causal prediction not subsumed by relation-representation / semantic-geometry work; not simply another pair of relation labels.

---

# 8. Animacy ≠ Agentivity

**Natural question:** What an entity *is* (animate/inanimate) is not identical to what role it plays in an event (agent/non-agent). Does a model keep entity ontology and event role separate?

**Why it initially looked good:**

- ontology and event role are conceptually distinct;
- recent mechanistic work has established animacy as a real causal object in language-model syntax;
- BCCWJ-InfoSt annotates animacy and agentivity on the same natural NPs.

**Kill evidence:**

The candidate fails the strict substrate/object test in its proposed form. BCCWJ-InfoSt’s agentivity annotation operationalizes an intentional actor-like property, so the hoped-for “inanimate but agentive” examples such as storms causing destruction are not valid positive agentivity gold under the corpus ontology. More broadly, recent linguistic/MI work treats animacy as a strong proto-agent cue while separate semantic-role-circuit work already studies agent/theme representations. The proposed 2×2 therefore either collapses under the available human annotation or becomes an artificial construction designed to force an orthogonal cell.

**Death code:** `ARTIFACT_FAILURE`

**Nearest-neighbor warning:** Do not revive as alive-vs-agentive, animacy-vs-semantic-role, ontology-vs-proto-agent, or by hand-labeling inanimate causes as “agents.” Do not use syntactic subjecthood as an agentivity proxy.

**Resurrection condition:** A natural corpus with independently annotated entity-level animacy and event-level semantic agency where all decisive cross-cells are genuinely present at scale, plus an N1 audit showing the title is not already absorbed by animacy and semantic-role mechanism work.

---

# 9. Agency ≠ Experience / Sentience

**Natural question:** An entity can be capable of acting without being capable of feeling, and vice versa. Do language models separately represent agency and subjective experience?

**Why it initially looked good:**

- classic two-dimensional mind-perception distinction;
- real entities/robots can populate the cross-cells;
- human rating resources exist.

**Kill evidence:**

A direct mechanistic project already applies the classic Gray-style **Agency / Experience** two-axis framework to language-model hidden states, including representational analysis and causal steering across modern open model families. That occupies the exact factorization object and the intervention story.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as agency-vs-sentience, competence-vs-feeling, mind-perception axes, robot agency-vs-experience, or “does the LLM have orthogonal mind dimensions?”

**Resurrection condition:** A genuinely different ontology of mental-state attribution with independent external gold and predictions not reducible to Agency/Experience.

---

# 10. Local Accessibility / Givenness ≠ Global Discourse Salience

**Natural question:** An entity can be easy to refer back to because it was just mentioned without being important to the whole document; conversely, a globally important entity need not be the most locally accessible at every point. Does a model separate local discourse accessibility from global entity importance?

**Why it initially looked good:**

- the distinction is linguistically natural and understandable without a dataset;
- GUM provides rich information-status labels, while GUMsley provides human summary-grounded entity salience annotations across many genres;
- the same corpus family appeared to offer row-level natural coverage rather than synthetic pairs.

**Kill evidence:**

N0 fails because the headline scientific object is already directly studied by 2026 discourse-salience work. **What makes an entity salient in discourse? Local and global prominence factors across genres** explicitly asks how local prominence/accessibility factors such as givenness, definiteness, subjecthood, mention frequency and related cues account for global discourse salience across a broad multi-genre corpus. A new project that changes the measurement to hidden-state factorization would therefore inherit the mother’s object and only add MI methodology.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Do not revive as givenness-vs-salience, accessibility-vs-importance, local-vs-global entity priority, recent-mention-vs-summary-worthiness, or by using another GUM layer/model. Those are the same scientific contrast.

**Resurrection condition:** A different discourse variable with a title-level distinction not already framed as a local-vs-global salience problem in the discourse literature, and with independent natural gold.

---

# Current non-rejected neighbors

The following ideas were discussed in the same search but are **not** killed by this file and must remain separate from the negative memory:

- **Assertion ≠ Presupposition** — still under S0/N0/N1 audit; do not mark dead merely because W13 killed a *failure-mechanism* presupposition-projection effect.
- **Prevalence ≠ Diagnosticity / Cue Validity** — substrate scale remains under audit; not yet adjudicated.
- **Coreference ≠ bridging reference** — high N0 risk and not currently shortlisted, but not formally killed here until the mother-inclusion audit is complete.

---

# Cross-cutting lesson from this domain

The main failure mode is now clear:

```text
linguistics gives two clean labels
+ a corpus contains both
→ temptation: call their hidden-state separation a new MI paper
```

That is not enough. A valid Hamdi-style topic still needs a **new scientific object** after N0/N1. If prior work already treats the two labels as the conceptual contrast, then “we probe/patch/steer them in an LLM” is normally a mechanism follow-up, not a new title-level question.
