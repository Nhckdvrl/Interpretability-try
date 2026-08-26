# 004 — Deontic facilitation in Wason reasoning

**Status: PRE-CANDIDATE / behavioral G0 only**

## Mother question

Why can the same conditional verification problem become easier when the rule is framed as an obligation rather than a descriptive regularity?

G0 tests only whether a robust *within-item* deontic facilitation effect exists in current open-weight models. No probe/SAE/patching work is allowed before this gate passes.

## Design

Two complementary banks are used:

1. **Matched synthetic bank (primary):** each item has identical antecedent, consequent and four cards. Only the rule realization changes:
   - descriptive: `If P, then Q.`
   - deontic: `If P, then the actor must Q.`
   Gold is programmatic: turn P and not-Q.
2. **NeuBAROCO EACL-2026 bank (external replication):** official `eacl2026/wason.tsv` (160 items; 80 deontic / 80 epistemic; four polarity forms).

Every item is evaluated under all 24 card permutations and two answer phrasings. We score all six unordered 2-card answers by exact teacher-forced continuation likelihood, so free-generation parsing cannot create the effect.

### Primary endpoint

For each matched synthetic item, average correctness probability over permutations/templates, then compute

`facilitation_delta = p_correct(deontic) - p_correct(descriptive)`.

Report mean delta, paired bootstrap CI, fraction of items with positive delta, and accuracy using argmax candidate.

### Frozen promotion rule

A model passes G0 only if all hold:

- mean matched-item facilitation delta >= **+0.08**;
- paired bootstrap 95% CI lower bound > **0**;
- positive delta on >= **65%** of matched items;
- effect is positive in at least **3/4 content domains**;
- no single answer template contributes > **60%** of aggregate gain.

Promote only if **2 open-weight models** pass (first: Qwen3-8B, Gemma-3-12B-IT). Otherwise KILL; do not rescue by weaker models or cherry-picked subsets.

The official NeuBAROCO comparison is secondary because its deontic and epistemic rows are not same-content minimal pairs; it is used as external replication, not as the causal estimate.

## Run

```bash
cd active/004_deontic_facilitation
python g0.py generate --out data/matched.jsonl
python g0.py run --model Qwen/Qwen3-8B --data data/matched.jsonl --out results/qwen3_8b.jsonl
python g0.py summarize --data data/matched.jsonl --results results/qwen3_8b.jsonl --out results/qwen3_8b_summary.json
pytest -q test_g0.py
```

Optional official-bank materialization:

```bash
python g0.py fetch-neubaroco --out data/neubaroco_wason.tsv
```

## STOP

If the matched same-content contrast is weak/non-general, archive immediately. A broad published deontic-vs-epistemic accuracy difference is not enough to justify mechanism work if the minimal pair does not survive.
