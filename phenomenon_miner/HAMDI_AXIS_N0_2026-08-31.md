# Hamdi-Style Mother-Inclusion N0 — 2026-08-31

Status: `AUTHORITATIVE CANDIDATE N0 / THREE-IDEA AUDIT`

This audit applies the repository's Natural-Question Gate and a stronger **mother-inclusion test**. The question is not whether a nearby paper exists; the question is whether prior work already occupies the same title-level scientific object, decisive contrast, and most of the mechanism/intervention story.

The three candidates came from the Hamdi-style route:

```text
strong mother / established object
→ identify a natural adjacent conceptual axis or unresolved meaning
→ ask a new scientific question that survives deleting dataset and MI vocabulary
→ exact collision + mother-inclusion audit
→ only survivors may enter active/
```

## Executive verdict

| candidate | N0 verdict | reason |
|---|---|---|
| #1 Alignment: descriptive human model vs normative policy | **PASS — SHARPENED** | broad descriptive/prescriptive behavior is occupied, but the internal *fate of the descriptive social model under alignment* and erasure-vs-reweighting-vs-readout arbitration remain open |
| #2 Superseded truth vs never-true falsehood | **KILL — DIRECT MECHANISM COLLISION** | 2026 *Geometry of Forgetting* already defines temporal drift as an independent representational axis, separates stale recall from confabulation, and adds cross-cutoff, mechanism and steering |
| #3 Actual-world truth vs local-world truth | **PASS — SHARPENED** | generic fictional truth and context-shaped truth are occupied, but the same proposition under two explicitly indexed worlds — simultaneous actual/local truth rather than domain difference or source conflict — remains a distinct object |

---

# 1 — What Does Alignment Change: The Descriptive Social Model or Its Readout?

## Natural question

> Alignment makes models give more normatively approved predictions and decisions. Does it actually erase or distort what the model knows about how people really behave, or does that descriptive social model remain intact while another normative signal wins at the output?

Ordinary example:

> In a repeated bargaining game, a model may know that a person who was just treated unfairly will retaliate, while also knowing that cooperation/fairness is the normatively preferred action. After alignment, which of these two internal objects changes?

This question is interesting before mentioning probes, heads, datasets or steering. It is a classic descriptive-vs-normative distinction in behavioral science, now turned into a concrete question about what post-training changes internally.

## Strong mothers and strongest neighbors

### A. Alignment Makes Language Models Normative, Not Descriptive — 2026

This mother already establishes the behavioral transformation at scale:

- 120 same-provider base/aligned pairs;
- >10,000 real human decisions;
- multi-round bargaining, persuasion, negotiation and repeated matrix games;
- base models much more often predict observed human behavior better in strategic multi-round settings;
- aligned models do better in settings where normative solutions approximate behavior.

What it **does not establish** is whether alignment destroys descriptive human-behavior knowledge, adds/strengthens a normative representation, or changes late arbitration/readout.

Reference: https://arxiv.org/abs/2603.17218

### B. A Theory of Response Sampling in LLMs: Part Descriptive and Part Prescriptive — ACL 2025 Main

This is the most dangerous inclusion neighbor. It already argues that LLM outputs combine:

- a descriptive/statistical component;
- a prescriptive/ideal component.

It evaluates pretrained and instruction-tuned Llama variants and reports stronger prescriptive influence under RLHF / instruction tuning. Therefore the following are **not novel claims**:

- LLM outputs contain both descriptive and prescriptive influence;
- post-training can increase prescriptive influence;
- observed samples can move from a statistical norm toward an ideal.

Crucially, the paper remains an output-level theory/behavioral analysis. Its limitations explicitly leave the origin of the prescriptive signal and mechanistic analysis open. It does not trace paired base→aligned hidden-state transformations of human-behavior knowledge or adjudicate erasure vs retained-knowledge/readout arbitration.

Reference: https://aclanthology.org/2025.acl-long.1454/

### C. What Do Large Language Models Know About Opinions? — ICLR 2026

This work is a second major constraint. It shows that internal knowledge of group opinions can exceed emitted answers, identifies middle-layer signals / late bottlenecks and performs causal steering.

Therefore **generic** `the model knows the social fact internally but output fails to use it` is not novel.

Our question must specifically concern **two competing targets under alignment** — observed human behavior and normative policy — and how paired base→aligned transformation changes their representations and arbitration.

## Why this is not a rename

The surviving object is not:

> descriptive and normative norms both affect LLMs.

That is occupied.

It is:

> **When alignment shifts behavior from descriptive toward normative predictions, what internal quantity changed?**

Three mechanisms make different predictions:

### H1 — Descriptive-model degradation / erasure

The aligned model becomes worse because the internal representation of likely human behavior itself becomes less accurate.

Prediction: a descriptive readout trained/evaluated on real human choices degrades before or independently of the final answer layer; base→aligned activation differences reduce recoverability of human-action information.

### H2 — Dual retention + stronger normative state

Descriptive information remains available, while alignment strengthens a separate normative/ideal representation.

Prediction: both descriptive and normative targets remain decodable; aligned models increase the normative signal without destroying descriptive decodability.

### H3 — Late arbitration / readout change

Both states are already present in base and aligned models, but post-training changes which one controls the final answer.

Prediction: descriptive representations remain comparable, while a late layer / writer / readout shifts the output toward normative responses; selective intervention can restore descriptive prediction without broadly degrading competence.

These are not cosmetic distinctions. They imply different interpretations of alignment and different fixes for LLM-as-human-simulator use.

## Mother-inclusion decision

`PASS — SHARPENED`.

The broad descriptive/prescriptive object is already occupied by ACL 2025. The behavior-level alignment trade-off is occupied by the 2026 mother. The new paper must therefore be explicitly framed as **mechanistic decomposition of what alignment changes in the social model**, not discovery of descriptive/normative bias.

## Data / first empirical object

Data should come from the mother paper or public behavioral-game datasets wherever possible. The question precedes the data.

Preferred structure:

```text
same game state s
human empirical next-action distribution D_human(s)
normative / equilibrium / approved action N(s)
base model M_base
aligned counterpart M_align
```

High-value subset is not a researcher-invented rare cell. It is the natural disagreement region where `D_human` and `N` diverge — exactly the region that defines descriptive-vs-normative behavioral science.

First behavior reproduction must confirm the mother effect on at least one open-weight base/aligned family before MI.

## Mechanistic ladder if reproduction passes

1. Paired base/aligned representational comparison for human-action prediction vs normative-action prediction.
2. Cross-task generalization: bargaining / repeated games / social dilemmas.
3. Layerwise fate analysis: where descriptive information changes and where normative information increases.
4. Causal interchange or subspace intervention only after two signals are behaviorally anchored.
5. Test whether restoring the base descriptive state repairs human-behavior prediction while preserving unrelated aligned capabilities.

## Hard kill / route rules

- `KILL_MOTHER_INCLUSION`: if a new/full version of the 2026 mother already performs paired hidden-state erasure-vs-readout analysis.
- `KILL_GENERIC_KNOWS_BUT_NOT_USE`: if the only result is internal human-behavior decodability > output accuracy.
- `KILL_NO_DUAL_TARGET`: if normative and descriptive labels are not independently defined on the same states.
- `KILL_NO_ALIGNMENT_TRANSFORMATION`: if base/aligned internal differences do not track the behavioral trade-off.
- `ROUTE_RESPONSE_SAMPLING`: if results reduce to the ACL 2025 descriptive/prescriptive sampling coefficient without a new internal causal object.

---

# 2 — Superseded Truth vs Never-True Falsehood

## Natural question

> "Angela Merkel is Germany's chancellor" is false now but was once true. "Angela Merkel is Japan's prime minister" was never true. Does a model internally distinguish these two kinds of falsehood?

The natural question is excellent. **The topic is nevertheless dead because the exact mechanistic object is already occupied.**

## Direct external collision

### The Geometry of Forgetting: Temporal Knowledge Drift as an Independent Axis in LLM Representations — 2026

The paper already makes the title-level claim we wanted:

- temporal drift / temporal validity is an internal residual-stream direction;
- it is geometrically independent of correctness and uncertainty;
- six instruction-tuned models;
- controlled AUROC 0.83–0.95;
- cross-cutoff experiment on byte-identical inputs;
- stale recall is explicitly separated from confabulation;
- a dedicated stale-recall-vs-confabulation probe reaches high AUROC;
- MLP retrieval dynamics and causal steering are analyzed.

Reference: https://arxiv.org/abs/2605.09195

Their `STALE-RECALL` vs `CONFABULATION` distinction already captures the core difference between a stored formerly-valid answer and an answer with no valid holder in the relevant timeline. The paper further calls temporal validity a third representational property independent from correctness and uncertainty.

That occupies not merely the mother phenomenon but the **new axis + representation + independence + mechanism/intervention package**.

## Internal F3 / state-update attack

This candidate is also not rescued by local history.

The repository already treats current-state/history and state-update questions as a broad mother family. Relevant internal negative knowledge includes:

- generic correction/retraction / misinformation continued-influence stories are already too crowded to revive without a new causal state-update object;
- `candidate_topics` Topic 26 studies historical temporal scope vs present-day pull and was stopped for artifact support, not because temporal state is a new untouched object;
- older temporal-access routes (e.g. Topic 05) demonstrate that changing the operationalization does not create a new scientific axis.

Even if we renamed the proposed target `superseded tag`, `historical validity`, `former truth`, or `current-state marker`, it would remain inside the same temporal-validity/state-update mother object and directly overlap the 2026 drift paper.

## Verdict

`KILL — DIRECT_MECHANISM_COLLISION + INTERNAL_FAMILY_INCLUSION`.

Do not register. Do not resurrect via Wikidata, office-holder facts, fact editing, model cutoff, or a different truth probe.

A resurrection would require a genuinely different natural object not captured by temporal validity itself — not merely another stale/current dataset.

---

# 3 — World-Indexed Truth: Actual Reality vs the Currently Stipulated World

## Natural question

> A sentence can be false in the real world and true inside a story, game, hypothetical, or explicitly stipulated scenario. Does a language model represent truth as a property of the proposition alone, or as a relation between a proposition and the world in which it is being evaluated?

Ordinary example:

> In reality, Paris is in France. In a hypothetical story we explicitly stipulate that Paris is in Germany. A competent model should be able to say both "in the story, Paris is in Germany" and "in reality, Paris is in France" without one truth value erasing the other.

This is a natural semantic distinction independent of any benchmark and has a direct MI question: does the model keep two truth statuses bound to two world indices, or overwrite/re-route a single truth state?

## Strong mothers and strongest neighbors

### A. How Context Shapes Truth — ACL 2026 Main

This mother shows that adding context geometrically transforms statement-level truth representations and that context conflicting with parametric knowledge causes larger changes than aligned context.

It occupies:

- context changes truth-vector geometry;
- context-vs-parametric conflict produces larger representational change.

It does **not** frame or test simultaneous truth of the same proposition relative to two explicitly licensed worlds. It treats context as evidence affecting statement truth, not as a world index under which a different truth valuation is valid.

Reference: https://aclanthology.org/2026.acl-long.1695/

### B. The Truthfulness Spectrum Hypothesis — 2026

This is the most dangerous broad truth-representation neighbor. It studies definitional, empirical, logical, fictional and ethical truth and shows domain-general plus domain-specific truth directions, concept erasure and causal steering.

Therefore the following are **not novel**:

- fictional truth differs geometrically from empirical truth;
- multiple truth directions exist;
- fictional-domain truth can have a domain-specific causal direction.

Our candidate survives only because its unit is different:

```text
not: truth_type ∈ {empirical, fictional, logical, ...}

but: the SAME proposition P
     evaluated under world w_actual
     and world w_local
```

The proposed object is **world binding / indexing of truth**, not truth-domain geometry.

Reference: https://arxiv.org/abs/2602.20273

### C. Language Models Use Lookbacks to Track Beliefs — ICLR 2026

This work reverse-engineers character-belief tracking using character-object-state bindings and lookback mechanisms. It shows models can bind mental-state content to agents.

That is adjacent because beliefs can differ from reality, but it does not study narrator/world truth or the same proposition's truth value under an actual vs stipulated-world index. A character's false belief is not the same semantic object as a proposition being true in a licensed hypothetical world.

Reference: https://arxiv.org/abs/2505.14685

### D. Context/parametric knowledge-conflict literature

Large literature asks whether models follow supplied context or parametric memory when they conflict. This candidate is **not** allowed to collapse into that question.

A local-world statement must be explicitly licensed as local truth (`In this story...`, `Under the following hypothetical...`), while an actual-world query remains simultaneously answerable. The scientific object is not "which source wins?" but "can both valuations coexist under different world indices?"

## Why this is not a rename

A standard context-conflict experiment has one operational target: choose context or memory.

A world-indexed truth experiment has two simultaneously valid answers:

```text
T(P, w_actual) = false
T(P, w_local)  = true
```

or the reverse.

The decisive property is **coexistence without overwrite**. The model should be able to switch query world while leaving proposition wording and local context fixed.

Three mechanism families:

### H1 — Truth overwrite

Local context rewrites the proposition-level truth state. Asking reality later requires reconstructing parametric truth or may fail.

### H2 — Dual valuation with world binding

The model preserves both valuations and binds each to a world/context representation. Querying a world selects the corresponding truth state.

### H3 — Single proposition state + late task routing

The internal proposition representation may not carry world-indexed truth; a late reader uses the query frame and retrieves the relevant evidence/source.

These predictions can be separated by matched query-world swaps and causal interchange once behavior is established.

## Mother-inclusion decision

`PASS — SHARPENED`.

The candidate is novel only under the world-indexed formulation. Generic fictional truth, generic truth-domain geometry, or parametric-vs-context conflict would be immediate ROUTE/KILL.

## Data / first empirical object

Do not begin by mining a benchmark-specific rare subset. Start with a small, transparent 2×2 sanity bank where world truth is deterministic by construction, then move to a natural source of story/game rules if the object is visible.

Minimal structure:

```text
proposition P
actual-world truth A(P)
explicit local-world stipulation L(P)
A(P) != L(P)

Query_actual(P, same context)
Query_local(P, same context)
```

Controls should include:

- actual/local aligned cases (`A(P)=L(P)`);
- label/order paraphrases;
- same local world with query-world swap;
- reverse polarity (`actual true/local false` and `actual false/local true`).

The headline phenomenon does not require model failure. A clean internal double representation is itself a publishable scientific answer if it is causal and general.

## Mechanistic ladder if behavior/capability passes

1. Confirm model can answer both world-indexed queries reliably on matched propositions.
2. Probe/geometry only to ask whether actual and local truth are simultaneously present; avoid training two unrelated domain probes and calling them axes.
3. Cross-world activation interchange: change world pointer/query while holding proposition content fixed.
4. Identify whether a world-selection state acts as reader/pointer for a truth representation.
5. Test causal double dissociation: manipulate world index without globally flipping proposition truth, and manipulate proposition truth within one world without changing the other.
6. Generalize across explicit hypotheticals, fictional settings and rule-governed mini-worlds.

## Hard kill / route rules

- `ROUTE_TRUTH_SPECTRUM`: if the result is only "fictional and empirical truth probes differ".
- `ROUTE_CONTEXT_CONFLICT`: if the result is only "the model follows context over memory".
- `ROUTE_TOM_BELIEF`: if the construct becomes agent belief rather than world-relative truth.
- `KILL_NO_COEXISTENCE`: if the model only stores one currently dominant truth value and no meaningful world-indexed computation can be identified beyond source selection.
- `KILL_NO_CAUSAL_BINDING`: if world identity is merely decodable but interventions do not selectively change world-relative evaluation.

---

# Final registration decision

Under this N0:

```text
#1 PASS → register with narrowed alignment-transformation claim
#2 KILL → rejected_candidates only
#3 PASS → register with world-indexed truth claim
```

Neither survivor is authorized for immediate full MI. Registration means the scientific object passed N0; the next stage is a small, frozen behavioral/capability reproduction and data-contract audit before expensive mechanism work.
