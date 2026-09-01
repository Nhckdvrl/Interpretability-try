# 036 — What Selects a Metaphor's Processing Route? Conventionality vs Aptness

Status: **HARD AUDIT / CONTINUE-PAPER-SCALE / GPU PAUSED**  
Former status: `PASS-REGISTER / GPU AUTHORIZED`  
Hard re-audit date: 2026-09-01

> **Important:** the headline scientific question survives the hard novelty audit, but the former first causal statistic does **not** yet identify `comparison` versus `categorization` strongly enough to justify GPU authorization. This project does not count in the fresh PASS register until the identifiability contract below is repaired and frozen.

## A. Frozen natural question

When a language model understands a metaphor, what determines whether it treats the expression as a **comparison between two concepts** or as **categorization under an abstract metaphorical category**: the vehicle's conventionality, the topic–vehicle pair's aptness, or neither in a discrete route-switching sense?

This question remains natural without any benchmark or MI vocabulary.

## B. Why the scientific question still survives

The external debate predates neural LMs:

- Bowdle & Gentner (2005), **Career of Metaphor**: as a vehicle becomes conventionalized, processing shifts from comparison toward categorization.
- Jones & Estes (2006): when conventionality and aptness are separated, **aptness** predicts metaphor/simile preference, comprehension and category-membership judgments, whereas conventionality does not reliably do so.
- Utsumi (2011): explicitly asks which property selects between **comparison** and **categorization**, contrasting conventionality, aptness and interpretive diversity.

Key sources:

- Bowdle & Gentner: https://pubmed.ncbi.nlm.nih.gov/15631593/
- Jones & Estes: https://doi.org/10.1016/j.jml.2006.02.004
- Utsumi: https://doi.org/10.1111/j.1551-6709.2010.01144.x

So the independent object is not `metaphor accuracy`; it is **route selection in metaphor comprehension**.

## C. 2026 strongest-neighbor re-audit

The earlier README understated how crowded the surrounding LLM space is. The following neighbors are now treated as explicit N2 warnings.

### C1 — Aptness is already an LLM scientific object

Yang et al. (2026), **`Rethinking Metaphor Evaluation: Aptness Judgments as a Cognitive Probe for Language Models`**, evaluates a broad model panel including LLaMA-3.3, DeepSeek, Gemma, Mixtral, Phi and QwQ. It treats human metaphor aptness as a cognitive dimension and shows a stable aptness-dependent performance gradient.

Source: https://doi.org/10.1007/s12559-026-10567-w

Therefore 036 cannot claim novelty from merely asking whether LLMs are sensitive to aptness.

### C2 — Conventional/novel metaphor processing is already analyzed internally

Ye et al. (ACL 2026 Main), **`Probing Semantic Alignment, Lexical Invariance, and Syntactic Influence in LLM Metaphor Processing`**, studies lexical invariance, semantic alignment and syntactic sensitivity and reports that stable lexical anchors may support conventional metaphors while biasing novel metaphors that require contextual integration.

Source: https://aclanthology.org/2026.acl-long.1286/

Therefore 036 cannot claim novelty from simply contrasting conventional versus novel metaphor representations.

### C3 — Why the exact selector object is not yet occupied

The hard search still did **not** find a 2025–2026 LLM paper that:

1. orthogonalizes **vehicle conventionality × topic–vehicle aptness**;
2. asks which factor selects **comparison versus categorization**;
3. causally adjudicates that selector in modern open-weight LMs.

The 2026 aptness paper asks whether aptness is a useful cognitive/evaluation axis; ACL 2026 asks how metaphor processing reflects semantic alignment, lexical anchors and syntax. Neither owns the exact `conventionality/aptness -> comparison/categorization route` question.

**Novelty verdict:** `N0/N2 SURVIVES FOR THE QUESTION`, but this does not by itself authorize the former experiment.

## D. Primary substrate remains valid

Jones & Estes (2006) publishes a natural 2×2 stimulus design:

- conventional / high aptness;
- conventional / low aptness;
- novel / high aptness;
- novel / low aptness.

There are 64 high/low-aptness pairs = 128 metaphor sentences, 32 per cell. High/low aptness pairs share the same vehicle, allowing aptness to change while vehicle conventionality is held fixed. The original experiments also use metaphor and simile forms and category-membership judgments.

Representative cells:

- conventional/high-apt: `Some runners are cheetahs`;
- conventional/low-apt: `Some skaters are cheetahs`;
- novel/high-apt: `That fashion model is a rail`;
- novel/low-apt: `That football player is a rail`.

This substrate is not the problem.

## E. Fatal issue discovered in the hard audit — route identifiability

The former first causal contract did this:

```text
metaphor: X is Y
vs
simile:   X is like Y

activation patch metaphor <-> simile
→ cross-form causal non-interchangeability
→ call that comparison-vs-categorization route difference
```

That inference is too strong.

### Why the old statistic is underidentified

A causal difference between `X is Y` and `X is like Y` can arise from:

- the lexical token `like`;
- different syntax / token positions;
- different output calibration or next-token geometry;
- generic metaphor-vs-simile form processing;
- route-independent semantic changes.

Literal `is`/`is like` controls reduce some confounds but **do not prove that the remaining causal difference is specifically comparison versus categorization**.

This matters because the paper headline is about a *processing route*, not merely grammatical-form dependence.

## F. What the original theory requires for route identification

Utsumi (2011) explicitly says that psychological work has used **two distinctive processing phenomena** to diagnose comparison versus categorization:

1. **grammatical concordance between form and function**;
2. **directionality / asymmetry in metaphor processing**.

It also gives a semantic distinction between the two computations:

- categorization emphasizes vehicle/category-typical properties and suppresses topic-specific irrelevant properties;
- comparison emphasizes properties shared by topic and vehicle while avoiding unshared vehicle-specific properties.

Critically, Utsumi first validates its comparison and categorization algorithms against these independent phenomena **before** using model selection to decide which route better explains a metaphor. That is the standard 036 must now meet as well.

## G. Required repair before GPU authorization

The repaired causal microscope must be frozen **before** GPU use and must satisfy all of the following.

### G1 — at least two independent route signatures

A result cannot be called `comparison-like` or `categorization-like` from metaphor-vs-simile patchability alone.

At least two theory-grounded signatures are required, with **at least one not defined by grammatical form**. Candidate families include:

- grammatical concordance;
- directionality / reversal sensitivity;
- feature-selection signature: common topic–vehicle properties versus vehicle/category-typical properties.

The exact second diagnostic must be tied to auditable human/theory material rather than invented after seeing model activations.

### G2 — independent route calibration

Before applying route labels to Jones–Estes metaphors, the proposed internal statistic/subspace must distinguish held-out **literal comparison** from **literal categorization** across surface realizations and lexical items.

A classifier that merely separates `is` from `is like` is invalid.

### G3 — causal validation, not decodability

The calibrated route state must causally change a route-diagnostic downstream measure on held-out calibration examples before it is used to interpret metaphor states.

### G4 — selector test remains frozen to the natural 2×2

Only after route validity is established may the Jones–Estes 2×2 test whether route evidence is predicted more strongly by:

- vehicle conventionality;
- metaphor aptness;
- neither / graded heterogeneous computation.

### G5 — no layer-time = human-time shortcut

Do **not** equate early transformer layers with early human processing stages. If directionality is used, the operationalization must be a model-internal causal/semantic signature, not a biological stage analogy.

## H. Story invariance still holds

If a valid route diagnostic is obtained:

- **Result A — conventionality dominates:** evidence compatible with a Career-of-Metaphor-like route shift.
- **Result B — aptness dominates:** route selection follows topic–vehicle fit rather than conventionalization.
- **Result C — neither:** LLM metaphor comprehension is not organized by a clean discrete selector along these classic accounts.

All three preserve the same headline.

If no valid route diagnostic can be established, the project is **KILL-MEASUREMENT / KILL-IDENTIFIABILITY**. It may not be rescued as `metaphor vs simile representations`, `aptness direction`, or `best metaphor head`.

## I. Current hard-audit verdict

```yaml
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
scientific_lineage: PASS
N0_object_ownership: PASS_FOR_EXACT_SELECTOR
N1_causal_occupancy: PASS
N2_delta_width: PASS_FOR_EXACT_SELECTOR
substrate: PASS
modern_open_model_premise: PASS
story_invariance: PASS
former_first_causal_statistic: FAIL_IDENTIFIABILITY
route_identification_contract: NEEDS_REPAIR
verdict: CONTINUE-PAPER-SCALE / HARD AUDIT
PASS_REGISTER: false
GPU_AUTHORIZED: false
```

## J. Re-authorization condition

036 may return to `PASS-REGISTER / GPU AUTHORIZED` only after a **specific, auditable, preregistered two-signature route-identification contract** is written that cannot be reduced to `metaphor form vs simile form`.

Until then: **no GPU sweep, no SAE hunt, no best-layer exploration.**
