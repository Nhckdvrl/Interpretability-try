# Strict Extension Register — 2026-09-01

Status: **3/3 STRICT EXTENSION PASS**  
Base register: **5/5 already reached before this search**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

```yaml
BASE_PASS_REGISTER: 5
STRICT_EXTENSION_TARGET: 3
STRICT_EXTENSION_PASS: 3
TOTAL_REGISTERED: 8

base_registered:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction

strict_extension_registered:
  - 042_uniqueness_vs_familiarity_definite_licensing
  - 043_kind_vs_member_generic_predication
  - 044_stage_vs_individual_predication

hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
```

## Why 042–044 have a higher bar than the base five

Every 042+ topic must pass the complete v2.1 protocol **plus** the strict extension overlay:

1. an orthogonal new scientific object/axis;
2. old RNN/BERT/ELMo object-ownership attack;
3. recent 2024–2026 body/appendix attack;
4. a causal specificity denominator that must be preserved;
5. held-out cross-setting abstraction;
6. at least **two of three** extra locks:
   - Lock A: orthogonal/same-surface/role-swap identifiability;
   - Lock B: cross-setting abstraction;
   - Lock C: two independent theory-grounded consequences.

Mechanizing an already-owned behavior is explicitly insufficient.

---

# 041 second re-audit

041 remains registered under the stricter standard, but its claim is narrowed.

Recent Ref-Adv-style work already owns:

- hard distractor reference;
- minimal necessary descriptors;
- descriptor deletion sufficiency;
- shortcut failures from redundant information.

Thus 041 is alive only for:

> **same-lexical context-conditioned modifier set-restriction role, transferable across property/domain/surface families and causally affecting referent narrowing while preserving property truth.**

See `active/041_contextual_set_restriction/SECOND_HARD_REAUDIT_2026-09-01.md`.

---

# 042 — Uniqueness vs Familiarity as Sources of Definiteness

Frozen question:

> When an LLM understands `the X`, does it know whether the definite is licensed because exactly one X fits, or because the intended X is already discourse-familiar?

Critical factorization:

```text
unique + unfamiliar
vs
nonunique + familiar
```

Human anchor: Srinivas, Rawlins & Heller orthogonal uniqueness × familiarity experiments.

Strongest computational warning: NAACL 2022 BERT article-system work already owns abstract article prediction, so 042 cannot be `does BERT/LLM know the article the?`.

Exact N2:

> **source-specific definite-licensing states for uniqueness and familiarity, with source-specific causal crossover while preserving the raw candidate-count and antecedent-memory facts.**

Strict locks:

```yaml
Lock_A_orthogonal_2x2: PASS
Lock_B_cross_setting_transfer: PASS
Lock_C_two_readouts: AVAILABLE
specificity:
  uniqueness: preserve CandidateCountLogit
  familiarity: preserve AntecedentRecallLogit
```

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED**.

---

# 043 — Direct Kind Predication vs Member-Level Characterizing Generic

Frozen question:

> Does the model know whether a true generic property belongs to the kind itself or is a generalization about individual members?

Classic contrast:

```text
Dinosaurs are extinct.  # direct kind predication
Tigers are striped.     # characterizing/member generic
```

This surrounding family is heavily occupied:

- CL 2024 owns generic exceptions, instantiations and property inheritance;
- Findings ACL 2026 owns generic-vs-quantificational distributional theory;
- LREC/ABRICOT owns abstractness/inclusiveness and context variation.

Therefore 043 is the highest-risk extension topic.

Exact N2:

> **a cross-predicate-family PredicationLevel state that causally governs whether a property is inherited by members and also affects an independent generic-form diagnostic, while preserving the base generic proposition.**

Strict locks:

```yaml
Lock_A_equivalent_factorization: PASS_WITH_LEXICAL_HARD_KILL
Lock_B_cross_predicate_surface_transfer: PASS
Lock_C_two_independent_diagnostics: PASS
specificity:
  - preserve GenericTruthLogit
  - preserve PredicateContentLogit
```

Fatal cliff:

> If `extinct/widespread/common` vocabulary or any predicate-only baseline explains the effect, **KILL immediately**. One successful inheritance metric is insufficient because CL 2024 already owns inheritance behavior.

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED WITH HARD LEXICAL KILL**.

---

# 044 — Stage-Level vs Individual-Level Predication

Frozen question:

> Does a true property characterize the individual as such, or only a particular spatiotemporal stage of that individual?

The topic is **not temporary vs permanent**.

Mandatory anti-shortcut evidence includes:

- same adjective with context/copula-induced reading shift;
- permanent-looking stage cases such as `dead`;
- temporally restricted individual/ser constructions such as `queen for a day`;
- duration-matched controls.

Old corpus semantics already uses IL/SL classes, so novelty is not the labels. Targeted search found no direct neural/LLM causal ownership of a context-conditioned predication-level state.

Exact N2:

> **a cross-context/cross-language predication-level state that controls at least two independent stage-sensitive consequences while preserving the asserted property itself.**

Strict locks:

```yaml
Lock_A_same_lexical_anti_duration: PASS
Lock_B_cross_setting_transfer: PASS
Lock_C_two_independent_stage_diagnostics: PASS
specificity:
  - preserve PropertyTruthLogit
```

Verdict: **STRICT-PASS-REGISTER / GPU AUTHORIZED**.

---

# Serious deaths during this extension search

## Focus/background / information structure

**KILL-NOVELTY.** 2026 GPT-2/GPT-Neo work directly manipulates contextual QUD focus and lexical `only`, including cue conflict, and explicitly argues models maintain discourse-level focus representations.

Record: `rejected_candidates/focus_information_structure_object_ownership_2026-09-01.md`.

## Permission vs ability / deontic vs dynamic modal sense

**KILL-NOVELTY.** IWCS 2023 directly probes BERT modal-sense representations, including whether modal sense abstracts beyond particular modal verbs. Modern AR + stronger causal MI is insufficient.

Record: `rejected_candidates/deontic_permission_vs_dynamic_ability_modal_sense_collision_2026-09-01.md`.

---

# Current full register

```yaml
034: PASS / FROZEN
035: PASS / FROZEN
038: PASS / FROZEN
040: PASS / FROZEN
041: STRICT-REAUDIT PASS / FROZEN
042: STRICT-PASS
043: STRICT-PASS / HIGH-RISK LEXICAL KILL
044: STRICT-PASS

036: HARD AUDIT / NOT REGISTERED
037: DEAD
039: DEAD

TOTAL_REGISTERED: 8
```

## One-line discipline

> **The extension search did not loosen the bar after reaching 5/5. It raised it: 042–044 survive only because each adds an orthogonal scientific object plus hard causal specificity and cross-setting/theory-diagnostic locks. Any collapse to an already-owned behavior kills the topic rather than downgrading the claim.**
