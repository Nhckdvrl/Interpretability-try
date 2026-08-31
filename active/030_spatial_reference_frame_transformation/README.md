# 030 — From Pixels to Perspectives: Reference-Frame Transformation in VLMs

Status: **ACTIVE / PASS-REGISTER / INITIAL VALIDATION NOT YET RUN**  
Route: **Hamdi Route A/B bridge — mechanistic mother object + independently established behavioral axis**  
Canonical registration: [`../../phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md`](../../phenomenon_miner/REGISTERED_SPATIAL_REFERENCE_FRAME_TRANSFORMATION_2026-08-31.md)

## 1. One-sentence question

A VLM first receives object locations in the camera/image plane. When the question asks for another person's or object's left/right/front/back, does the model **transform its internal coordinates**, select another latent frame, or keep an egocentric code and translate only at the end?

## 2. Background and mothers

### Mechanistic mother

**Linear Mechanisms for Spatiotemporal Reasoning in Vision Language Models** (ICLR 2026).

The mother establishes content-independent causal **spatial IDs**:

- objects are rendered on a `4×4` image grid;
- the released pipeline extracts universal spatial IDs;
- it explicitly saves horizontal and vertical spatial axes as `{model}_x.pt` / `{model}_y.pt`;
- steering those representations changes spatial beliefs;
- the official implementation covers LLaVA, LLaMA, Qwen, InternVL and Gemma checkpoints.

Operationally, these IDs are grounded in the **image plane**. The mother therefore gives us a concrete mechanistic object before we introduce perspective.

### Behavioral mother

**Do Vision-Language Models Represent Space and How? Evaluating Spatial Frame of Reference under Ambiguities** (ICLR 2025 Oral; COMFORT).

COMFORT studies a classical spatial-cognition variable: **frame of reference (FoR)**. The same scene can be interpreted relative to:

- Camera / egocentric frame;
- Addressee-centered frame;
- Relatum/intrinsic frame.

The paper establishes that VLMs often default to egocentric interpretations and have difficulty flexibly adopting another legitimate FoR.

Critically, LLaVA-1.5-7B and LLaVA-1.5-13B overlap between the behavioral and mechanistic mothers. We therefore do not need to gamble on whether the behavior exists on a model whose spatial IDs we can analyze.

## 3. Scientific question and competing mechanisms

### H1 — Late linguistic remapping

Spatial IDs remain camera-centric through most of the network. The model only maps the camera-relative relation into a different answer word late in the language/readout pathway.

Prediction: mother `x/y` projections stay camera-aligned across FoR prompts; only late answer states differ.

### H2 — Explicit intermediate coordinate transformation

The model transforms the image-plane code into a target coordinate system before answering.

Prediction: a layer-local rotation/reflection/rebasing of the `x/y` geometry appears and is causally necessary for correct alternative-FoR answers.

### H3 — Multiple frame-specific codes + selector

Several coordinate systems coexist and a query-controlled selector decides which code affects the answer.

Prediction: multiple frame-specific states are concurrently available, while causal influence changes with the frame cue.

## 4. Data and artifacts

### Spatial-ID mother artifacts

Official repository: `Raphoo/linear-mech-vlms`.

Useful components:

- `spatial_id_derivation/` — 4×4 grid generation, ID extraction, `x/y` axis computation;
- Objaverse object renders used for universal ID extraction;
- `mirror_attr_swapping/` — causal information-flow experiment under horizontal image flip;
- saved model-specific spatial ID tensors where available.

The released extraction pipeline lists models including LLaVA-7B/13B, Qwen, InternVL, Gemma and others.

### FoR behavioral substrate

COMFORT / COMFORT-CAR provides scenes and reference-frame manipulations with analytic spatial conventions. Prefer the exact subset and prompts used in the mother rather than designing a new perspective benchmark.

Primary matched unit:

> **same scene + same object relation + different requested FoR**

The ideal test changes only the FoR instruction/interpretive origin while keeping the visual scene fixed.

## 5. Initial model panel

Start with the checkpoint overlap, not a broad VLM panel:

1. LLaVA-1.5-7B;
2. LLaVA-1.5-13B as replication.

Only after the mechanism is established should we consider Qwen/InternVL/Gemma families with independently verified FoR behavior.

## 6. Initial validation plan

### V0 — Reproduce the mechanistic mother object

Goal: verify that we can recover the mother spatial IDs before adding perspective.

Steps:

1. Pin `Raphoo/linear-mech-vlms` revision.
2. Download or reproduce the small 4×4 grid experiment.
3. Run `spatial_id_derivation` for LLaVA-1.5-7B-equivalent tooling.
4. Confirm:
   - monotonic projection on the horizontal axis as object x-position changes;
   - monotonic projection on the vertical axis as y-position changes;
   - weak dependence on object identity relative to location;
   - mother-style steering changes left/right logits in the intended direction.
5. Freeze these `x/y` directions before looking at COMFORT failures.

**Stop condition:** if the mother spatial ID cannot be faithfully reproduced, do not redefine a new spatial direction ad hoc.

### V1 — Replay the existing FoR phenotype on the overlapping checkpoint

Goal: verify only that our exact local checkpoint/template reproduces the mother-established behavior.

Steps:

1. Use the released COMFORT-CAR items/prompts.
2. Build matched Camera/Addressee/Relatum examples from the same scene.
3. Measure exact answer/logit behavior using the mother scoring protocol.
4. Verify a usable denominator of:
   - Camera-correct items;
   - target-FoR correct items;
   - egocentric-default failures under Addressee/Relatum prompts.
5. Freeze the matched item IDs.

This is a checkpoint bridge, not a new behavior-discovery study.

### V2 — Trace mother `x/y` IDs under different FoR queries

For each frozen same-scene FoR set:

1. Extract object-word / relevant residual states by layer.
2. Project them on the mother-frozen `x/y` axes.
3. Compare the geometry under Camera vs Addressee vs Relatum queries.
4. Ask where the requested FoR first changes:
   - the spatial code itself;
   - only its causal influence;
   - only the late answer representation.
5. Separate correctly handled alternative-FoR trials from egocentric-default failures.

This directly distinguishes H1 from mechanisms that modify/select the internal spatial code.

### V3 — Analytic coordinate-transform intervention

This is the central mechanistic experiment.

1. Use COMFORT geometry metadata to determine the mathematically correct transformation from camera coordinates to the requested FoR.
2. Express the transformation in the 2-D span of mother `x/y` spatial IDs where appropriate: sign flip, axis rotation/reflection, or rebasing dictated by the item geometry.
3. Inject the transformed spatial-ID component into the candidate layer/object state of an alternative-FoR failure.
4. Measure whether the answer changes specifically toward the target FoR.
5. Compare with:
   - same-norm random direction;
   - simple left/right sign flip when it is geometrically wrong;
   - unrelated-scene spatial ID;
   - late answer-label steering;
   - camera-frame native ID injection.

A selective target-FoR rescue is substantially stronger evidence than generic spatial steering.

### V4 — Query/selector patch

Goal: distinguish explicit numerical transformation from multiple latent frame codes.

1. Hold image and object relation fixed.
2. Patch only the representation induced by the FoR cue/query between Camera and Addressee/Relatum prompts.
3. Test whether this switches which spatial code controls the answer without numerically changing the object-location representation.
4. Measure whether multiple candidate coordinate representations are simultaneously decodable and causally available.

A selector-only answer switch supports H3; a transformed object-state requirement supports H2.

### V5 — Failure decomposition

Classify egocentric-default failures into:

- **transform failure:** target-frame representation never appears;
- **selection failure:** target-frame code exists but does not control output;
- **readout failure:** correct transformed relation exists and is selected, but answer token mapping is wrong.

The mechanism paper should explain this taxonomy, not simply report another FoR accuracy table.

## 7. Fatal controls

- Freeze mother `x/y` directions before examining FoR conditions.
- Never learn a new steering direction directly from target answers and call it a coordinate transform.
- Same scene / same object relation whenever comparing FoRs.
- Geometry-derived transforms must come from scene metadata, not post-hoc fitted directions.
- Same-norm random and geometrically incorrect transform controls.
- Camera-correct and alternative-FoR-correct controls.
- Separate causal changes in spatial code from late answer-token steering.

## 8. Promote / kill criteria

### Promote if

- both mother objects reproduce on an overlapping checkpoint;
- the FoR cue causes a stable internal change in spatial-code geometry or causal selection;
- an analytic transform or selector intervention selectively changes target-FoR behavior.

### Scientifically useful null

If FoR behavior changes while the causal spatial ID remains camera-centric until the output layer, the result establishes that output-level coordinate-system fits do **not** imply transformed internal world coordinates.

### Kill / redesign if

- no mother checkpoint can simultaneously reproduce spatial IDs and FoR behavior;
- apparent target-frame directions must be trained directly from answer labels rather than inherited from mother geometry;
- all effects reduce to generic answer-token steering with no perspective-specific causal structure.

## 9. Paper-level narrative

> **When a multimodal model reasons from a perspective different from the camera's, does it transform its internal world representation, choose among latent coordinate systems, or merely translate an egocentric answer at the end?**

The result connects VLM interpretability, spatial cognition, embodied reasoning and diagnosis of perception-vs-transformation-vs-selection failures.
