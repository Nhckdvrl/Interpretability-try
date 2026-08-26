# 006 mechanism experiment log

**Run date:** 2026-08-27
**Anchor model:** `Qwen/Qwen2.5-14B-Instruct`, BF16, four RTX PRO 6000 Blackwell GPUs
**Status:** Phase 0 complete; Phase 1 representation timeline and first Phase 2 natural interchanges complete

## Bottom line

The first mechanism result is positive but narrower than the final paper claim.

When a posterior is serialized as the fixed-width eight-token string `0.xxxxxx`, **replacing the entire numeric span is sufficient to transfer the downstream policy action**. A donor value that crosses the fixed threshold almost completely transfers the donor action in both gold-posterior and likelihood-elicited self-mean bridge prompts. The effect is far larger than the current same-posterior and same-action controls and was observed across two A/B mappings and three thresholds. The same-action controls are not yet posterior-distance matched, so this selectivity comparison remains exploratory.

The final numeric token and final query token are individually insufficient, whereas replacing the whole number is sufficient. This does not yet show which digit tokens are necessary or whether the signal is distributed across them. Whole-span interchange remains nearly complete through decoder layer 15, decays over layers 16–24, and is almost absent after layer 25. Meanwhile, the literal serialized value remains linearly decodable from pooled states at the original span. This is an exploratory separation between **decodability at a source location** and **causal sensitivity to replacing that source**.

This does not yet establish that the direct prompt forms the same posterior and fails to route it. Direct-prompt single-position patches were null, but a homologous multi-position direct state or receiving path has not yet been localized. The supported claim is therefore:

> In explicit-belief bridge prompts, early-layer replacement of the complete serialized number is sufficient to transfer action. That source-site intervention loses efficacy over layers 16–24 even though the literal value remains decodable there.

## 1. Behavioral preflight

The mechanism corpus uses the exact symmetric `0.8/0.2` likelihood family, priors `0.2/0.5/0.8`, count differences `-2…2`, and thresholds `0.3/0.5/0.7`. It contains 42 non-boundary policy cases, balanced 21 ACT / 21 WAIT, crossed with 16 surface variants and six belief conditions.

On the full Phase 0 run:

- posterior mean MAE: `0.1306`; posterior argmax MAE: `0.1441`;
- direct semantic action accuracy: `0.570`;
- gold bridge accuracy: `0.932`;
- self-mean bridge condition-implied accuracy: `0.896`;
- self-argmax bridge condition-implied accuracy: `0.933`;
- counterfactual bridge follow rate: `0.897`;
- irrelevant-number original-task accuracy: `0.597`.

The primary mechanistic surface used ACT/WAIT action words, `greater-than`, high-clause-first, with both option mappings. On this anchor, direct error rate was `36.7%`, semantic mapping consistency was `73.8%`, and gold/self bridge rescued all eligible direct errors. The broader surface factorial remains important for later robustness because aggregate mapping consistency is only `55.1%`.

Primary behavior files:

- `results/qwen25_14b_phase0_posteriors.jsonl`
- `results/qwen25_14b_phase0_actions.jsonl`
- `results/qwen25_14b_phase0_summary.json`

## 2. Numerical and intervention controls

Two implementation issues were fixed before interpreting causal effects:

1. Residual caches now preserve BF16 instead of converting BF16 activations to FP16.
2. Natural interchange now uses a batch-local two-forward design. The first forward captures receiver and donor states and baseline logits in one padded batch. The second forward uses the identical batch shape and patches only receiver states. This removes BF16 batch-shape drift from the causal difference.

The tokenizer audit found that every fixed-width posterior is exactly eight tokens (`0`, `.`, and six digit tokens). `BELIEF_NUM_END` was added after confirming it points to the final digit, not the decimal point. Ten tests now pass.

## 3. Representation timeline

At `QUERY_END`, the earlier grouped probes found:

- direct posterior: best Pearson `r=.943`, `R²=.837` at layer 46;
- direct decision margin: best `r=.950`, `R²=.865` at layer 46;
- direct semantic action: best balanced accuracy `.738` at layer 29;
- gold bridge semantic action: balanced accuracy `1.00` at layer 28;
- self bridge semantic action: balanced accuracy `.917` at layer 27.

Cross-format bridge→direct posterior probes on the same matched cases preserved rank correlation (`r≈.88–.91`) but had low direct-scale `R²≈.07`. Because this analysis did not hold out evidence families across train and test, it is descriptive only and is not evidence of shared abstract geometry or causal use.

The corrected joint eight-token span probe is much stronger than the last-token probe. With evidence-family grouped cross-validation:

- gold bridge mean-pooled literal serialized value reaches `r=.956`, `R²=.873` at layer 25;
- self-mean bridge mean-pooled serialized posterior reaches `r=.975`, `R²=.847` at layer 28;
- self-mean condition action reaches balanced accuracy `.948` at layer 24.

For self-mean values, mean-pooled literal-value decoding rises from `r=.470` at layer 5 to `.915` at layer 15 and `.967–.975` over layers 20–28. The final-token probe fails on these arbitrary six-digit values, showing only that the final token alone is inadequate. The pooled probe may exploit token identity; abstract posterior representation requires held-out values, formats, and evidence decompositions.

Probe files:

- `results/qwen25_14b_probe_timeline_summary.json`
- `results/qwen25_14b_probe_belief_span_joint.jsonl`
- `results/qwen25_14b_probe_belief_span_joint_summary.json`

## 4. Natural causal interchange

### 4.1 Single-position negative controls

Whole-residual patches at `QUERY_END` produced no donor-action flips in direct or gold bridge across all 48 layers. Normalized recovery stayed near zero and crossing effects were comparable to posterior-equivalent controls.

Coarse direct scans at `EVIDENCE_END`, `THRESHOLD_NUM_END`, `RULE_END`, and `MAPPING_END` also found no continuous, directionally aligned posterior-transfer window. `BELIEF_NUM_END` in gold bridge was likewise null. These results rule out final-digit and query-end carrier accounts at the tested sites; they do not rule out another individual digit, a multi-position state, or a path-level state.

### 4.2 Eight-token posterior span

Natural donor pairs hold threshold, instruction, action vocabulary, and option mapping fixed. Crossing donors change the serialized posterior across the policy boundary. Gold-bridge posterior-equivalent donors change prior/evidence decomposition while holding the exact posterior fixed. Non-crossing donors change posterior magnitude without changing the policy action.

At layer 0, across 12 crossing pairs:

| Condition / span | Mean recovery (pair-bootstrap 95% CI) | Donor-action IIA | Mean absolute semantic-logit effect | Control effect |
|---|---:|---:|---:|---:|
| Gold, number only | `.981 [.944, 1.014]` | `12/12` | `49.64` | same-posterior `0.29`; non-crossing `2.61` |
| Gold, full belief statement | `.983 [.944, 1.017]` | `12/12` | `49.73` | same-posterior `0.29`; non-crossing `2.69` |
| Self-mean, number only | `.981 [.947, 1.015]` | `12/12` | `49.71` | non-crossing `3.20` |

These intervals are conditional pair bootstraps over 12 deterministically selected, baseline-correct crossing pairs, some sharing donors. They are not evidence-family population intervals.

All crossing effects point in the donor direction. The pairs cover both A/B mappings, thresholds `0.3/0.5/0.7`, and both action directions. The near identity of number-only and full-statement curves shows that additionally swapping the surrounding statement tokens contributes little in this subset, conditional on swapping the number. It does not show that surrounding role semantics are unnecessary.

Gold number-span layer trajectory:

| Layer | Mean recovery | Donor-action IIA |
|---:|---:|---:|
| 0 | `.981` | `1.00` |
| 15 | `.977` | `1.00` |
| 16 | `.847` | `.917` |
| 18 | `.689` | `.833` |
| 20 | `.432` | `.417` |
| 22 | `.355` | `.250` |
| 24 | `.221` | `.167` |
| 25 | `.022` | `0` |
| 28 | `-.002` | `0` |

Self-mean follows the same transition: recovery is `.961` with `12/12` IIA at layer 15, `.860` with `12/12` at layer 16, `.395` with `.417` IIA at layer 20, `.164` with zero IIA at layer 24, and approximately zero after layer 25.

Primary causal files:

- `results/qwen25_14b_phase2_span_summary.json`
- `results/qwen25_14b_interchange_gold_belief_number_summary.json`
- `results/qwen25_14b_interchange_gold_belief_statement_summary.json`
- `results/qwen25_14b_interchange_selfmean_belief_number_summary.json`

## 5. Current interpretation and next experiment

The following is the working hypothesis generated by the result, not a demonstrated stage model:

1. the external numeric tokens initially carry the counterfactual posterior almost literally;
2. layers 5–15 may transform literal numeric states while the source-span swap remains causally effective;
3. layers 16–24 may transport role-licensed content toward an as-yet-unidentified receiver;
4. after layer 25, the literal value remains decodable at the source span, but replacing that source state no longer changes the output.

The next high-value experiment is not a global DAS search. It is a focused propagation/localization study over layers 14–25:

- rank belief-span → later-token attention/MLP components with AtP*/attribution patching;
- exactly patch the shortlisted heads/MLPs and their outputs at rule, mapping, and query positions;
- test whether report/self-bridge posterior states can rescue matched direct errors at a validated receiving site;
- include noising and denoising directions, same-posterior controls, norm-matched random controls, and both mappings;
- only after a natural receiving path is validated, fit a low-dimensional alignment within that layer window.

The decisive unfinished question is whether direct prompts possess a homologous posterior state that is formed but weakly routed, or instead lack a sufficiently aligned posterior state. The current experiments establish only the externalized source-side sufficiency result and localize a source-site decay window; the receiver and any transport path remain unknown.
