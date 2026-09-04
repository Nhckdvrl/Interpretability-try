# Experiment Log

## S0-1 — exact overlapping-checkpoint source audit

Question:
Does the frozen Llama-3.1-8B-Instruct checkpoint show nontrivial conditional-context effects
in both mother windows before we attempt cross-task causal transfer?

Experiment:
Aggregate the released donkey-conditional anaphora accuracy/effect-size file and parse final
Likert ratings from the presupposition release by its externally supplied high/mid/low bands.

Prediction:
Both windows should be nontrivial rather than floor/ceiling. This establishes only a behavior
denominator. Similar behavior does not establish a shared update state.

Result:
On released Llama-3.1-8B-Instruct outputs, donkey-conditional anaphora is near ceiling:
0.977 accuracy over 1,280 comparisons, although the continuous mean log-probability effect is
large (2.746). Presupposition final ratings parse for 87/90 items; means are 5.586 (high),
4.833 (mid) and 5.107 (low). The high-low separation is only 0.479 and the ordering is not
monotone because mid is below low.

Interpretation:
The behavioral state is mixed. Both windows show some conditional-context sensitivity, but
the frozen comparison does not yet provide two similarly informative intervention targets:
anaphora's binary accuracy is saturated and presupposition separation is modest/nonmonotone.
Cross-task patching now would make a null uninterpretable. The next experiment should use the
continuous anaphora effect and a deterministic presupposition-support logit on matched pairs,
then require nonzero within-task patch effects before cross-task transfer.

Next:
If both windows pass, construct antecedent clean/corrupt pairs with a shared binary downstream
readout and verify within-task patchability before any cross-task transfer. Cross-task transfer
is not meaningful when either within-task denominator is absent.

## S0-2 — deterministic presupposition denominator

Question:
Does the modest released Likert separation survive a deterministic, judge-free readout that
can serve as the presupposition side of a causal transfer ratio?

Experiment:
Use all 90 released problem-set items and force one of three semantic classes (low/mid/high).
Every item is evaluated under all six mappings of the semantic classes to A/B/C, and logits
are converted back to semantic scores before aggregation. This prevents option-position or
label-token preference from defining the result. The frozen gate requires balanced accuracy
>=0.45 and high-vs-low accuracy >=0.65.

Prediction:
A usable within-task denominator should distinguish at least high from low and remain stable
under label remapping. If all classes collapse to one response, there is no clean recipient
metric for presupposition patching.

Result:
Llama-3.1-8B-Instruct predicted `high` for all 90 source items after counterbalanced semantic
aggregation. Balanced accuracy was 0.333 and high-vs-low accuracy was 0.500. The confusion
matrix (low/mid/high rows and columns) was `[[0,0,30],[0,0,30],[0,0,30]]`. No item retained
the same semantic prediction across all six raw label orders. Mean gold-vs-best-other margins
were +1.013 for high, -0.977 for mid, and -1.129 for low.

Interpretation:
The deterministic presupposition behavior is a response-class collapse, not a usable graded
local-context computation. Together with the released nonmonotone Likert means, this fails
the frozen within-task denominator. A cross-task null would be uninterpretable because the
presupposition recipient does not reliably express the intended high/mid/low distinction.
This is behavior-floor/confound evidence for the current checkpoint and readout, not evidence
that anaphora and presupposition mechanisms are separate.

Next:
Stop 035 on Llama-3.1-8B-Instruct before activation patching. A future restart requires an
independently validated deterministic presupposition-support measure on the same frozen
scientific items; it may not select a lexical subset or redefine the project as anaphora-only.

## S0-3 — corrected cross-family recipient validation

Question:
Was S0-2 a genuine absence of a usable presupposition recipient, or an implementation failure
that should be repaired before deciding the venue-scale shared-computation question?

Experiment:
Audit the runner, correct its system instruction from the accidentally reused two-choice
`A/B` contract to an explicit `A/B/C` contract, and rerun all 90 source items under all six
label mappings on both Llama-3.1-8B-Instruct and Qwen3-8B. Aggregate semantic logits across
the mappings. In addition to the three-class score, evaluate the preregistered forced
high-versus-low comparison over all 60 high/low source items by comparing their aggregated
semantic logits directly.

Prediction:
A usable recipient should separate high from low above the frozen 0.65 floor without global
class collapse in both model families. Failure in opposite directions across families would
indicate model-specific response priors rather than a shared, stable local-context behavior.

Result:
The corrected Llama run still predicted `high` for all 90 items: balanced accuracy 0.333,
forced high/low accuracy 0.500, and label-order stability 0.011. Qwen predicted `low` for 68
items and `high` for 22: balanced accuracy 0.367, forced high/low accuracy 0.550, and
label-order stability 0.511. Neither model predicted the mid class after semantic
aggregation. The panel gate failed.

Interpretation:
The original S0-2 output was invalid because of the two-choice system instruction, but the
corrected result independently reaches the same scientific decision. The two checkpoints
show opposite global response priors and neither supplies the robust presupposition recipient
required to interpret cross-phenomenon causal transfer. This does not show that anaphora and
presupposition mechanisms are separate. It shows that this project lacks one of the two
behavioral legs needed to adjudicate shared versus separate dynamic-context computation.
Turning the result into a prompt-bias, label-order, or presupposition-classification paper
would be a substantial and narrower change of scientific object.

Next:
Archive 035. Do not run representation or patching experiments, and do not preserve an
indefinite paused state. Reopening requires a new externally validated presupposition behavior
window, not tuning on these 90 items.
