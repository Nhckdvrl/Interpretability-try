# Frozen G0 — mass shortcut + cross-view latent-property constancy

Date: 2026-08-31
Status: `G0 AUTHORIZED BY HANDOFF / NOT REGISTERED / NO MI`

This directory implements the two mass-related frontier checks from
`phenomenon_miner/HANDOFF_HAMDI_SEARCH_2026-08-31.md`. It does **not** register
either topic and does **not** authorize probes/SAEs/patching/steering.

## Scientific objects kept separate

### A. Visual/apparent-size -> mass shortcut

Natural question: when estimating mass from an image, does apparent object size
act as a shortcut that pulls the estimate even when the real object is unchanged?

The strongest G0 is within-object: use multiple real views of the **same object**,
so true mass, material, category and object identity are fixed by design. Regress
`log(predicted_mass)` on `log(apparent_area_fraction)` after object fixed effects.
This avoids rescuing the effect with post-hoc product/material subsets.

A secondary cross-object analysis using metric `x_length/y_length` may be reported,
but it is not allowed to rescue a null within-object apparent-size effect unless
all category/material controls were frozen before seeing model outputs.

### B. Mass-specific cross-view instability

Natural question: does the estimated value of a latent, physically invariant
property (mass) change substantially when only the camera view changes?

Use the same real object, >=4 views, identical prompt and deterministic decoding.
Quantify within-object dispersion in log-mass space. A view-instability claim must
remain after same-view rerun and image-pipeline controls.

## Frozen model-family panel

Default three-family panel (one checkpoint per genuinely different family):

- `Qwen/Qwen3-VL-8B-Instruct`
- `google/gemma-3-12b-it`
- `OpenGVLab/InternVL3_5-8B`

Substituting a checkpoint is allowed only for a hard loading/license failure and
must be documented **before outputs are inspected**. Do not add a fourth family
post hoc to rescue a 1/3 result.

Each model is served separately through an OpenAI-compatible local multimodal
endpoint. The runner records the model string returned/declared by the server;
commit the exact model revision/hash alongside outputs.

## Frozen prompt

Mass task, one image only:

> Estimate the mass of the main physical object in this image. Use only what is
> visible in this image and ordinary real-world knowledge. Return JSON only with
> `mass_kg` as one positive number and `category` as a short common-noun label.

No bounding box, depth, true dimensions, true mass, other views, examples, chain
of thought, or PhysQuantAgent visual prompts are shown to the tested VLM.

The category string is a **control only**, never central gold. No LLM judge is
used. For any object for which the source artifact has an externally supplied
category/name, that field should be preserved in the manifest and used instead.

## Required manifest

JSONL, one row per image/view:

```json
{"object_id":"...","view_id":"...","image_path":"...","true_mass_kg":1.23,
 "apparent_area_fraction":0.18,"metric_x_m":0.11,"metric_y_m":0.07,
 "source_category":null,"pipeline_variant":"original"}
```

Required for the primary cross-view G0:

- `object_id`
- `view_id`
- `image_path`
- `true_mass_kg`
- >=4 usable views per object

`apparent_area_fraction` is bounding-box or mask area divided by full image area,
computed without using tested-model outputs. The exact detector/segmenter and
thresholds must be frozen before model calls. `metric_x_m/y_m` can come from the
public PhysQuantAgent Record3D depth+intrinsics measurement pipeline.

## Same-view and pipeline controls

Before the full run, deterministically choose a fixed 10% of object-view rows by
SHA256 of `object_id/view_id` and duplicate them as `repeat_id=1`. Exact same image,
prompt and decoding settings are used. This estimates residual decoding/runtime
variation.

For a fixed 10% subset, prepare one frozen resize/letterbox control variant without
content crop. Do not choose this subset after looking at mass errors. A purported
view effect is fatal if it is comparable to same-view/pipeline-induced variation.

## Frozen parsing

Accepted output requires a finite positive `mass_kg`. Markdown fences are stripped,
then one JSON object is parsed. No semantic repair by an LLM. A single regex
fallback for an explicit numeric `mass_kg` field is allowed and logged. All other
responses are parse failures and remain in the denominator.

## Primary statistics

For each family and each eligible object:

- `log_mass = log(pred_mass_kg)`
- `view_log_range = max(log_mass) - min(log_mass)`
- `view_ratio = exp(view_log_range)`
- `view_log_sd = sd(log_mass)`

For the apparent-size shortcut, fit the pooled within-object slope

`demean_object(log(pred_mass)) ~ beta * demean_object(log(apparent_area_fraction))`.

This is the primary size-shortcut statistic. No product subtype or extreme-size
subset is permitted.

## Frozen hard gates

### Cross-view instability promotion

A family counts as positive only if all hold:

1. >=80% of source objects remain eligible after predeclared parse/measurement exclusions;
2. median object `view_ratio >= 2.0`;
3. >=50% of eligible objects have `view_ratio >= 2.0`;
4. same-view repeat median absolute log difference <= 0.05;
5. resize/letterbox-control shift is materially smaller than ordinary cross-view dispersion;
6. category/control output is substantially more stable than mass (report modal-label share; no threshold rescue).

Promotion requires the positive criterion in >=2/3 model families. Otherwise:
`KILL-S0 / NO-BROAD-CURRENT-OPEN-FAMILY-CROSS-VIEW-MASS-INSTABILITY`.

### Apparent-size shortcut promotion

A family counts as positive only if all hold:

1. the within-object slope beta is positive;
2. beta >= 0.25 (doubling apparent area implies roughly >=19% mass pull);
3. a deterministic object-cluster bootstrap 95% interval excludes 0;
4. the sign is not driven by one object (leave-one-object-out sign remains positive for >=90% of eligible objects removed);
5. same-view/pipeline controls cannot account for the slope.

Promotion requires >=2/3 families. Otherwise:
`KILL-S0 / NO-BROAD-CURRENT-OPEN-FAMILY-VISUAL-SIZE-MASS-SHORTCUT`.

These thresholds are deliberately strict because the repository bar requires a
scientifically substantial phenotype, not merely a nonzero coefficient.

## Anti-rescue rules

If either G0 dies, do **not** revive it by:

- selecting a product/material/category subtype;
- selecting only close/far or extreme views;
- changing the prompt after seeing outputs;
- adding a weaker model family;
- switching to synthetic heavy/light objects;
- replacing mass with volume/density (that factorization is already terminal);
- calling generic mass error evidence for a size shortcut;
- calling generic visual perceptual constancy the topic.

## Output artifacts that must be committed after execution

- exact manifest + SHA256
- exact checkpoint revisions
- raw request/response JSONL per family
- parsed per-view table
- object-level dispersion table
- same-view/pipeline-control table
- size fixed-effect slope + bootstrap + leave-one-object-out audit
- one frozen summary JSON containing the two independent verdicts

Until those artifacts exist, both frontiers remain unregistered and MI is forbidden.
