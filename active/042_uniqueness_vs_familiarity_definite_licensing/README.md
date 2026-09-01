# 042 — Why Is “the X” Licensed? Uniqueness vs Familiarity in LLM Definiteness

Status: **STRICT-PASS-REGISTER / GPU AUTHORIZED**  
Date: 2026-09-01  
Route: **A/C hybrid — mature omitted semantic axis + simple latent object**  
Protocol: `FINDING_RULES.md` v2.1 + `STRICT_EXTENSION_GATE_2026-09-01.md`

## A. Frozen natural question

> **When an LLM understands a phrase like “the door”, does it know whether that definite description works because only one door fits, or because the intended door is already familiar from the discourse?**

These are two classic but different sources of definiteness:

- **UNIQUENESS** — exactly one contextually relevant entity satisfies the description;
- **FAMILIARITY** — the intended entity is discourse-familiar / already introduced.

The crucial natural cross-cases are:

```text
unique but unfamiliar
vs
familiar but non-unique
```

The project asks whether modern LLMs maintain and causally use these two licensing sources separately rather than collapsing them into one generic `definite / salient referent` signal.

---

## B. Independent scientific object

The uniqueness-vs-familiarity debate predates neural language models by many decades. Russell/Frege-style accounts emphasize unique satisfaction; Heim/Kamp-style dynamic accounts emphasize familiarity/discourse referents; hybrid and strong/weak-definite theories use both in different ways.

The strongest controlled human anchor is Srinivas, Rawlins & Heller, *Asymmetries between uniqueness and familiarity in the semantics of definite descriptions* (SALT 2020/2021 publication). They orthogonally manipulate:

```text
Uniqueness:   unique / non-unique matching referent
Familiarity:  previously mentioned / not previously mentioned
```

while keeping the critical final definite description constant across conditions.

Their comprehension/production results show an important asymmetry: familiarity helps, but is weaker than uniqueness. Thus the two cues are empirically separable rather than merely two labels for the same successful reference condition.

Cross-linguistic semantics strengthens the reality of the distinction: some languages morphosyntactically distinguish uniqueness-based from anaphoric/familiarity-based definiteness, and recent Mandarin bridging work explicitly teases apart uniqueness and familiarity mechanisms.

---

## C. Strongest computational neighbors — N0 / N1 / N2

### C1 — NAACL 2022 BERT article-system work

`Abstraction not Memory: BERT and the English Article System` evaluates BERT on three-way article prediction (`a/an`, `the`, zero) and argues that BERT captures high-level article-use generalization rather than merely memorizing corpus strings.

**Occupies:** article choice / abstract article-system competence in BERT.

**Does not occupy:** orthogonal uniqueness × familiarity factorization, source-specific internal states, or source-specific causal intervention.

Therefore 042 may not claim novelty as `BERT/LLMs understand definiteness or the article the`.

### C2 — computational coreference / discourse models

Coreference and discourse models obviously exploit prior mention, salience, candidate uniqueness and lexical compatibility.

**Occupy:** reference resolution using these cues.

**Do not automatically occupy:** whether the *same definite licensing judgment* contains separable uniqueness-source and familiarity-source states with distinct causal roles when the factors conflict.

If 042 only becomes `which cue matters more for coreference`, kill N2.

### C3 — 038 / 035 overlap warning

- 038 asks how a **still-unresolved reference** is internally represented.
- 035 asks whether anaphora and presupposition share a **dynamic local-context update**.
- 042 asks a different factorization: **what licenses a definite description when uniqueness and familiarity are crossed?**

042 may not retreat into ambiguity architecture or generic dynamic-context representation.

### C4 — exact N2 delta

The required contribution is:

> **A causally separable pair of definite-licensing sources — uniqueness and familiarity — that generalize across lexical/discourse realizations and control definite/referent licensing while preserving the raw candidate-count and antecedent-memory facts from which those sources are computed.**

No strongest-neighbor search found a neural/LLM paper directly owning this factorization and causal-use question.

---

## D. Strict Extension Gate

### Lock A — orthogonal 2×2 identifiability: PASS

Use the human-established four cells:

```text
U- F-  # nonunique + unfamiliar
U- F+  # nonunique + familiar
U+ F-  # unique + unfamiliar
U+ F+  # unique + familiar
```

The decisive comparison is not `the` vs `a`. It is:

```text
unique-but-unfamiliar
vs
familiar-but-nonunique
```

which forces the two sources apart.

Critical final definite description is held constant inside each item family.

### Lock B — cross-setting abstraction: PASS

Required transfer across at least:

1. ordinary English definite descriptions;
2. bridging / relational definites where antecedent mention and uniqueness can be manipulated separately;
3. held-out lexical/domain families;
4. optional cross-lingual validation in a language whose nominal forms independently distinguish relevant definiteness sources.

### Lock C — two independent consequences: available but not required

Two theory-grounded downstream consequences can be used:

- definite-form / licensing preference;
- candidate-specific referent resolution under source conflict.

042 already passes A+B, but both readouts should be reported when feasible.

---

## E. Substrate

### E1 — human 2×2 comprehension materials

The Srinivas–Rawlins–Heller paradigm uses 32 story families with two potential referents and orthogonal uniqueness/familiarity manipulation. The critical final definite remains condition-matched.

This is the primary human semantic anchor.

### E2 — deterministic controlled clones

For scalable causal analysis, create theory-licensed discourse worlds from the same 2×2:

```text
entities: A, B
shared noun class: door / cup / technician / etc.

Uniqueness manipulation:
  only A satisfies target description
  vs A and B both satisfy it

Familiarity manipulation:
  A previously explicitly introduced
  vs A not previously introduced
```

Gold candidate count and mention history are deterministic. No LLM judge.

The synthetic extension is a microscope; it does not define the distinction.

### E3 — independent naturalistic validation

Recent work on bridging and cross-linguistic definiteness supplies contexts where uniqueness and familiarity mechanisms can be independently licensed. Use only released/reconstructible stimuli whose source factor is theory-defined.

---

## F. Frozen S0

Primary models:

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

### S0-1 — raw capability denominators

Before any source claim, verify deterministic competence on:

- `CandidateCountLogit`: whether one or multiple candidates satisfy the description;
- `AntecedentRecallLogit`: whether the intended entity was previously introduced;
- basic target identity under unconflicted U+F+ cases.

### S0-2 — licensing-source double dissociation

Use forced candidate/article scoring, not free-form LLM judges.

Primary behavioral quantities:

```text
DefiniteLicensingLogit = log P(definite continuation) - log P(indefinite/repair continuation)

ReferentMargin = log P(intended referent) - log P(competing referent)
```

Required qualitative structure:

- U+F- should receive substantial licensing from uniqueness without antecedent familiarity;
- U-F+ should show familiarity-driven recovery despite non-unique descriptive content;
- U-F- should be weakest;
- U+F+ provides the aligned control.

The paper does not require LLM behavior to match the exact human cue weighting; all stable outcomes answer the same question.

### S0-3 — shortcut controls

Balance/reverse:

- noun repetition;
- antecedent recency;
- candidate order;
- lexical description length;
- entity names;
- discourse wording.

If the cross-cells collapse after these controls, terminate the current model scope.

---

## G. Frozen causal-use contract

### G1 — estimate source-specific states

Estimate candidate `UniquenessSource` and `FamiliaritySource` directions/subspaces from balanced training items while controlling raw source facts.

Discovery and test splits are disjoint in nouns/domains and discourse templates.

### G2 — uniqueness intervention

On held-out U+F- vs matched controls:

```text
attenuate / swap UniquenessSource
→ change definite/referent licensing
while preserving CandidateCountLogit
```

If the edit merely makes the model forget how many matching candidates exist, the uniqueness-source claim fails.

### G3 — familiarity intervention

On held-out U-F+ vs matched controls:

```text
attenuate / swap FamiliaritySource
→ change definite/referent licensing
while preserving AntecedentRecallLogit
```

If the edit merely deletes the antecedent entity from memory, the familiarity-source claim fails.

### G4 — source-selective crossover

The decisive statistic is a `Source × Intervention` interaction:

```text
UniquenessSource edit:
  larger effect when uniqueness is the active licensing source

FamiliaritySource edit:
  larger effect when familiarity is the active licensing source
```

with random/shuffled directions, matched raw-fact directions and generic coreference controls.

### G5 — strongest superficial alternative

A generic `salience / easy reference` direction could correlate with both factors. Therefore a PASS result requires source-specific crossover and preservation denominators, not merely linear separability of U/F labels.

---

## H. Story invariance

### Result A — separable licensing sources

Modern LLMs maintain distinct, abstract uniqueness and familiarity signals and use them differentially to license definite reference.

### Result B — one source dominates

Both raw facts are understood, but only one source forms a reusable causal licensing state; this provides model evidence relevant to the long-standing asymmetry debate.

### Result C — collapsed salience/reference heuristic

After controls, the model has no separable source states; definiteness behavior reduces to generic referent salience/ease despite knowing candidate count and mention history.

All three answer the same headline question.

---

## I. Hard kills

1. New direct neural/LLM collision that already factorizes uniqueness × familiarity internally and causally -> `KILL-NOVELTY`.
2. Only `the` article prediction is shown -> `KILL-N2` relative to NAACL 2022.
3. Familiarity state is just antecedent/coreference memory and fails preservation -> `KILL-IDENTIFIABILITY`.
4. Uniqueness state is just candidate counting and fails preservation -> `KILL-IDENTIFIABILITY`.
5. Both states reduce to generic salience/confidence -> no source-specific claim.
6. Cross-lexical/discourse transfer fails -> no abstract source claim.
7. Best-layer/probe-only result -> `KILL-SCALE`.
8. Failed frozen S0 cannot be repaired through prompt/subset search.

---

## J. Venue-scale comparison

- **NAACL 2025 property-inference theory paper:** a classic cognitive factorization remains the scientific object; model evidence adjudicates rather than invents it.
- **EMNLP 2025 Outstanding filler-gap:** cross-setting causal transfer is required to call an internal representation abstract.
- **ACL 2026 Tool Irrelevance:** two natural factors are orthogonalized and causal pathway specificity is tested while preserving generic capability.
- **NAACL 2022 BERT article system:** establishes that neural models can capture abstract article-use regularities, but does not own the uniqueness-vs-familiarity source factorization.

---

## K. Strict registration verdict

```yaml
base_FINDING_RULES_v2_1: PASS
route: A/C
new_orthogonal_object_or_axis: PASS
old_neural_object_ownership: CLEAR_FOR_SOURCE_FACTORIZATION
recent_LLM_object_ownership: CLEAR_FOR_SOURCE_FACTORIZATION
external_human_2x2: PASS
model_independent_gold: PASS
Lock_A_orthogonal_factorization: PASS
Lock_B_cross_setting_abstraction: PASS
Lock_C_two_consequences: AVAILABLE
specificity_denominators:
  - CandidateCountLogit
  - AntecedentRecallLogit
central_confound_identifiable: PASS_WITH_HARD_KILLS
story_invariance: PASS
behavior_lottery: false
verdict: STRICT-PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **042 asks whether modern LLMs distinguish and causally use two classic sources of definiteness — uniqueness and discourse familiarity — rather than merely predicting `the` or resolving a salient referent. The source intervention must change definite/referent licensing while preserving the raw candidate-count or antecedent-memory fact that licenses it.**
