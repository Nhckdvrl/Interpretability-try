# Rejected Candidate — Object Recognition ≠ State-Dependent Affordance

Date: 2026-08-31
Status: **TERMINAL REJECTION**

## Natural question

> Recognizing what an object is does not by itself tell us what actions are physically possible in its current state. Do VLMs distinguish object identity from state-dependent affordance, or do they fall back to category-level action priors?

Examples include a container that must be open before inserting something, a graspable part whose current state changes where interaction is possible, or an object whose present configuration blocks an otherwise typical action.

## Why it looked good

- This is an everyday physical-world distinction rather than an LLM-internal benchmark construct.
- The object category can stay fixed while physical state changes, providing natural within-object controls.
- Affordance is action-relevant and potentially supports a meaningful mechanism question: category prior versus state-sensitive physical representation.
- Current embodied/VLM literature reports failures where agents recognize scenes and instructions yet choose physically invalid actions.

## Kill evidence

The title-level object is already directly occupied in 2026.

`StateVLM: A State-Aware Vision-Language Model for Robotic Affordance Reasoning` explicitly targets fine-grained object states together with affordance reasoning and introduces the Object State Affordance Reasoning (OSAR) benchmark. The paper is not merely using object state as a control; `state-aware affordance reasoning` is the named scientific object.

CVPR 2026 `BOP-ASK: Object-Interaction Reasoning for Vision-Language Models` independently makes object affordances, physical compatibility, and interaction reasoning central evaluation dimensions, explicitly arguing that conventional visual/spatial recognition masks these interaction failures.

Other 2026 embodied work likewise explicitly decomposes affordance representations for manipulation and treats state/progress-conditioned interaction as a first-class modeling target.

Therefore a mechanistic project asking whether hidden states separate object identity/category from current-state affordance, or where category priors override state cues, is a direct behavior/method-object → mechanism continuation rather than a new title-level scientific object.

## Death code

`KILL-N0 / DIRECT-STATE-AFFORDANCE-MOTHER`

## Nearest-neighbor warning

Do not resurrect as:

- identity vs affordance;
- category prior vs functional state;
- open/closed container affordance;
- graspability vs object recognition;
- physical compatibility vs semantic recognition;
- another household-object dataset or robot benchmark;
- a probe, SAE, activation-patching, or steering study of `affordance features`.

Those remain inside the already named state-aware/object-interaction affordance family.

## Resurrection condition

Only reconsider if a separate natural physical phenomenon is found whose title-level question is not object affordance, object-state localization, physical compatibility, graspability, or interaction reasoning, and where affordance is merely a downstream control rather than the object of study.
