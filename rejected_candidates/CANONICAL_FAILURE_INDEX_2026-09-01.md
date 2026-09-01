# Canonical Failure Index — Semantic Dedupe Memory

**Updated:** 2026-09-01  
**Purpose:** prevent repeated literature search, implementation effort, and GPU use on scientific questions that have already been seriously audited and rejected.

> This file is a **semantic dedupe index**, not a brainstorm source. Do not generate new candidates by negating or recombining entries below.

## Mandatory use before HARD AUDIT

For every new serious candidate:

1. state the one-sentence scientific object;
2. generate 5–10 semantic aliases;
3. search this index + `rejected_candidates/` + `archive/`;
4. if the candidate belongs to an existing cluster, treat it as **dead by default**;
5. reopen only if the specific resurrection condition is satisfied by genuinely new evidence.

Changing model family, benchmark, prompt, language, subset, probe, SAE, steering, patching method, or layer does **not** create a new scientific object.

---

# A. Entity / identity / social-property cluster

## A1. Real vs fictional / ontological status

**Status:** occupied externally / do not copy Hamdi object.

Canonical object: familiarity/knowledge of an entity is distinct from whether the entity is real or fictional.

Do not revive as real-vs-imaginary direction, existence steering, historical-vs-fictional entity status, or ontology-vs-familiarity.

## A2. Ownership vs current possession/use

**Status:** `KILL-NOVELTY`.

Canonical object: owner identity is distinct from who currently possesses/uses the object.

Fatal evidence: 2026 dynamic-world/RLVR work explicitly factorizes world state into independent `(owner, possessor, integrity)` slots; loan/return change possession without ownership while gift/sale change ownership.

Do not revive as owner/possessor subspaces, loan-vs-gift state tracking, possession/ownership patching, or borrowing semantics.

## A3. Formal authority / rank vs epistemic expertise / competence

**Status:** `KILL-NOVELTY`.

Canonical object: having institutional power is distinct from actually knowing the domain.

Fatal evidence: strongest 2026 mechanistic authority/sycophancy neighbors explicitly distinguish competence-defined expertise from socially recognized institutional authority and directly test expertise framing.

Record: `formal_authority_vs_epistemic_expertise_collision_2026-09-01.md`.

Do not revive as rank-vs-competence direction, expert-low-rank vs novice-high-rank 2×2, source credibility, or authority/expertise double dissociation.

## A4. Enduring social role / office vs current occupant

**Status:** `KILL-NOVELTY`.

Canonical object: an office such as `president` persists while its time-indexed occupant changes.

Fatal evidence: TempLAMA/EvolveBench/2026 temporal-KG work already treats president/CEO/chairperson/position-held as time-varying relations; modern mechanistic work already owns relation/entity binding and subject→relation→object factual retrieval.

Record: `enduring_role_vs_current_occupant_binding_collision_2026-09-01.md`.

Do not revive as officeholder slot, incumbent replacement, role-filler binding, presidency-vs-president, or time-indexed role cells.

## A5. Ascribed vs achieved social status/role

**Status:** `KILL-DATA / KILL-SCALE`.

Canonical object: roles assigned by birth/status vs acquired through achievement/action.

Fatal issue: the Granularity-Axis mother inventory is heavily skewed toward institutional/achieved roles and does not provide a natural balanced cross of ascribed/achieved × granularity. Continuing requires manufacturing a new synthetic role inventory and then discovering behavior by GPU.

Do not revive by hand-labeling the existing role list or creating an ad-hoc 2×2.

## A6. Numerical identity / same token vs qualitative similarity / same type

**Status:** HARD-REJECT FAMILY unless a genuinely distinct substrate appears.

Canonical object: `the same object` is different from `an exactly similar object`.

Risk: broad entity identity, entity matching, coreference, and entity-tracking mechanisms are already heavily occupied. A viable revival must demonstrate a scientific object and task not reducible to tracking/matching entities or comparing properties.

## A7. Natural kind vs artifact / function-material-appearance essentialism

**Status:** `KILL-NOVELTY`.

Canonical object: what determines category identity for natural kinds/artifacts; purpose/function vs material/appearance.

Fatal evidence: Cognitive Science 2023 directly applies transformation-task essentialism to LLMs and compares function, material, appearance, and living/non-living/artifact domains.

Record: `essentialist_function_material_appearance_2026-09-01.md`.

Do not revive as telos, artifact essence, natural-vs-artificial ontology, or function-over-appearance hidden states.

---

# B. Semantic relation / lexical-semantic cluster

## B1. Taxonomic `same kind` vs thematic `go together`

**Status:** `KILL-NOVELTY / former 039 archived`.

Canonical object: taxonomic and thematic relatedness as distinct semantic relation types.

Fatal evidence: the same 659-pair TxThm norms and taxonomic/thematic distinction are already used directly in language-model representation/behavior studies; modern LLMs already perform taxonomic-vs-thematic choices. Remaining delta was mostly hidden-state/causal mechanization.

Record: `taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`.

Canonical lesson: **object ownership, not title ownership**.

## B2. Whole-part / meronymy vs kind-of / taxonomy

**Status:** `KILL-NOVELTY`.

Canonical object: part-of relation versus is-a/category relation.

Fatal evidence: dedicated LLM part-whole semantic competence work already includes behavior, probability, and representation analysis; LREC 2026 semantic-relation work already uses probe/SAE/activation patching.

Do not revive as meronymy direction, part-of vs is-a patching, or relation-type steering.

## B3. Metonymic literal denotation vs transferred referent

**Status:** `KILL-NOVELTY`.

Canonical object: `White House -> institution`, container-for-content, producer-for-product, etc.

Fatal evidence: COLING 2020 directly studies metonymic meaning shift in contextual Transformer representations; NAACL 2025 owns literal/metonymic LLM resolution; LREC 2026 extends to semantic coreference/referential transfer.

Record: `metonymic_referential_transfer_representation_collision_2026-09-01.md`.

## B4. Relative vs absolute gradable adjective thresholds

**Status:** `KILL-NOVELTY`.

Canonical object: context-derived standards (`tall`) versus minimum/maximum endpoint standards (`wet`, `straight`, `full`).

Fatal evidence: AAAI 2023 Adjective Scale Probe explicitly treats relative, minimum-absolute, and maximum-absolute adjectives as formal-semantic LM objects and probes their context sensitivity/entailments.

Record: `relative_vs_absolute_gradable_threshold_computation_collision_2026-09-01.md`.

## B5. Canonical/telic function vs ad-hoc affordance/use

**Status:** `KILL-NOVELTY`.

Canonical object: what an artifact is conventionally for versus what it can be used for in a specific context.

Fatal evidence: GPT-4 lexical coercion/telic-default work plus modern Llama/Gemma context-sensitive affordance work already own default function vs context-induced action affordance as a computational object.

Do not revive as canonical action vs possible use, telic role vs affordance, unusual-use steering, or coercion mechanism.

## B6. Habitual/dispositional vs current episodic state

**Status:** `KILL-NOVELTY`.

Canonical object: `John smokes` versus `John is smoking` / habitual vs episodic predication.

Fatal evidence: TACL 2019 already explicitly decomposes generic/habitual/episodic semantic properties and predicts them from contextual LM representations; SitEnt/DiSCo treat habituality as an independent clause-level semantic property.

Record: `habitual_vs_episodic_event_representation_collision_2026-09-01.md`.

## B7. Cardinal quantity vs ordinal position

**Status:** `KILL-NOVELTY`.

Canonical object: `three objects` vs `the third object` / magnitude vs order.

Fatal evidence: ACL 2026 number-representation work explicitly studies numeric and ordinal information geometry; 2026 ordinal-representation work on Gemma/Qwen includes activation patching.

Record: `cardinal_vs_ordinal_number_representation_collision_2026-09-01.md`.

---

# C. Epistemic / belief / uncertainty cluster

## C1. Ambiguity vs ignorance / aleatoric vs epistemic uncertainty

**Status:** `KILL-NOVELTY`.

Canonical object: `the question has multiple valid answers` versus `the model lacks the answer`.

Fatal evidence: ICML 2024 + AAAI 2026 + ACL 2026 and other work directly decomposes input/aleatoric ambiguity from epistemic knowledge gaps, including internal representations.

Record: `ambiguity_vs_ignorance_uncertainty_2026-09-01.md`.

## C2. Risk vs ambiguity / known vs unknown probabilities

**Status:** `KILL-NOVELTY`.

Canonical object: measurable risk vs Knightian ambiguity / Ellsberg known-urn vs unknown-urn.

Fatal evidence: modern open Qwen3/OLMo3 work already demonstrates ambiguity aversion and uses internal steering/intervention to change it.

Record: `risk_vs_ambiguity_decision_state_collision_2026-09-01.md`.

## C3. Speaker commitment / factivity / projection

**Status:** `KILL-NOVELTY`.

Canonical object: same embedded proposition under `know` vs `think` / speaker commitment to p.

Fatal evidence: NAACL 2025 directly studies projection/speaker-belief commitment and whether explicit belief representations are necessary.

Record: `speaker_commitment_factivity_representation_collision_2026-09-01.md`.

## C4. Evidential source type / direct vs hearsay vs inference

**Status:** `KILL-NOVELTY`.

Canonical object: source-sensitive evidentiality independent of proposition content.

Fatal evidence: ACL 2026 and contemporaneous work explicitly separates evidentiality from epistemic stance in Llama/Qwen/Gemma and studies source-sensitive reasoning.

Do not revive as witnessed/heard/inferred directions or source-certainty subspaces.

## C5. Knowledge vs justified true belief / Gettier status

**Status:** `KILL-NOVELTY`.

Canonical object: true justified belief that is correct through epistemic luck versus genuine knowledge.

Fatal evidence: 2026 machine experimental-philosophy work directly studies LLM Gettier cases and explicitly discusses whether responses reflect underlying belief/knowledge states.

Record: `gettier_knowledge_vs_justified_true_belief_collision_2026-09-01.md`.

## C6. De re vs de dicto / referential opacity

**Status:** `KILL-NOVELTY`.

Canonical object: world-level identity vs identity as represented inside another agent's belief (`Superman = Clark Kent`, but Lois may not know it).

Fatal evidence: SCiL 2023 directly asks whether neural models understand de re/de dicto; TACL 2023 uses referential opacity as a central semantic object.

Record: `de_re_vs_de_dicto_attitude_opacity_collision_2026-09-01.md`.

## C7. Use vs mention / asserted vs quoted proposition

**Status:** `KILL-NOVELTY`.

Canonical object: whether a proposition is asserted/used versus merely mentioned/quoted.

Fatal evidence: dedicated LLM use–mention work directly owns the object.

Do not revive as quote-state direction, assertion-vs-mention patching, or attribution framing.

---

# D. Agent / action / planning cluster

## D1. Desire vs intention

**Status:** `KILL-NOVELTY`.

Canonical object: wanting an outcome versus having formed an intention/plan to realize it.

Fatal evidence: Findings ACL 2025 directly studies belief/desire/intention representations and retention in open-source LLaMA conversational agents.

Record: `desire_vs_intention_mental_state_representation_collision_2026-09-01.md`.

## D2. Goal vs subgoal / terminal vs intermediate status

**Status:** `KILL-SCALE / KILL-BEHAVIOR`.

Canonical object: final goal versus subordinate instrumental step.

Fatal issue: clean hierarchy requires synthetic task construction; labels are unsurprising and risk becoming a planning-benchmark state probe rather than a paper-scale natural object.

## D3. Action precondition vs action effect

**Status:** `KILL-NOVELTY`.

Canonical object: what must be true before an action versus what becomes true after it.

Fatal evidence: modern world-model/action-model work already owns preconditions/effects as explicit LLM state variables.

Record: `action_precondition_vs_effect_world_model_collision_2026-09-01.md`.

## D4. Hard constraints vs soft preferences

**Status:** `KILL-NOVELTY`.

Canonical object: conditions that make plans invalid versus preferences that merely rank valid plans.

Fatal evidence: direct modern LLM planning work already studies the distinction.

## D5. Semantic tool relevance vs operational availability

**Status:** `KILL-NOVELTY`.

Canonical object: irrelevant tool versus relevant/right tool that is unavailable, masked, unsupported, or inaccessible.

Fatal evidence: ACL 2026 owns semantic irrelevance; FAIL-TaLMs/CAR-bench/AdaPlanBench own unavailable/missing/unsupported capabilities. Crossing them into a new 2×2 is an occupied-axis combination, not a new object.

Record: `tool_relevance_vs_operational_availability_collision_2026-09-01.md`.

## D6. Tool necessity vs usefulness/relevance

**Status:** `KILL-NOVELTY`.

Canonical object: a tool can help/relevance-match without being necessary to solve the task.

Fatal evidence: 2026 `When2Tool`, model-adaptive tool necessity, and metacognitive tool-use work directly decode/steer tool-necessity or need-to-call signals.

Do not revive as necessity direction, useful-vs-required subspace, or knowing-doing gap.

## D7. Self-generated vs user-provided content/source

**Status:** `KILL-NOVELTY`.

Canonical object: whether identical text is represented differently when authored by the model versus supplied by the user.

Fatal evidence: ICLR 2025 self-authorship residual vector + causal steering; 2026 self-recognition/role-tag work.

Do not revive as self-vs-user direction, source-aware entrainment, or authorship steering.

## D8. Ownership/possession world-state and role/occupant binding

See A2/A4. Do not reintroduce these as agent-memory or state-tracking topics.

---

# E. Cognitive bias / decision cluster

## E1. Choice-supportive bias: memory distortion vs evaluative reweighting

**Status:** `KILL-NOVELTY`.

Canonical object: post-choice bias due to corrupted recall versus memory-independent later evaluation/rationalization.

Fatal evidence: AAAI 2025 mother already explicitly decomposes memory-based and evaluation-based choice-supportive bias and shows the effect can survive without contextual-memory failure.

Record: `choice_supportive_memory_vs_evaluation_locus_collision_2026-09-01.md`.

## E2. Typicality vs frequency/commonness

**Status:** `KILL-NOVELTY`.

Canonical object: prototypicality/category representativeness versus how often something occurs.

Fatal evidence: modern LM typicality work, including open-model studies, already occupies the conceptual axis.

## E3. Descriptive/statistical norm vs prescriptive/ideal norm

**Status:** `KILL-NOVELTY`.

Canonical object: what is common/average versus what is ideal/should be.

Fatal evidence: ACL 2025 Best Paper `A Theory of LLM Sampling: Part Descriptive and Part Prescriptive` explicitly decomposes LLM sampling/prototypes into descriptive and prescriptive components.

Do not revive as common-vs-normal, average-vs-acceptable, stereotype-vs-norm, or descriptive/prescriptive hidden axes.

## E4. Cause vs enabling condition / causal role distinctions

**Status:** `KILL-NOVELTY`.

Canonical object: cause, enable, prevent, correlate, etc.

Fatal evidence: fine-grained causal NLP resources/work already label and model these distinctions; nearby causal-relation object is crowded.

## E5. Intentional lie vs honest error

**Status:** `KILL-NOVELTY`.

Canonical object: same false output produced knowingly/deceptively versus from genuine error.

Fatal evidence: 2026 RIFT directly controls wrongness and studies deception-vs-error internal signatures in Qwen/Phi.

Do not revive as lie/error direction, truthful-knowledge-vs-false-output conflict, or deception-with-same-answer patching.

---

# F. Event / temporal / discourse cluster

## F1. Event completion / imperfective paradox / culmination

**Status:** `KILL-NOVELTY / KILL-SUBSTRATE`.

Canonical object: progressive/imperfective description versus whether an event actually culminates/completes.

Fatal evidence: ACL 2026 already studies progressive→culmination inference and internal representations; Aug 2026 follow-up argues that parts of the benchmark/teleological-bias interpretation are conceptually mis-specified.

Do not revive as event-completion direction, progressive vs completed state, or telicity patching.

## F2. Attempted/intended event vs realized event

**Status:** `KILL-NOVELTY`.

Canonical object: attempted/planned event versus event factuality/actual occurrence.

Fatal evidence: event factuality and implicativity work already treats fact/possibility/impossibility and factuality inference as central LLM objects; white-box/meta-factivity work is already emerging.

## F3. Habitual vs episodic

See B6.

## F4. Temporal order / duration / distance / interval relation / deictic-vs-sequential frames

**Status:** crowded; do not create a new internal-axis paper without a genuinely distinct scientific object.

2024–2026 temporal-representation work already covers order, duration, distance, interval relations, and temporal reference frames.

## F5. Collective vs distributive plurality

**Status:** HARD LEAD / not registered, but currently unattractive due to overlap and duplication risk.

Canonical object: group-level event predication versus member-wise predication; deeper theory asks ambiguity vs underspecification.

Positive substrate: UDS-EventStructure has human distributivity annotations.

Risks: 2025 plural interpretive-bias behavior and earlier distributivity probing already exist; the deeper `alternatives vs underspecified state` architecture is too close in shape to active 038, reducing register diversity and novelty attractiveness.

Do not promote without a concept-level delta beyond both plural-bias work and 038's unresolved-state architecture.

## F6. Information structure / focus vs background/givenness

**Status:** HARD LEAD / not registered.

Canonical object: same proposition but different information-structural focus/background.

Positive evidence: mature linguistic object; 2025 cognitive work shows LLM judgments can depend on backgroundedness.

Current blocker: no sufficiently strong published modern-open-family paired phenotype/artifact has yet been verified. Do not create GPU behavior discovery data just to test whether the effect exists.

---

# G. Figurative-language cluster

## G1. Metaphor literal-vs-figurative architecture

**Status:** multiple variants rejected/crowded.

Do not revive generic literal-vs-figurative, lexical-anchor, aptness-only, metaphor-detection, or metaphor-vs-simile representation topics.

## G2. 036 conventionality vs aptness selecting comparison vs categorization

**Status:** `HARD AUDIT / NOT PASS / GPU PAUSED` — **not dead**, but former metric is dead.

The scientific selector question survives novelty. The former causal metric (`metaphor↔simile activation non-interchangeability`) failed identifiability because grammatical-form differences do not uniquely identify comparison vs categorization.

Reauthorization requires two independent theory-grounded route signatures, including at least one not defined by metaphor-vs-simile form. Candidate repair uses role-reversal/directionality plus human property-source diagnostics, but no frozen metric is yet clean enough.

Do not count 036 as PASS until that contract is genuinely repaired.

## G3. Metonymy

See B3.

## G4. Idiom route / literal-figurative competition

**Status:** previously rejected/crowded.

EACL 2026 causal work already studies parallel literal/figurative competing pathways. Do not revive with different idiom sets or newer models.

---

# H. Generic dedupe rules learned from recent failures

## H1. Object ownership, not title ownership

A paper can kill a candidate even when its headline sounds unrelated. Read methods, factor definitions, appendices, and discussion. Recent examples:

- former 039: cultural-fidelity/topic-model papers already owned taxonomic-vs-thematic relation type inside experiments;
- ownership-vs-possession: RLVR paper explicitly encoded `(owner, possessor, integrity)` world state;
- authority-vs-expertise: authority-mechanism paper explicitly contrasted institutional authority with competence;
- role-vs-occupant: temporal-KG papers plus generic binding mechanisms jointly occupy the object.

## H2. A new 2×2 is not automatically a new scientific object

If axis A and axis B are both already established LLM objects, crossing them does not necessarily create N2 novelty.

Canonical example: semantic tool relevance × tool availability.

## H3. Strong human theory does not rescue occupied LLM object

Classical distinctions such as Gettier knowledge, risk-vs-ambiguity, relative-vs-absolute adjectives, de re/de dicto, and habitual-vs-episodic remain scientifically meaningful, but they are not fresh LLM paper objects once neural/LLM work already explicitly studies them.

## H4. No modern-open phenotype = no GPU lottery

A concept can be novel and natural yet still fail registration if modern open-model behavior/substrate is not externally established.

Examples encountered:

- ownership-vs-possession looked good before hidden collision was found;
- teleological purpose/cause distinctions had strong human data but no sufficiently strong modern-open premise;
- focus/background information structure remains only a HARD LEAD;
- ascribed-vs-achieved social roles lacked balanced mother cross-cells.

## H5. Generic mechanism occupation can kill a special-case object

If the proposed contribution reduces to applying an already-established generic causal mechanism to a new semantic relation, N2 may still fail.

Examples: role/occupant under generic relation binding; life-status under generic entity→attribute factual retrieval; part-whole under generic semantic-relation MI.

---

# Current live boundary after this index

```yaml
PASS_REGISTER:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture

HARD_AUDIT_NOT_REGISTERED:
  - 036_metaphor_processing_route_selection

HARD_LEADS_NOT_REGISTERED:
  - focus_vs_background_information_structure
  - collective_vs_distributive_plurality  # weak due to overlap/diversity concerns

TARGET: 5
CURRENT_PASS: 3
```

The index must be updated whenever a serious candidate dies in a way that creates a new alias family or dedupe cluster. Individual rejection records remain the evidence source; this file is the fast semantic lookup layer.
