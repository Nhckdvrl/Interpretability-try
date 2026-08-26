# Single Replacement Search After 006 — 2026-08-27

**Goal:** find exactly one replacement candidate under the natural-phenomenon-first rule.

## Selected candidate — Piagetian conservation under physical transformation

### Natural mother phenomenon

When an object or collection changes appearance, some quantitative properties remain invariant: spreading coins does not change their number; reshaping clay does not change its amount; pouring liquid into a differently shaped container does not by itself change volume. Developmental psychology studies why a reasoner can be misled by salient appearance changes even when the underlying quantity is unchanged.

This phenomenon exists independently of VLMs and has a mature cognitive account involving both transformation-invariant representation and inhibition of misleading perceptual heuristics.

### Existing behavioral evidence

ICML 2026 `Vision Language Models Cannot Reason About Physical Transformation` introduces ConservationBench: 192 conserving videos plus 192 matched non-conserving controls across number, length, size, and volume, evaluated under many prompt/frame conditions over 112 VLMs.

Key evidence:

- human accuracy: ~98.35%;
- 82/112 VLMs have strict paired accuracy below 10%;
- only three top systems exceed the 33.3% chance level under the strict paired criterion;
- Qwen3-VL-8B-Instruct: conserve 53.12%, non-conserve 31.52%, strict 8.59%;
- Qwen3-VL-8B-Thinking: conserve 52.92%, non-conserve 16.31%, strict 7.42%;
- performance on conserving and non-conserving tasks is negatively correlated (r≈-0.51), indicating default heuristics rather than a generic low-accuracy problem;
- prompting, more frames, and curated frame selection do not repair the failure.

### Decisive mechanism question

Why does appearance change defeat quantity conservation?

Competing explanations:

- **H1 Endpoint quantity representation failure:** the model never forms an adequate representation of the relevant quantity in one or both states.
- **H2 Transformation/invariant tracking failure:** endpoint quantities can be represented, but the model fails to maintain or compare the invariant through the dynamic transformation.
- **H3 Appearance-heuristic override / inhibitory failure:** the relevant quantity/invariance signal survives internally, but salient visual heuristics dominate the final decision.

The H3 branch is independently motivated by the human cognitive literature on Piagetian conservation, where failures have been linked to inability to inhibit misleading perceptual heuristics such as `longer row -> more items`.

### Collision audit

- ConservationBench itself is behavioral: it provides matched controls, prompt/frame ablations, text/empty-image controls, and broad model evaluation, but not causal hidden-state analysis adjudicating H1/H2/H3.
- WM-ABench is a broader atomic world-model benchmark, not a mechanism study of conservation.
- VLM-Lens is a general interpretability toolkit with demonstration analyses, not a conservation mechanism paper.
- Targeted searches for conservation / physical transformation with activation patching, causal tracing, or mechanistic interpretability did not surface a direct work that answers the matched conservation-vs-nonconservation mechanism question.

### Cheap G0

Do not regenerate the phenomenon. Reuse the published matched conserving/non-conserving examples and run a small local subset on an analyzable open VLM (Qwen3-VL-8B first; a second open family/architecture for confirmation if practical). Replace free-form judging with constrained A/B/C teacher-forced scoring or exact option-token scoring, so no commercial API or LLM judge is needed.

G0 asks only whether the published strict paired failure survives our local deterministic readout on the pinned model(s). If it does not, stop.

### Mechanism → method

- H1 -> improve/align quantitative visual state representations;
- H2 -> train or route transformation-invariant state tracking/comparison;
- H3 -> selectively gate/suppress appearance heuristics when they conflict with conserved-quantity evidence.

These are meaningfully different repairs, so the mechanism result matters to the method.

## Verdict

`PRE-CANDIDATE / RECOMMENDED REPLACEMENT FOR 006`

This is preferred over 006 because the external phenomenon is natural, the behavior is already large and broad, the decisive contrast is matched and public, and the white-box mechanism question remains open.
