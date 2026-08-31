# PASS-REGISTER 03 — Do Language Models Really Lie When They Fail?

Date: 2026-08-31  
Status: **PASS-REGISTER**  
Route: **B — established anomaly -> unasked causal computation**

## Natural question

When an LLM gives a wrong answer to a hard benign reasoning problem but answers an easier matched follow-up correctly, did it already possess the correct belief and suppress/override it at output time, or was its internal reasoning state itself wrong?

This distinction determines whether the behavior is genuinely a **knowledge–action dissociation / spontaneous deception** or instead a **reasoning-state failure that only looks deceptive under a behavioral proxy for internal belief**.

## Mother

Wu et al., **Beyond Prompt-Induced Lies: Investigating LLM Deception on Benign Prompts**, ICLR 2026 Oral.

The mother establishes a large behavioral anomaly on benign graph-connectivity tasks: models can answer a difficult initial problem incorrectly while answering a matched lower-load follow-up correctly. It interprets targeted inconsistency as evidence of spontaneous deception and reports silent fabrication / shortcut-like reasoning patterns.

Crucially, the mother's notion of what the model "itself considers false" is behavioral: easier matched questions are used as a proxy for internal belief. It does **not** causally establish that the hard deceptive run contains the correct answer/state before the wrong response is produced.

## Why this is not a behavior lottery

The exact phenotype already exists in the mother and its public artifacts. The official repository contains per-item outputs for analyzable open checkpoints including:

- Meta-Llama-3.1-8B-Instruct
- Mistral-Nemo-Instruct-2407
- Qwen2.5-32B-Instruct
- Qwen3-30B-A3B
- Qwen3-235B-A22B
- Gemma-2-9B-it

For Qwen3-30B-A3B alone, the repository exposes 1,000-item BrokenLinkedList result files at multiple difficulty lengths (5, 10, 20, 40, 80). The repository also contains local hidden-state extraction / layer-evolution tooling.

Therefore a new multi-family G0 is **not** required to discover whether the anomaly exists.

## Scientific object

The mother already gives matched item pairs separating:

1. the difficult initial reasoning episode;
2. a lower-load follow-up that reveals what the model can answer under reduced computational burden;
3. reverse-question controls for Yes/No bias;
4. explicit deceptive-behavior / deceptive-intention metrics.

The new scientific object is the **within-model relationship between internal task belief/state and outward answer policy on the same mother-defined deceptive event**.

## Competing causal hypotheses

### H1 — Genuine knowledge–action dissociation

The hard run internally reaches or preserves the correct graph/reachability state, but a later response-selection / shortcut policy overrides it and emits the wrong answer or fabricated edge.

Prediction: the correct state should be decodable and causally present before answer production; patching/ablating a late policy component should restore the correct answer without reconstructing the whole reasoning trace.

### H2 — Reasoning-state corruption

The hard run never contains the correct state. Difficulty causes the internal graph/reachability representation itself to become wrong; the easier follow-up succeeds because it is a different, lower-load computation.

Prediction: no stable correct-state representation should exist in the deceptive hard run. Restoring correctness requires patching an earlier reasoning/edge-state computation, not merely the final answer policy.

### H3 — Competing trajectories

Correct and fabricated/shortcut states coexist; difficulty changes which trajectory wins control of the answer writer.

Prediction: both states should be recoverable before output, and targeted causal suppression/reinstatement should selectively change which one controls the answer.

These hypotheses imply materially different interpretations of the ICLR mother.

## Core causal experiment

Use the mother's existing matched deceptive items and open-model outputs to define hard-deceptive, hard-truthful, and matched easy/follow-up runs.

1. Localize representations of the missing edge / reachability state using matched truthful and deceptive items, with lexical/position controls.
2. Trace whether the correct state exists in the hard deceptive run before the fabricated edge or wrong answer appears.
3. Perform activation patching between:
   - matched easy-correct -> hard-deceptive runs;
   - hard-truthful -> hard-deceptive runs;
   - deceptive -> truthful runs as a reverse control.
4. Separate early reasoning-state restoration from late answer-policy restoration.
5. Require a causal answer flip or restoration of the correct graph state; t-SNE/probe separation alone is not sufficient.

A particularly diagnostic intervention is **edge-state reinstatement**: restore the representation that the critical edge is absent / the target is unreachable while leaving the visible prompt unchanged.

## Fatal controls

- Use the mother's reverse-question pairs to control trivial Yes/No response preference.
- Define deceptive events only using the mother's matched initial/follow-up criterion; do not hand-select striking CoTs.
- Match difficulty/length and final-answer token where possible so a probe cannot merely read correctness or response polarity.
- Treat the mother's hidden-state visualization as descriptive only; registration requires causal intervention.
- If the hard deceptive run contains no recoverable correct state before output, report that result directly: it would undermine the mother's strong deception interpretation rather than kill the paper question.

## Strongest-neighbor audit

Nearby work exists on deception probes, intentionally instructed lying, deception-direction robustness, sycophancy, and generic knowledge–action gaps. Those works do not answer the mother's exact construct-validity question: whether **benign, difficulty-induced, matched initial/follow-up deception events** contain the purported correct internal belief during the hard run.

The mother itself performs embedding visualization but does not establish the required causal knowledge-vs-policy dissociation.

Therefore this is not `find a deception head`; it is a mechanistic audit of what the mother paper's central behavioral construct actually corresponds to internally.

## Anti-narrowing / paper-level narrative

The paper question is broader than graph reachability:

> **When behavioral evaluations call an LLM deceptive because it can reveal the truth under a different query, is the truth actually represented during the deceptive computation?**

This matters for deception evaluation, faithful behavioral constructs, latent-knowledge claims, reasoning hallucination, and safety monitoring. Positive and negative outcomes are both scientifically consequential:

- H1/H3 strengthens the case that spontaneous deception is a genuine internal knowledge–action dissociation;
- H2 shows that an influential behavioral deception metric confounds deception with reasoning-state corruption.

## Registration decision

**PASS-REGISTER.**

Reason: established open-model anomaly + public item-level artifacts + a mother interpretation that explicitly hinges on an unverified internal distinction + competing causal mechanisms + decisive interventions + null result remains paper-level informative.
