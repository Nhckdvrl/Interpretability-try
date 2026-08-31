# V2 causal state audit protocol

## Frozen population

Recipients are exactly the 24 items satisfying all of:

1. model family: local cached Meta-Llama-3.1-8B-Instruct mirror;
2. regular/positive-direction `BrokenLinkedListRephrase` prompt;
3. independently rescored V0 phenotype is hard-wrong/follow-up-correct;
4. greedy V1 replay phenotype is also hard-wrong/follow-up-correct.

Reverse wording is excluded from the recipient population. It remains available only as an answer-polarity control. The 13 hard-truthful controls likewise agree between independently rescored V0 and deterministic V1.

## Deterministic environment state

For each frozen item, `build_v2_population.py` records:

- ordered node chain and every present directed edge;
- the unique missing edge and its chain index;
- source and target nodes;
- directed reachability and correct answer;
- source-side and target-side components;
- character spans for each visible fact edge and query entity.

These fields come from graph traversal over released problem metadata. No model output or released `correctness` column is used as graph truth.

## Completed answer-state preflight

`trace_v2_answer_state.py` applies the model's final RMSNorm and unembedding to every intermediate prompt-final residual state, measuring the `No − Yes` logit margin. Every cohort has correct answer `No`, so this comparison does not exploit between-item answer polarity.

This trace is descriptive. It can locate when an answer state becomes available, but it cannot distinguish a correct reachability representation from a generic answer-token state.

`run_v2_transplant_preflight.py` replaces the hard prompt's final-token residual state at selected layers. It compares:

- the same item's easy-correct donor;
- a shuffled easy-correct donor;
- a hard-truthful donor;
- a same-norm random displacement.

Matched and shuffled easy donors have essentially identical effects. Consequently, whole-state rescue is treated only as evidence that the transplantation primitive works.

## Required graph-specific causal test

The next intervention must isolate graph state from answer state:

1. construct a balanced graph-state × query-polarity panel, with the same graph identities represented under reachable/unreachable and positive/reverse questions;
2. learn edge-existence and reachability readouts with graph-instance-grouped splits;
3. reject any direction that merely tracks `Yes` versus `No` or prompt wording;
4. localize the earliest layer/token where the graph-state direction has held-out signal;
5. on hard-deceptive recipients, replace only the localized low-rank graph component with a matched correct-state coefficient;
6. compare against shuffled graph donors, answer-direction patches, unrelated-edge patches, and same-norm random patches;
7. reverse the intervention on hard-truthful runs.

## Paper-level decision rule

Evidence for a latent correct state requires all of the following before answer emission:

- held-out, answer-controlled decoding of the true missing-edge/reachability state in hard-deceptive runs;
- a causal effect from intervening on that localized graph component;
- graph-matched intervention outperforming shuffled answer-state transfer;
- specificity against unrelated-edge, answer-direction and random controls.

If these conditions fail while easy/truthful graph states pass them, the result supports reasoning-state corruption rather than late deceptive policy override. If they pass and a later intervention changes only answer selection, the result supports a late override account.
