# Hamdi-Style Topic Search — Current Handoff

Date: 2026-09-01  
Status: **AUTHORITATIVE CURRENT STATE — 5/5 PASS / TARGET REACHED**

```yaml
CURRENT_FRESH_PASS_REGISTER: 5
CURRENT_FRESH_ACTIVE_TOPICS: 5
CURRENT_HARD_AUDIT_TOPICS: 1
fresh_register_target: 5
remaining_needed: 0
required_protocol: PAPER-SCALE v2.1
registered_projects:
  - 034_prospective_memory_retrieval_architecture
  - 035_shared_dynamic_context_update
  - 038_unresolved_reference_representation_architecture
  - 040_numerical_identity_vs_qualitative_sameness
  - 041_contextual_set_restriction
hard_audit_not_registered:
  - 036_metaphor_processing_route_selection
archived_after_registration:
  - 037_generic_generalization_licensing
  - 039_same_kind_vs_go_together_semantic_relation
fresh_search_status: STOP_BY_DEFAULT_TARGET_REACHED
```

## Mandatory reads next turn

1. root `README.md`
2. `phenomenon_miner/FINDING_RULES.md` — v2.1
3. this handoff
4. `phenomenon_miner/CURRENT_SEARCH_FLOW_2026-09-01.md`
5. `rejected_candidates/CANONICAL_FAILURE_INDEX_2026-09-01.md`
6. `phenomenon_miner/HARD_REAUDIT_REGISTER_2026-09-01.md`
7. active 034 / 035 / 036 / 038 / 040 / 041 READMEs
8. `active/038_unresolved_reference_representation_architecture/HARD_REAUDIT_2026-09-01.md`
9. `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`
10. `phenomenon_miner/NEXT_AGENT_PROMPT_2026-09-01.md`

## Frozen PASS register

### 034

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

Future intentions: strategic monitoring vs spontaneous cue-triggered retrieval vs dynamic switching.

### 035

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

Shared dynamic local-context update across anaphora and presupposition.

### 038

**PASS-REGISTER / GPU AUTHORIZED / HARD RE-AUDIT PASSED / FROZEN.**

Question:

> When reference is still unresolved, does the model keep multiple candidate referents, an underspecified state, or prematurely commit?

Keep its H1-vs-H2 identifiability kill. Do not rescue failure as generic ambiguity representation.

### 040

**PASS-REGISTER / GPU AUTHORIZED / FROZEN.**

Question:

> **If two things are exactly alike, does the model still know whether they are literally the same individual or merely two different things of the same kind?**

040 is numerical identity vs qualitative/type sameness, not generic entity tracking. Davis & Altmann 2021 RNN is a serious precursor. Required N2 delta remains an abstract cross-surface numerical-identity state causally controlling token-specific history transfer while preserving shared type knowledge.

Frozen first causal contract:

```text
identity intervention
→ changes token-specific HistoryTransferLogit
while
preserving shared TypeKnowledgeLogit
```

### 041 — fifth PASS

**PASS-REGISTER / GPU AUTHORIZED. Route C.**

Natural question:

> **When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?**

Frozen object:

> **context-conditioned modifier set restriction** — whether a modifier actually reduces the currently live referent set, separately from ordinary property meaning.

Why this survived:

1. Leffel et al. 2014 supplies an independent same-lexical human semantics/neuroscience object: context changes whether the same adjective/determiner limits the set under discussion.
2. Old incremental reference resolution, neural pragmatic reference, and overmodification work are treated as serious predecessors. They own candidate elimination, informativeness, distractor sensitivity and redundancy behavior.
3. Therefore the N2 claim is deliberately stronger: a **reusable context-conditioned modifier-role state** in a pretrained AR LLM, cross-lexical/domain/surface and causally used for referent narrowing.
4. The controlled causal microscope uses a three-object **same-world role swap**. Object facts, target, target phrase, modifier words, modifier truth, total world and live-set cardinality stay fixed; only which already-known alternatives are live changes, causing the identifying modifier to swap.
5. The biggest confound is a hard kill: if the signal is raw scene facts, active-candidate identity, lexical position, salience, or generic reference competence, no abstract-role claim survives.

Frozen first causal contract:

```text
SetRestrictionRole intervention
→ changes modifier-specific ReferentMargin / referent narrowing
while
preserving PropertyTruthLogit
```

Cross-property/domain/surface transfer plus scene-fact controls are mandatory. If only `informative adjective > redundant adjective` survives, `KILL-N2`.

Full card: `active/041_contextual_set_restriction/README.md`.

## 036

**CONTINUE-PAPER-SCALE / HARD AUDIT / GPU PAUSED / NOT REGISTERED.**

The conventionality/aptness selector question survives, but comparison-vs-categorization route identification remains underidentified. Re-enter only after a real two-signature calibration contract exists. The 5/5 target gives no reason to force-repair it.

## 037 / 039

Archived. Do not revive. 039 remains the canonical warning that naturalness + excellent substrate is not enough if prior work owns the scientific object.

## New terminal records from the final search

- `mass_count_grammar_vs_conceptual_individuation_collision_2026-09-01.md`: old neural mass/count syntax-semantics and contextual coercion work already own the attractive object; modern AR + MI would be N2-thin.
- `means_vs_side_effect_moral_role_collision_2026-09-01.md`: means-vs-side-effect is directly an LLM moral factor in MoCa/OffTheRails; the stronger intentionality-mediation theory variant lacks a frozen analyzable-open behavior anchor and is not GPU-authorized.

Keep these in semantic dedupe memory.

## Failure-library discipline remains binding

Before any future serious candidate:

```text
one-sentence object
→ 5–10 aliases
→ canonical failure index
→ rejected_candidates + archive
→ strongest-neighbor BODY / appendix search
```

A semantic match is dead by default unless a documented resurrection condition is met. Backbone/dataset/language/probe/SAE/patching/steering changes do not create a new object.

## Main-paper expansion discipline

Read `phenomenon_miner/PAPER_EXPANSION_REFERENCE_2026-09-01.md`.

Reference-backed ladder:

```text
phenomenon / natural object
→ broad characterization and controls
→ abstraction / cross-setting transfer
→ causal use and specificity
→ mechanism-derived falsifiable behavioral prediction
→ targeted confirmation
→ optional mitigation / architecture generalization
```

For 041 freeze only the earned first three stages now:

```text
same-world modifier-role double dissociation
→ cross-lexical/domain/surface abstraction
→ causal referent-narrowing specificity while preserving property truth
```

Do not pre-write a failure mechanism. Only after Stage 3 reveals a stable mechanism may it derive a new falsifiable failure and later mitigation.

## Current task boundary

The fresh-search target is complete at **5/5**. Do not continue count-filling search by default. Next work should be one of:

- execute the frozen cheap S0 / causal microscope for a registered topic;
- compare/prioritize the five registered projects for execution;
- react to genuinely new fatal novelty evidence;
- continue fresh search only if the user explicitly asks for more than five.

## One-line instruction

> **Authoritative register is now 5/5: 034, 035, 038, 040, 041. 041 is contextual modifier set restriction, not generic reference resolution or adjective redundancy. The target is reached; preserve strict kills and move from topic search to frozen experimental execution unless explicitly asked to search further.**
