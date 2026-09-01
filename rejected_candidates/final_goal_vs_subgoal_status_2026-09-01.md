# Rejection — Final Goal vs Subgoal Status

Date: 2026-09-01  
Verdict: **KILL-SCALE / KILL-BEHAVIOR**

## Natural question

Does an LLM planner internally distinguish **the thing it ultimately needs to achieve** from **an intermediate state that is only useful on the way there**?

## Semantic aliases

- final goal vs subgoal
- objective vs milestone
- end state vs waypoint
- parent goal vs intermediate goal

## Why it looked promising

The distinction is easy to explain, directly relevant to long-horizon agents, and could support clean hierarchical-plan interventions.

## Decisive kill evidence

Current LLM-agent/planning literature is already saturated with **explicit goal decomposition into subgoals**, e.g. G2RL-LM, MiRA, ReCAP and 2026 latent/subgoal planning frameworks. Yet these works do not establish a surprising native-model phenomenon showing that `final-goal status` and `subgoal status` are a hidden semantic distinction worth discovering internally.

Representative sources:

- https://chirikjianlab.github.io/G2RL-LM/
- https://arxiv.org/abs/2603.19685
- https://arxiv.org/abs/2510.23822

To create a clean MI study we would have to define hierarchical plans, label goal levels, and then ask whether those experimenter-supplied labels are encoded. That risks a **synthetic/formal annotation creating the object**, not a pre-existing behavioral/model fact. The obvious positive result (`the model can decode which line is the final goal`) is also too unsurprising to carry a Main-paper Route-C headline.

## Strongest-neighbor warning

Do not revive as goal-level probe, parent-vs-child plan direction, subgoal hierarchy SAE, or milestone-status patching merely by changing the planning benchmark.

## Death code

`F1/F8 — no independently established surprising phenotype; central object collapses toward experimenter-defined plan-role labels.`

## Resurrection condition

Only reconsider if prior/released model behavior reveals a robust, unexpected **goal-status phenomenon** that exists before our hierarchy annotations and whose explanation is paper-scale.
