# Implicit-causality production/comprehension sharing

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Semantic aliases

- shared production/comprehension event-causal representation
- implicit-causality shared state vs modality-specific readout
- production prior reused in pronoun interpretation
- next-mention prior vs pronoun-interpretation mechanism
- Bayesian reference architecture in LLMs

## Natural question

Do language production and comprehension in LLMs reuse a shared event-causal representation, with modality-specific readout producing their asymmetry, or are causal biases separately computed in production and interpretation?

The external question is real: psycholinguistics has long debated the extent to which production and comprehension share representations/processes, and Bayesian reference models relate interpretation to a production/next-mention prior plus a form-specific likelihood.

## Why it initially looked unusually strong

ACL 2025 Short `Leveraging Human Production-Interpretation Asymmetries to Test LLM Cognitive Plausibility` provides 541 production and 541 interpretation items and releases row-level outputs for Llama-3.1-8B-Instruct, Llama-3.3-70B-Instruct, Qwen2.5-32B-Instruct, and GPT-4o. Llama models show IC effects in both modes under preregisterable prompts and can show the production/interpretation asymmetry; Qwen provides a pre-existing dissociation (interpretation IC effect but no production IC effect).

## Decisive N2 kill

The conceptual mechanism question is too tightly entailed by the mother paper's own core motivation.

The mother introduction explicitly explains the human production/interpretation asymmetry as interpretation combining the next-mention bias with the bias/likelihood of using a pronoun for a referent, and states that it is unknown whether/how LLMs handle this difference because their native next-token probability does not directly expose the required conditional decomposition. The paper then makes the production-vs-interpretation distinction its central research object.

Therefore a causal study asking whether the same event-causal/production state is reused in interpretation, versus whether the two tasks use separate readouts, most naturally reads as:

> ACL'25 established the production/interpretation asymmetry and its theoretical decomposition; we reveal how the model internally implements that decomposition.

That is exactly the behavior -> mechanism step that the current N2 delta-width rule rejects unless a wider independent scientific axis remains.

The novelty surface is additionally narrowed by COLING 2025 `Unveiling Language Competence Neurons`, which already performs targeted neuron ablation and activation manipulation for implicit causality in GPT-2-XL. It does not test production/comprehension sharing, but it means the IC internal-mechanism space is not empty.

## Data note

The rejection is **not** a substrate rejection. The LingMechLab repository is unusually good: row-level CSVs for all four model conditions, exact stimuli, prompts, and local Hugging Face inference code are public.

## Nearest-neighbor warning

Do not resurrect by renaming the shared state as `event model`, `causal role`, `production prior`, or `Bayesian prior`, or by using cross-task activation patching. Those are implementations of the same mother-motivated decomposition.

## Resurrection condition

Only reopen if a broader independent production/comprehension theory question can be instantiated across multiple unrelated linguistic phenomena (not just IC/reference) with already-public matched modern-open-model behavioral windows, such that implicit causality is merely one validation window rather than the source of the headline question.
