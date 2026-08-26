# 004 — Deontic facilitation in Wason selection

**Status: PRE-CANDIDATE — frozen behavioral G0 only.**  
**Do not start mechanism work before this G0 passes.**

## Mother question

> Why can the same conditional reasoning problem become easier when the rule is expressed as an obligation/prohibition rather than as a descriptive regularity?

Abe et al. (EACL 2026) provide strong behavioral motivation with NeuBAROCO, but their deontic and epistemic rows are different semantic items, not minimal modality swaps. The official dataset therefore motivates the phenomenon but cannot by itself establish this causal wording.

## Logic-review corrections

The decisive G0 now uses **32 true matched problems** rather than pseudo-pairing unrelated official rows. Within each pair, cards, propositions, gold answer, logical form, and semantic frame are identical; only the consequent modality changes, e.g. `enters` vs `must enter` (and `does not` vs `must not`).

The generic task instruction is deliberately neutral: it contains no `violation`, obligation, permission, or prohibition cue. It also contains **no concrete answer-pair example**; the previous `1,4` example could privilege one gold pattern.

## Frozen decisive contrast

- 8 semantic frames;
- 4 polarity forms (`pos-pos`, `pos-neg`, `neg-pos`, `neg-neg`);
- 2 modality realizations per base problem;
- 64 rows = 32 matched pairs.

Every row is evaluated under **all 24 card permutations** and 2 neutral prompt templates. Full permutation counterbalancing removes residual dependence on relative card ordering rather than balancing only marginal positions. All six unordered two-card answers are teacher-forced as complete continuations.

Per model: `32 × 2 modalities × 24 permutations × 2 templates = 3,072` prompt evaluations.

For each true pair:

```text
delta_accuracy = accuracy_deontic - accuracy_epistemic
delta_p_gold   = p_gold_deontic - p_gold_epistemic
```

A strong pair requires deontic accuracy `>= .75`, epistemic accuracy `<= .25`, and `delta_p_gold >= .15`.

A model passes only if mean accuracy delta `>= .10`, mean probability delta `>= .08`, paired-bootstrap CI lower bound `> 0`, at least 3/4 polarity forms are positive, at least 4/32 pairs are strong, and strong pairs occur in at least two forms. At least two open-weight models must pass.

## Why a pass matters

A pass establishes the actual prerequisite for the proposed mechanism question: **same propositions, same cards, same logical gold, different modality wording, different reasoning success**. Only then is it meaningful to distinguish failure to form the counterexample, modality-dependent routing into violation search, and late answer arbitration.

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

If the matched effect is absent, unstable across forms/templates/orderings, or passes only in one model family, archive the topic. Do not rescue it with unmatched official rows, answer examples, easier hand-picked frames, weaker models, or mechanism evidence.
