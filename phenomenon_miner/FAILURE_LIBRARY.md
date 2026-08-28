# Reusable behavioral failure controls

## Enumeration/framing candidates: three terminal controls

Source failure: `archive/009_packed_unpacked_event_splitting`.

1. **Reorder invariance.** If reversing an extensionally identical branch list
   changes the readout at the same scale as the claimed effect, branch order or
   formatting is a sufficient explanation.
2. **Within-family refinement signature.** Branch-count curves are meaningful
   only when k=2/3/4 are nested refinements of the same event. Cross-taxonomy
   branch-count slopes are not mechanism evidence. A stable opposite-direction
   slope is terminal for a monotone splitting account.
3. **Repacking recovery.** Recompressing an unpacked list should shrink the
   absolute packed/unpacked difference toward zero. A larger same- or
   opposite-sign deviation is not recovery and points to wording/formatting
   sensitivity.

These controls should be frozen before model calls and should not be relaxed to
retain a framing-dependent candidate.

## Identity-fusion candidates: capability-gated null is terminal

Source failure: `active/006_existential_witness_collapse`.

1. **Separate recognition from use.** A claim such as “the model knows identity is unresolved but acts as if it were resolved” requires a recognition gate and an operational downstream action. Re-asking the same entailment question does not establish a dissociation.
2. **Gate on both identity directions.** Independent existential witnesses imply neither sameness nor distinctness. Recognition must verify that the model leaves both worlds open; otherwise apparent fusion can be ordinary quantifier/coreference failure.
3. **Explicit same/distinct action controls are mandatory.** The downstream action must flip correctly when identity is explicitly same versus explicitly distinct. Without this, an unknown-world preference is not interpretable as witness fusion.
4. **A clean capability-gated null should kill the candidate.** In 006, Qwen3-8B passed 40/40 recognition and action-control gates across 8 domains, yet `p_collapse(unknown)` was about `9.4e-5` with 0 strong cases. This directly falsified the frozen illegal-join prediction for the operationalization; changing prompts, datasets, thresholds, or model strength afterward would be rescue, not validation.
5. **Do not misread answer-order failure as conceptual incapacity.** Gemma3-12B passed existence and shared-witness recognition but showed severe answer-order instability on the distinctness probe. Such a model is not a valid phenotype denominator, but the failure should be diagnosed narrowly rather than labeled as generic inability to understand existential quantification.

General lesson: once one strong model cleanly passes the full capability denominator and robustly exhibits the normative preservation behavior across the full natural panel, the discovery-track operationalization is terminal unless a pre-specified reason invalidates the dataset or scorer. A second model with a gate artifact is not a license to redesign the task until a positive effect appears.
