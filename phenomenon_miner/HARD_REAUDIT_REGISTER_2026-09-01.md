# Fresh Register Hard Re-Audit — 2026-09-01

Protocol: `FINDING_RULES.md` v2.1  
Trigger: former 039 was found to have a fatal N2 collision after registration. The entire non-frozen edge of the register was therefore re-audited using the stricter rule **object ownership, not title ownership**.

## Result

```yaml
PASS_REGISTER:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
HARD_AUDIT_NOT_REGISTERED:
  - 036_metaphor_processing_route_selection
ARCHIVED:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
CURRENT_FRESH_PASS_REGISTER: 3
TARGET: 5
```

## 039 — KILL-NOVELTY

Former question: taxonomic similarity / `same kind` versus thematic relatedness / `go together` as a reusable causal relation state.

Fatal result: the object is already studied directly enough in language-model representations and LLM behavior that the remaining contribution was primarily stronger MI.

See:

- `rejected_candidates/taxonomic_vs_thematic_relation_type_n2_collision_2026-09-01.md`
- `archive/039_same_kind_vs_go_together_semantic_relation/`

Canonical lesson:

> A neighbor can own the scientific object inside its experiments/discussion even if its headline is about cultural fidelity, topic modeling, evaluation, or something else.

## 036 — QUESTION SURVIVES, REGISTRATION DOES NOT

Question:

> What selects comparison versus categorization in metaphor comprehension: conventionality, aptness, or neither?

### Novelty audit

The exact selector question still appears unoccupied.

Important neighbors:

- Yang et al. (2026), `Rethinking Metaphor Evaluation: Aptness Judgments as a Cognitive Probe for Language Models` — already owns aptness as an LLM cognitive/evaluation axis.
- Ye et al. (ACL 2026 Main), `Probing Semantic Alignment, Lexical Invariance, and Syntactic Influence in LLM Metaphor Processing` — already owns lexical anchoring, novelty/conventionality-related analysis, semantic alignment and syntax.

Neither orthogonalizes conventionality × aptness to decide comparison versus categorization. Thus the **question-level N2 delta survives**.

### Why former PASS was nevertheless too early

The former first causal statistic equated metaphor↔simile activation non-interchangeability with comparison↔categorization route difference.

That is underidentified. `X is Y` and `X is like Y` differ in syntax, the token `like`, positions and generic form processing. Even strong form controls do not prove that the remaining causal difference is specifically the claimed cognitive route.

Utsumi (2011) explicitly validates comparison/categorization using multiple independent processing signatures, including grammatical concordance and directionality, before using the models to adjudicate selector theories.

Therefore 036 is now:

```yaml
verdict: CONTINUE-PAPER-SCALE / HARD AUDIT
PASS_REGISTER: false
GPU_AUTHORIZED: false
reason: route-identifiability contract not yet sufficient
```

Re-authorization requires a frozen route-calibration design with at least two independent theory-grounded signatures, at least one not defined by metaphor-versus-simile grammatical form.

## 038 — HARD RE-AUDIT PASSED

Question:

> Before reference is uniquely resolved, does the model keep multiple candidate referents, an underspecified reference state, or prematurely commit?

Checked strongest neighbors include:

- `It Depends` — persistent referential ambiguity behavior;
- `Correct-Detect` — ambiguity detection/resolution trade-off;
- `When Agents Commit Too Soon` — generic hidden-state representational commitment in agents;
- EACL 2026 idiom `Tug-of-war` — parallel literal/figurative causal pathways;
- Aug 2026 ambiguous-word activation patching — internal representations after lexical sense disambiguation;
- BlackboxNLP 2024 contextual grammatical cues — activation patching among redundant disambiguating cues.

None owns the exact unresolved-reference representational-format question. 038 also already freezes an explicit H1-vs-H2 identifiability kill: if candidate-specific causal coverage cannot be distinguished from a candidate-balanced shared unresolved state, the architecture claim terminates.

Verdict: **PASS-REGISTER / GPU AUTHORIZED**.

Detailed audit: `active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md`.

## 034 / 035 — lightweight fatal-collision-only scan

No new direct fatal collision was found.

### 034

2026 human prospective-memory work continues to sharpen strategic monitoring / spontaneous retrieval / dynamic multiprocess theory, but the search did not find an LLM mechanistic paper that causally adjudicates these retrieval architectures. Keep frozen.

### 035

Dynamic semantics continues to independently motivate anaphora + presupposition as context-update phenomena, but the search did not find a modern LLM paper demonstrating a shared causal dynamic local-context operation across the two phenomena. Keep frozen.

## Current discipline

The honest register is now **3/5**, not 5/5 and not 4/5.

Do not repair the count first. Repair/audit the science first.

Next work:

1. either repair 036's route-identifiability contract to PASS quality, or leave it out;
2. broad-search replacements using the 039 object-ownership lesson;
3. expect high mortality; do not register a candidate merely because two slots are open.
