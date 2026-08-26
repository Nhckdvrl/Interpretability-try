# Rejected Candidates — Multimodal Grounding / Perception–Knowledge Conflict

**Domain:** VLM perception–knowledge conflicts, counterfactual familiar objects, visual prior override, visual illusions.  
**Status:** current breadth-first scan closed after direct 2026 mechanism collision.

---

## 1. Familiar-object prior overrides counterfactual pixels

**Natural question:** If an image clearly shows an impossible or counterfactual version of a familiar object, why does a VLM answer with the familiar real-world property instead of what is visibly present?

**Why it initially looked good:** Extremely visual and intuitive: a five-legged dog, a four-stripe Adidas logo, or another familiar object is directly observable, yet prior knowledge can override the pixels. It offers a clean natural competition between perception and memorized knowledge and a straightforward causal-intervention story.

**Kill evidence:** The behavioral space is already populated by counterfactual visual benchmarks. More decisively, `Vision-Default, Prior-Override: Causal Mechanisms of Perception-Knowledge Conflict in Vision-Language Models` (June 2026) gives a component-level causal account across three VLM families using activation patching and ablation. It finds sparse late attention heads that are causally necessary for prior-grounded answers, decomposes them into routing and writing roles, and flips many prior-grounded outputs back toward visual grounding by ablation. This directly occupies the proposed mechanism narrative.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** Do not revive as counterfactual object attributes, impossible familiar objects, logo modifications, color conflicts, count conflicts, or “pixels vs world knowledge” on another VLM.

**Resurrection condition:** Need a perceptual failure whose decisive contrast cannot be reduced to perception–parametric-knowledge conflict and whose causal mechanism predicts a distinct intervention.

**Key reference:** https://arxiv.org/abs/2606.28273

---

## 2. Generic visual-illusion belief despite measurable pixels

**Natural question:** Why does a VLM report the familiar illusion interpretation even when its own visual measurements or annotations contain evidence for the physically correct answer?

**Why it initially looked good:** The phenomenon is vivid and independently established in human perception; some VLM studies report a dissociation between extracting useful visual annotations and making the final inference.

**Kill evidence:** The generic story sits too close to the now-mechanized perception–knowledge conflict family. In addition, `Seeing the Evidence, Missing the Answer` (2026) already behaviorally frames visual-illusion failures as a dissociation between evidence extraction and inference and evaluates tool-assisted fixes. Without a sharper phenomenon, a mechanistic version is likely to read as “another prior-overrides-vision case.”

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** Müller-Lyer, Ebbinghaus, Ponzo, impossible-object, or counterfactually modified illusion variants do not create novelty by themselves.

**Resurrection condition:** A specific illusion must show a surprising computation absent from generic prior override—for example, the correct metric relation is causally represented and used in nearby tasks, but a separate illusion-triggered transformation reverses only the final relation.

**Key references:** https://arxiv.org/abs/2606.28273 ; https://arxiv.org/abs/2603.20100

---

# Current lessons from the domain

1. “VLM sees X but says memorized Y” is now directly mechanized in 2026 and should be treated as occupied.
2. Counterfactual-image benchmarks are useful G0 sources, but switching object property or VLM family does not restore novelty.
3. A viable multimodal topic now needs a different natural computation than generic visual-vs-prior routing.