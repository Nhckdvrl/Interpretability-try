# B1 pre-analysis freeze — 041 Pilot B

Everything in this document and in the two builder scripts it names is frozen **before any panel
model has been run on B0 or B1**. Execution order is:

```text
D&R materials inherited  ->  B1 design and analysis plan frozen (this document, tagged)
                         ->  panel opened  ->  B0 replication  ->  B1 confirmatory
```

**B0 is not a gate for B1.** Regardless of whether B0 reproduces the human main effects, the window
asymmetry or the null interaction in any given family, B1 is executed unchanged on all four
families. Selecting families by their B0 result would be model-level outcome-conditioned selection
and is prohibited.

**Relation between B0 and B1, stated precisely.** B0 and B1 share the preregistered Davies &
Richardson adjective-event families. Surface instances do not overlap, but the families are
inherited, so the honest statement is: *no B1 instantiated critical trial is evaluated before the B1
design and analysis plan are frozen, and B0 outcomes are not used for item, family, model, window or
analysis selection.*

## 1. Frozen materials and construction

| element | frozen value |
|---|---|
| adjective-event families | the 12 critical quartets of Davies & Richardson (2021), *J. Pragmatics* 178:258-269, AAM at White Rose eprints 172760 |
| B0 stimuli | `stimuli/b0_dr_replication.jsonl`, 48 rows, built by `scripts/build_b0_dr_replication.py`, materials verbatim with two transcription notes recorded in the script docstring |
| B1 stimuli | `stimuli/b1_function_cross.jsonl`, 13,824 reference rows + 1,536 explanation rows, built by `scripts/build_b1_function_cross.py` |
| seed | 20260904 (construction is fully deterministic; no sampling anywhere) |
| world schema | 4 entities: `A = P+Q+` (target, carries `Z`), `B = P-Q+`, `C = P+Q-`, `D = P+Q-` |
| live sets | `R+` = {A,B,C}; `R-` = {A,C,D}. World text identical across R conditions; only the live-entity clause differs |
| `P` | the D&R adjective of the item; always the studied modifier |
| `Q` | a second orthogonal described dimension; **restricts in both R conditions**, so the R manipulation is not a P-vs-Q swap |
| `Z` | one background fact, true of the target, stated in every cell, never in the referring description, never an option in the referential readout; non-targets carry matched background facts |
| E manipulation | matrix verb phrase only: `E+` = the D&R `+sem` verb (the event `P` bears on), `E-` = the D&R `-sem` verb (the event `Z` bears on) |
| description conditions | `full`, `drop_p`, `drop_q`, `bare` |
| surface forms | `np`, `relative_pq`, `relative_qp` (relative-clause forms carry the modifier-order counterbalance; prenominal order is not reversed, because reversed adjective order is independently marked in English and would confound the surprisal readout) |
| counterbalancing | target entity index (4), live-cue paraphrase (2), answer-option rotation (3), explanation-option order (2), entity presentation order tied to the target rotation |

## 2. Frozen cell definitions

For the studied modifier `P`:

```text
R+  live {A,B,C}: drop P -> 2 live satisfiers  => P restricts
R-  live {A,C,D}: drop P -> 1 live satisfier   => P does not restrict
E+  matrix event is the one P bears on
E-  matrix event is the one Z bears on
```

Gold is computed from the described properties and the live set, never from a model or a hand label.
`scripts/build_b1_function_cross.py::certify` asserts, for every reference row: live set size 3;
target in the live set; and live-satisfier cardinality exactly 1 / 2 / 2 / 3 for
`full` / `drop_p` / `drop_q` / `bare` under `R+`, and 1 / 1 / 3 / 3 under `R-`.

## 3. Frozen readouts

**Reference.** Deterministic single-token forced choice over the three live entities.

```text
ReferenceMargin = log P(gold option letter) - log sum_over_distractor_letters P(letter)
ReferenceConsequence(P) = ReferenceMargin(full) - ReferenceMargin(drop_p)
ReferenceConsequence(Q) = ReferenceMargin(full) - ReferenceMargin(drop_q)      # control readout
```

**Explanation.** Deterministic single-token forced choice between the `P` cause and the `Z` cause,
option order counterbalanced, computed for `full` and `drop_p` on the `np` surface form.

```text
ExplanationMargin = log P(P-cause letter) - log P(Z-cause letter)
ExplanationConsequence(P) = ExplanationMargin(full) - ExplanationMargin(drop_p)
```

**Surprisal.** Mean per-token NLL of the `P` span and of the `P`+noun span in the critical sentence,
given the preceding text. This is the B0 measure carried into the crossed worlds. In B0 the two
windows are the D&R windows: the noun phrase (adjective + noun) and the following wrap-up phrase.

## 4. Frozen analysis

Rows = manipulation, columns = consequence. All contrasts are computed within item and world, then
averaged over items; confidence intervals are non-parametric bootstrap over items, 5,000 resamples,
matching the existing 041 scripts.

```text
dRR = mean[ReferenceConsequence(P)   | R+] - mean[ReferenceConsequence(P)   | R-]
dRE = mean[ExplanationConsequence(P) | R+] - mean[ExplanationConsequence(P) | R-]
dER = mean[ReferenceConsequence(P)   | E+] - mean[ReferenceConsequence(P)   | E-]
dEE = mean[ExplanationConsequence(P) | E+] - mean[ExplanationConsequence(P) | E-]
```

Denominators, predictable in advance and in the human data already, reported as a gate and not as a
contribution: `dRR > 0` and `dEE > 0`. `ReferenceConsequence(Q)` is expected to be positive and
approximately equal across R conditions; a large R-dependence there would mean the `Q`-constant
construction failed and is reported as such.

Frozen readings of the matrix:

| structure | signature |
|---|---|
| orthogonal routing | `dRR`, `dEE` large; `dRE`, `dER` within their bootstrap intervals of zero |
| generic relevance | all four positive |
| competition | a directed negative cross-effect |

## 5. Frozen execution details

- **Panel and checkpoints:** `Qwen/Qwen3-8B` (36 blocks), `NousResearch/Meta-Llama-3.1-8B-Instruct`
  (32), `google/gemma-3-12b-it` (48), `mistralai/Mistral-Small-24B-Instruct-2501` (40). All four are
  confirmatory; none is spent on screening.
- **Inference:** `bfloat16` weights, deterministic scoring, no sampling, no chain of thought. Any
  hidden-state capture stores `float32` (Gemma-3-12B's residual stream exceeds the float16 range in
  the middle third of the stack; see the correction in `EXPERIMENT_LOG.md`).
- **Tokenizer handling:** option scoring reads the logit of the single option-letter token under each
  model's own tokenizer. Surprisal windows are located by character offsets recorded at build time
  and mapped through the offset mapping; a token straddling a window boundary is assigned to the
  earlier window and the count of such tokens is reported per model. Window scores are mean per-token
  NLL, so multi-token adjectives are length-normalised.
- **Exclusions:** none post hoc. No item is dropped, and no family is dropped, on the basis of any
  model's behaviour. Structural defects are fixed at build time, before this freeze. If a family
  cannot produce a defined readout at all (degenerate option probabilities), that is reported as a
  result for that family rather than repaired by re-selection.

## 6. Item selection policy

No model of any kind is used to select items. Structural validity is certified deterministically in
`certify()`. Adjective-event plausibility is inherited from previously normed human materials, where
the `+sem`/`-sem` contrast was validated against 31 readers and verb frequency was controlled within
each quartet to within 1.2 Zipf (SUBTLEX-UK). Any future model-based smoke test must use auxiliary
families excluded from all confirmatory analyses, with criteria restricted to task validity — does
the model parse the format, is the target recoverable, is the readout off floor and ceiling — and may
never depend on the size or sign of the predicted R/E effect.

Paper text: *Critical items were frozen before any evaluation on the four preregistered model
families. Structural validity was certified deterministically; adjective-event plausibility was
inherited from previously normed human materials. B0 and B1 share the preregistered adjective-event
families, but no B1 trial was evaluated before the design and analysis plan were frozen, and B0
outcomes were not used for item, family, model, window or analysis selection.*
