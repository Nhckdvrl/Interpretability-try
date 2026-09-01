# Rejection Record — Risk vs Ambiguity Decision State

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish uncertainty with **known outcome probabilities** (risk) from uncertainty where the probabilities themselves are **unknown** (ambiguity), rather than treating both as one generic uncertainty signal?

## Semantic aliases

- risk vs ambiguity
- known vs unknown probabilities
- Ellsberg uncertainty
- ambiguity aversion
- Knightian uncertainty vs measurable risk

## Why it looked promising

Risk versus ambiguity is a classic, benchmark-independent distinction from decision theory and cognitive neuroscience. Human behavior and neural evidence support different processing for known and unknown probabilities. The question is immediately intelligible and has natural matched gambles such as the Ellsberg known-urn versus unknown-urn design.

## Decisive kill evidence

The exact modern-LLM behavioral object is already established and has already begun to receive internal interventions.

- 2024 machine decision-making work explicitly evaluates GPT-4 on the Ellsberg paradox.
- More importantly, 2026 `Sparks of Rationality: Do Reasoning LLMs Align with Human Judgment and Choice?` evaluates modern open models including Qwen3 and OLMo3 on a direct known-urn versus unknown-urn ambiguity-aversion task. It reports that neutral Qwen3 exhibits substantial/near-ceiling ambiguity aversion and analyzes the effect across stake sizes.
- The same work uses representation-level/activation steering interventions (RLS/ICP) and shows that internal emotional steering changes the ambiguity-aversion index, including reducing ambiguity aversion toward neutrality in some Qwen3/OLMo3 settings.
- Contemporary work training Qwen-2.5/Gemma models to explain human decisions also explicitly identifies ambiguity aversion among learned cognitive mechanisms.

Therefore `risk vs ambiguity in current open LLMs` is not an unestablished model property. A project learning a risk/ambiguity direction and causally patching the Ellsberg choice would primarily mechanize and refine an already direct behavioral/intervention object.

## Strongest-neighbor warning

Do not revive as:

- risk vs ambiguity direction;
- known-probability vs unknown-probability hidden state;
- Ellsberg circuit;
- ambiguity-aversion steering;
- uncertainty-type subspace in Qwen/Llama;
- mechanistic explanation of Qwen3's known-urn preference.

The absence of a paper whose headline is exactly `risk-vs-ambiguity mechanistic interpretability` is not enough once the scientific object and internal manipulability are already directly studied.

## Death code

`F2 / N1-N2 — modern open-model Ellsberg/ambiguity-aversion behavior and internal interventions are already established; remaining delta is stronger factorization.`

## Resurrection condition

Only reconsider if a distinct decision-science property is found that cannot be reduced to ambiguity aversion, generic uncertainty decomposition, probability weighting, risk preference, or known-vs-unknown outcome probabilities.
