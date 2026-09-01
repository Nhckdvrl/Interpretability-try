# 042 — Why Is “the X” Licensed? Uniqueness vs Strong Familiarity

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED / HARD RE-AUDIT PASSED**  
Date: 2026-09-01  
Route: **A/C hybrid — mature semantic axis + causal source factorization**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When an LLM understands a phrase like “the door”, does it know whether the definite description is licensed because exactly one door fits, or because the intended door has been made strongly familiar in the discourse?**

Frozen factors:

- **UNIQUENESS** — exactly one contextually relevant entity satisfies the descriptive content;
- **STRONG FAMILIARITY** — the intended referent has been explicitly established/re-mentioned in the relevant interlocutor discourse strongly enough to support anaphoric pickup.

Critical cross:

```text
unique but not strongly familiar
vs
non-unique but strongly familiar
```

This is not an article-prediction paper and not a generic coreference/salience paper.

## B. Why the familiarity wording was tightened

Srinivas, Rawlins & Heller (SALT 2020/2021) provide the primary human 2×2. Their stories contain two potential referents and orthogonally manipulate uniqueness and familiarity while keeping the critical final definite condition-matched.

A second hard audit found an important precision issue: the potential referents are already linguistically introduced in the broader story setup. The `+Familiarity` manipulation is therefore **not** simply `antecedent exists vs antecedent absent`. It makes the target strongly discourse-familiar through explicit interlocutor mention/re-mention before the critical definite.

Thus 042 must not operationalize familiarity as generic memory for whether an entity ever occurred in context.

The external result remains strong: uniqueness and familiarity independently affect comprehension/production, but familiarity is a weaker cue than uniqueness. The two sources are behaviorally separable.

## C. Strongest-neighbor audit

### C1 — NAACL 2022 BERT article-system work

`Abstraction not Memory: BERT and the English Article System` studies `a/an` vs `the` vs zero article prediction and abstract generalization.

**Occupies:** neural article-system competence.  
**Does not occupy:** orthogonal uniqueness × strong-familiarity source states or source-selective causal crossover.

042 dies if it reduces to `models know when to predict the`.

### C2 — coreference / discourse salience

Prior models use mention history, salience, uniqueness and compatibility to resolve reference.

**Occupies:** cue use for reference.  
**Does not automatically occupy:** whether uniqueness and strong familiarity form separable *licensing-source states* when crossed while the raw source facts are preserved.

042 dies if it becomes `which cue matters more for coreference`.

### C3 — modern definiteness/bridging work

Recent formal/experimental work continues to tease apart uniqueness and familiarity, especially through bridging/relational definites. This strengthens the naturalness and cross-setting path but is not neural causal ownership of the source factorization.

### C4 — exact N2

> **Modern LLMs maintain causally separable uniqueness-source and strong-familiarity-source states that transfer across discourse realizations and differentially license definite reference while preserving the raw candidate-structure and discourse-mention facts from which those sources are computed.**

No direct neural/LLM causal ownership of this exact object was found in the hard search.

## D. Strict extension locks

### Lock A — orthogonal 2×2: PASS

```text
U- F-
U- F+
U+ F-
U+ F+
```

The decisive source conflict is `U+F-` vs `U-F+`, not `the` vs `a`.

### Lock B — cross-setting abstraction: PASS

Mandatory transfer across at least:

1. original-style ordinary definite descriptions;
2. bridging / relational definite contexts where uniqueness and anaphoric familiarity can be separated;
3. held-out noun/domain families;
4. held-out discourse wording and mention-position families.

Cross-lingual morphology may strengthen the paper later but is not needed to define novelty.

### Lock C — two consequences: AVAILABLE / strengthening

- `DefiniteLicensingLogit`;
- candidate-specific `ReferentMargin` under source conflict.

042 already passes strict A+B; both should still be reported when feasible.

## E. Substrate

### E1 — human 2×2

Primary anchor: Srinivas–Rawlins–Heller, 32 story families, each instantiated in the four uniqueness/familiarity conditions. Critical definite descriptions are matched within item families.

### E2 — deterministic causal microscope

Create theory-licensed clones with two or more explicit candidate entities.

Uniqueness is manipulated by how many candidates satisfy the critical descriptive content.

Strong familiarity is manipulated by whether the target is explicitly selected/re-mentioned in the interlocutor dialogue, **while all entities remain represented in the broader context**.

This mirrors the human distinction more faithfully than deleting an antecedent entirely.

Gold is deterministic. No LLM judge.

## F. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### F1 — raw source-fact denominators

Before source claims, require intact:

```text
CandidateStructureLogit
  # which/how many candidates satisfy the description

DialogueMentionFactLogit
  # whether the target received the explicit strong-familiarity re-mention/manipulation

EntityPresenceLogit
  # both candidates are still represented/remembered
```

`AntecedentRecallLogit` is no longer the primary familiarity denominator because mere prior occurrence does not identify the human manipulation.

### F2 — licensing-source behavior

```text
DefiniteLicensingLogit =
  log P(definite continuation)
  - log P(indefinite/repair continuation)

ReferentMargin =
  log P(intended referent)
  - log P(competing referent)
```

Required qualitative structure:

- U+F-: uniqueness can license despite lack of strong dialogue familiarity;
- U-F+: strong familiarity can help despite descriptive non-uniqueness;
- U-F-: weakest source configuration;
- U+F+: aligned control.

The model need not reproduce human weighting exactly.

### F3 — mandatory salience controls

Balance or independently manipulate:

- recency;
- raw mention count;
- grammatical subject/object position;
- entity order;
- noun repetition;
- description length;
- speaker identity;
- candidate naming.

If `+F` is reducible to raw recency or extra token count, no abstract familiarity-source claim.

## G. Frozen causal-use contract

### G1 — uniqueness source

Estimate `UniquenessSource` on balanced training families.

On held-out U+F- items:

```text
attenuate / swap UniquenessSource
→ change definite/referent licensing
while preserving CandidateStructureLogit
```

If candidate counting itself is damaged, fail specificity.

### G2 — strong-familiarity source

Estimate `StrongFamiliaritySource` while explicitly controlling recency, mention count and raw entity memory.

On held-out U-F+ items:

```text
attenuate / swap StrongFamiliaritySource
→ change definite/referent licensing
while preserving:
   DialogueMentionFactLogit
   EntityPresenceLogit
```

If the intervention simply erases the re-mention event or the entity, fail specificity.

### G3 — decisive crossover

```text
UniquenessSource edit:
  larger source-specific effect when uniqueness is the active licensing source

StrongFamiliaritySource edit:
  larger source-specific effect when strong familiarity is the active licensing source
```

Require matched raw-fact directions, generic salience/coreference directions, random and shuffled controls.

## H. Story invariance

- **A — separable sources:** two reusable causal licensing sources.
- **B — one source dominates:** both raw facts understood, but only one source becomes a reusable licensing computation.
- **C — salience collapse:** source behavior reduces to recency/coreference/easy-reference heuristics despite intact raw facts.

All outcomes answer the same headline.

## I. Hard kills

1. Direct neural/LLM uniqueness × familiarity causal factorization found -> `KILL-NOVELTY`.
2. Only article prediction -> `KILL-N2`.
3. Familiarity effect is raw recency/mention count -> `KILL-IDENTIFIABILITY`.
4. Familiarity intervention erases target/entity or raw dialogue-mention fact -> `KILL-SPECIFICITY`.
5. Uniqueness intervention destroys candidate structure -> `KILL-SPECIFICITY`.
6. Both source states collapse to generic salience/confidence -> no source claim.
7. No held-out discourse/domain transfer -> no abstract source claim.
8. Probe/best-layer only -> `KILL-SCALE`.
9. Failed S0 cannot be rescued by prompt/subset search.

## J. Strict verdict

```yaml
base_v2_1: PASS
human_orthogonal_2x2: PASS
familiarity_definition_corrected: STRONG_DISCOURSE_FAMILIARITY
N0_N1_N2: PASS_AFTER_SECOND_AUDIT
Lock_A: PASS
Lock_B: PASS
Lock_C: AVAILABLE
specificity_denominators:
  - CandidateStructureLogit
  - DialogueMentionFactLogit
  - EntityPresenceLogit
central_salience_confound: IDENTIFIABLE_WITH_HARD_KILL
story_invariance: PASS
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **042 asks whether LLMs causally separate uniqueness from strong discourse familiarity as two sources of definite licensing. Familiarity is not mere antecedent recall: source interventions must change licensing while preserving candidate structure, the explicit dialogue re-mention fact, and entity memory.**