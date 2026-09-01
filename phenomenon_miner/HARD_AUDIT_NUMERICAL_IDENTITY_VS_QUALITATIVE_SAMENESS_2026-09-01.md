# HARD AUDIT — Numerical Identity vs Qualitative Sameness

**Date:** 2026-09-01  
**Status:** `HARD AUDIT / NOT REGISTERED / NO GPU SWEEP`  
**Route:** C (simple natural object first), with an older computational precursor that must be beaten at N2.

## Natural question

> **If two things are exactly alike, does an LLM still know whether they are literally the same individual object or merely two different objects of the same kind?**

Examples:

- one onion that is chopped and later smelled = **same individual token** despite qualitative change;
- a second, identical onion = **different token of the same type** despite high qualitative similarity;
- two identical cups can be qualitatively the same while numerically distinct;
- one cup can change color/shape yet remain numerically the same object.

This is not a benchmark construct. Philosophy/cognitive science distinguish **numerical identity** (one and the same individual) from **qualitative identity/sameness** (sharing properties/type).

## Why this is currently promising

### 1. Independent human scientific object

Dranseika, Nichols & Strohminger (Cognition 2023), `Which kind of sameness? Disambiguating two senses of identity with a novel linguistic task`, explicitly distinguishes numerical sameness from qualitative sameness and exploits languages such as Lithuanian where the two senses can be lexically separated (`same_N` vs `same_Q`). The paper argues that ordinary English `same` conflates two distinct folk-identity judgments and provides multiple experimental windows (including cups/twins and diachronic personal change).

The distinction is older than LLMs and applies across objects, people, temporal change and languages.

### 2. Natural event-comprehension substrate

Solomon, Hindy, Altmann & Thompson-Schill (J Cogn Neurosci 2015) use **120 natural event frames** crossed as:

- same token;
- different token of the same type;
- different token of a different type;

and independently cross minimal vs substantial object change.

Example:

```text
The chef will weigh/chop an onion.
Then she will smell the onion.          # same token
Then she will smell another onion.      # different token, same type
Then she will smell a piece of garlic.  # different type
```

The design was created to distinguish competition between mutually exclusive states of one object token from mere similarity between representations. It is not a synthetic benchmark invented for LLMs.

### 3. Negative result is scientifically meaningful

The question is not `does a benchmark effect exist?`. The natural possibilities are:

- **abstract numerical identity:** the model distinguishes individual identity from type/feature similarity and uses the distinction causally;
- **local token tracking only:** the model can follow discourse entities in some settings but lacks a reusable abstract identity relation;
- **similarity collapse:** representations primarily reflect qualitative/type similarity and fail under same-looking-different-token or changed-same-token cases.

All three answer the same headline question.

## Important correction to the old search gate

Route C v2.1 does **not** require an already published exact Llama/Qwen phenotype before the question can enter HARD AUDIT. A deterministic semantic axis with real external substrate is legal. Cheap capability reproduction may be an execution gate; GPU may not be used to redefine the question after the fact.

Thus `no exact modern-open paper found` is neither a PASS nor a KILL by itself.

## Strongest computational precursor — must not be ignored

Davis & Altmann (Cognition 2021), `Finding event structure in time: What recurrent neural networks can tell us about event structure in mind`, is a serious N2 neighbor.

They train text-only LSTM language models and analyze hidden representations for the same event family. Study 2 explicitly compares:

```text
... weigh the onion      # same token
... weigh another onion  # different token, same type
```

and concludes that the RNNs are sensitive to the distinction between **the same token** and **a different token of the same type**.

This means the project CANNOT claim novelty as:

> `neural language models distinguish same-token from another-token.`

That object has an older computational precedent.

## Exact N2 delta required for survival

The only sufficiently wide version is the **abstract identity relation** question:

> **Do modern autoregressive LLMs maintain a reusable representation of numerical identity that is separable from qualitative/type similarity and survives changes of surface form, object properties, task, domain and linguistic realization?**

The paper must go beyond the Davis–Altmann event-specific result in at least the following ways:

1. **cross-domain abstraction** — not only event-state propagation/onions;
2. **double dissociation** — same token despite substantial qualitative change AND different token despite near-identical qualities;
3. **cross-surface generality** — not reducible to `the` vs `another`, noun repetition, recency, or explicit IDs/names;
4. **causal use** — the identity representation must affect identity-sensitive downstream inference, not merely be decodable;
5. ideally **cross-linguistic lexicalization** — languages that independently lexicalize numerical vs qualitative sameness provide a natural validation window rather than an English `same` prompt artifact.

If these cannot be established, the project reduces to `RNN result -> modern LLM + stronger MI` and is **KILL-NOVELTY**.

## Hard confounds

A valid result must separate numerical identity from:

- exact lexical repetition;
- definite article vs `another` cue;
- recency / most-recent-mention preference;
- ordinary coreference resolution;
- entity/name matching;
- qualitative embedding similarity;
- object type/category identity;
- state-change magnitude;
- one-mention vs two-mention counting;
- world plausibility and lexical association.

## Candidate natural measurement windows

### Window A — event token × change

Solomon et al. 2015:

```text
referent: same-token | different-token-same-type | different-type
change:   minimal | substantial
```

This is valuable because it directly creates the two crucial cross-cases:

- same numerical object despite large qualitative/state change;
- different numerical object despite same type/high similarity.

### Window B — explicit numerical vs qualitative sameness language

Dranseika et al. 2023:

- Lithuanian `same_N` / `same_Q` task;
- cups/twins and diachronic identity windows;
- potential Spanish/German/Lithuanian lexical validation where numerical and qualitative sameness have different conventional expressions.

This window helps avoid defining the object solely through English `the` / `another`.

### Window C — independent identity-sensitive downstream inference

Need a public/natural task where correct inference changes depending on whether a later mention is:

- the same object with changed properties;
- a different but qualitatively matching object.

This window is NOT yet frozen. It must be found rather than invented post hoc.

## Cheap S0 philosophy

Do not run a broad GPU sweep to ask whether the paper question exists. The axis already exists externally.

A legal cheap execution gate can ask whether a prespecified analyzable open checkpoint understands the frozen contrasts without prompt engineering. A null result answers part of the frozen question (`modern model collapses/does not robustly use numerical identity on this substrate`) and cannot trigger a new identity story.

Modern checkpoints can be selected for analyzability (e.g. Llama/Qwen) rather than because a prior paper already published the exact effect.

## Causal-use target — provisional, not yet frozen

A strong causal question would be:

> Does an identity-sensitive state learned without explicit `same/different` labels causally determine whether properties/history are transferred from an earlier mention to a later referent?

Necessary control pattern:

- perturb toward **same-individual** should increase transfer of token-specific history only when identity is genuinely ambiguous/contested;
- it must NOT simply increase lexical coreference or generic semantic similarity;
- perturb toward **different-individual-same-type** should block token-specific history transfer while preserving type/category knowledge;
- generic entity-tracking / recency controls must not reproduce the effect.

This contract needs further hardening before registration.

## Current novelty verdict

```yaml
natural_question: PASS
benchmark_removal: PASS
natural_object: PASS
human_scientific_object: PASS
natural_cross_cells: PASS
human_row_level_substrate: STRONG
modern_open_exact_phenotype_required_by_rule: false
modern_analyzable_checkpoint_available: true
N0_direct_modern_LLM_collision: NOT_FOUND_SO_FAR
N2_older_RNN_same_token_vs_same_type_precursor: SERIOUS
exact_required_delta: abstract_cross_domain_numerical_identity
central_confound_control: NOT_YET_FULLY_FROZEN
independent_causal_readout: NOT_YET_FROZEN
verdict: HARD_AUDIT
PASS_REGISTER: false
GPU_AUTHORIZED: false
```

## Next audit steps

1. exhaustive novelty search for aliases: numerical identity, qualitative identity, token/type identity, sameness, re-identification, identity persistence, same-object vs identical-object, token/type event representation;
2. inspect Davis–Altmann code/stimuli and determine exactly how broad their representation claim is;
3. recover/audit row-level stimuli for Solomon 2015 and Dranseika 2023;
4. find one independent natural downstream window where numerical identity changes inference while type similarity is matched;
5. freeze a causal-use statistic that cannot be reduced to coreference or recency;
6. only then decide PASS vs KILL.

## One-line discipline

> **This lead is promising because the natural object and cross-cells are unusually clean. It survives only if the paper is about an abstract numerical-identity relation, not merely re-running `the onion` vs `another onion` with a newer model and activation patching.**
