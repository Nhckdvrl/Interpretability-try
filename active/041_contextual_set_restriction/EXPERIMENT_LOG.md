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

## B0 — Davies & Richardson (2021) replicated as window surprisal

Question:
Their 2x2 crosses referential relevance (contrast set present or not) with semantic relevance of the
adjective to the matrix event (`fed` vs `tickled the hungry rabbit`), on 12 vignettes, N=31,
self-paced reading, two windows. Does it appear in an LM when reading time is replaced by token
surprisal — the measure they themselves invoke when interpreting their result?

Experiment:
Their 48 critical items verbatim, scored as raw running text with no chat template, on the noun
phrase (adjective + noun) and the wrap-up window. Four families. Bootstrap over the 12 items, which
is the only variance we have: there is no participant dimension, so intervals are wide by
construction and this is a denominator rather than a claim.

Result — the two halves of their design come apart:

| model | window | referential | semantic | interaction |
|---|---|---|---|---|
| Qwen3-8B | NP | -0.193 | -0.928 [-1.854,+0.070] | +0.145 |
| | wrap-up | +0.228 | **-0.560** | +0.079 |
| Llama-3.1-8B | NP | -0.002 | **-1.345** | +0.156 |
| | wrap-up | **+0.215** | -0.403 | +0.097 |
| Gemma-3-12B | NP | +0.152 | **-1.144** | +0.350 |
| | wrap-up | +0.205 | -0.244 | -0.008 |
| Mistral-24B | NP | **+0.327** | **-0.873** | +0.175 |
| | wrap-up | **+0.142** | -0.378 | +0.095 |

Semantic relevance eases the noun-phrase window in 4/4 (three intervals exclude zero; Qwen misses by
0.07) and the interaction is near zero everywhere, matching their own null. Referential relevance
does not replicate at all: absent or reversed in every family, significantly positive in Llama's
wrap-up and both of Mistral's windows.

Interpretation:
The failure is the predicted one. Their referential factor is a *licensing* manipulation — `there
were two spiders` supplies a contrast set but gives the second spider no properties, so `the scary
spider` is not denotationally restricting. Humans infer that the modifier is licensed; the models do
not. This turns the argument for B1's denotational R axis from a design choice into an empirical
fact, and it is why B0 is the natural-language window in place of S4.

Note:
Mistral's tokenizer refuses `return_offsets_mapping`, so span location gained a cumulative-prefix
path. It is identical to the offset path on Qwen3-8B: maximum absolute difference 0.000e+00 over all
48 rows, zero rows with differing token counts (`logs/span_scoring_equivalence.txt`).

## B1 — referential relevance crossed with explanatory relevance

Question:
When the same true modifier changes only whether it narrows the live referent set, or only whether
the matrix event is one it bears on, which of those changes what the modifier contributes to
reference and what it contributes to explanation?

Experiment:
Fixed four-entity worlds, `A = P+Q+` the target, live sets `{A,B,C}` and `{A,C,D}` so that `P`
swaps role while the sibling `Q` restricts in both — no competition is built into the stimuli. World
text is byte-identical across R conditions. The E axis changes only the matrix verb, inheriting the
twelve D&R adjective-event pairings. Reference is a forced choice over the live entities;
explanation is the length-normalised log probability of a fixed continuation (`Because the rabbit
was hungry.`), byte-identical across E+ and E-, so the contrast is a pure context swap with no
option-order bias. 13,824 reference and 1,536 explanation rows, four families, frozen under
`B1_PREANALYSIS_FREEZE` before the panel was opened.

Result:

| | Qwen3-8B | Llama-3.1-8B | Gemma-3-12B | Mistral-24B |
|---|---|---|---|---|
| dRR | **+23.46** | **+2.11** | **+9.88** | **+3.76** |
| dRE true property | **+0.096** | **+0.032** | +0.025 | **+0.018** |
| dRE contrasting property | **-0.064** | **-0.031** | **-0.148** | **-0.071** |
| dER | -0.84 | -0.19 | **-1.68** | **-0.44** |
| dEE | -0.069 | -0.002 | **-0.188** | **-0.083** |
| \|dER\|/dRR | 3.6% | 9.1% | 17.0% | 11.7% |

Making the modifier referentially load-bearing redistributes explanatory support: 4/4 families
suppress the contrasting property, 3/4 raise the true one. The opposite signs rule out the reading
that breaking reference merely degrades every downstream continuation, which would move both the
same way. The reverse coupling is real but 3.6-17% of dRR.

Interpretation:
Two quantities are deliberately not claimed. `dEE` is negative in 4/4 but `G2_E` already raises the
baseline under E+, so there is less headroom for the noun-phrase mention to add; saturation explains
it and it is not treated as a finding. `dER` has a mundane source: an event-relevant verb partially
predicts the property, so dropping the adjective costs less when the verb already points at it.

`RC(Q)` differs across R conditions by design, not by failure. `Q` restricts in both, but dropping it
leaves 2 live candidates under `R+` and 3 under `R-`, and S7 already established that the state
scales with how many candidates a modifier removes.

The observed structure is a directed asymmetry, which is none of the three patterns the freeze named
in advance. It is reported as found rather than forced into a label.

## C4 — is the coupling carried by the referential-role state?

Question:
B1's R->E coupling is behavioural. Is it carried by the modifier's referential-role state, or by
something else the live-set clause changes?

Experiment:
The S1 mass-mean estimator and the frozen S3 edit `h' = h + alpha (mu_opposite - h.d) d`, unchanged,
applied at the P-modifier token inside the B1 vignettes. Half the property families held out; the
depth is chosen by held-out probe AUC and never by causal performance. Controls are S3's: a
shuffled-label direction and a random unit direction. Read out on held-out families only.

Result — the restriction-role state is present in the naturalistic worlds (held-out AUC 0.933-1.000)
and editing it moves the explanation readout, `alpha = 4`, on modifiers that are restricting:

| model | layer | held-out AUC | dES true property | dES contrasting property |
|---|---|---|---|---|
| Qwen3-8B | 22 | 0.972 | **-0.0150** | **+0.0298** |
| Llama-3.1-8B | 12 | 0.969 | **-0.0246** | **+0.0292** |
| Gemma-3-12B | 24 | 0.933 | +0.0010 | **+0.1189** |
| Mistral-24B | 20 | 1.000 | -0.0011 | **+0.0065** |

Releasing the referential role releases the suppression of the contrasting property in 4/4, and
lowers support for the true property in 2/4. Random directions are at zero except for two small
significant cells in Gemma and Mistral; the shuffled direction carries 20-42% of the role effect in
Qwen and Gemma, which is the same ratio S3 reported (10-40%) and is a known weakness of permuted
mass-mean baselines rather than a new problem.

This mirrors B1 exactly, including which half is which: the contrasting-property effect is the 4/4
one in both the behavioural and the causal experiment, and Gemma is the family missing the
true-property effect in both. Effect sizes (0.015-0.030 nats/token) are the same order as the
behavioural effect they explain (dRE 0.018-0.096).

Not claimed:
The reference context of C4 is uninformative and is reported as such. In B1 the sibling `Q`
restricts in both conditions by design, so removing `P`'s role leaves reference intact — margins are
+2 to +23 and accuracy is above 0.99. The edit moves ReferenceMargin by 0.01-0.10 and is not
selective. The causal evidence for the reference side stays with S3, where it is -0.89 to -4.28,
selective in 4/4, with property truth preserved.

Also not claimed:
The mechanism suggests an over-attribution failure — within `E-`, where the property does not bear on
the event, making it referentially load-bearing should still raise support for it as an explanation.
All four families are positive (+0.009 to +0.042) but only Llama's interval excludes zero. At the
level of raw support the item variance is too large; the within-item `dRE` differencing is where this
effect is clean. A 1/4 result is recorded as a directional trend, not promoted to a claim.

---

# Pilot B — from restrictiveness to discourse function

Frozen before the panel was opened: `B1_PREANALYSIS_FREEZE.md`, tag `B1_PREANALYSIS_FREEZE`.
Execution order was freeze -> B0 -> B1, and B0 was explicitly not a gate for B1.

## B0 — Davies & Richardson (2021) in an LM

Question:
Their 2x2 crosses referential relevance (contrast set present or not) with semantic relevance
(`fed` vs `tickled the hungry rabbit`), fully crossed, 12 vignettes x 4 versions, N=31, self-paced
reading. Does it appear in an LM when reading time is replaced by window surprisal — the measure
they themselves appeal to when interpreting their result?

Experiment:
Their 48 critical items verbatim, two transcription notes recorded rather than silently applied.
Mean per-token NLL over their two windows: the noun phrase (adjective + noun) and the wrap-up
phrase. Raw running text, no chat template, no forced choice. Four families.

Result — the two factors separate cleanly:

| model | window | referential | semantic | interaction |
|---|---|---|---|---|
| Qwen3-8B | NP | -0.193 | -0.928 [-1.854, +0.070] | +0.145 |
| | wrap-up | +0.228 | **-0.560** | +0.079 |
| Llama-3.1-8B | NP | -0.002 | **-1.345** | +0.156 |
| | wrap-up | **+0.215** | -0.403 | +0.097 |
| Gemma-3-12B | NP | +0.152 | **-1.144** | +0.350 |
| | wrap-up | +0.205 | -0.244 | -0.008 |
| Mistral-Small-24B | NP | **+0.327** | **-0.873** | +0.175 |
| | wrap-up | **+0.142** | -0.378 | +0.095 |

Bold marks bootstrap intervals over the 12 items excluding zero; negative eases processing.

Interpretation:
Semantic relevance replicates in the noun-phrase window in all four families, and the interaction is
near zero everywhere, matching their own null. Referential relevance does not replicate: it is absent
or reversed in every family and significantly positive in three cells. That is the predicted failure
rather than a surprise — their referential factor is a *licensing* manipulation ("there were two
spiders" supplies a contrast set but no properties, so `the scary spider` does not denotationally
pick anything out), and it is exactly the half B1 replaces with gold computed from the described
properties. B0 turns "why B1 needs a denotational R axis" from a design argument into a measurement.

Only 12 items carry the variance here; D&R's power came from 31 participants and we have no
participant dimension. That is a property of B0 as a denominator and is not fixable by adding models.

Note:
Mistral's tokenizer refuses `return_offsets_mapping`, so span scoring gained a cumulative-prefix
path. It is identical to the offset path on Qwen3-8B to 0.000e+00 over all 48 rows
(`logs/span_scoring_equivalence.txt`).

## B1 — referential relevance x explanatory relevance on the same content

Question:
With the world text fixed and only the live-entity clause or the matrix verb changing, does making a
modifier referentially load-bearing change what that same content is taken to explain, and does
event-relevance change what it does for reference?

Experiment:
48 four-entity worlds over the 12 D&R adjective-event families, 13,824 reference rows and 1,536
explanation rows, gold computed from denotations, structural validity asserted in code with no model
consulted. `Q` restricts under both R conditions so no competition is built into the stimuli. The
explanation readout is the length-normalised log probability of a fixed continuation, identical
across `E+` and `E-`, plus the same with the property's contrasting value.

Result:

| | Qwen3-8B | Llama-3.1-8B | Gemma-3-12B | Mistral-24B |
|---|---|---|---|---|
| G1 `RC(P)` R+ - R- | +23.46* | +2.11* | +9.88* | +3.76* |
| G2_E `ES_p` E+ - E- | +0.53* | +0.17* | +0.35* | +0.21* |
| **dRR** | +23.46* | +2.11* | +9.88* | +3.76* |
| **dRE** true property | +0.096* | +0.032* | +0.025 | +0.018* |
| **dRE** contrasting property | **-0.064*** | **-0.031*** | **-0.148*** | **-0.071*** |
| **dER** | -0.84 | -0.19 | -1.68* | -0.44* |
| **dEE** | -0.069 | -0.002 | -0.188* | -0.083* |
| \|dER\| / dRR | 3.6% | 9.1% | 17.0% | 11.7% |

Interpretation:
The gates pass everywhere and are denominators. The finding is the off-diagonal. Making a modifier
referentially load-bearing redistributes explanatory support *property-specifically*: the true
property gains in 3/4 families and the contrasting property loses in **4/4**, with opposite signs.
The opposite signs are what rules out the obvious alternative, that breaking reference simply
degrades every downstream continuation — that would move both continuations the same way.

The reverse influence is real but an order of magnitude weaker: `dER` is negative in all four,
significant in two, and 3.6-17% of `dRR`. Its likely source is mundane and is reported as such: an
event-relevant verb partially predicts the property, so reference has a back-channel when the
adjective is dropped.

Two quantities are deliberately *not* claimed. `dEE` is negative in all four but `G2_E` already
raises the baseline under `E+`, so there is less headroom for the NP mention to add; saturation
explains it and it is not treated as a result. And within `E-`, raw `ES_p` under `R+` minus `R-` is
positive in all four families but significant only in Llama (+0.029 [+0.011, +0.048]); the
over-attribution reading it would support is recorded as a directional trend, not a claim.

`RC(Q)` differs across R conditions (-0.64 to -5.57, all significant). This is design, not failure:
`Q` restricts under both conditions, but dropping it leaves 2 live candidates under `R+` and 3 under
`R-`, and S7 already established that the state scales with how many candidates a modifier removes.

The observed structure is a directed asymmetry, which is none of the three patterns the freeze named.
It is reported as found rather than forced into a label.
