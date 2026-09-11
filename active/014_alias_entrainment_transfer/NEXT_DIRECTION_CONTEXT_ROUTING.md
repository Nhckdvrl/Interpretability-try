# 014 Next Direction — Context-Dependent Routing of Contextual Entrainment

Status: **HARD-AUDIT CANDIDATE / NOT YET PROMOTED**  
Parent project: `014_alias_entrainment_transfer`  
Parent verdict remains unchanged: **CROSS-SURFACE-BUT-NOT-REFERENCE-SPECIFIC**

## 1. Why this direction exists

The r4 result closes the original reference-specific question:

- broad cross-surface spillover is strong and replicates across three model families, both frames, both directions, and strong association controls;
- the effect falls sharply across `compositional -> partial -> opaque -> opaque_strict`;
- after association matching, `opaque_strict` has no stable shared-referent residue;
- Phase 2 supports a shared upstream cause with exact entrainment;
- Phase 3 shows direct write from entrainment heads is mainly lexical / seen-form and grows with surface overlap.

Therefore the next scientific question must **not** be another alias subtype, acronym direction, entity-specific rescue, or generic path-localization exercise.

The unresolved object is:

> **What determines the destination of contextual salience once exact lexical exposure has occurred?**

Two qualitatively different accounts remain compatible with the current evidence.

### H1 — Static pretrained lexical graph

Exact-token entrainment raises salience of the seen form, and any cross-surface spillover follows lexical/semantic associations already encoded in model weights. The route is largely fixed by pretraining statistics.

### H2 — Dynamic contextual routing

Exact-token entrainment produces an upstream salience signal, but the destination of that signal is selected online by the meaning/entity binding active in the current context.

The key distinction is therefore not `surface vs entity`, which r4 has already constrained, but:

```text
fixed pretrained association
vs
context-selected active binding
```

## 2. Frozen headline question

> **When the same surface form is resolved to different meanings/entities by context, does an otherwise identical extra exposure route contextual entrainment toward the currently active interpretation?**

Short form:

> **Does contextual entrainment follow the word, or the meaning currently bound to that word?**

This must remain an entrainment-routing question. A generic lexical ambiguity / WSD / entity-linking result is not sufficient.

## 3. Primary behavioral microscope

Use naturally ambiguous attested surfaces `A` with two independently gold referents `E1` and `E2`.

Example shape:

```text
C1: natural context that resolves A -> E1
C2: natural context that resolves A -> E2
```

The exact same surface `A` is used in both conditions.

For each referent, choose an unseen target surface:

```text
B1 = canonical/redirect surface for E1
B2 = canonical/redirect surface for E2
```

`B1` and `B2` must be absent from the prompt during the entrainment assay.

Within each disambiguating context compare:

```text
WITH_EXTRA_A    same context + one additional mention of A
NO_EXTRA_A      same context, no additional mention
```

Primary effect:

```text
Delta(B | C) = log P(B | C + extra A) - log P(B | C)
```

Primary routing interaction:

```text
R = [Delta(B1 | C1) - Delta(B2 | C1)]
  - [Delta(B1 | C2) - Delta(B2 | C2)]
```

This difference-in-differences is mandatory. Ordinary `P(B1|C1) > P(B2|C1)` only demonstrates disambiguation / word-meaning priming and does not answer the project question.

## 4. Why this design is decisive

Across `C1` and `C2`, the repeated surface is literally identical. Therefore the following are held fixed:

- token identity;
- tokenization;
- exact repetition count;
- orthography;
- lexical frequency;
- generic mother-style exact entrainment;
- the surface's global pretrained association network.

Only the current interpretation/binding changes.

A positive cross-over in `R` therefore cannot be reduced to the fact that different strings were exposed.

## 5. Data route — natural gold first

Primary construction should use natural public artifacts, not LLM-authored ambiguity labels.

Preferred source pattern:

- Wikipedia hyperlink anchors where the **same anchor string** links to different entity pages in different natural contexts;
- Wikipedia/Wikidata entity IDs as independent referent gold;
- Wikipedia redirect/canonical surfaces for `B1/B2`;
- entity-clustered inference so prolific ambiguous surfaces do not dominate.

External validation resources may include established ambiguous-entity datasets such as AmbER / AmbigDocs, but the exact usable row-level population must be audited before registration.

Required source audit before any model call:

1. count unique ambiguous surface forms;
2. count unique referent pairs;
3. verify both target surfaces can be kept absent from the assay prompt;
4. inspect popularity imbalance between referents;
5. remove cases where one target string is a substring of the repeated surface or leaks through context;
6. random manual audit of context->referent correctness;
7. freeze all entity/surface IDs and source revisions.

## 6. Fatal novelty control

Generic word-meaning priming is already known in humans and has been tested in LLMs. Generic entity disambiguation and binding are also occupied.

Therefore the candidate is killed if its strongest claim can be summarized as either:

```text
recent exposure to one meaning makes that meaning easier to access
```

or:

```text
LLMs can disambiguate an ambiguous name in context
```

The non-negotiable novelty object is:

> **whether the incremental causal effect of exact lexical exposure — contextual entrainment — is itself routed by the currently active interpretation/binding.**

## 7. Outcome-robust interpretation

### Outcome A — dynamic routing

`R` is robustly positive across families/populations: the same repeated string sends extra salience toward different unseen forms depending on current interpretation.

Interpretation:

> contextual entrainment is not only a fixed lexical-copy bias; its downstream destination is context-dependent.

### Outcome B — static graph

Exact entrainment is present, but `R` is null after capability and leakage controls.

Interpretation:

> cross-surface spillover seen in r4 is primarily a property of pretrained lexical/association structure rather than online referential routing.

This is a meaningful boundary result and directly explains why `opaque_strict` identity did not survive r4.

### Outcome C — independent semantic priming

A routing-like behavioral interaction exists, but exact-entrainment interventions leave it unchanged.

Interpretation:

> contextual entrainment and context-specific semantic/meaning priming are distinct processes whose behavioral effects were superposed in the original alias setting.

All three outcomes answer the same scientific question. No post-hoc subset rescue is permitted.

## 8. Causal follow-up — only after behavioral construct passes

Entrapment-head discovery must be independent of the ambiguity bank:

1. reproduce exact contextual entrainment on a mother-faithful dataset;
2. discover/select entrainment heads using EXACT/random conditions only;
3. freeze those components;
4. ablate them on the ambiguity-routing bank;
5. re-estimate `R`.

Primary causal question:

> does removing independently identified exact-entrainment machinery selectively attenuate the context-dependent routing interaction?

This separates:

- `entrainment -> dynamically routed downstream`,
- from `entrainment + independent semantic priming`.

Do not select heads on alias/ambiguity effect size.

## 9. Secondary causal microscope — newly established binding

Only after the natural ambiguity result is interpretable, test whether routing can use a relation created in the current context rather than one memorized in pretraining.

Example shape:

```text
In this document, A is called ZORP.
In this document, C is called FLEN.
```

Exposure to `ZORP`/`FLEN` must be exactly balanced. Then add an extra occurrence of `A` or `C` and test whether the corresponding nonce label receives an incremental boost.

This is **not** a primary dataset and cannot rescue a failed natural result. It is a causal microscope for distinguishing:

```text
pretrained-edge propagation
vs
online-binding propagation
```

Mandatory controls include bidirectional definition order, multiple mapping templates, no-binding token-matched controls, position counterbalancing, and target-exposure equality. One-direction sequence-copy effects are not sufficient.

## 10. Forbidden pivots

Do not turn this into:

- another acronym / abbreviation study;
- another alias subtype leaderboard;
- generic WSD/entity-linking;
- generic word-meaning priming;
- `best head` / `alias converter head` localization;
- person-only or one ambiguous-surface family;
- RAG benchmark engineering;
- F2-only / short-distance rescue;
- entity/reference-specific revival of r4 Q2.

The parent verdict remains historical truth.

## 11. Promotion bar

Promote this direction only if all of the following survive hard audit:

1. a broad natural ambiguous-surface population with independent referent gold can be frozen;
2. the difference-in-differences estimand cleanly separates incremental entrainment from baseline disambiguation;
3. novelty survives direct comparison with word-meaning priming, entity-disambiguation, binding, and contextual-entrainment literature;
4. at least two plausible causal accounts remain with different intervention predictions;
5. null dynamic routing still yields a Main-scale boundary claim rather than merely `no effect`;
6. the paper can retain the full 014 r4 result as C1 and use the new question as a genuine explanatory extension, not a post-hoc redefinition of r4 Q2.

## 12. Intended paper ladder if promoted

```text
C1  Boundary already established by 014 r4:
    cross-surface spillover is real but decays with lexical/derivational distance;
    shared reference alone is not a stable causal unit.

C2  Routing:
    hold the repeated surface fixed and change only its contextually resolved
    interpretation; test whether incremental entrainment changes destination.

C3  Causal composition:
    independently identified exact-entrainment machinery x active contextual
    binding/interpretation; determine whether they form one routed process or
    two independent sources of bias.
```

## One-line decision

> **Do not add more alias categories. The next high-value question is whether the same lexical entrainment signal is routed differently when current context binds the same surface to a different interpretation.**
