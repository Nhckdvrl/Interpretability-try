# Rejection — Concrete vs Abstract Representation

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a language model internally distinguish **concrete things that can be directly experienced** from **abstract concepts**?

## Semantic aliases

- concrete vs abstract
- concreteness representation
- abstract concept representation
- experiential grounding vs abstraction

## Why it looked promising

This is a nearly ideal simple semantic axis on naturalness alone: ordinary people understand it immediately, large human concreteness norms exist, and matched words can support a clean representation/causal-use experiment.

## Decisive kill evidence

Xie et al., **“Distinguishing Concreteness Differences in LLM Representations via Linear Probing”** (CogSci 2026) already makes **how concreteness is represented across LLM layers** its direct scientific object. It probes Qwen3 and Gemma3-Instruct hidden representations using human concreteness ratings and explicitly characterizes layer-wise linear separability from abstract to concrete.

Sources:

- https://escholarship.org/uc/item/835897q6
- https://research.manchester.ac.uk/en/publications/distinguishing-concreteness-differences-in-llm-representations-vi/

Recent work on human–LM representational alignment and abstract/concrete grounding further crowds this axis. Adding activation patching or steering would mainly upgrade the method from probe to causal MI while retaining the same object, which fails N2.

## Strongest-neighbor warning

Do not revive as:

- concreteness direction;
- abstractness SAE feature;
- concrete/abstract steering;
- grounded-vs-abstract hidden state;
- a different human concreteness norm or model family.

## Death code

`F2 / N0-N2 — direct 2026 hidden-representation ownership of the exact semantic axis.`

## Resurrection condition

Only reconsider if a new independent property can be orthogonalized from concreteness and remains a paper-scale question after removing the CogSci 2026 object.
