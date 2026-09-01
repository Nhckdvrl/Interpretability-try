# 041 Second Hard Re-Audit — strict post-5/5 standard

Date: 2026-09-01  
Verdict: **STRICT-PASS RETAINED / CLAIM NARROWED / GPU AUTHORIZED**

## Frozen question

> When a description contains several properties, does an LLM know which property is actually narrowing down which object we mean, and which property is merely extra description in the current context?

Frozen object remains:

> **same-lexical, context-conditioned modifier set-restriction role**, causally separable from ordinary property truth.

## Why this second audit was necessary

After the base 5/5 target was reached, the acceptance bar was raised in `phenomenon_miner/STRICT_EXTENSION_GATE_2026-09-01.md`. 041 was therefore attacked as though it were a new 042+ candidate.

The main question was whether recent 2025–2026 referring-expression work has already occupied `which descriptor is necessary/discriminative` strongly enough that 041 collapses to method-only novelty.

## New strongest neighbors

### ICLR 2026 — Ref-Adv

`Ref-Adv: Exploring MLLM Visual Reasoning in Referring Expression Tasks` constructs hard-distractor referring-expression items with only the information necessary to uniquely identify a target and explicitly performs descriptor-deletion sufficiency and word-order ablations.

This is a stronger collision than the earlier generic reference-resolution literature.

**It owns:**

- hard distractor discrimination;
- minimal necessary descriptive information;
- descriptor deletion as a behavioral necessity test;
- failures caused by redundant descriptors / shortcut grounding.

Therefore 041 may **not** claim novelty as:

> `which descriptor is necessary?`

or

> `models know which adjective is discriminative/informative`.

### 2026 reinforced / discriminative reference-generation work

Recent multimodal reference-game work directly trains descriptions to distinguish a target from distractors. Together with older incremental reference and neural-pragmatic models, this means behavioral discriminativeness is a thoroughly occupied object family.

## Exact surviving N2

041 survives only at the following narrower level:

> **Does the same lexical modifier acquire an abstract functional state according to whether it currently reduces the live discourse candidate set, does that state transfer across lexical/property/domain/surface families, and does changing that state causally alter modifier-specific referent narrowing while preserving the modifier's ordinary property truth?**

This is not equivalent to descriptor necessity because the decisive role-swap keeps the whole world, target phrase and modifier truths fixed while only the currently live candidate set changes.

## Strict-extension locks

### Lock A — same-surface / role-swap identifiability: PASS

Canonical world:

```text
A = large red circle
B = large blue circle
C = small red circle

target phrase = "the large red circle"

live {A,B}: red restricts, large does not
live {A,C}: large restricts, red does not
```

Object facts and wording are fixed; contextual role swaps.

### Lock B — cross-setting abstraction: PASS

Mandatory held-out transfer across:

- property families;
- noun/object domains;
- candidate-set wording;
- modifier order.

### Lock C — two independent theory consequences: not required for retention

041 already passes Locks A+B. Its causal consequence is referent narrowing, with property truth as the specificity denominator.

## Causal specificity retained

Primary statistic remains a Role × Intervention interaction on `ReferentMargin`.

The intervention must preserve `PropertyTruthLogit`.

If recent reference benchmarks can fully explain the result as ordinary descriptor necessity, or if a same-lexical role direction fails held-out transfer, the project dies.

## New fatal novelty condition

Kill 041 if a prior neural/LLM paper is found that jointly establishes:

1. same lexical modifier switching restrictive role because only the live referent set changes;
2. a transferable internal role representation beyond individual property/scene facts;
3. causal editing of that role changing referent narrowing;
4. preservation of the underlying property representation.

Behavioral descriptor deletion alone is now explicitly **not enough to protect 041's novelty**, but it is enough to kill any weaker version of 041.

## Final second-audit verdict

```yaml
base_v2_1: PASS
strict_extension_gate_applied: true
new_neighbors_strengthened: true
behavioral_descriptor_necessity_claim: OCCUPIED
exact_same_lexical_contextual_role_object: CLEAR
Lock_A_role_swap: PASS
Lock_B_cross_setting_transfer: PASS
specificity_denominator: PropertyTruthLogit
N2: PASS_ONLY_FOR_NARROW_FROZEN_OBJECT
PASS_REGISTER: true
GPU_AUTHORIZED: true
```

> **041 stays alive, but only as a context-conditioned semantic-role paper. If it becomes a descriptor-importance or referring-expression benchmark paper, kill it immediately.**
