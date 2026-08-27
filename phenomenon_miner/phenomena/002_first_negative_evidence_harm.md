# Candidate 002 — First-Negative-Evidence Harm

## One-sentence phenotype

On a natural multiple-choice science question, telling a model that **one wrong option has been independently verified as wrong** can make an item it previously answered correctly become wrong; supplying two or three such eliminations then usually restores performance.

## Discovery probe

Source distribution: 40 randomly selected GPQA Diamond questions (local cached copy). The question, options, and gold answer are held fixed. Conditions add only externally verified eliminations of wrong options: `negative_1`, `negative_2`, `negative_3`. A matched control gives the model the equivalent surviving-option set (`remaining_k`). Temperature is 0; exact-answer scoring.

Raw outputs: `phenomenon_miner/results/gpqa_negative_*_wave1.json`.

## Wave-1 evidence (40 items/model)

| model | baseline | negative_1 | negative_2 | negative_3 | baseline-correct → negative_1-wrong |
|---|---:|---:|---:|---:|---:|
| Qwen3-4B | 45.0% | 57.5% | 60.0% | 95.0% | 2 |
| Qwen3-8B | 25.0% | 47.5% | 65.0% | 95.0% | 0 |
| Qwen3-14B | 45.0% | 50.0% | 57.5% | 90.0% | 3 |
| Qwen3-32B | 50.0% | 45.0% | 57.5% | 95.0% | **7** |
| Gemma3-12B | 40.0% | 32.5% | 50.0% | 90.0% | **6** |
| Phi4-mini | 32.5% | 25.0% | 42.5% | 85.0% | **5** |
| Llama3.1-8B | 32.5% | 27.5% | 42.5% | 77.5% | **3** |

The item-level harm occurs in six of seven runs (Qwen3-8B is the exception), while aggregate `negative_1` accuracy decreases for Gemma, Phi, Llama, and Qwen3-32B. In every model, three verified eliminations sharply improve accuracy. This is therefore a **non-monotone, threshold-like information-use pattern**, not a claim that one elimination always lowers mean accuracy.

## Why it is promising

- Natural statement: “one option has been verified wrong” should never remove information.
- Cross-family and cross-size item-level recurrence (Qwen 4/8/14/32B, Gemma, Phi, Llama).
- Clear shape: local harm at one elimination, then recovery/cliff at three eliminations.
- Mechanistic openings: option-set renormalization, negative-evidence gating, verification-token anchoring, or competition between elimination and latent answer retrieval.

## Required controls before promotion

1. Repeat on a fresh GPQA split and on MMLU/ARC questions; report confidence intervals.
2. Match the surface form and length of negative hints with irrelevant verified facts.
3. Randomize which wrong option is eliminated and test whether harm depends on option position or semantic proximity.
4. Compare `negative_k` with an explicit two-stage instruction (“cross out these options, then solve from scratch”) to separate reasoning failure from instruction-following.
5. Inspect all baseline-correct → negative_1-wrong examples manually; reject cases where the hint is ambiguous or the baseline answer was parser-matched spuriously.
6. Test free-form answer plus confidence, and activation/logit interventions only after the behavioral effect survives these controls.

## Collision / novelty audit

This is adjacent to general negative evidence, confirmation bias, and metamorphic monotonicity tests. The specific candidate claim is narrower: **a single verified elimination can selectively damage already-correct answers, followed by recovery when eliminations accumulate**. Do not claim novelty until an exact-search audit is completed.

## Status

`candidate — cross-family smoke signal; not yet promoted to confirmed phenomenon`.
