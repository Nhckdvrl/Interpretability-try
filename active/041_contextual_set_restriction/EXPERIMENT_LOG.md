# 041 — Experiment Log

Panel: five independent families — `Qwen/Qwen3-8B` (36 blocks),
`NousResearch/Meta-Llama-3.1-8B-Instruct` (32), `google/gemma-3-12b-it` (48),
`microsoft/Phi-4-mini-instruct` (32) and `mistralai/Mistral-Small-24B-Instruct-2501` (40).
All readouts are deterministic single-token forced choice; gold is computed from denotations.

Panel status: S0 **5/5**, S1 **4/4** run, S3 **4/4** run.

## S0 — same-world role swap

Question:
With every object fact, the target phrase and the lexical modifiers held fixed, does the cost of
omitting a modifier track whether that modifier restricts the currently live candidate set?

Experiment:
96 worlds over six property families. A = target, B differs on dimension 2, C differs on
dimension 1; the question makes either {A,B} or {A,C} live, so the same modifier restricts in one
context and not in the other. Four description conditions (full, drop each modifier, bare), three
surface forms including two relative-clause orders, two question paraphrases, two answer mappings;
9,216 items per model.

Result — all five families pass, with the same structure everywhere:

| model | full | bare | drop restricting | drop other | role-swap interaction |
|---|---|---|---|---|---|
| Qwen3-8B | 0.996 | 0.482 | 0.470 | 0.998 | +20.09 [+18.92, +21.26] |
| Llama-3.1-8B | 0.971 | 0.570 | 0.560 | 0.982 | +2.52 [+2.39, +2.65] |
| Gemma-3-12B | 0.996 | 0.632 | 0.585 | 1.000 | +9.04 [+8.32, +9.76] |
| Phi-4-mini | 0.997 | 0.533 | 0.576 | 0.987 | +3.97 [+3.76, +4.19] |
| Mistral-Small-24B | 1.000 | 0.587 | 0.607 | 1.000 | +4.22 [+4.01, +4.44] |

The bare-description column is the intended floor: with no modifier the choice is genuinely
undetermined and every model sits near chance. Dropping the modifier that restricts costs almost
the whole effect while dropping the same lexical modifier in the paired context costs nothing. In
every model the interaction has the same sign and comparable magnitude across all six property
families, all three surface forms, both question paraphrases and both answer mappings.

Interpretation:
The behavioural gate passes cleanly, but a clean pass here is a capability result, not a finding:
`FINDING_RULES` C1 already grants prior incremental reference-resolution work the idea that words
narrow a candidate set. The value of S0 is that it licenses the mechanistic question and fixes the
denominators. Item-level preferences under omission-induced ambiguity are lexical noise that flips
sign with the adjective (`tall` +13.35 versus `flat` -11.78), which is why the headline statistic
is the within-world cross-context difference, where such preferences cancel.

Next:
Restriction and description uniqueness are perfectly confounded in these worlds. Separate them
before claiming any role state.

## S1 — restriction crossed with uniqueness

Question:
Is modifier restriction represented at the modifier token independently of whether the description
still picks out a unique referent?

Experiment:
Three-object live sets with a satisfier-vs-non-satisfier readout that stays defined when two
objects satisfy the description. `unique` worlds have one satisfier, `duplicate` worlds two, fully
crossed with which dimension restricts, so the same lexical modifier appears in both roles with
identical description text and only the scene differing. 6,912 items and 4,608 modifier-token
states per model at nine relative depths; probes are mass-mean with whole property families held
out.

Result — three families run, all pass. Behaviour survives the decorrelation: the
restricting-minus-other omission cost is +27.45 [+26.12, +28.77] in unique worlds and still +15.80
[+15.25, +16.38] in duplicate worlds for Qwen, +5.05 [+4.84, +5.26] versus +2.40 [+2.27, +2.52] for
Llama, and +8.75 [+8.36, +9.14] versus +4.66 [+4.43, +4.89] for Phi.
Decoding restriction at the modifier token reaches AUC 0.997–0.998 within unique worlds and 1.000
within duplicate worlds in all three families, with layer 0 at exactly 0.500 as the
counterbalancing control requires. Cross-uniqueness transfer (worst direction, threshold-free) is
0.867 for Qwen, 0.929 for Llama and 0.877 for Phi. The uniqueness direction classifies restriction
at 0.399, 0.405 and 0.363, i.e. it carries no restriction information at all.

Interpretation:
The first pass of this analysis used balanced accuracy for the transfer and reported 0.50–0.60,
which looked like a failure; that was a threshold artifact, because duplicate worlds shift the mean
projection. With the threshold-free statistic the direction transfers almost perfectly. Restriction
is therefore encoded at the modifier token as something separable from a generic ambiguity signal.

Next:
Decide whether that state is used, not merely present.

## S2 — first causal attempt (superseded)

Result:
Only Qwen at 50% depth showed a selective effect (role interaction -1.329 [-1.488, -1.176], role
minus random -0.970); Llama was flat at every depth (all |effects| < 0.03), and referent accuracy
stayed at 1.000 everywhere.

Interpretation:
Two implementation defects, not a null. The edit added a fixed vector to every edited token instead
of replacing that token's component along the role direction with the opposite class mean, and a
single class-mean step is negligible against clean margins of +4 to +29 logits. Llama's class means
are closer together, which is exactly why a fixed 1x step did nothing to it despite AUC 0.99.

## S3 — causal specificity, counterfactual replacement

Question:
Does replacing the restriction-role component at one modifier token with its counterfactual value
change which modifier the model relies on, beyond shuffled-label and random directions, on a
held-out surface form, while raw property truth survives?

Experiment:
`h' = h + alpha * (mu_opposite - h . d) * d` at the modifier token, with alpha frozen at 1, 2, 4
before running and both intervention directions tested. The direction is estimated from S1 states
on three training property families and applied to the three held-out families; controls are a
shuffled-label direction re-estimated within family and a random unit direction. Test items include
the `relative_21` wording, which the direction was never estimated on. A matched property-truth
question shares the identical prompt so the same tokens are edited.

Result — the contract passes in all four families run, each at the depth where its own probe
peaked, with property truth preserved and both surface forms negative:

| model | depth | alpha | role interaction | shuffled | random | on restricting | on other | reverse | property truth |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-8B | 50% | 2 | -3.333 [-3.599, -3.070] | -0.119 | +0.003 | -2.98 | +0.36 | +2.74 | 0.948 -> 1.000 |
| Qwen3-8B | 50% | 4 | -4.279 [-4.783, -3.781] | -0.354 | -0.039 | -4.16 | +0.12 | +4.31 | 0.948 -> 1.000 |
| Llama-3.1-8B | 25% | 4 | -1.666 [-1.833, -1.510] | -0.273 | +0.005 | -1.61 | +0.06 | +0.40 | 0.810 -> 0.862 |
| Phi-4-mini | 25% | 4 | -1.898 [-2.113, -1.705] | -0.374 | -0.036 | -1.76 | +0.14 | +1.04 | 0.971 -> 0.971 |
| Gemma-3-12B | 25% | 4 | -0.891 [-1.151, -0.670] | -0.039 | +0.012 | -0.91 | -0.02 | -0.48 | 1.000 -> 1.000 |

The effect is carried entirely by the restricting modifier: the same edit applied to the same
lexical modifier in the paired world where it does not restrict moves margin the other way or not
at all. The reverse intervention is positive in three of four families, so the axis is a
bidirectional handle rather than a lesion; Gemma is the exception. Referent accuracy finally moves
at the largest alpha (1.000 -> 0.990 / 0.935 / 0.953 / 0.984). Effects hold on the `relative_21`
wording, which the direction was never estimated on, and in every family they are larger there than
on the wording the direction came from.

Interpretation:
The frozen H2 causal-specificity contract passes on all four families run, with H3 preservation
intact everywhere.
Referent accuracy is saturated at 1.000 in most cells, so the claim rests on margin rather than on
flipped choices except at the largest alpha; that is stated rather than hidden.

Next:
The panel requirement is met (S0 5/5, S1 4/4, S3 4/4). What remains before writing is the Leffel
natural-language validation window from section E1 — the synthetic worlds are the microscope, and
the published human question-answer paradigm is still the missing bridge — plus a scaling series
within one family.

## S4 — Leffel natural-language validation window

Question:
Does the restriction effect appear in the published human question-answer paradigm, where the
critical answer phrase is fixed and only the preceding question changes which alternatives are
live?

Experiment:
40 items in the Leffel et al. (2014) same-answer format, both questions realised as parallel
clefts so the wording stays matched whatever the action phrase is, with a one-line scene that
makes both felicitous and holds the facts constant. Two readouts: `modifier_needed` asks directly
whether the modifier is needed to know which one is meant, and `answer_adequacy` asks whether the
reply already says which one is meant, tested on both the full and the reduced answer. Two answer
mappings; all five panel families.

Result — the two readouts separate, and the split is interpretable:

| model | modifier_needed gap | reduced-answer adequacy gap |
|---|---|---|
| Qwen3-8B | +0.088 | **+0.838** (0.163 restricting vs 1.000 non-restricting) |
| Mistral-Small-24B | +0.300 | **+0.675** (0.125 vs 0.800) |
| Gemma-3-12B | -0.037 | **+0.425** (0.575 vs 1.000) |
| Phi-4-mini | +0.075 | +0.212 (0.388 vs 0.600) |
| Llama-3.1-8B | 0.000 | 0.000 (0.500 vs 0.500) |

Interpretation:
The adequacy readout — which asks exactly what restriction is defined as, whether the reduced
description still picks the referent out — carries the effect in three of five families and meets
the 3/5 threshold. The direct metalinguistic question does not work anywhere: every model says the
modifier is needed most of the time regardless of context, which is the familiar over-informativeness
bias and is a property of the question, not of the object. Llama sits at exactly 0.500 on both
readouts, i.e. it answers by position and never engages the yes/no format; that is a format failure
distinct from the clean synthetic behaviour it shows in S0 and S1.

The natural window is therefore weaker than the synthetic microscope (3/5 rather than 5/5, one
readout dead) and should be presented as a validation bridge rather than as the main evidence.

Next:
041 has met every frozen gate. Remaining work is paper construction, not validation: a scaling
series within the Qwen family, and a decision on how much of the S4 window to report.

## S6 — scaling series (robustness, not a claim)

Question:
Does the effect hold across model size, and does anything about it change with scale?

Experiment:
Qwen3 at 1.7B, 4B, 8B, 14B and 32B (28/36/36/40/64 blocks) on the S0 role-swap worlds and the S1
decorrelated worlds, with the same frozen readouts, controls and probes.

Result:

| size | S0 full acc | S0 role-swap interaction | S1 cost gap (unique) | probe AUC (unique/duplicate) | cross-uniqueness transfer |
|---|---|---|---|---|---|
| 1.7B | 0.770 | +7.79 [+7.00, +8.59] | +19.42 | 0.999 / 0.996 | 0.938 |
| 4B | 0.994 | +23.70 [+21.91, +25.51] | +34.43 | 0.999 / 1.000 | 0.852 |
| 8B | 0.996 | +20.09 [+18.91, +21.25] | +27.45 | 0.997 / 1.000 | 0.867 |
| 14B | 0.999 | +21.09 [+19.78, +22.41] | +27.95 | 1.000 / 1.000 | 0.890 |
| 32B | 1.000 | +13.89 [+13.44, +14.35] | +16.54 | 1.000 / 1.000 | 0.840 |

Interpretation:
There is no scaling story here and the log should not manufacture one. The effect is present and
the same sign at every size that anyone reads this work against; behaviour saturates by 4B and the
interaction does not grow after that — 4B's is the largest and 32B's the smallest of the capable
models. The probe is at ceiling throughout. This is a robustness check.

A 0.6B point was also run and is **discarded**, not reported. Two reasons, either sufficient.
First, nobody reads interpretability claims at sub-billion scale; the field's range is 7B-27B.
Second, the claim it was going to support — representation present while behaviour is absent — does
not survive its own numbers: 0.6B's behaviour is small but reliably non-zero on every continuous
metric (role-swap interaction +0.44 [+0.40, +0.47]; unique cost gap +1.176 [+1.060, +1.287]), so
"at chance" depended on thresholded accuracy, which is exactly the artifact Schaeffer et al.
(NeurIPS 2023) identify behind apparent emergence. An earlier draft of this log and of the summary
page led with that dissociation; that framing was wrong and has been removed.

Next:
If a representation/use gap exists it has to be shown inside a capable model, by task load rather
than by parameter count. That is S8.

## S7 — binary role, or graded by how much the modifier removes?

Question:
Everything so far contrasts restricts / does not restrict. What quantity does the modifier-token
state actually carry — a binary flag, or the size of the reduction that modifier is responsible for?

Experiment:
Four-object live sets in which dimension 2 removes exactly k candidates, k in {0, 1, 2, 3}, while
dimension 1 never restricts and supplies the within-world k = 0 anchor. Candidate-set size, number
of described objects and both lexical modifiers are identical across all four degrees; only which
objects fill the set changes. The role direction is the one estimated in S1 on training property
families, and projections are read on held-out families only.

Result — the state tracks the degree; the behaviour mostly does not:

| degree k | Qwen cost / projection | Llama | Phi | Gemma |
|---|---|---|---|---|
| 0 | +1.43 / +3.07 | +0.80 / +2.34 | +1.27 / +6.01 | -0.20 / +10.10 |
| 1 | +34.21 / +17.46 | +6.35 / +22.31 | +10.96 / +17.16 | +12.95 / +23.69 |
| 2 | +37.38 / +28.29 | +6.57 / +24.77 | +14.08 / +22.93 | +15.23 / +31.24 |
| 3 | +32.76 / +33.43 | +5.81 / +25.97 | +10.68 / +25.69 | +17.99 / +33.02 |

From k = 1 to k = 3 the projection rises in every family (+91% Qwen, +16% Llama, +50% Phi,
+39% Gemma) while the behavioural cost is flat or slightly negative in three of them
(-4%, -9%, -3%). Gemma is the exception: its behaviour rises +39%, matching its projection, so the
dissociation is 3/4 rather than 4/4 and that is how it should be reported.

What is 4/4 is the relative coding. As the graded modifier's degree rises, the *other* modifier's
projection falls monotonically through zero in every family: +21.7 to -23.5 (Qwen), +16.8 to -27.6
(Llama), +11.9 to -24.6 (Phi), +22.7 to -28.4 (Gemma). The two modifiers are not carrying
independent per-modifier flags; they are coded against each other.

Interpretation:
Full accuracy is 1.000 in every cell, so nothing here is a capability limit. In three families the
model holds a graded representation of how much each modifier narrows the live set and reads it out
as an all-or-nothing decision. Together with the scaling dissociation, both directions of the
representation-use gap now have evidence: the state exists before the behaviour does, and it carries
a finer quantity than the behaviour uses.

Note:
Gemma's first pass returned NaN projections because its stored states contained inf; the numbers
above are from the repeated float32 run. See the correction below.

## Correction — float16 overflow in stored states

The state-capture scripts stored residuals in float16. That was fine for Llama, Phi, Mistral and
every Qwen size (max |activation| 27-452), but Gemma-3-12B's residual stream exceeds 65504 in the
middle third of the stack, so layers 24, 30, 36 and 42 overflowed to inf: 11,547 values in the S1
capture and 8,559 in S7.

What this affected: Gemma's S1 probe numbers were read at contaminated depths, and its suspiciously
exact `uniqueness direction on restriction = 0.500` was an artifact — NaN scores fail `scores > 0`
uniformly, which a balanced-accuracy readout reports as exactly chance. Gemma's S3 causal result is
unaffected because its passing cell is at 25% depth, layer 12, which is inf-free.

Fix: state capture now stores float32, and Gemma's S1, S7 and causal runs were repeated under it.
The same defect is recorded against the archived `045`, whose verdict does not depend on it.

## S8 — task load inside capable models: negative

Question:
If a representation/use gap exists, it should be findable inside an 8B-12B model by making the task
harder rather than by shrinking the model. Does raising set-intersection load degrade the model's
use of the restriction role faster than its representation?

Experiment:
Ternary-valued dimensions so that every non-target object differs from the target on at least two
described slots and exactly one modifier restricts in every world. Two load axes measured
separately: modifier load (2, 3, 4 adjectives with the live set fixed at 4) and candidate load
(7, 10, 13 objects with the description fixed at 4 adjectives). Use is the omission-cost asymmetry
between the restricting modifier and the mean of the others; representation is a noun-held-out probe
at the modifier tokens of the full description. Four families at 8B-12B.

Result — the prediction fails, and on one axis it reverses:

| axis | Qwen use / probe | Llama | Phi | Gemma |
|---|---|---|---|---|
| modifiers 2 -> 4 | +27.99 -> +22.69 / 1.000 -> 0.971 | +5.09 -> +3.86 / 1.000 -> 0.973 | +8.82 -> +5.66 / 1.000 -> 0.947 | +9.82 -> +7.69 / 1.000 -> 0.982 |
| candidates 7 -> 13 | +16.14 -> +15.95 / 0.975 -> 0.779 | +2.81 -> +2.40 / 1.000 -> 0.778 | +4.66 -> +4.11 / 0.959 -> 0.803 | +6.81 -> +9.45 / 0.984 -> 0.818 |

On the modifier axis use falls 19-36% while the probe falls 2-5%, which is the predicted direction
but a small effect. On the candidate axis the probe falls far more than use in all four families,
and Gemma's use rises 39% — the opposite of the prediction. Full-description accuracy stays at
0.898-1.000 throughout, so the manipulation never made the task hard in the first place.

Interpretation:
S8 does not establish a representation/use gap and is recorded as a negative result. Two candidate
reasons, neither rescued here: the load never bit, since accuracy never left ceiling; and on the
candidate axis a longer scene plausibly makes the restriction fact itself harder to compute, so the
probe drop need not mean the representation is weaker relative to use.

Consequence for the topic: together with the discarded 0.6B point, the "represented before used"
claim is removed from 041 entirely. Nothing is lost, because S7 already carries a representation/use
gap of a cleaner kind, at 8B-12B, inside single models, with full accuracy at 1.000 in every cell:
the state's projection scales with how many candidates a modifier removes while the behavioural cost
does not. That is the claim to make; S8 was not needed and did not work.
