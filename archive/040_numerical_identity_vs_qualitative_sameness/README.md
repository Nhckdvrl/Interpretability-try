# 040 — Same Thing or Just the Same Kind? Numerical Identity vs Qualitative Sameness in LLMs

Status: **ARCHIVED AFTER REPRESENTATION AND CAUSAL-USE GATES**
Date: 2026-09-01  
Route: **C — simple natural object first**

Execution update (2026-09-04): direct identity behavior passed in Qwen, but the arbitrary-
history contract, binding-boundary transplant, cross-surface identity readout, and cross-task
causal intervention all failed their frozen gates. The project is archived rather than
narrowed to generic binding recency; see `FINAL_VERDICT.md` and `EXPERIMENT_LOG.md`.

## A. Frozen natural question

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual object or merely two different objects of the same kind?**

The two crucial cross-cases are ordinary and predate LLMs:

- **same individual despite qualitative change** — one onion is chopped and later referred to again;
- **different individuals despite qualitative similarity** — a second, otherwise identical onion is introduced.

This is the classic distinction between **numerical identity** (one and the same individual) and **qualitative sameness/identity** (sharing type or properties).

The paper is not about a benchmark, a determiner, or an entity-tracking head. It asks whether modern LLMs maintain and causally use this distinction.

---

## B. Why this is a real scientific object

The distinction is independently established in philosophy, psycholinguistics and cognitive science.

### B1 — explicit folk-identity separation

Dranseika, Nichols & Strohminger (Cognition 2023), *Which kind of sameness? Disambiguating two senses of identity with a novel linguistic task*, exploits Lithuanian lexical markers that distinguish:

- `same_N` — numerically the same individual;
- `same_Q` — qualitatively the same / same kind.

Study 2 uses twins and cups to validate the distinction, and the paper argues that the method is useful generally for studying identity persistence rather than only moral-personality judgments.

DOI: `10.1016/j.cognition.2023.105545`

### B2 — natural token × state-change dissociation

Solomon, Hindy, Altmann & Thompson-Schill (J Cogn Neurosci 2015), *Competition between Mutually Exclusive Object States in Event Comprehension*, uses **120 event frames** in a natural 3 × 2 design:

```text
referent:
  same token
  different token / same type
  different token / different type

x

object change:
  minimal
  substantial
```

Example:

```text
The chef will weigh/chop an onion.
Then she will smell the onion.          # same numerical token
Then she will smell another onion.      # different token, same type
Then she will smell a piece of garlic.  # different type
```

The design was created specifically to distinguish competition between mutually exclusive states of one individual token from mere representational similarity. Human conflict effects occur for substantial state change of the **same token**, not for a **different token of the same type**.

Open article: `https://pmc.ncbi.nlm.nih.gov/articles/PMC6352722/`

This supplies the exact scientific double dissociation needed by 040:

```text
large qualitative change + numerical identity
!=
strong qualitative similarity + numerical distinctness
```

---

## C. Strongest-neighbor audit — N0 / N1 / N2

### C1 — Davis & Altmann 2021 RNN precursor: serious, not ignored

Cognition 2021, *Finding event structure in time: What recurrent neural networks can tell us about event structure in mind*, trains text LSTM RNNs and analyzes hidden representations for related event materials. One study explicitly contrasts:

```text
... the onion      # same token
... another onion  # different token of the same type
```

The RNNs are sensitive to the distinction.

This is a **real computational precursor**. Therefore 040 may NOT claim novelty as:

> `neural language models distinguish the onion from another onion`.

However, the 2021 paper is framed around event-state propagation in RNNs, reports representational similarity rather than causal use, and explicitly concludes that much remains unknown about the extent to which the networks encode objects as specific tokens.

DOI: `10.1016/j.cognition.2021.104651`

Public artifact: `forrestdavis/ExperimentNorming` contains row-level stimuli including `stimuli/multi_sent_another.xlsx`, `multi_sent.xlsx`, state-change files, and analysis/results files.

### C2 — modern entity tracking is adjacent but does not own the identity-vs-similarity object

Important modern mechanistic neighbors:

1. **ICLR 2024 — Fine-Tuning Enhances Existing Mechanisms: A Case Study on Entity Tracking.**  
   Finds a Llama entity-tracking circuit that tracks the position of an already individuated correct entity.

2. **EMNLP 2024 — Representational Analysis of Binding in Language Models.**  
   Finds low-rank Binding-ID representations for binding already indexed entities to attributes and causally edits those bindings.

3. **ACL 2026 — Cell-Based Representation of Relational Binding in Language Models.**  
   Models relation binding as entity × relation cells and causally manipulates bound attributes across domains.

4. **ICML 2026 — Do Language Models Track Entities Across State Changes?**  
   Explains PUT/MOVE/REMOVE mechanisms and finds a fragile global REMOVE tag.

These works largely start **after individuation has already been supplied by the task**: entities have names, indices, box positions, or unique object labels. They ask how attributes/states are bound and retrieved.

ICML 2026 is the closest modern warning. Its authors explicitly note that the original REMOVE data contain only **one object of the same type across all boxes**, so a global removal heuristic remains behaviorally correct. They then introduce a `Shared-label Objects in Multiple Boxes` stress test, where two `pill` mentions in different boxes expose the global-removal failure.

That is evidence that modern LLMs can fail when **same label/type no longer identifies one unique individual**. But the paper treats this as a predicted failure of a REMOVE mechanism; it does not factorize or causally characterize **numerical identity vs qualitative/type sameness** as the scientific object.

### C3 — exact N2 delta

040 asks a question not owned by the RNN precursor or modern entity-tracking papers:

> **Do modern LLMs maintain a reusable numerical-identity state that remains distinct from qualitative/type similarity and causally governs which token-specific history is inherited by a later mention?**

To earn this delta, 040 must demonstrate more than local tracking:

1. same individual remains the same through substantial property/state change;
2. different individuals remain distinct despite identical/same-type properties;
3. the distinction generalizes across lexical/surface cue families;
4. intervention changes **token-specific history transfer**, not generic type knowledge or all coreference;
5. at least one independent validation window goes beyond the original onion/event carrier.

If only event-specific `the` vs `another` tracking survives, 040 collapses toward Davis–Altmann and is **KILL-NOVELTY**.

---

## D. Why this is not generic coreference / binding / entity tracking

Coreference asks which mention refers to which entity. Binding work asks which attribute is attached to an already indexed entity. Entity tracking asks how an already individuated object changes location/state.

040 asks the prior representational question:

> **What makes two mentions count as the same individual at all, when type/appearance similarity points one way and diachronic continuity points another?**

The decisive cross-cases are therefore mandatory:

```text
same individual + large change
versus
different individual + near-identical qualities
```

A method that succeeds only when names/IDs/determiners directly label identity does not establish the 040 object.

---

## E. Measurement substrate

### E1 — primary natural event window

Use the published Solomon/Hindy/Davis event family, not a newly invented benchmark. The Davis–Altmann public repository supplies executable row-level descendants of this paradigm.

Frozen factors:

```text
Identity:
  SAME_TOKEN
  DIFFERENT_TOKEN_SAME_TYPE

StateChange:
  MINIMAL
  SUBSTANTIAL
```

`DIFFERENT_TYPE` remains a control for generic type/semantic similarity.

All valid released items are used; no model-effect subset selection.

### E2 — independent qualitative-vs-numerical sameness window

Dranseika et al. 2023 provides an external identity definition using Lithuanian `same_N` versus `same_Q`, with cups/twins and diachronic-person cases.

This is a validation window, not a requirement that the primary LLM experiment be in Lithuanian. It prevents the paper from defining numerical identity solely as English `the`/`another` coreference.

### E3 — controlled causal microscope is allowed

For causal use, a small controlled continuation/QA layer may introduce **arbitrary token-specific history** (e.g. a nonce tag or arbitrary property attached to one object token). This is legitimate because:

- numerical identity is defined independently by the human science;
- the central labels are not invented for the paper;
- the controlled property exists only to test whether history follows the individual rather than its type.

The controlled microscope may not replace the natural event window as the paper object.

---

## F. Prespecified models and architecture scope

### Primary mechanistic panel

- `meta-llama/Llama-3.1-8B-Instruct`
- `Qwen/Qwen3-8B`

These are modern, analyzable autoregressive Transformer families. A family contributes to the causal claim only if it passes the frozen S0 capability gate.

### Secondary architecture generalization — strengthening, not headline

The identity question is architecture-agnostic, so a successful primary result can be tested on substantially different sequence models:

- **diffusion LM:** LLaDA-8B / Dream-family open checkpoints;
- **linear/recurrent-like LM:** an analyzable Mamba/RWKV-style checkpoint only if it passes the same frozen S0.

This is scientifically motivated because the strongest old precursor is an LSTM RNN while current work is dominated by autoregressive Transformers. It can test whether numerical identity is an architecture-general solution or represented differently across recurrent/linear, autoregressive-attention and diffusion paradigms.

However:

> **architecture comparison is secondary evidence, not the novelty claim.**

A failure of a dLLM/linear model cannot change the 040 headline or rescue a weak primary result.

---

## G. Frozen S0 — obvious experiments first

### S0-1 — behavioral identity double dissociation

Across all released event items, require the model to distinguish:

- SAME_TOKEN after substantial change;
- DIFFERENT_TOKEN_SAME_TYPE despite maximal type similarity.

Use deterministic forced-choice/logit scoring. No LLM judge.

The primary behavioral quantity is an identity-sensitive logit contrast under matched type:

```text
IdentityUse =
  score(token-specific history belongs to later referent)
  - score(token-specific history does not belong to later referent)
```

Expected sign:

- SAME_TOKEN: positive;
- DIFFERENT_TOKEN_SAME_TYPE: negative or substantially lower.

`DIFFERENT_TYPE` is not allowed to define the effect; it is only a semantic-similarity control.

### S0-2 — surface-cue generalization

The effect must reproduce across at least **two prespecified cue families** so it cannot be only `the` vs `another`:

1. definite/new-token event-anaphora family inherited from the natural materials;
2. a held-out paraphrase/continuity family where identity is established through event continuity/description rather than the same determiner pair.

Training and causal-subspace discovery may not see the held-out cue family.

### S0-3 — no behavior lottery

S0 does not decide what the paper is about. The question is already frozen.

If both primary model families fail the frozen identity double dissociation, terminate 040 for this model scope. Do not prompt-search, subset-search, or rewrite the paper as `coreference failures`.

---

## H. Frozen first causal contract

The causal claim is deliberately simple:

> **Does an internal numerical-identity state causally control inheritance of token-specific history, separately from type/category knowledge?**

### H1 — identity-state estimation

Estimate a low-dimensional `NumericalIdentity` direction/subspace at the later referent/integration state from training contexts with human-defined SAME_TOKEN versus DIFFERENT_TOKEN_SAME_TYPE labels.

Constraints:

- use cue-family-disjoint validation;
- balance object types and state-change magnitude;
- residualize or explicitly control noun identity/repetition, token length, recency, determiner family, semantic similarity and generic coreference features;
- do not select a best layer on the causal test set.

### H2 — first causal test: token-specific history transfer

Use held-out identity contexts in which one object token has an arbitrary episode-specific property/history and a same-type competing object does not share that history.

Primary readout:

```text
HistoryTransferLogit =
  log P(history/property of the first token is inherited by the queried later referent)
  - log P(competing token's history / non-inheritance answer)
```

Bidirectional prediction:

- patch/steer toward **SAME numerical individual** -> increase first-token history transfer;
- patch/steer toward **DIFFERENT individual, same type** -> decrease first-token history transfer.

### H3 — double-dissociation control

The same intervention must **not** simply destroy or increase generic type knowledge.

A separate `TypeKnowledgeLogit` tests facts shared by both same-type objects.

Required pattern:

```text
identity intervention:
  changes token-specific HistoryTransferLogit
  while preserving shared TypeKnowledgeLogit
```

A generic relatedness/coreference/recency direction that changes both is not sufficient.

### H4 — mandatory negative controls

- random matched directions;
- shuffled identity labels;
- explicit lexical-cue (`the` vs `another`) direction;
- noun-repetition direction;
- generic semantic-similarity/type direction;
- generic entity-binding/coreference control where identity is already explicitly indexed.

Primary effects are summarized over a preregistered depth range / held-out layer-selection protocol; no post-hoc best-head story.

---

## I. Story invariance

### Result A — abstract numerical identity

Modern LLMs maintain a cross-surface numerical-identity state, distinct from qualitative similarity, and causally use it to decide which token-specific history persists.

### Result B — local tracking without abstract identity

Models can solve some discourse tracking cases, but the representation does not transfer across cue/domain windows or fails the identity-specific causal double dissociation. Entity tracking is therefore more local/surface-bound than an abstract numerical-identity representation.

### Result C — similarity / cue collapse

After controls, apparent identity sensitivity reduces to determiners, repetition, recency, type similarity or generic binding. Modern LLMs do not robustly separate numerical identity from qualitative sameness on the frozen scope.

All results answer the same question. None permits a pivot to `best identity head`, `coreference benchmark`, or generic entity-tracking paper.

---

## J. Fatal controls / hard kills

1. **New direct collision:** a 2024–2026 modern LLM paper is found that explicitly factorizes numerical identity vs qualitative sameness and causally studies it -> `KILL-NOVELTY`.
2. **RNN collapse:** only the original event-specific `the` vs `another` effect survives, with no cross-surface abstraction or identity-specific causal use -> `KILL-NOVELTY` relative to Davis–Altmann.
3. **Lexical cue collapse:** identity effect vanishes outside the determiner/wording family used for discovery -> `KILL-LEXICAL-CUE`.
4. **Coreference collapse:** the same mechanism is fully explained by a generic already-indexed coreference/binding signal and cannot distinguish same-token-changed from different-token-same-type -> `KILL-IDENTIFIABILITY`.
5. **Similarity collapse:** different-token same-type cases are treated as same solely according to semantic/type similarity -> no abstract identity claim.
6. **No causal specificity:** intervention changes generic type knowledge as much as token-specific history -> no numerical-identity causal claim.
7. **Best-layer-only result:** only a localized neuron/head effect remains -> `KILL-SCALE`.
8. **Architecture fishing prohibited:** dLLM/Mamba/RWKV results may strengthen generality but cannot rescue a failed AR-LM identity claim by changing the headline.

---

## K. Venue-scale comparison

- **NAACL 2025 property inference / taxonomy vs similarity:** a simple, externally real cognitive distinction is isolated and causally analyzed in LMs. 040 similarly separates two notions that ordinary language often conflates.
- **ACL 2026 `Do LLMs Know Tool Irrelevance?`:** semantic relevance is separated from structural matching. 040 separates individual identity from qualitative/type similarity using controlled cross-cases.
- **ACL 2026 Cell-Based Relational Binding:** establishes that modern LLM discourse binding can support a full Main-paper mechanistic story. 040 asks an earlier and distinct question: how the model determines whether two mentions belong to one individual before attributes are bound/propagated.
- **ACL 2025 `Llama See, Llama Do`:** a simple model fact becomes paper-scale through broad evidence, causal mechanism and consequences. 040 follows the same simplicity-first philosophy rather than pre-writing an elaborate architecture theory.

---

## L. Registration verdict

```yaml
route: C
paper_scale: PASS
benchmark_removal: PASS
natural_object: PASS
normal_scope: PASS
human_scientific_object: PASS
natural_double_dissociation: PASS
public_row_level_event_artifact: PASS
N0_modern_direct_object_ownership: PASS
N1_direct_causal_occupancy: PASS
N2_delta_over_RNN_precursor: PASS_WITH_HARD_KILL
N2_delta_over_entity_tracking: PASS_WITH_HARD_KILL
modern_analyzable_open_models: PASS
central_gold_without_llm_judge: PASS
surface_cue_control: FROZEN
identity_vs_type_double_dissociation: FROZEN
causal_use_question: FROZEN
story_invariance: PASS
architecture_generalization: SECONDARY_ONLY
verdict: PASS-REGISTER
GPU_AUTHORIZED: true
```

## One-line freeze

> **040 asks whether modern LLMs represent and causally use numerical identity — being literally the same individual — separately from merely being qualitatively/type-similar. Entity tracking, binding, RNN event sensitivity, dLLM comparison and particular lexical cues are measurement windows or neighbors; none may replace the frozen headline.**
