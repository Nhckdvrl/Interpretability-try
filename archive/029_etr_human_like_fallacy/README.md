# 029 — Human-Like Fallacies: Alternative Filtering or Prior Contamination?

Status: **ACTIVE / PASS-REGISTER / V0 PROVENANCE AUDITED — EXACT 383 MANIFEST MISSING**

Route: **Hamdi Route B — established anomaly → unasked causal computation**  
Canonical registration: [`../../phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md`](../../phenomenon_miner/REGISTERED_ETR_HUMAN_LIKE_FALLACY_MECHANISM_2026-08-31.md)

## 1. One-sentence question

When an LLM makes the same logical mistake predicted for humans by Erotetic Theory of Reasoning (ETR), is it actually performing an ETR-like **alternative-maintenance / alternative-filtering computation**, or does the same behavioral fallacy arise from semantic priors or a late output shortcut?

## 2. Background and mother result

The mother paper is **Theory-Grounded Evaluation of Human-Like Fallacy Patterns in LLM Reasoning** (Richardson et al., ICLR 2026; earlier title: *Stronger Language Models Produce More Human-Like Errors*).

The mother does not merely report low logic accuracy. It defines a theory-grounded scientific object: an **ETR-predicted fallacy event** on formally specified reasoning problems.

Its important established results are:

- 383 formally specified PyETR problems evaluated across 38 models;
- stronger models do not simply become uniformly more logically correct; among the errors they still make, the fraction matching ETR-predicted human fallacies increases with capability;
- reversing premise order preserves the logical content but blocks many ETR-like fallacies;
- the premise-reversal rescue is already reported on analyzable open checkpoints, including Gemma, Mistral and Phi-family models;
- the paper explicitly treats its evidence as behavioral/correlative and does **not** claim that the model implements ETR internally.

This makes the topic safe from the old behavior-lottery failure mode: the anomaly and a semantics-preserving intervention already exist before our work begins.

## 3. What the mother did not ask

ETR explains characteristic human fallacies through the maintenance and filtering of candidate alternatives. A fallacy can arise when a logically necessary alternative is removed too early and is not reinstated.

The mother shows that LLM outputs line up with ETR predictions, but behavioral alignment does not imply mechanistic equivalence.

Our paper asks whether the **internal computation** is actually ETR-like.

### H1 — Premature alternative filtering

The model internally represents multiple live alternatives. In a fallacy trial, one required alternative is causally suppressed too early. Premise reversal rescues the answer because it changes the temporal order of filtering.

Expected signature:
- an alternative-specific state exists in correct/reversed runs;
- it disappears or loses causal influence in original-order fallacy runs;
- restoring that state selectively rescues the fallacy.

### H2 — Semantic/prior contamination

The formal reasoning process remains mostly intact, but semantic/common-sense prior components bias or overwrite it.

Expected signature:
- abstracting predicate content weakens the fallacy mechanism;
- causal ablation of semantic/prior components rescues the answer without reconstructing a specific alternative-maintenance state.

### H3 — Late output imitation / readout shortcut

The model never performs a computation resembling ETR. Human-like errors arise from response priors or late answer selection.

Expected signature:
- no causally necessary alternative state tracks premise-order rescue;
- most of the effect appears only close to answer writing.

## 4. Data and artifacts

Primary inherited artifacts:

- `Oxford-HAI-Lab/PyETR` / PyPI `pyetr`;
- `Oxford-HAI-Lab/etr_case_generator`;
- generated valid/invalid/fallacy datasets;
- evaluation logs and lm-eval integration;
- the mother's exact original-order ↔ premise-reversed manipulation.

Primary statistical unit:

> **same formal reasoning problem × same model × original/reversed premise order**

The most valuable matched cells are:

1. original order = ETR fallacy, reversed order = correct (**reversal rescue**);
2. original/reversed both correct (**order-robust control**);
3. incorrect but non-ETR error (**wrong-answer control**);
4. ETR fallacy not rescued by reversal (**ETR-but-no-rescue control**).

No central LLM judge should define these cells. Use the formal PyETR labels and rule-based answer correctness.

## 5. Initial model panel

Do not begin with a large multi-family sweep. The mother has already done existence testing.

Recommended order:

1. **one mother-confirmed open checkpoint with a strong reversal-rescue denominator** for pipeline validation;
2. replicate the key causal result on at least two additional mother-confirmed open families;
3. only after the mechanism is stable, broaden the panel.

Mother-confirmed examples include Gemma-2-9B-IT, Mistral-Small-24B-Instruct-2501 and Phi-4; Llama/Mistral/OLMo family results can be used as additional replication depending on local tooling.

## 6. Initial validation plan

### V0 — Artifact freeze and exact mother reproduction

Goal: prove that our experimental population is exactly the mother's scientific object.

Steps:

1. Pin commit/release versions of PyETR and `etr_case_generator`.
2. Recreate the 383-problem inventory and record stable item IDs.
3. For every item, store:
   - formal premises;
   - correct answer;
   - ETR-predicted error class;
   - original premise order;
   - mother's reversed order.
4. Recompute the logical/ETR labels from the formal generator rather than copying a spreadsheet blindly.
5. From public mother logs, build the matched cell table listed above.
6. Freeze a `validation_manifest` before inspecting hidden states.

**Stop condition:** if the public artifacts cannot reproduce the mother-defined ETR/reversal population, do not proceed to MI.

### V1 — Cheap behavior replay, not behavior discovery

Goal: confirm that our local inference stack preserves the already-known phenotype.

Steps:

1. Select 50–100 mother-confirmed reversal-rescue pairs for one open checkpoint.
2. Re-run with the mother's decoding/template as faithfully as possible.
3. Verify:
   - original-order fallacy rate;
   - reversed-order rescue rate;
   - answer-label balance;
   - no prompt/template artifact.
4. Run the same items with answer-label permutation and innocuous formatting controls.

This is a **pipeline sanity check**, not a new G0. If the mother phenotype cannot be reproduced because of template/model-version mismatch, fix provenance before continuing.

### V2 — Build an ETR-state readout without an LLM judge

Goal: operationalize the candidate alternative state using the formal ETR state machine.

Steps:

1. For each premise prefix, compute from PyETR which alternatives should still be live.
2. Mark token positions corresponding to the end of each premise and the final answer position.
3. Extract residual-stream / attention-head activations at those positions.
4. Train simple held-out linear readouts for **formal alternative presence**, using problem-grouped splits so lexical identity cannot leak across train/test.
5. Compare:
   - reversal-rescued ETR fallacies;
   - order-robust correct items;
   - non-ETR wrong items.
6. Repeat with predicate renaming / abstraction controls.

Readout success alone is **not** evidence for the paper claim; it only gives a target for intervention.

### V3 — Earliest divergence localization

Goal: find where original-fallacy and reversed-rescue runs first differ in the fate of the logically required alternative.

Steps:

1. Align matched original/reversed runs at premise boundaries rather than raw token index.
2. Measure alternative-readout trajectories through depth.
3. Use causal tracing / patch sweeps to identify layers/tokens where reversed-run state begins to affect the final correct answer.
4. Compare with generic correctness directions and answer-token logit directions.

A useful candidate stage must be **ETR-specific**, not merely a generic correct-vs-wrong classifier.

### V4 — Core causal test: alternative reinstatement patch

For a reversal-rescued pair:

1. Use original-order fallacy run as recipient.
2. Patch the candidate alternative-bearing state from the reversed correct run at the localized premise/layer position.
3. Measure change in the exact formal answer logit / generated answer.
4. Perform the reverse patch (fallacy → rescued run).
5. Run controls:
   - same-norm random direction;
   - unrelated problem patch;
   - order-robust correct pair;
   - non-ETR wrong pair;
   - late answer-state patch.

The target result is **selective rescue of ETR fallacies**, not a generic accuracy boost.

### V5 — Distinguish H1/H2/H3

After a causal locus exists:

- **H1 test:** does the intervention specifically restore a formally required alternative?
- **H2 test:** do semantic/prior-head ablations rescue without alternative-state reconstruction, and does predicate abstraction collapse the effect?
- **H3 test:** is the entire causal difference confined to late answer selection with no earlier alternative-state dependence?

## 7. Fatal controls

- No central LLM judge for logical correctness or ETR category.
- Problem-grouped train/test splits for any readout.
- Predicate renaming / content abstraction to separate formal structure from semantic prior.
- Answer-label permutation to remove label preference.
- Non-ETR wrong answers as a crucial control.
- Reverse patching and unrelated-item patching.
- A probe is descriptive until a causal intervention changes behavior.

## 8. Promote / kill criteria for the initial stage

### Promote to full MI if

- the mother reversal-rescue phenotype is faithfully reproduced locally;
- there is a stable, held-out alternative-state target derived from formal ETR, not answer correctness;
- at least one causal intervention selectively affects ETR fallacies more than matched wrong-answer controls.

### Do not force H1 if

- alternative-state readouts are non-causal;
- only late answer-policy patches matter;
- semantic/prior ablations explain the phenotype better.

Those outcomes are still scientifically useful because the paper can establish a concrete **behavioral cognitive-model fit ≠ mechanistic equivalence** result.

### Kill / redesign if

- the public mother artifacts cannot support the reported matched reversal population;
- apparent alternative-state effects reduce to answer-token, lexical, or generic correctness leakage;
- no intervention can distinguish the three hypotheses after the pre-registered causal tests.

## 9. Paper-level narrative

The wide claim is not “we found a logic head.” It is:

> **When humans and LLMs make the same theory-predicted reasoning error, do they converge on the same kind of computation or only on the same output?**

This connects mechanistic interpretability with cognitive modeling, formal reasoning, scaling-induced human-like biases, and the limits of behavioral analogy.
