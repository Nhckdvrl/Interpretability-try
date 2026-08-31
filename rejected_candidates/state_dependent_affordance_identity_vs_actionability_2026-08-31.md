# Object identity != current actionability / state-dependent affordance

Status: **TERMINAL REJECTION (2026-08-31)**

## Natural question

Recognizing an object such as a drawer, door, container, or tool does not imply that the corresponding action is currently possible. Does a VLM rely on category-level affordance priors instead of the object's present physical state when deciding whether it can be opened, grasped, entered, manipulated, etc.?

## Why it looked good

This is a natural external-world distinction with deterministic physical meaning: object identity is relatively stable while actionability changes with current state and geometry. It also offers an intuitive mechanism contrast between a semantic/category prior and state-conditioned physical grounding.

## Kill evidence

The title-level object is already directly occupied in 2026. ACL 2026 `ADAPT: Benchmarking Commonsense Planning under Unspecified Affordance Constraints` introduces DynAfford specifically because embodied agents often execute instructions without checking whether target objects can actually be manipulated. Its core task requires agents to perceive object states, infer implicit preconditions, and adapt actions according to changing affordances. `StateVLM: A State-Aware Vision-Language Model for Robotic Affordance Reasoning` likewise explicitly targets fine-grained object-state understanding and affordance reasoning, including graspable regions.

Therefore `object recognized but current affordance/actionability misread`, `category prior vs present state`, or an MI decomposition of those components is not a new scientific object; it is a direct mechanism successor to an already explicit state-dependent-affordance mother family.

## Death code

`KILL-N0 / DIRECT-STATE-DEPENDENT-AFFORDANCE-MOTHER`

## Nearest-neighbor warning

Do not resurrect via a different object class, robotics dataset, image-only setup, open-vs-closed state, graspability, openability, enterability, category-prior language, or probes/SAEs/patching. These remain state-aware affordance reasoning.

## Resurrection condition

A different physical-world anomaly whose title cannot be reduced to current object-state -> affordance/actionability reasoning, with current-open-model behavior established independently.
