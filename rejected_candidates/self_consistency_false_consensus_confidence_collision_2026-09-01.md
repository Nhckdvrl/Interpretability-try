# Rejection Record — Self-Consistency / False Consensus as Epistemic Confidence

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

If a language model repeatedly gives the same answer across independent samples, does that reflect a genuinely high-confidence knowledge state, or can the model be locked into a stable but wrong attractor that merely produces behavioral agreement?

## Semantic aliases

- self-consistency vs correctness
- false consensus
- repeated answer vs genuine confidence
- stable wrong attractor
- behavioral commitment vs epistemic confidence
- agreement-is-not-accuracy

## Why it looked promising

A 2026 preregistered study on Qwen2.5-7B and Llama-3-8B reports that majority-vote self-consistency can backfire on many hard science questions and that high answer agreement is poorly calibrated to correctness. The natural question `does repeated agreement mean the model really knows?` is broad, easy to explain, and benchmark-removal friendly.

## Decisive kill evidence

The exact internal object is already directly occupied.

- **`When Agreement Fails: Detecting False Consensus via Hidden-State Consistency` (2026)** explicitly defines **false consensus** as high sample agreement on an incorrect answer and asks whether hidden states distinguish trustworthy from spurious consensus. On Qwen2.5-7B-Instruct it finds correct-consensus and wrong-consensus trajectories differ in hidden-state consistency, especially at shallow layers, and builds a hidden-state gate that recovers accuracy lost by naive agreement-based early stopping.

- **`When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement as Confidence Signals` (2026)** directly studies the assumption that self-agreement indicates correctness and concludes agreement is only a weak, regime-dependent confidence proxy; repeated confident errors recur across prompts/providers.

- Contemporary agent work on **premature commitment** further shows hidden-state similarity can predict behavioral consistency/settling while failing to separate committed-correct from committed-wrong trajectories, explicitly distinguishing commitment from truth.

Therefore the proposed scientific object `stable repeated answer = genuine confidence vs wrong attractor` is already a current behavioral and hidden-state object. A new activation-patching/SAE study would mainly deepen an already direct mechanistic question.

## Strongest-neighbor warning

Do not revive as:

- wrong-attractor direction;
- self-consistency confidence circuit;
- agreement-vs-correctness subspace;
- repeated-answer commitment state;
- false-consensus activation patching;
- internal difference between stable-correct and stable-wrong answers.

## Death code

`F2 / N1-N2 — false consensus and its hidden-state signature are already directly studied in modern open LLMs.`

## Resurrection condition

Only reconsider if a distinct model property is found that cannot be reduced to self-consistency, confidence/calibration, premature commitment, hidden-state consistency, or sampling-based uncertainty.
