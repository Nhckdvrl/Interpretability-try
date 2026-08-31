# PASS-REGISTER 02 — From Pixels to Perspectives: Reference-Frame Transformation in VLMs

Status: `PASS-REGISTER`
Date: 2026-08-31
Route: `A/B bridge — mechanistic mother object + independently established behavioral axis`

## Natural question

> A VLM first sees locations in the camera/image plane. When the question asks for *someone else's* left/right/front/back, how does the model internally change coordinate frames?

## Mechanistic mother

**Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models** (Kang et al., ICLR 2026).

Scientific object: content-independent **spatial IDs** bound to object-word activations and causally used for spatial reasoning.

Operational mother object is unusually concrete:
- universal IDs are derived from objects placed on a `4×4` image grid;
- the released pipeline extracts explicit horizontal and vertical directions as `{model}_x.pt` and `{model}_y.pt`;
- spatial-ID steering causally changes left/right and other spatial beliefs;
- released extraction covers LLaVA, LLaMA, Qwen, InternVL and Gemma checkpoints;
- official `mirror_attr_swapping` traces transfer under a horizontal image flip, but does not change the coordinate-system origin/orientation requested by the query.

Thus the mother establishes an **image-plane/camera-grounded x/y code**, but does not ask how that code is transformed when a task demands another frame of reference.

## Behavioral mother / natural omitted variable

**Do Vision-Language Models Represent Space and How? Evaluating Spatial Frame of Reference under Ambiguities** (Zhang et al., ICLR 2025 Oral; COMFORT).

Frame of reference (FoR) is a classical variable in spatial cognition and spatial language, not a paper-invented label.

COMFORT-CAR places the same spatial scene under multiple legitimate origins:
- Camera / egocentric frame;
- Addressee-centered frame;
- Relatum/intrinsic frame.

It establishes that VLMs often prefer the egocentric frame and fail to flexibly adopt alternative FoRs. Crucially, **LLaVA-1.5-7B and LLaVA-1.5-13B appear in COMFORT and in the spatial-ID mother pipeline**, so the behavioral axis and mechanistic object meet on analyzable open checkpoints rather than requiring a speculative cross-model G0.

COMFORT's claim about “underlying coordinate systems” is inferred from output-probability curves against analytic FoR conventions; it does not localize or causally intervene on hidden spatial-ID representations.

## The unasked computation

Given a camera/image-plane spatial ID and a query specifying another perspective, how is the required coordinate transformation implemented?

### H1 — Late linguistic remapping

The visual/spatial ID remains camera-centric throughout most of the model. A late language/readout computation maps camera-relative relations into words appropriate for the requested perspective.

Prediction: projections onto mother x/y IDs remain camera-aligned across layers even under Addressee/Relatum queries; only late answer-token states change. Analytically rotating the ID early will not behave like a natural FoR change.

### H2 — Explicit intermediate coordinate transform

The model actively rotates/reflects/rebases the camera spatial code into a target-frame code before answering.

Prediction: a layer-local transformation of the x/y spatial-ID geometry should track the requested frame. Patching the transformed state from a correctly answered target-FoR run into a matched failure should selectively rescue that FoR.

### H3 — Multiple frame-specific codes + selector

Camera-, addressee-, and relatum-centered spatial codes coexist; the question controls a selector/gate rather than numerically transforming one code.

Prediction: frame-specific subspaces remain simultaneously decodable, but causal influence changes with the query. Patching the frame-selection state should switch interpretations while preserving object locations.

## Core causal tests

### 1. Matched FoR intervention

Use COMFORT-CAR scenes while changing only the requested FoR. Track mother spatial-ID projections and causal influence across layers.

### 2. Analytic spatial-ID transform

Because the mother exposes horizontal/vertical ID axes, construct the geometrically prescribed rotation/reflection/rebasing for a target FoR and inject it into object-word activations. Compare against:
- native target-FoR prompting;
- random same-norm directions;
- simple left/right sign flip;
- late label remapping;
- unrelated-scene ID patches.

A selective target-FoR answer change would be substantially stronger evidence than generic spatial steering.

### 3. Selector patch

Patch only query/frame-cue states across Camera/Addressee/Relatum prompts while holding the image fixed. This discriminates an explicit transformed code from a multi-code selector mechanism.

### 4. Failure decomposition

COMFORT reports an egocentric preference. Determine whether failures arise from:
- inability to construct non-camera coordinates;
- successful construction but failure to select/use them;
- successful spatial transformation followed by wrong linguistic readout.

This converts a benchmark failure into a mechanistic taxonomy with different remediation targets.

## Strongest-neighbor audit

1. **Kang et al., ICLR 2026** — owns spatial IDs, causal steering, image mirroring, depth diagnosis, and generic information transfer; does not study Camera/Addressee/Relatum reference-frame transformations.
2. **COMFORT, ICLR 2025 Oral** — owns the FoR behavioral phenomenon and output-probability fitting; no hidden-state causal mechanism.
3. **The Dual Mechanisms of Spatial Variable Binding in Vision-Language Models** (2026) — activation patching shows vision-encoder and LM-backbone ordering mechanisms on Qwen2-VL/Gemma; does not study viewpoint/reference-frame conversion.
4. **Knowing Isn't Always Saying: When Do Spatial Encodings Reach Answers in Vision-Language Models?** (Aug. 2026) — direction patching studies conditional transport of spatial-ID information to answer logits; does not introduce or mechanistically factor a reference-frame variable.
5. Perspective-aware / allocentric works (APC-VLM, Allocentric Perceiver, AlloEgo-VLM, SymPL/GCA) perform explicit external coordinate conversion, prompting, training, or symbolic geometry; they motivate the distinction but do not reverse-engineer the pretrained VLM's internal spatial-ID transformation.

Targeted searches for `spatial ID + reference frame`, `egocentric/allocentric + activation patching`, `coordinate transformation + mechanistic VLM`, and `perspective taking + causal tracing` found no direct occupancy as of 2026-08-31.

## Anti-narrowing / ACL-EMNLP narrative

The paper is not “another spatial benchmark.” Its broad question is:

> **When a multimodal model must reason from a perspective different from the camera's, does it transform its internal world representation, select among latent coordinate systems, or merely translate an egocentric answer at the end?**

This connects:
- multimodal mechanistic interpretability;
- perspective taking and spatial language;
- egocentric vs allocentric representation;
- embodied/robotic reasoning;
- cross-lingual/cultural FoR conventions;
- diagnosis of whether failures are perception, transformation, selection, or readout failures.

Even a null result is informative: if COMFORT behavior changes without any corresponding transformation of causal spatial IDs, it establishes a dissociation between output-level coordinate-system fits and the model's actual internal spatial code.

## Registration rationale

- strong concrete mechanistic mother: YES
- exact mother object available in code: YES (`x/y` image-plane spatial IDs)
- omitted variable independently grounded: YES (FoR)
- behavioral mother already establishes FoR phenotype: YES
- overlapping analyzable open checkpoints: YES (LLaVA-1.5-7B/13B)
- public artifacts: YES (both mothers)
- no expensive behavior-discovery G0 needed: YES
- N0 title ownership clean: YES
- N1 causal-computation ownership clean after Aug-2026 search: YES
- >=2 competing causal mechanisms: YES (3)
- discriminating intervention: YES (analytic ID transform + selector patch)
- broad ACL/EMNLP/VLM narrative: YES

`PASS-REGISTER = 2/5` after this registration.
