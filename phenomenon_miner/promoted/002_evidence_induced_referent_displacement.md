# Promoted phenomenon 002: Evidence-Induced Referent Displacement

Status: `PROMOTE TO CONFIRMATORY BEHAVIOR + MECHANISTIC PILOT`
Date: 2026-08-27

## One-sentence phenomenon

After a model has correctly identified the entity being described, one more
truthful, relevant, human-written clue about that entity can make the model
answer with a *related participant, part, product, character, or neighboring
concept* instead; a later clue often restores the original correct answer.

In plain language:

> The model already knows who the question is about. Tell it one more true fact
> about that person and somebody mentioned in the fact can become the new
> answer.

The working name is **Evidence-Induced Referent Displacement (EIRD)**. A more
specific mechanistic name, if the causal tests support it, is **answer-slot
rebinding**.

## Why this is natural rather than constructed

- The text comes unchanged from questions written by expert human quizbowl
  authors.
- The progression is native to the task: the same question is heard one clue at
  a time.
- There are no invented worlds, arbitrary symbols, options, synthetic
  distractors, or model-written transformations.
- Each added clue is true of the same gold answer and was written to help a
  human identify it.
- Evaluation is free generation, not direct choice.

The broken expectation is extremely simple: after the answer has become
identifiable, another correct clue should not change *what the question is
about*.

## Discovery panel

The first sweep used all 3,042 native prefixes from 782 Protobowl questions
(2011–2013). Current local models were run deterministically with an
answer-only free-generation prompt:

- Qwen3-4B, Qwen3-8B, Qwen3-14B;
- Gemma3-4B, Gemma3-12B;
- Phi-4-mini.

The independent historical response archive added:

- Gemma-1.1-2B and 7B;
- Llama-3-8B and Llama-3-70B-Instruct;
- Mistral-7B-Instruct;
- Cohere Command-R-Plus;
- GPT-3.5-Turbo and GPT-4o.

This gives six newly run current models plus eight archived models, spanning
Qwen, Gemma, Phi, Llama, Mistral, Cohere, and OpenAI families. Historical
scores are used only where the released scorer marks the transition; newly run
outputs are kept verbatim for semantic audit.

## Canonical untouched examples

All arrows below are successive native clue prefixes. No answer options were
shown.

| Gold and new truthful clue | Structured displacement | Models showing the trajectory |
|---|---|---|
| **Goliath**; next clue says he is challenged by Jesse's son | `Goliath → David → Goliath` | Qwen3-4B, Phi-4-mini, Gemma-1.1-7B, Mistral-7B |
| **Mozilla**; next clue describes its popular browser product | `Mozilla → Firefox → Mozilla` | Qwen3-4B, Phi-4-mini, Cohere Command-R-Plus |
| **Kim Jong-un**; next clue discusses his missiles reaching the US | `Kim Jong-un → North Korea / nuclear missiles → Kim Jong-un` | Qwen3-8B, Gemma3-4B, Phi-4-mini |
| **Sagittarius**; next clue describes its brightest star and asterism | `Sagittarius → Centaurus / Crux / Cancer → Sagittarius` | Phi-4-mini, Gemma3-4B, Gemma3-12B; archived Mistral-7B also flips and recovers |
| **Pride and Prejudice**; next clue narrates characters at a ball | `work → Mr. Collins / George Wickham → work` | Qwen3-4B, Gemma3-4B |
| **Watership Down**; next clue says the protagonists are rabbits | `work → warren / rabbits → work` | Qwen3-4B, Gemma3-12B |
| **Hera**; next clue describes Io and her husband | `Hera → Io / Aphrodite → Hera` | Qwen3-4B, Gemma3-4B |
| **Mount Rushmore**; next clue compares it with Stone Mountain | `Mount Rushmore → Stone Mountain → Mount Rushmore` | Qwen3-8B, Gemma-1.1-7B, Llama-3-8B, Llama-3-70B |

The exact wrong answer need not be copied from the clue. For example, a clue
that should further disambiguate William Jennings Bryan made Gemma3-12B and an
archived Mistral-7B both produce **Robert Lansing**, the neighboring Secretary
of State association, before the next clue restored Bryan. That observation is
important: EIRD is not reducible to token recency or literal copying.

## Held-out source replication

After naming the candidate, the same untouched-prefix sweep was run on a
separate source: 300 questions (2,039 clue prefixes) from the 2024 Chicago Open
dataset. These questions are more than a decade newer and substantially harder
than Protobowl 2011–2013.

With a deliberately simple machine filter—correct at prefix *t*, a
substantially different lexical answer at *t+1*, and recovery at a later
prefix—the held-out sweep returned:

| Model | Machine-filtered correct→wrong→later-correct candidates |
|---|---:|
| Qwen3-4B | 14 |
| Gemma3-4B | 13 |
| Phi-4-mini | 21 |

These are **candidate counts, not final prevalence estimates**. They require a
registered human semantic audit because short-answer aliases can fool exact
matching. Manual inspection already finds the same structured phenotype, for
example:

- `thymic epithelial cells → cytotoxic T cells → thymic epithelial cells`
  after a clue about the cells presenting antigens to developing lymphocytes;
- `granular materials → Janssen model → granular materials` after a clue about
  a model of those materials;
- `King Harsha → Pulakeshin II → King Harsha` after a clue placing Harsha's
  empire relative to the Chalukyas;
- `spectral theorem → resolution of the identity → spectral theorem` after a
  clue describing what the theorem induces;
- `rule of law → liberalism / legitimacy → rule of law` in both Qwen and Gemma
  after an abstract relational clue.

Thus the candidate is not tied to a single old dataset, domain, family, or
answer type.

## What makes the error a phenotype rather than generic non-monotonicity

The key dependent variable is not merely accuracy loss. It is the destination
of the changed answer.

The new answer typically occupies a predictable structural relation to the
gold:

- agent ↔ patient or opponent (`Goliath → David`);
- organization ↔ product (`Mozilla → Firefox`);
- whole ↔ part or member (`Watership Down → rabbits`);
- work ↔ character (`Pride and Prejudice → Mr. Collins`);
- class ↔ instance (`black holes → Sagittarius A*` in an archived model);
- entity ↔ attribute, consequence, method, or neighboring association.

This suggests that additional evidence does not simply erase knowledge. It can
preserve local semantic content while changing which node is bound to the
answer slot.

## Distinction from nearby mother phenomena

- **Not ordinary distractor sensitivity:** the added sentence is relevant,
  truthful supporting evidence, not an irrelevant or adversarial document.
- **Not knowledge conflict:** no statement contradicts the gold answer.
- **Not Lost in the Middle:** contexts are short, and the critical change is a
  single adjacent clue.
- **Not generic recency or copying:** some displaced answers are inferred
  neighbors not present in the new clue, and the wrong entity is structurally
  related to the gold.
- **Not CoT Answer Drift:** no chain of thought is requested or supplied. The
  nearest literature defines Answer Drift as a final answer inconsistent with
  an otherwise correct generated rationale; EIRD is triggered by external
  human evidence and changes the referent itself.
- **Not merely incremental-QA difficulty:** the published Quizbowl work studies
  guessing and buzzing curves, but the exact correct→related-node→correct
  trajectory and its internal binding mechanism are not its stated object.

An exact-scope literature audit is still required before claiming novelty.
Current searches did not locate a paper centered on this phenotype.

## Mechanistic opening

The central question is clean:

> Does the model lose the representation of the original answer, or does it
> retain that representation while rebinding the output/answer slot to the
> newly salient related entity?

This produces a strong causal program:

1. **Matched activation trajectories:** compare stable `A→A`, displacement
   `A→B`, and recovery `A→B→A` prefixes from the same human question.
2. **Answer and role probes:** separately decode the gold entity, new entity,
   target answer type, and semantic role across layers and token positions.
3. **Activation patching:** patch the stable-prefix state into the displacement
   prefix at the new clue tokens, final token, and candidate-entity token
   positions.
4. **Causal head search:** locate heads that preserve the discourse target
   versus heads that route the most recently activated relation argument to the
   output.
5. **Matched interchange:** swap representations of the gold and related node
   while holding the human clue and query fixed; test whether the output follows
   the patched binding rather than entity familiarity.
6. **Representation/readout dissociation:** if the gold remains linearly
   decodable during a wrong answer and a small intervention restores it, the
   phenomenon becomes substantially stronger than a generic knowledge failure.

## Confirmatory behavioral design

Keep the primary dataset natural. Use edits only as secondary causal controls:

- mask or pronominalize the related entity;
- preserve the fact while reversing surface mention order;
- add an equally long true clue with no new relation participant;
- explicitly restate the target type (`name the person`, `name the work`) only
  as a diagnostic rescue;
- separate literal-copy displacement from inferred-neighbor displacement;
- stratify agent–patient, whole–part, organization–product, work–character,
  class–instance, and abstract concept–consequence relations.

The preregistered primary statistic should be:

`P(correct_t → related-wrong_{t+1} | correct_t, truthful relational clue)`

against matched non-relational true-clue transitions, with per-question paired
tests and mixed effects over model family, size, domain, and relation type.

## Current caveats

- Discovery is post hoc; the held-out source must receive a blinded semantic
  audit before reporting prevalence.
- Exact-match scoring produces false alarms for aliases, singular/plural forms,
  and accepted subtypes. All promoted examples above were inspected as semantic
  answer changes.
- Larger models are often more robust on individual items; generality here
  means that the structured failure recurs across families and sizes, not that
  every model flips on every clue.
- Quizbowl is natural expert-authored language but still a trivia genre. A
  second non-quizbowl replication (incremental biography, RAG, or dialogue
  reference tracking) would materially strengthen the claim.

## Decision

EIRD clears the current discovery gate better than the earlier constructed
spatial candidate:

- natural human source text;
- a one-sentence, surprising behavioral claim;
- free-generation evidence;
- recurrence across families, sizes, years, and domains;
- structured rather than random errors;
- a sharp representation-versus-binding mechanism question;
- provisional room between generic evidence distraction and CoT answer drift.

Next work should be confirmatory scoring and causal localization—not more
phenomenon naming.
