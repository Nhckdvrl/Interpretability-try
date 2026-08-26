# 004 — Deontic facilitation in Wason selection

**Status: PRE-CANDIDATE — frozen behavioral G0 only.**  
**Do not start probes, patching, SAE, head searches, or mitigation before this G0 passes.**

## Mother question

> Why can a language model fail a conditional-rule check in a descriptive setting but solve the same logical form much better when the rule is phrased as an obligation/prohibition?

The behavioral prerequisite is the deontic-facilitation effect reported by Abe et al. (EACL 2026). The official paper introduces a Wason Selection Task dataset with 160 items: 80 epistemic/descriptive and 80 deontic, balanced across four polarity forms (`pos-pos`, `pos-neg`, `neg-pos`, `neg-neg`). The source data are public in `kmineshima/NeuBAROCO` under CC BY 4.0.

This project first asks only whether the effect is still large and stable in modern open-weight models under deterministic scoring and presentation controls. If not, kill it before mechanism work.

## Why this G0 is stricter than a simple replication

The original phenomenon is behavioral; our mechanism question would require clean/corrupt contrasts later. Before paying that cost, this G0 adds two controls that do not change the task:

1. **Card-position counterbalancing.** Every item is run under four cyclic rotations so every original card appears once in every displayed position.
2. **Full answer-set likelihood.** A Wason item has exactly six possible unordered two-card answers. We teacher-force all six complete strings (`1,2` ... `3,4`) rather than sampling a free-form answer or assuming a single-token label.

Two semantically equivalent prompt templates are used. Qwen3 thinking is disabled in the chat template so the initial comparison is ordinary instruction-following behavior, not a hidden mixture of long reasoning budgets.

## Frozen dataset

Pinned source:

```text
kmineshima/NeuBAROCO
commit 447929fdabe07bc3d13efae8e0c527fd458df177
eacl2026/wason.tsv
```

Fetch it with:

```bash
deontic-fetch --out data/wason.tsv
```

Do not add new Wason domains or synthetic items to rescue a failed G0.

## Unit of analysis

Each official row is evaluated under:

- 4 card rotations;
- 2 prompt templates;
- 6 complete candidate answers.

That yields 8 deterministic variants per item and 1,280 prompt evaluations per model.

At the item level we average:

- exact-choice accuracy across the 8 variants;
- normalized probability of the logically correct pair.

For the effect estimate, rows are paired **only for balanced form-stratified aggregation**: within each logical form, the 20 epistemic rows and 20 deontic rows are sorted by official ID and paired by ordinal. These are not claimed to be lexical minimal pairs.

## Frozen endpoints

Primary endpoints per model:

- mean paired `deontic_accuracy - epistemic_accuracy`;
- mean paired `deontic_p_gold - epistemic_p_gold`;
- paired bootstrap 95% CI for the probability delta;
- number of polarity forms with positive mean probability delta.

A **strong facilitation pair** requires all of:

- deontic item accuracy `>= 0.75`;
- paired epistemic item accuracy `<= 0.25`;
- `deontic_p_gold - epistemic_p_gold >= 0.15`.

## Frozen model-level pass rule

A model passes only if:

- mean paired accuracy delta `>= +0.10`;
- mean paired correct-answer probability delta `>= +0.08`;
- paired bootstrap 95% CI lower bound for probability delta is `> 0`;
- at least 3 of 4 polarity forms have positive mean probability delta;
- at least 8 of 80 form-stratified pairs are strong facilitation pairs.

Run in order:

1. `Qwen/Qwen3-8B`
2. `google/gemma-3-12b-it`
3. `Qwen/Qwen3-14B` only as confirmation

Promote only if at least **two models** independently pass. Do not weaken thresholds after seeing results; do not cherry-pick only `pos-pos`; do not switch to weaker models to manufacture the effect.

## What a pass would justify next

Only after G0 passes do we build true semantic matched pairs and distinguish competing mechanisms such as:

- the descriptive condition never forms the right counterexample representation;
- both conditions represent `P ∧ ¬Q`, but only deontic language routes into violation search;
- both routes reason correctly internally and differ only in late answer arbitration.

The decisive later experiment would ask whether a computation induced by deontic rules can causally rescue an abstract/nonce Wason task without importing normative lexical content. None of that belongs in G0.

## Usage

```bash
cd active/004_deontic_facilitation
python -m pip install -e '.[test]'
pytest -q

deontic-fetch --out data/wason.tsv

# smoke
deontic-run \
  --model Qwen/Qwen3-8B \
  --data data/wason.tsv \
  --out results/qwen3_8b_smoke.jsonl \
  --limit 8

# full: remove --limit
deontic-run \
  --model Qwen/Qwen3-8B \
  --data data/wason.tsv \
  --out results/qwen3_8b_g0.jsonl

deontic-summarize \
  --data data/wason.tsv \
  --results results/qwen3_8b_g0.jsonl \
  --config configs/g0.json \
  --out results/qwen3_8b_g0_summary.json
```

## Integrity checks

The loader refuses:

- non-official row count;
- unbalanced modal/form cells;
- duplicate IDs;
- malformed gold pairs;
- unexpected TSV schema.

The summarizer refuses duplicate variants, unknown item IDs, missing items, or an incomplete number of prompt/order variants. These failures are errors, not silently dropped rows.
