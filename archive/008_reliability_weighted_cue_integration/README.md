# 008 — Reliability-weighted multimodal cue integration

**Status:** `KILLED / ARCHIVED`
**Validated:** 2026-08-27

## Mother question

> Why can a VLM read both visual and textual measurements, and sometimes detect which is more reliable, yet still route the fused estimate toward a dominant modality rather than the reliability-weighted optimum?

The project concerns uncertainty use during fusion, not generic visual accuracy.

## Logic corrections

The initial scaffold explicitly stated both sigmas. That reduced the task to reading one marker plus inverse-variance arithmetic and could not distinguish uncertainty representation from fusion. The corrected G0 instead:

- renders nine image measurements as a visible dot distribution;
- supplies nine text measurements and their mean;
- encodes reliability only through cue spread—sigma is never shown;
- obtains image-only, text-only, and combined responses for every item;
- requires both unimodal interfaces to be readable before interpreting fusion;
- infers observed image weight from the model's own unimodal estimates;
- compares it with the hidden generative inverse-variance optimum;
- includes five mirrored reliability regimes from image-dominant to text-dominant.

## G0 results

| Model | Image readout MAE | Text readout MAE | Weight MAE | Reliability correlation | Key phenotype |
|---|---:|---:|---:|---:|---|
| Qwen3-VL-2B-Instruct | 1.82 | 0.024 | 0.556 | -0.459 | near-complete text capture; observed image weight ≈0 in every regime |
| Gemma3-4B-IT | 2.52 | 0.56 | 0.400 | +0.802 | reliability-sensitive, but systematically underweights image |

The unimodal probes show coarse access to both cues, but the interfaces are not matched: the text prompt states its mean explicitly while the image requires visual averaging. Qwen's combined output nearly copies that explicit text scalar; Gemma shows an exploratory reliability trend but remains image-underweighted. These are candidate phenotypes requiring symmetric-access preflight before they can support a reliability-routing claim.

## Mechanism opening and paper scope

- probe/patch reliability information encoded by visual spread;
- distinguish reliability representation from modality-gating failure;
- trace where the text stream captures the continuous-value readout;
- test targeted routing interventions rather than globally increasing visual attention.

The conference-sized claim is reliability-sensitive but modality-biased fusion across two VLM families. It should remain on controlled continuous estimation and not expand to all multimodal hallucination or robustness.

## Files

- `g0.py` — deterministic PNG generator, local VLM runner, and scorer;
- `data/manifest.jsonl`, `stimuli/` — 60 frozen cue-integration trials;
- `results/*_g0.jsonl` and summaries — complete Qwen/Gemma runs;
- `tests/test_008_g0.py` — stimulus, hidden-sigma, parser, and oracle-scoring tests.

## Archive decision

No further preflight or mechanism experiment will be run. The current G0 cannot distinguish modality bias from explicit-scalar copying because the text supplies its mean while the image requires visual averaging. More importantly, the broad optimal multimodal cue-combination question is already directly covered by the public psychophysics BayesBench across four magnitude tasks and nine models. Rebuilding a symmetric custom dataset would not repair that narrative collision.

The complete study design is in [`INTERPRETABILITY_PLAN.md`](INTERPRETABILITY_PLAN.md). Its preflight supersedes immediate white-box analysis of the current G0: the explicit text mean versus implicit visual mean is an access/copy confound, so symmetric raw/raw and summary/summary stimuli must be refrozen first.
