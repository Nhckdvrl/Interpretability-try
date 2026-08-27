# Primacy Lock — behavioral preflight only

**Status:** `PRE-CANDIDATE / DO NOT START MECHANISM`.

Mother question:

> When a fact is updated repeatedly in context, does the model fail because the newest binding was never represented strongly enough, or because multiple versions remain available but a temporal/version selector retrieves an obsolete state?

This directory intentionally contains only cheap behavioral validation. No probe, SAE, activation patching, steering, head scan, or circuit search should be added before both gates below are passed on two model families.

## Why these two tests

### A. Matched PI/RI replication

The same update history is queried in two ways:

- `FIRST`: retrieve the original value;
- `LATEST`: retrieve the current value.

The behavioral anchor comes from *Transformers Remember First, Forget Last* (2026), which reports PI > RI across 39 LLMs. For the first local smoke test we reuse the public 46-category / 400-value dictionary released with *Unable to Forget* rather than inventing new category/value stimuli.

Important: `pi_ri_g0.py` is a compact structural reproduction, **not a claim of byte-for-byte reproduction of the 2026 paper's prompt template**. Before any confirmatory table, compare its exact prompt/order/query protocol with the target paper/code and freeze the final version in git.

### B. LongMemEval ecological audit

Use the official cleaned LongMemEval data and only `knowledge-update` items. The script never constructs new memories. It asks the official question over the official history and performs a conservative, deterministic stale-intrusion audit.

An incorrect answer is labeled `high_precision_stale_intrusion` only when:

1. the generated answer occurs verbatim in an older history session; and
2. the official gold answer occurs in a later history session.

This deliberately misses paraphrases. It is meant to answer "does the synthetic primacy phenotype have any obvious natural counterpart?" without paying for an LLM judge. The lexical accuracy printed by this script is **not** the official LongMemEval score.

## Data

Do not commit downloaded data; root `.gitignore` already ignores `data/` and `artifacts/`.

Public PI dictionary:

```bash
mkdir -p data/primacy_lock
wget -O data/primacy_lock/pi_source.json \
  https://raw.githubusercontent.com/zhuangziGiantfish/Unable-to-Forget/main/testing_data/dict_category_double-word_46-400_v1-1.json
```

Official cleaned LongMemEval oracle file (cheap ecological gate):

```bash
wget -O data/primacy_lock/longmemeval_oracle.json \
  https://huggingface.co/datasets/xiaowu0162/longmemeval-cleaned/resolve/main/longmemeval_oracle.json
```

For the final ecological check, repeat on `longmemeval_s_cleaned.json` if the target model/context budget allows it. Do not silently substitute a custom history generator.

## 1. Unit tests

```bash
cd preflight/primacy_lock
python -m unittest discover -s tests -v
```

## 2. Generate frozen matched PI/RI cases

Smoke test first:

```bash
python pi_ri_g0.py generate \
  --source-json ../../data/primacy_lock/pi_source.json \
  --counts 3,10,50 \
  --seeds 0,1 \
  --n-keys 46 \
  --out ../../artifacts/primacy_lock/cases_smoke.jsonl
```

Candidate confirmatory grid after the prompt is checked against the paper:

```bash
python pi_ri_g0.py generate \
  --source-json ../../data/primacy_lock/pi_source.json \
  --counts 3,10,50,100,200,300 \
  --seeds 0,1,2,3,4 \
  --n-keys 46 \
  --out ../../artifacts/primacy_lock/cases_frozen.jsonl
```

Every seed/update-count history produces a matched `first` and `latest` case. The assignment history is byte-identical inside the pair; only the temporal target in the final question changes.

## 3. Run against a local vLLM/OpenAI-compatible server

Example:

```bash
python pi_ri_g0.py run \
  --cases ../../artifacts/primacy_lock/cases_smoke.jsonl \
  --endpoint http://127.0.0.1:8246 \
  --model Qwen/Qwen3-14B \
  --out ../../artifacts/primacy_lock/qwen3_14b_pi_ri.jsonl \
  --verbose
```

Then summarize independently:

```bash
python pi_ri_g0.py summarize \
  --results ../../artifacts/primacy_lock/qwen3_14b_pi_ri.jsonl \
  --out ../../artifacts/primacy_lock/qwen3_14b_pi_ri.summary.json
```

The scorer reports:

- FIRST and LATEST accuracy by update count;
- paired `FIRST - LATEST` gap;
- latest-query `primacy_intrusion` (returned version 1);
- latest-query `stale_intrusion` (returned another obsolete same-key version);
- fraction of latest errors that are same-key historical values;
- session-level near-zero (`<=5%`) and near-perfect (`>=85%`) counts, useful for checking the reported bimodal collapse rather than only averaging it away.

Run the same frozen JSONL against at least one Qwen and one Gemma checkpoint. Do not regenerate different cases per family.

## 4. LongMemEval knowledge-update audit

Start with oracle evidence sessions:

```bash
python longmemeval_audit.py run \
  --dataset ../../data/primacy_lock/longmemeval_oracle.json \
  --endpoint http://127.0.0.1:8246 \
  --model Qwen/Qwen3-14B \
  --out ../../artifacts/primacy_lock/qwen3_14b_longmemeval.jsonl \
  --verbose
```

Smoke with `--limit 20` if needed. The summary reports the number and share of high-precision stale intrusions among deterministic lexical errors. Inspect the raw JSONL before interpreting the rate.

## Frozen stop-loss gate

Do **not** start mechanism work unless all of the following hold:

1. **Cross-family matched asymmetry:** the same frozen PI/RI cases show a substantial `FIRST - LATEST` gap in both Qwen and Gemma. A working pre-registration threshold is `>= 0.25` mean gap at at least two interference levels with `n_updates >= 50`.
2. **Error identity:** on latest queries, the effect is mainly same-key historical intrusion rather than missing/format/hallucination. Working threshold: `>= 0.50` of latest-query errors match an obsolete value for the same key.
3. **Prompt/parser audit:** parsed fraction remains high (`>= 0.95`), and the direction survives at least one frozen wording/order check. Do not tune wording separately per model.
4. **External anchor:** official LongMemEval `knowledge-update` histories yield a non-trivial set of high-precision stale-version errors in both families. Do not set a paper claim from lexical accuracy alone; manually inspect these candidates and, if needed, use the benchmark's official evaluator later.
5. **No salvage:** if the matched asymmetry fails on one family, do not revive it by weakening models, selecting seeds, changing update counts after seeing results, or moving directly to hidden states.

If 1–3 pass but 4 fails, the project remains a synthetic memory phenomenon and should not advance under the repository's current G0 rules.

## Expected next step only if G0 passes

The first mechanism experiment should be designed to distinguish:

- **write failure:** latest binding is not represented;
- **version-selection failure:** old and new bindings coexist but the temporal target routes to the wrong version;
- **late overwrite:** a correct latest-state representation is present but later computation reactivates an obsolete binding.

Do not add a generic "which layer can probe the latest value?" experiment without a causal matched intervention that can distinguish these alternatives.
