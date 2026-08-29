# 012 Source-Discount Recovery — two-family first shot

Date: 2026-08-29  
Data: `data/frozen_d0.jsonl` (108 scenarios, sha256 `cde7f3fa9dfeb94645fa2e254507013c26cb2ffb01793b9bd889a86668af1c3a`)  
Contract: `configs/frozen_g0.json` `2026-08-29-r2`  
Summarizer output: **`HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR` for both families. `smoke_cross_family_pass: false`.**  
Project-level disposition: **`R2-HOLD-INSTRUMENTATION-ARTIFACT`** — a frozen capability probe was invalidated by a decisive answer-order artifact, and the outcome phenotype stayed structurally uninterpretable because the weighting denominator was zero. This is **not** recorded as a scientific hard kill of the phenomenon. All r2 raw output is retained unmodified.

Models were pinned by revision rather than left to the cache: Qwen3-8B `b968826d9c46dd6066d109eabc6255188de91218`, Gemma-3-12B-IT `96b6f1eccf38110c56df3a15bffe176da04bfd80`, both bfloat16. The bank was split into four stride-4 shards so every shard spans all twelve cells; Qwen ran on fvcrc21 GPUs 0-3 at batch 32 and Gemma on fvcrc20 GPUs 0-3 at batch 16 (its 262k vocab makes a batch-64 logits tensor ~26 GB). 28,944 scored prompts per model, 57,888 total, no shard errors. Scoring is the frozen `HFChoiceScorer` exact A/B continuation log-probability; nothing in the harness, the bank or the thresholds was touched.

## Headline

| metric | Qwen3-8B | Gemma-3-12B-IT |
|---|---|---|
| scenario pairs | 108 | 108 |
| support-gated | 104 | 104 |
| memory-gated | **0** | **29** |
| weighting-capable (denominator) | **0** | **0** |
| eligible cells | 0 / 8 | 0 / 8 |
| verdict | `HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR` | `HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR` |

There is no eligible denominator in either family, so the recovery, reinstatement and gap-shrink figures are structurally empty and are **not interpreted**. `cell_mean_gap_shrink` is `NaN` for both.

## Denominator 1 — source/message/credibility memory

The failure is not diffuse. Two of the three memory probes are at ceiling in both models with no answer-order effect at all:

| probe | Qwen mean | Qwen order gap | Gemma mean | Gemma order gap |
|---|---|---|---|---|
| `source_identity` | 0.997–1.000 | ≤ 0.005 | 1.000 | 0.000 |
| `message_direction` | 0.997–1.000 | ≤ 0.004 | 0.999 | ≤ 0.002 |
| `source_credibility` | **0.560** (low/short) | **−0.809** | **0.706** (high/short) | **+0.574** |

Source identity and message direction survive both delays perfectly. Everything that kills the gate is the `source_credibility` yes/no probe, and it is binding in 216/216 scenario-directions for Qwen and 216/216 for Gemma.

### That probe is contaminated by answer position

The gold answer on this probe is always "Yes", and the two answer orders place "Yes" at A and at B. The counterbalancing separates content from position, and it shows position winning:

- **Qwen**, `low`/`short`: 0.156 when Yes is A, 0.964 when Yes is B — it picks **B** in both orders. On the same probe with the `high` source ("more reliable?") it answers by content in both orders (1.000 / 0.983). So it can affirm "more reliable" and falls back to a position prior on "less reliable".
- **Gemma**: the opposite prior. 0.993–0.999 when Yes is A, 0.419–0.767 when Yes is B, for both sources.
- The two content-option probes in the same prompt family show order gaps of ≤0.005, so neither model is position-biased in general — only on this yes/no item.

The delay direction confirms it: the probe is *worse at short delay than long* in both models and both sources, which is backwards for anything memory-shaped. And the relevant numbers are visible in the prompt at answer time, so this item never tested retention in the first place — it tested whether the model will state a comparison it can read.

**Reading:** the hard kill is mechanically correct under the frozen contract, and the counterbalancing did its job by refusing a position-driven answer into the denominator. But it is not evidence that these models lose source credibility over a delay. It is evidence that this particular yes/no item cannot measure the thing on these two models.

## Denominator 2 — immediate source-weighting

Independent of the probe artifact, the immediate discount gap fails on belief in both families:

| | Qwen belief | Qwen action | Gemma belief | Gemma action |
|---|---|---|---|---|
| mean initial gap | **+0.011** | +0.080 | **+0.032** | +0.231 |
| median | +0.013 | +0.048 | **+0.000** | +0.243 |
| fraction > 0 | 0.67 | 0.83 | 0.53 | 0.81 |
| threshold | 0.05 | 0.04 | 0.05 | 0.04 |

Among Gemma's 58 support-and-memory-gated direction entries, 53 fail on `belief_initial_gap` and 29 on `action_initial_gap`.

So both models separate a high-credibility from a low-credibility source **in the consequential action readout** — Gemma strongly, at +0.23 — while the belief readout is at or near zero, with Gemma's median exactly 0.000 and only 53% of entries positive. This is an observation, not a claim: it needs the scorer and artifact audit below before anyone treats a belief/action dissociation as real.

## What this does and does not license

- The frozen bank, thresholds, cell membership and prompts were not changed, before or after seeing this. They stay frozen.
- No recovery claim, in either direction, is supported. The delay conditions ran, but with no eligible pair there is nothing to interpret.
- The result does **not** establish "these models lack source credibility memory". The probe that produced the kill is demonstrably position-driven, and the two clean memory probes are at ceiling.

## Required before anything else

Per repository process, a smoke is followed by raw-case, scorer, capability and artifact audits before any N1 or panel expansion. The specific items this run raises:

1. Whether `source_credibility` should be re-specified as a two-content-option item (like `source_identity` and `message_direction`) rather than yes/no. That changes a **capability gate**, not the outcome measure, but it is a harness revision and requires a re-freeze and a re-run, not a re-scoring of this data.
2. Whether the belief readout wording is measuring what the action readout is measuring, given the size of the gap between them.
3. Whether the four support-gate failures (104/108 in both families) share a cell or a source-profile shape.

## Disposition and what r3 changes

`d0_verdict` stays `PASS`; D0 was never in question here. The project records this run as `R2-HOLD-INSTRUMENTATION-ARTIFACT` and proceeds to a contract `2026-08-29-r3` in which **exactly one instrumentation item changes**: `source_credibility` becomes a counterbalanced two-content-option item like the other two memory probes.

```text
According to the audited source records, which statement about the source that
delivered the earlier message is correct?
  A. It was the more reliable of the two sources.      (order 0)
  B. It was the less reliable of the two sources.
```

with the labels swapped in order 1, and gold now flipping with which source spoke — high to "more", low to "less". Across source x order the gold is A twice and B twice, so a standing position preference scores at chance and cannot pass, while answering requires the chain earlier message -> source identity -> source profile -> relative credibility. That is closer to the source-credibility binding the phenomenon needs than "will the model say Yes to a comparative".

Nothing else moves. The 108-scenario bank, the 101/7 primary-secondary membership, the cell bootstrap, the support probes, the belief and action readout wording, `p_target` aggregation, and every initial-weighting, recovery, reinstatement and model-pass threshold are byte-identical to r2; the only other diff in `frozen_g0.json` is `contract_version`. r3 is a **full** re-run of both models over all 28,944 rows each — no splicing of new credibility rows onto r2 readouts, which would leave a mixed-contract dataset in the record for no meaningful saving.

### The r3 decision rule, fixed in advance

- If the memory gate recovers but `belief_initial_gap` still keeps weighting-capable pairs near zero, that is a genuine `HARD-KILL-SOURCE-WEIGHTING-CAPABILITY-FLOOR` and 012's current operationalization ends there. The belief readout will **not** be swapped for a log-odds measure to rescue it.
- Only if the weighting denominator is large enough do the low-source rebound, gap shrink, high-source retention, source-cue reinstatement and matched-length control get read at all.

### Design note, deliberately not acted on

The belief/action asymmetry above is suspicious in a way that has a measurement-theoretic explanation: `p_target` differences saturate near 0 and 1, so 0.90 -> 0.99 reads as 0.09 while 0.99 -> 0.999 reads as 0.009, though the two are comparable in preference strength. A semantic log-odds readout, `log P(target continuation) - log P(other continuation)`, does not saturate that way, and the raw files already store `label_logprobs`, so it is computable from this run.

It is recorded here as a design note for a possible future secondary diagnostic and is **not** added to any gate in r3. Adopting it now — after seeing which gate failed — would be swapping the measurement for the one that survives, which is exactly the discipline this project is built to refuse. If 012 dies on the belief weighting floor, a future question can pre-register the log-odds readout from the start; that version would be clean.
