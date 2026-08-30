# 014 D1 r4 pre-model authorization record

Date: 2026-08-30
Outcome visibility at freeze: **no D1 r4 model call made**
Decision: **AUTHORIZED FOR D1 r4 BEHAVIORAL RUN**

## Contract closure

The corrected r4 population and control bank required by
`configs/contract_d1_r4.yaml` have been materialized before model evaluation:

- RedirectQA test: 61,120 source rows;
- 10,226 unique non-degenerate surface pairs across 9,387 entities;
- 8,928 preregistered intended pairs (`Aliases_and_Abbreviations` or
  `Spelling_variants`);
- all entity types, all redirect surfaces, both directions, and all four
  structural strata retained in the raw bank;
- 7,771 source pairs have at least one independently sourced Wikidata
  real-world associate candidate;
- Wikipedia `20231101.en` scanned at sentence level with cooccurrence
  implementation `d1-r4-cooc-v2`: 71,902 surfaces, 200,454 requested ordered
  pairs, 192,922,024 total surface-sentence hits;
- final matched bank: 1,768 ordered items, 1,471 surface pairs, 1,370 entities;
- confirmatory matched population: 1,571 ordered items, 1,220 entities;
- 1,288 items also have the optional same-type sensitivity control;
- intended matched opaque-strict source feasibility: 323 entities, above the
  preregistered per-family capability floor of 60 before applying a model gate.

The raw population remains saved independently of matched survivors. Matching
attrition is reported rather than used to redefine entity type, surface class,
direction, or model capability.

## Audit-time amendment

The first frozen-bank attempt exposed candidates for which both relevant joint
cooccurrence counts were zero. Additive smoothing made these candidates tie the
alias score even though corpus association was not independently attested.
Before any model call, the validity rule was amended to require
`c(ASSOC, target) >= 1`. The candidate must still satisfy the original
`S(ASSOC→target) >= S(alias→target)` rule, real-world relation requirement,
different-referent requirement, and target-token leakage exclusion.

The final bank records both raw joint counts. A deterministic 20-row matched
control audit confirmed every sampled control had positive joint count and no
sampled control was coreferential with the target entity. Source, candidate,
matched-control, and unmatched/attrition audit samples each contain 20 rows.
RedirectQA `Typical_Errors` remain in the diagnostic bank but are excluded from
confirmatory Q1/Q2 exactly as preregistered.

## Frozen fingerprints

| artifact | SHA256 |
|---|---|
| broad surface bank | `8d8911d9631df7aeab8d8c2c6545a071c1624e4dcae46e3eec4104477cdeea86` |
| Wikidata enrichment | `c1d100803455cd7c4743e64f802c2f21fb2f9c2e5034274ca7bff44d0b484c7a` |
| ASSOC candidate bank | `634692c48a8acb5f6197451124fd7d071a900107f37fb864163f92a38f883933` |
| final matched bank | `917d178533925088fe1641a72e7481eb97e18c237466416cc15608391978db37` |
| counted surface pattern inventory | `f1424f91530bce77d2f903cbdcb5b242f846de183c881fc5fd530c305dc8855a` |

The next authorized action is the frozen Qwen/Gemma/Llama D1 r4 behavioral
run. No mechanism experiment is authorized until Q1/Q2 are evaluated.

## Analysis-integrity amendment before the final run

An initial integrity pass showed that using `ASSOC_ANY` itself as the hard
identity probe foil would select on the same pair later contrasted by Q2. Those
outputs were discarded. The final gate uses an independent deterministic
different-entity foil, matched on coarse type and token length and forbidden to
share target/seen/ASSOC tokens. The bank is re-fingerprinted below after this
field is materialized, and all three model families are rerun against that SHA.
