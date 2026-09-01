# Canonical Failure Index — Semantic Dedupe Memory

**Updated:** 2026-09-01  
**Purpose:** prevent repeated literature search, implementation effort, and GPU use on scientific questions already seriously audited.

> This is a **semantic dedupe index**, not a brainstorm source. Do not generate new candidates by negating or recombining entries below.

## Mandatory use before HARD AUDIT

For every serious candidate:

1. state the one-sentence scientific object;
2. generate 5–10 semantic aliases;
3. search this index + `rejected_candidates/` + `archive/`;
4. if it belongs to a killed cluster, treat it as **dead by default**;
5. reopen only with genuinely new evidence satisfying the recorded resurrection condition.

Changing model family, dataset, prompt, language, subset, probe, SAE, steering, patching method, or layer does **not** create a new scientific object.

---

# A. Entity / identity / social-property cluster

## A1. Real vs fictional / ontological status

**Occupied externally.** Hamdi-style real-vs-imaginary entity status is not available to copy.

Aliases: real/fictional, real/imaginary, existence status, ontology vs familiarity.

## A2. Ownership vs current possession/use

**KILL-NOVELTY.** 2026 dynamic-world/RLVR work explicitly factorizes `(owner, possessor, integrity)`; loan/return separate possession from ownership.

Do not revive as borrowing semantics, owner/possessor subspaces, or state tracking.

## A3. Authority/rank vs expertise/competence

**KILL-NOVELTY.** 2026 mechanistic authority/sycophancy work explicitly distinguishes institutional authority from competence and tests expertise framing.

Record: `formal_authority_vs_epistemic_expertise_collision_2026-09-01.md`.

## A4. Enduring social role/office vs current occupant

**KILL-NOVELTY.** Temporal-KG/EvolveBench-style work already treats president/CEO/chairperson/position-held as time-varying relations; modern binding/retrieval work owns relation→occupant binding mechanisms.

Record: `enduring_role_vs_current_occupant_binding_collision_2026-09-01.md`.

## A5. Ascribed vs achieved social role

**KILL-DATA / KILL-SCALE.** Granularity-Axis public role inventory is too skewed toward institutional/achieved roles; a clean cross requires manufacturing a new synthetic inventory.

## A6. Numerical identity vs qualitative/type sameness — LIVE OVERRIDE

**NOT A REJECTION. ACTIVE 040 PASS-REGISTER.**

Frozen object:

> being literally the same individual vs merely being the same kind / qualitatively identical.

Why this is not killed by generic entity tracking:

- human science supplies an independent identity distinction and natural cross-cases;
- Davis–Altmann 2021 RNN event sensitivity is a serious precursor but not the full abstract causal object;
- modern binding/tracking work starts largely after individuation is supplied;
- 040 must show cross-surface abstraction and identity-specific causal history transfer while preserving type knowledge.

Do not use this index to kill 040 merely because `entity tracking`, `coreference`, or `binding` appears nearby. Read `active/040_numerical_identity_vs_qualitative_sameness/README.md`.

## A7. Natural kind vs artifact / function-material-appearance essentialism

**KILL-NOVELTY.** Cognitive Science 2023 directly compares function/telos, material, appearance and natural/artifact domains in LLM categorization.

Record: `essentialist_function_material_appearance_2026-09-01.md`.

## A8. Life-status / alive-vs-dead as entity attribute

**DO NOT PROMOTE WITHOUT A DISTINCT OBJECT.** Generic entity→attribute factual retrieval and biographical datasets already cover birth/death facts. `alive/dead` alone risks being merely another factual attribute.

---

# B. Semantic / lexical relation cluster

## B1. Taxonomic `same kind` vs thematic `go together`

**KILL-NOVELTY / former 039 archived.** Same TxThm norms and distinction already appear in LM representation/behavior work; remaining delta became stronger MI.

Record: `taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`.

## B2. Whole-part / meronymy vs kind-of / taxonomy

**KILL-NOVELTY.** Dedicated LLM part-whole work and semantic-relation MI already occupy the object.

## B3. Metonymic literal denotation vs transferred referent

**KILL-NOVELTY.** Contextual Transformer work, NAACL 2025 and LREC 2026 already study metonymic meaning shift/resolution/referential transfer.

Record: `metonymic_referential_transfer_representation_collision_2026-09-01.md`.

## B4. Relative vs absolute gradable adjective thresholds

**KILL-NOVELTY.** AAAI 2023 Adjective Scale Probe explicitly treats relative, minimum-absolute and maximum-absolute adjectives and their context/entailment behavior.

Record: `relative_vs_absolute_gradable_threshold_computation_collision_2026-09-01.md`.

## B5. Canonical/telic function vs ad-hoc affordance/use

**KILL-NOVELTY.** Lexical coercion/telic-default work plus modern context-sensitive affordance work already owns default purpose vs context-induced use.

## B6. Habitual/dispositional vs episodic/current state

**KILL-NOVELTY.** TACL 2019 and SitEnt/DiSCo already treat habitual vs episodic as contextual LM semantic properties.

Record: `habitual_vs_episodic_event_representation_collision_2026-09-01.md`.

## B7. Cardinal quantity vs ordinal position

**KILL-NOVELTY.** ACL 2026 number/ordinal geometry and 2026 ordinal activation-patching work occupy the object.

Record: `cardinal_vs_ordinal_number_representation_collision_2026-09-01.md`.

## B8. Regular polysemy / shared generative structure

**KILL-NOVELTY.** Already terminal in earlier search; do not revive with newer models or MI.

## B9. Sound symbolism / sublexical phonology vs distributional association

**KILL-NOVELTY.** Earlier audit found direct ownership/crowding. Do not reopen as phonological latent direction.

## B10. Mass/count grammar vs conceptual individuation / object-substance construal

**KILL-NOVELTY / N0-N2.** The attractive axis is real, but older neural and contextual-representation work already directly studies it.

Aliases: mass vs count, grammatical countability, conceptual individuation, object vs substance construal, object-mass nouns, nominal coercion, mass-to-count/count-to-mass coercion, mass/count syntax-semantics interface.

Decisive warning:

- Kulkarni, Treves & Rothstein (2020), *Can mass-count syntax be derived from semantics?*, directly frames the relation between mass/count syntactic use and semantic classes and tests it with a neural model;
- Liu & Chersoni (CogALex 2022) studies nominal coercion in static/contextual embeddings including BERT.

Modern Llama/Qwen + SAE/probe/patching does not create a fresh object.

Record: `mass_count_grammar_vs_conceptual_individuation_collision_2026-09-01.md`.

---

# C. Epistemic / belief / uncertainty cluster

## C1. Ambiguity vs ignorance / aleatoric vs epistemic uncertainty

**KILL-NOVELTY.** ICML 2024 + AAAI 2026 + ACL 2026 and related work directly decompose ambiguity/input uncertainty from knowledge gaps, including internal representations.

Record: `ambiguity_vs_ignorance_uncertainty_2026-09-01.md`.

## C2. Risk vs ambiguity / known vs unknown probabilities

**KILL-NOVELTY.** Modern open-model Ellsberg/ambiguity-aversion work already includes internal steering/intervention.

Record: `risk_vs_ambiguity_decision_state_collision_2026-09-01.md`.

## C3. Speaker commitment / factivity / projection

**KILL-NOVELTY.** NAACL 2025 directly studies projection and speaker-belief commitment, including representation questions.

## C4. Evidential source type / direct vs hearsay vs inference

**KILL-NOVELTY.** ACL 2026 and contemporaneous work separate evidentiality from epistemic stance in Llama/Qwen/Gemma.

## C5. Knowledge vs justified true belief / Gettier

**KILL-NOVELTY.** 2026 machine experimental-philosophy work directly studies LLM Gettier intuitions and underlying knowledge/belief interpretation.

Record: `gettier_knowledge_vs_justified_true_belief_collision_2026-09-01.md`.

## C6. De re vs de dicto / referential opacity

**KILL-NOVELTY.** SCiL 2023 directly asks whether neural models understand de re/de dicto; TACL 2023 uses referential opacity as a core semantic object.

Record: `de_re_vs_de_dicto_attitude_opacity_collision_2026-09-01.md`.

## C7. Use vs mention / asserted vs quoted

**KILL-NOVELTY.** Dedicated LLM use–mention work owns the object.

## C8. Self-generated vs user-provided source/authorship

**KILL-NOVELTY.** ICLR 2025 self-authorship residual vectors + causal steering and 2026 self-recognition/role-tag work directly occupy this object.

---

# D. Agent / action / planning / tool cluster

## D1. Desire vs intention

**KILL-NOVELTY.** Findings ACL 2025 directly studies belief/desire/intention representations in open-source LLaMA agents.

Record: `desire_vs_intention_mental_state_representation_collision_2026-09-01.md`.

## D2. Goal vs subgoal / terminal vs intermediate

**KILL-SCALE / KILL-BEHAVIOR.** Clean hierarchy needs synthetic task construction and risks becoming a planning-state probe.

## D3. Action precondition vs effect

**KILL-NOVELTY.** Modern action/world-model work already owns preconditions/effects as explicit state variables.

## D4. Hard constraints vs soft preferences

**KILL-NOVELTY.** Modern LLM planning work already studies validity constraints vs ranking preferences.

## D5. Tool semantic relevance vs operational availability

**KILL-NOVELTY.** ACL 2026 owns irrelevance; FAIL-TaLMs/CAR-bench/AdaPlanBench-style work owns unavailable/missing/unsupported capability. Crossing occupied axes is not a new object.

Record: `tool_relevance_vs_operational_availability_collision_2026-09-01.md`.

## D6. Tool necessity vs usefulness/relevance

**KILL-NOVELTY.** 2026 When2Tool/model-adaptive necessity/metacognitive tool-use work decodes or steers need-to-call signals.

## D7. Explore vs exploit / commitment mode

**KILL-NOVELTY.** Recent 2026 work already studies exploration/exploitation behavior and hidden adaptive exploration; irreversibility/commitment also has direct causal work.

## D8. Same-label entity tracking as a generic topic

**OCCUPIED, but does not automatically kill 040.** Modern entity-tracking work covers binding/state propagation and same-label stress tests. Do not propose a generic `same label confusion mechanism` paper.

---

# E. Cognitive bias / decision / moral cluster

## E1. Choice-supportive bias: memory distortion vs evaluative reweighting

**KILL-NOVELTY.** AAAI 2025 mother explicitly separates memory-based and memory-independent evaluation-based bias.

Record: `choice_supportive_memory_vs_evaluation_locus_collision_2026-09-01.md`.

## E2. Typicality vs frequency/commonness

**KILL-NOVELTY.** Modern LM typicality work occupies the conceptual axis.

## E3. Descriptive/statistical norm vs prescriptive/ideal norm

**KILL-NOVELTY.** ACL 2025 Best Paper explicitly decomposes LLM sampling/prototypes into descriptive and prescriptive components.

## E4. Cause vs enabling condition / fine-grained causal role

**KILL-NOVELTY.** Fine-grained causal NLP already labels/models cause, enable, prevent, correlate etc.

## E5. Intentional lie vs honest error

**KILL-NOVELTY.** 2026 RIFT controls wrongness and studies deception-vs-error internal signatures.

## E6. Self-consistency / high agreement vs true confidence / false consensus

**KILL-NOVELTY.** 2026 work directly distinguishes correct and false high-agreement consensus using hidden-state consistency in Qwen and audits self-agreement as confidence.

Record: `self_consistency_false_consensus_confidence_collision_2026-09-01.md`.

## E7. Common/average vs normal/acceptable; descriptive stereotype vs prescriptive norm

See E3. Do not rename and revive.

## E8. Means vs side effect / instrumental vs incidental harm

**KILL-NOVELTY for the simple object.** Means/side-effect is already an explicit LLM moral factor in MoCa and procedural dilemma work such as OffTheRails.

Aliases: means vs side effect, means vs byproduct, instrumental vs incidental harm, necessary means vs foreseen consequence, Doctrine of Double Effect, causal role of harm, means principle.

A stronger independent human theory question exists — direct moral-rule computation vs mediation through intentional attribution — but it is **not GPU-authorized** here because the exact theory-diagnostic means/side-effect phenotype is not frozen on an analyzable modern open checkpoint. Searching models/prompts until it appears would be behavior lottery.

Record: `means_vs_side_effect_moral_role_collision_2026-09-01.md`.

---

# F. Event / temporal / discourse / reference cluster

## F1. Event completion / imperfective paradox / culmination

**KILL-NOVELTY / KILL-SUBSTRATE.** ACL 2026 studies progressive→culmination and internal representations; later work questions benchmark interpretation.

## F2. Attempted/intended event vs realized event

**KILL-NOVELTY.** Event factuality / implicativity already owns fact/possibility/impossibility as LLM objects.

## F3. Temporal order / duration / distance / interval / reference frames

**CROWDED.** 2024–2026 temporal-representation work covers these. Do not build a new internal-axis paper absent a genuinely independent object.

## F4. Collective vs distributive plurality

**HARD LEAD / NOT REGISTERED.** Natural object and UDS-EventStructure substrate exist, but 2025 plural interpretive-bias behavior + earlier distributivity probing reduce novelty; ambiguity-vs-underspecification version overlaps active 038 in architecture shape.

## F5. Focus vs background / information structure

**HARD LEAD / NOT REGISTERED.** Mature linguistic object; current blocker is insufficient verified modern-open paired phenotype/artifact. Route C rules do not require an exact published phenotype in principle, but a concrete deterministic substrate + causal-use path still need hard audit before promotion.

## F6. Unresolved reference alternatives vs underspecification

**ACTIVE 038 PASS.** Not a rejection. Do not create near-duplicate ambiguity-architecture topics.

## F7. Context-conditioned modifier set restriction — LIVE OVERRIDE

**NOT A REJECTION. ACTIVE 041 PASS-REGISTER.**

Frozen object:

> whether a modifier actually reduces the currently live referent set, separately from the modifier's ordinary property meaning.

Do **not** kill 041 merely because old reference-resolution/pragmatic work studies distractors, informative adjectives, candidate elimination or redundant modifiers. Those are explicitly conceded neighbors.

041 survives only at the stronger object level:

> an abstract, reusable, context-conditioned modifier-role state in a pretrained AR LLM, cross-lexical/domain/surface and causally used for referent narrowing while preserving property truth.

The decisive microscope keeps the same world, target, target phrase and modifier truths fixed while swapping only the live candidate set, causing which modifier actually rules out an alternative to swap.

Hard kill if the signal reduces to raw scene facts, active-candidate identity, lexical position, salience, generic reference competence, or merely `informative > redundant` behavior.

Read `active/041_contextual_set_restriction/README.md` before claiming a collision.

---

# G. Figurative-language cluster

## G1. Generic literal vs figurative metaphor mechanism

**CROWDED / KILLED variants.** Do not revive generic literal-vs-figurative, lexical-anchor, aptness-only, or metaphor-vs-simile representation topics.

## G2. 036 conventionality vs aptness selecting comparison vs categorization

**LIVE HARD AUDIT / NOT PASS / GPU PAUSED.** Exact selector question survives, but former metric is underidentified. Reauthorization requires two independent theory-grounded route signatures, including one not defined by metaphor-vs-simile form.

## G3. Metonymy

See B3.

## G4. Idiom literal/figurative competition

**KILL-NOVELTY.** EACL 2026 causal work already studies parallel literal/figurative pathways.

---

# H. Other canonical deaths from earlier search

Do not revive without explicit resurrection evidence:

- agreement attraction encoding vs retrieval — behavior weak / similarity-interference collision risk;
- proactive interference encoding vs retrieval — novelty collision;
- implicit-causality production vs comprehension sharing — behavior/N2 unsafe;
- thematic fit / generalized event schema — novelty;
- shared semantic-frame state across frame ID and thematic fit — novelty + behavior;
- literal semantics vs pragmatic enrichment — PaCE/dual-pathway collision;
- analogy relational structure vs surface similarity — novelty;
- verbatim vs gist memory traces — novelty;
- monotonicity shared computation — novelty;
- negation suppression vs constructive representation — novelty;
- linguistic convergence priming vs audience design — novelty/data;
- good-enough syntax–semantic arbitration;
- belief bias;
- idiom literal/figurative architecture;
- anchoring;
- false premise / Moses illusion;
- reflexive attraction;
- depth-charge illusion;
- earlier 004/005/006-style failed phenomena logged in their existing records.

Use exact individual rejection records for decisive evidence and resurrection conditions.

---

# I. General dedupe lessons

## I1. Object ownership, not title ownership

Read methods, factors, appendices and discussion. A paper with an unrelated headline may still own the exact object.

## I2. A new 2×2 is not automatically a new object

Crossing two already-established axes is usually not enough.

## I3. Strong human theory does not rescue an occupied neural/LLM object

Gettier, risk-vs-ambiguity, de re/de dicto, habituality, scalar adjectives, means-vs-side-effect etc. remain scientifically real but are not fresh once neural/LLM work owns them.

## I4. Route C does NOT require an exact modern-open published phenotype

The obsolete over-strict rule is removed. A deterministic natural semantic/cognitive axis with real external substrate can enter HARD AUDIT and then a frozen cheap S0.

But GPU may not be used to discover whether the topic should be renamed after the fact.

040 and 041 are canonical live examples.

## I5. Generic mechanism occupation can kill special cases

If the contribution is only applying a known generic binding/retrieval/uncertainty/reference mechanism to a new label, N2 may still fail.

041 therefore dies if its result is merely generic referent elimination or modifier informativeness, just as 040 dies if it is merely generic coreference/entity tracking.

## I6. Failure logging is mandatory

Every seriously audited death gets an individual rejection record with aliases, decisive evidence, nearest-neighbor warning and resurrection condition. This index is only the fast semantic lookup layer.

---

# Current live boundary

```yaml
PASS_REGISTER:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction

HARD_AUDIT_NOT_REGISTERED:
  - 036_metaphor_processing_route_selection

HARD_LEADS_NOT_REGISTERED:
  - focus_vs_background_information_structure
  - collective_vs_distributive_plurality

TARGET: 5
CURRENT_PASS: 5
REMAINING: 0
SEARCH_STATUS: TARGET_REACHED_STOP_BY_DEFAULT
```

> **Before spending literature time or GPU, semantic-dedupe the scientific object here first. The fresh target is now 5/5; count never protects a topic from new fatal evidence.**
