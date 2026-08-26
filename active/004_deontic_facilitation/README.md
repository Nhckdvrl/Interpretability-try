# 004 — Deontic facilitation in Wason selection

**Status: PRE-CANDIDATE — frozen behavioral G0 only.**  
**Do not start mechanism work before this G0 passes.**

## Mother question

> Why can the same conditional reasoning problem become easier when the rule is expressed as an obligation/prohibition rather than as a descriptive regularity?

Abe et al. (EACL 2026) provide strong behavioral motivation with NeuBAROCO, but their deontic and epistemic rows are different semantic items, not minimal modality swaps. The official dataset therefore motivates the phenomenon but cannot by itself establish this causal wording.

## Logic-review correction

The first draft incorrectly paired unrelated official rows by within-form ordinal and used those pseudo-pairs for bootstrap and strong-pair gates. It also used the word `violated` in the generic task prompt, which could inject the hypothesized deontic cue into the epistemic control. Both are removed.

## Frozen decisive contrast

The corrected bank contains **32 true matched problems**:

- 8 semantic frames;
- 4 polarity forms (`pos-pos`, `pos-neg`, `neg-pos`, `neg-neg`);
- 2 modality realizations per base problem.

Within each pair, cards, propositions, gold answer, logical form, and semantic frame are identical. Only the consequent modality changes, e.g.:

```text
epistemic: If the badge is blue, then the employee enters Gate A.
deontic:   If the badge is blue, then the employee must enter Gate A.
```

Negative consequents use `does not` vs `must not`. Total: 64 rows = 32 matched pairs.

The task instruction itself is neutral and does not contain `violation`, `obligation`, `permission`, or similar normative cues.

## Controls and scoring

Each row is evaluated under 4 cyclic card rotations and 2 neutral prompt templates. All six unordered two-card answers are scored as complete teacher-forced continuations. Per model this is `32 × 2 × 4 × 2 = 512` prompt evaluations.

For each true pair:

```text
delta_accuracy = accuracy_deontic - accuracy_epistemic
delta_p_gold   = p_gold_deontic - p_gold_epistemic
```

A strong pair requires deontic accuracy `>= .75`, epistemic accuracy `<= .25`, and `delta_p_gold >= .15`.

A model passes only if mean accuracy delta `>= .10`, mean probability delta `>= .08`, paired-bootstrap CI lower bound `> 0`, at least 3/4 polarity forms are positive, and at least 4/32 pairs are strong. At least two open-weight models must pass. Do not weaken gates after seeing results.

## Why a pass matters

A pass establishes the exact behavioral prerequisite for later mechanism work: the same propositions/cards/gold computation are present, but descriptive vs normative modality changes whether the model identifies the required counterexample. Only then test representation failure vs routing into violation-search vs late answer arbitration.

## Usage

```bash
cd active/004_deontic_facilitation
python -m pip install -e '.[test]'
pytest -q

deontic-generate --out data/matched_wason.jsonl

deontic-run --model Qwen/Qwen3-8B --data data/matched_wason.jsonl --out results/qwen3_8b_g0.jsonl

deontic-summarize --data data/matched_wason.jsonl --results results/qwen3_8b_g0.jsonl --config configs/g0.json --out results/qwen3_8b_g0_summary.json
```

## STOP rule

If the matched effect is absent, unstable across forms/templates, or passes only in one model family, archive the topic. Do not rescue it with the unmatched official rows, easier hand-picked frames, weaker models, or mechanism evidence.
