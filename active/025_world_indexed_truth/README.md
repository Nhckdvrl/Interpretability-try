# 025 — World-Indexed Truth: Actual Reality vs the Stipulated World

**Status:** `N0-PASS / HOLD_PREREQUISITE_CAPABILITY / NO-MI`
**Created:** 2026-08-31  
**Selection route:** Hamdi-style adjacent-axis extension  
**Priority:** high exploratory candidate; do not start MI until a simple world-indexed capability/behavior contract is frozen.

## 1. The question in plain language

> A sentence can be false in the real world and true inside a story, game, hypothetical, or explicitly stipulated scenario. Does a language model represent truth as a property of the sentence alone, or as a relation between the sentence and the world in which it is evaluated?

Simple example:

> In reality, Paris is in France. Suppose a story explicitly says that in its world Paris is in Germany. A competent model should be able to maintain both statements: “in the story, Paris is in Germany” and “in reality, Paris is in France.” Does it internally keep two world-bound truth values, or does the local context overwrite one global truth state?

This is a standard semantic distinction, not a benchmark trick. The research question remains interesting if every dataset name is deleted.

## 2. Why this is Hamdi-style rather than benchmark mining

Hamdi's ontology project takes an existing epistemic object — whether the model knows an entity — and asks about a nearby but conceptually independent object — whether the entity exists. This project has the same desired structure:

```text
existing truth-representation work
→ truth is usually treated as a property of a statement/domain
→ natural missing object: truth relative to a world/context index
```

The goal is not to find another failure caused by misleading context. The question is whether the model internally represents the semantic relation:

```text
Truth(proposition, world)
```

rather than only a proposition-level true/false score.

## 3. Strongest neighbors and novelty boundary

### 3.1 How Context Shapes Truth — ACL 2026 Main

This mother studies statement-level truth vectors before and after adding context. It shows:

- context changes truth-vector direction and magnitude;
- relevant and irrelevant context produce different geometric transformations;
- context conflicting with parametric knowledge causes larger changes than aligned context.

Reference: https://aclanthology.org/2026.acl-long.1695/

Therefore **we cannot claim**:

- first work on context changing internal truth representations;
- first hidden-state analysis of parametric/contextual knowledge conflict;
- first evidence that context can rotate/amplify truth vectors.

The surviving question is different: the local context does not merely provide competing evidence about one world. It explicitly defines another evaluation world in which a different truth value is legitimate, while the real-world truth remains simultaneously queryable.

### 3.2 The Truthfulness Spectrum Hypothesis — 2026

This paper is a direct threat to any broad “different kinds of truth have different representations” story. It tests:

- definitional truth;
- empirical truth;
- logical truth;
- fictional truth;
- ethical truth;
- additional lying/honesty settings.

It finds domain-general and domain-specific truth directions, concept-erasure results and causal steering.

Reference: https://arxiv.org/abs/2602.20273

Therefore **the following claims are dead**:

- fictional truth has its own direction;
- empirical and fictional truth are geometrically different;
- there are multiple truth notions in LLM representations.

Our unit of analysis must be the **same proposition under two world indices**, not two corpora/domains of statements.

### 3.3 Language Models Use Lookbacks to Track Beliefs — ICLR 2026

This work reverse-engineers how models bind character-object-state information to individual agents and retrieve belief states that can differ from reality.

Reference: https://arxiv.org/abs/2505.14685

It is adjacent because agent beliefs can be false relative to reality. But:

```text
character believes P
```

is not the same semantic relation as:

```text
P is true in stipulated world W
```

A belief is a mental state indexed to an agent; a fictional/hypothetical world's truth conditions are licensed by the discourse/game/world itself. If this project degenerates into ToM belief tracking, route it immediately.

### 3.4 Parametric-vs-context conflict literature

There is extensive work on whether a model follows conflicting context or parametric memory. That is not our title-level question.

Ordinary conflict:

```text
memory says P
context says not-P
which source wins?
```

World-indexed truth:

```text
P has truth value v1 in actual world
P has truth value v2 in explicitly stipulated local world
both are legitimate answers depending on query index
```

A successful model should **not resolve the conflict by choosing one source**. It should preserve both and answer according to the requested world.

## 4. Exact N0 novelty claim

Allowed working claim:

> **We study whether LLM truth representations are world-indexed: can the same proposition carry simultaneously accessible but different truth values for actual reality and an explicitly stipulated local world, and what internal mechanism binds/selects the relevant valuation?**

Not allowed:

- first fictional truth representation;
- first multiple truth directions;
- first context-vs-parametric conflict representation;
- generic role-playing / “models can play along”;
- generic story comprehension.

## 5. Why MI is necessary rather than decorative

Behavior alone can show that a model switches answers when asked “in the story?” versus “in reality?”. That does not tell us what it represents internally.

Three qualitatively different computations can produce identical correct behavior.

### H1 — Overwrite + reconstruction

The local stipulation overwrites the proposition's current truth state. When asked about reality, the model reconstructs/retrieves the original parametric answer again.

### H2 — Dual world-bound valuation

Both actual and local truth values coexist, each bound to a world representation/pointer. Querying the world selects the matching value.

### H3 — Source/task routing without world-indexed truth

The model keeps source information (“context says X”, “memory says Y”) and a late task router chooses which source to trust; there is no genuine world-bound truth state.

These explanations make different causal predictions. Distinguishing H2 from H3 is the core interpretability contribution.

## 6. D0 philosophy: first prove capability, not a contrived failure

Unlike the failed Top-6 topics, this project does **not require a new behavioral failure to exist**. A clean positive finding that models maintain world-indexed truth would itself be scientifically interesting.

The first stage should therefore establish a simple capability object, not search for a rare error subset.

### Minimal deterministic schema

For proposition `P`:

```text
A(P) = actual-world truth
L(P) = local-world truth under explicit stipulation
require A(P) != L(P)
```

With the **same local-world context held fixed**, ask:

```text
Q_actual: In the real world, is P true?
Q_local:  In the stipulated story/world, is P true?
```

Both answers are gold by construction/source truth.

Balanced polarity:

- actual true / local false;
- actual false / local true.

Aligned controls:

- actual true / local true;
- actual false / local false.

The key prerequisite is that open models can reliably answer both query indices without elaborate prompting.

## 7. Data options

Dataset must remain an instrument. Prefer a mix of very transparent programmatic worlds and natural story/game worlds.

### A. Minimal controlled worlds

Use common real-world facts with a single explicit counterfactual stipulation:

> “For the following hypothetical only, assume that Paris is in Germany.”

Gold actual truth comes from a trusted factual source; local truth is deterministic from the stipulation.

This is acceptable because the conceptual variable — world index — exists before the generated example, and construction is direct rather than a five-condition rare filter.

### B. Fiction / game-rule worlds

Use propositions whose local truth is established by canonical fictional/game text while actual-world truth is independently known. This provides natural-world confirmation after the clean controlled stage.

### C. Avoid

- adversarial misinformation passages pretending to be factual evidence;
- false-premise QA where only one answer is considered correct;
- character-belief datasets where the index is an agent rather than a world;
- comparing unrelated empirical statements to unrelated fictional statements.

Those would change the question.

## 8. Behavioral/capability gate before MI

A frozen pilot must show that at least one open model has strong paired competence:

```text
same P + same local context
Q_actual correct
AND
Q_local correct
```

across both polarity directions and more than one domain/world type.

If models simply cannot follow explicit hypothetical indexing, `HOLD_PREREQUISITE_CAPABILITY`; do not weaken the world distinction until it becomes solvable.

If behavior is nearly perfect, that is **good**, not a problem: we can then study how the internal computation succeeds.

## 9. Mechanistic program

### M1 — Same-proposition paired representations

The central analysis must compare **the same proposition** across query-world conditions. Avoid training one probe on empirical facts and another on fictional facts.

Ask whether actual/local truth values are simultaneously recoverable from a common context before the final query.

### M2 — World-index representation

Locate candidate representations of the active/requested world or local-world state.

The goal is not simply to decode the word “story”. Controls should transfer across:

- `in this story`;
- `under this hypothetical`;
- `according to these game rules`;
- paraphrases that share no fixed lexical marker.

### M3 — Causal binding / selection

Perform interventions that change world selection while holding proposition content fixed.

Strong evidence for H2 would look like:

```text
change world-selection state
→ local/actual truth readout switches selectively
→ proposition content and unrelated facts stay stable
```

### M4 — Double dissociation

Aim for two interventions:

1. alter/select world index without globally flipping proposition truth;
2. alter proposition truth within one world without changing the other world's valuation.

A true double dissociation would make the world-indexed story much stronger than generic context routing.

### M5 — Generalization

Replicate the mechanism across:

- simple explicit counterfactuals;
- fictional/story worlds;
- rule-governed mini-worlds.

The mechanism need not be identical in every domain, but the core world-binding operation must generalize beyond one prompt template.

## 10. Fatal controls

- **Same proposition:** actual/local comparisons must not use unrelated statements.
- **Same context:** query-world contrast should hold local-world context fixed.
- **Source conflict control:** distinguish “which source is trusted” from “which world is queried”.
- **Lexical-index control:** world decoding must generalize beyond fixed words such as `real` and `story`.
- **Role-play control:** merely obeying `pretend X` at output is not evidence for internal dual valuation.
- **Belief control:** character belief and world truth must stay conceptually separate.

## 11. Hard kill / route rules

- `ROUTE_TRUTH_SPECTRUM`: only result is empirical-vs-fictional probe geometry.
- `ROUTE_CONTEXT_TRUTH`: only result is context rotates a truth vector.
- `ROUTE_KNOWLEDGE_CONFLICT`: only result is context wins/loses against parametric memory.
- `ROUTE_TOM`: object becomes agent-specific belief tracking.
- `KILL_NO_WORLD_BINDING`: world label is decodable but causal tests reveal only ordinary source/task routing.
- `KILL_NO_SELECTIVITY`: interventions globally change truthfulness or compliance rather than the requested world valuation.
- `KILL_TEMPLATE_ONLY`: result depends on a single lexical frame and does not transfer to paraphrases/world types.

## 12. N0 verdict

```yaml
natural_question_gate: PASS
mother_inclusion_n0: PASS_SHARPENED
external_concept_anchor: possible-world / world-relative truth
novelty_claim: same-proposition world-indexed truth representation and causal selection
screening_authorized: false
mechanism_authorized: false
```

The minimal 2×2 capability/data contract is now frozen as
[`configs/d0_contract.json`](configs/d0_contract.json). It contains 64 audited
propositions, aligned and conflicting local valuations, paired actual/local
queries under three world frames and three paraphrase families, for 256 scored
queries total. D0 behavior is authorized; representation work remains forbidden
until the predeclared four-family gate passes.

## D0 outcome (2026-08-31)

Both frozen runs returned `HOLD_PREREQUISITE_CAPABILITY`. The sub-2B v1 had no
family pass. In the models-only strong-checkpoint v2, Qwen3-8B, Gemma3-12B,
Llama3.1-8B, and Mistral-Small-24B all showed high conflict joint accuracy
(0.828–0.922) but failed aligned controls (0.219–0.625). This exposes a
conflict-only false positive compatible with contrast/anti-copy routing rather
than dual world-bound valuation. Full results and adjudication are in
[`D0_REPORT.md`](D0_REPORT.md). No mechanism work is authorized.

Full N0: [`../../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md`](../../phenomenon_miner/HAMDI_AXIS_N0_2026-08-31.md).
