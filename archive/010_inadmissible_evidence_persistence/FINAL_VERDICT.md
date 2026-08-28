# Final verdict — D0 v3 calibration

Status: `TERMINAL-HOLD-D0V3-CONTRACT / ARCHIVE-CURRENT-OPERATIONALIZATION`

D0 v3 fixed the two identifiable harness defects: polarity became a direct
verdict choice and the clean `never_seen` baseline no longer refers to missing
evidence. The pair-level admitted capability gate passed 12/12 for both
Qwen3-8B and Gemma3-12B.

The calibration nevertheless failed its frozen neutral-control requirement:

- Qwen3-8B neutral-artifact fraction: `0.75`;
- Gemma3-12B neutral-artifact fraction: `0.8333`;
- allowed maximum: `0.10`.

Both models produced large negative struck content-swap deltas, including under
truth-neutral procedural exclusion. Raw inspection ruled out label inversion,
but the generic neutral-context control is already large enough to make those
negative deltas uninterpretable. They are retained as a possible inversion
diagnostic only, not promoted to a phenotype.

The current 005 operationalization is therefore closed with no v4/v5 repair,
panel expansion, N1, or mechanism work. The abstract scientific question is not
killed: this run calibrates and rejects the present benchmark contract. New
validation resources move to 006.

Source rationale: Kassin and Sommers distinguish procedural from
reliability-based exclusion (`https://doi.org/10.1177/01461672972310005`); the
LegalBench hearsay task is CC BY 4.0; the procedural factor is anchored to the
current U.S. federal civil-rules source; the Sandberg et al. materials are
public at `https://osf.io/mh6ae/`. D0 v3 transformations remain explicitly
marked calibration-only with independent human review pending.
