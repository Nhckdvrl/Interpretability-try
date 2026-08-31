# Directed vs random exploration in LLM agents

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- information-bonus vs decision-noise exploration
- directed vs random exploration
- UCB-like vs stochastic exploration
- uncertainty bonus vs choice-temperature mechanism

## Natural question

When an LLM agent explores uncertain options, does it deliberately add value to informative choices (directed exploration), increase stochasticity to explore at random, or combine both computations?

This is a classic decision-science question and easily passes benchmark removal.

## Decisive N2 kill

The LLM-specific strategy-level axis is already directly occupied before mechanistic interpretability.

`Comparing Exploration-Exploitation Strategies of LLMs and Humans` (2025/updated 2026) uses canonical cognitive-science bandit tasks and interpretable choice models specifically to decompose LLM behavior into directed and random exploration and reports that reasoning-enabled LLMs show a mixture of both.

The August 2026 `Semantic Bandits` paper explicitly characterizes this prior work as model-based analyses separating directed exploration, random exploration, perseveration, and related choice components, while contributing a separate semantic-prior axis.

A new activation-patching/circuit paper asking whether the observed choice parameters arise from an information-bonus pathway or decision-noise pathway would therefore most naturally be described as validating/internalizing an already-claimed LLM strategy decomposition. That fails the current N2 delta-width test.

## Nearest-neighbor warning

Do not resurrect by changing the bandit task, horizon, model family, or by framing `reasoning vs no reasoning` as a mechanism. The directed/random strategy axis itself has already been used as the LLM scientific object.

## Resurrection condition

Only reopen if a genuinely new decision-theoretic axis is identified that is orthogonal to directed/random exploration and already has natural behavioral cross-cells on modern open models, rather than merely explaining how the published exploration parameters are represented.
