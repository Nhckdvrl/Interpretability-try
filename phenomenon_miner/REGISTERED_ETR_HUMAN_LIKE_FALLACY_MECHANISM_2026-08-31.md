# PASS-REGISTER 01 — Human-Like Fallacies: Alternative Filtering or Prior Contamination?

Status: `PASS-REGISTER`
Date: 2026-08-31
Route: `B — established anomaly → unasked causal computation`

## Natural question

> When an LLM makes the same logical mistake humans predictably make, is it actually using a human-like alternative-filtering computation, or does the same answer arise from a different shortcut?

## Mother

**Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning** (Richardson et al., ICLR 2026; earlier title: *Stronger Language Models Produce More Human-Like Errors*).

Scientific object: an `ETR-predicted fallacy event` on a formally specified reasoning problem.

Statistical unit: model × PyETR reasoning problem response, with logically correct / incorrect and ETR-predicted / non-ETR error classification; premise-order reversal supplies a semantics-preserving intervention.

Established result:
- 383 formally specified PyETR problems, 38 models;
- as capability increases, the fraction of errors that are ETR-predicted human-like fallacies rises (`rho=0.360, p=0.0265`), while overall logical correctness is uncorrelated with capability;
- reversing premise order blocks fallacy production in many models despite preserving logical content;
- analyzable open checkpoints show the same intervention phenotype, including Gemma-2-9B-IT (55.17% of fallacies blocked, p=0.0107), Mistral-Small-24B-Instruct-2501 (34.53%, p=1.4e-4), Phi-4 (44.68%, p=9.34e-5), plus multiple Llama/Mistral/OLMo models with the broader pattern.

Mother explicitly states that these observations are correlative and do **not** establish a causal mechanism.

## Inherited artifact / recipe

No new benchmark is required.

Public mother substrate:
- `Oxford-HAI-Lab/PyETR` / PyPI `pyetr`;
- `Oxford-HAI-Lab/etr_case_generator`;
- generated invalid/fallacy datasets;
- evaluation logs and lm-eval integration;
- exact premise-reversal manipulation.

The project therefore begins from an already-established open-model anomaly and an existing semantics-preserving intervention, rather than a speculative G0.

## The unasked computation

ETR explains the human fallacy by maintaining disjunctive alternatives and filtering them as evidence arrives; characteristic errors arise when an alternative is eliminated too early and is not recovered.

The mother shows output-level alignment with ETR but does not establish whether the transformer performs anything computationally analogous.

### H1 — Premature alternative filtering

The same formal reasoning machinery used for correct inference represents multiple candidate alternatives, but in fallacy trials one alternative is causally suppressed too early. Premise reversal rescues the answer because it changes the timing/order of this elimination.

Prediction: before the final answer, fallacy trials should show a localized loss/suppression of the logically necessary alternative; reversal should preserve it. Patching the preserved alternative state from the reversed run into the original run should rescue the answer without changing problem semantics.

### H2 — Semantic/prior contamination

The formal reasoning circuit itself is intact. Separate semantic/common-sense/prior components bias or overwrite its result, analogous to prior mechanistic work showing belief-bias contamination of syllogistic circuits.

Prediction: ablating/patching prior-related components rescues fallacies without reconstructing an ETR-like alternative-maintenance state; content abstraction should strongly weaken the mechanism.

### H3 — Output imitation / readout shortcut

The model never implements an ETR-like intermediate computation. Human-like answers arise from learned response priors or late answer selection.

Prediction: internal representations will not exhibit a causally necessary alternative state whose fate tracks the premise-order rescue; late readout interventions will explain most of the phenotype.

## Main causal experiment

**Alternative reinstatement patch.**

For the same item, compare original order (fallacy) and reversed order (rescued). Locate the earliest point where representations diverge with respect to the logically required alternative. Patch the candidate alternative-bearing state from the rescued run into the fallacy run, with symmetric reverse-patching and unrelated-item controls.

A genuine alternative-filtering mechanism predicts selective rescue of ETR fallacies, not generic accuracy gains.

Secondary controls:
- content-preserving predicate renaming / abstraction;
- answer-label permutation;
- unrelated premise-order permutations;
- formal-reasoning circuit vs commonsense-head ablations;
- matched incorrect-but-non-ETR errors;
- cross-family replication on at least Gemma, Mistral and Phi/Llama where the mother already reports the phenotype.

## Strongest-neighbor audit

1. **Richardson et al. / ICLR 2026 mother** — owns the behavior, explicitly disclaims causal mechanism.
2. **Premise Order Matters in Reasoning with Large Language Models** (ICML 2024) — establishes broad order sensitivity but does not study ETR-specific fallacies or their internal mechanism.
3. **Reasoning Circuits in Language Models: A Mechanistic Interpretation of Syllogistic Inference** — discovers a middle-term suppression circuit and semantic belief-bias contamination in categorical syllogisms, but does not test PyETR/ETR alternative filtering, the inverse-scaling human-fallacy phenomenon, or the premise-reversal rescue mechanism.

Searches for `Erotetic/ETR + activation patching/mechanistic`, `human-like fallacy + mechanism`, `premise reversal + mechanistic`, and `alternative filtering + LLM` found no direct occupancy of the proposed causal question as of 2026-08-31.

## Anti-narrowing / ACL-EMNLP narrative

This is not a benchmark paper about one logic puzzle family. The broad question is whether behavioral convergence between human and machine reasoning reflects convergence in **computation**, or merely convergence in outputs.

The result bears on:
- cognitive theories of LLM reasoning;
- whether scaling/post-training imports human cognitive shortcuts;
- formal reasoning reliability;
- when behavioral similarity licenses mechanistic analogy;
- mechanistic distinctions between normative reasoning and learned human priors.

A null result is scientifically informative: if ETR predicts errors but no ETR-like internal state exists, the work establishes a concrete dissociation between behavioral cognitive-model fit and mechanistic equivalence.

## Registration rationale

- strong mother: YES
- behavior already established: YES
- analyzable open families: YES
- public artifact and exact intervention: YES
- no expensive G0 needed to discover phenotype: YES
- N0 title ownership clean: YES
- N1 key causal test unoccupied: YES as of search date
- >=2 competing causal mechanisms: YES (3)
- surprising discriminating intervention: YES (alternative reinstatement under premise-reversal pair)
- broad ACL/EMNLP narrative: YES

`PASS-REGISTER = 1/5` after this registration.
