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

## C4 — is the coupling carried by the referential-role state?

Question:
B1 found the coupling behaviourally. Is it carried by the modifier's referential-role state, or by
something else the live-entity clause changes?

Experiment:
The S1 mass-mean estimator and the frozen S3 counterfactual replacement, both unchanged, applied
inside the B1 vignettes at the P-modifier token, with six of the twelve property families held out
and the direction never chosen by causal performance. The edit pushes a restricting modifier toward
the non-restricting class mean. Readout: the fixed-continuation explanation support, for the true
property and for the property's contrasting value. Shuffled-label and random directions as controls,
the S3 convention. Four families.

The probe-AUC argmax was **replaced by a sweep over all five captured depths** before reading any
result, because held-out AUC saturates (1.000 in Mistral) and the argmax is then arbitrary. The
sweep changed the reading and is reported in full.

Result — role minus shuffled, alpha 4, at each family's selective site, held-out families only:

| model | site (depth) | AUC | true property | contrasting property |
|---|---|---|---|---|
| Qwen3-8B | 22 (61%) | 0.972 | **-0.0095** | **+0.0173** |
| Llama-3.1-8B | 12 (37%) | 0.969 | **-0.0227** | **+0.0235** |
| Gemma-3-12B | 24 (50%) | 0.933 | -0.0157 | **+0.0882** |
| Mistral-Small-24B | 20 (50%) | 1.000 | **-0.0043** | +0.0046 |

Bold marks bootstrap intervals over held-out items excluding zero.

Interpretation:
Removing the referential-role component moves the explanation the way B1's behaviour predicts:
support for the true-property explanation falls and support for the contrasting property rises. The
sign is correct in 4/4 on both halves and significant in 3/4 on each, with a different family the
exception on each half. Magnitudes (0.004-0.088 nats/token) are the same order as the behavioural
redistribution they explain (`dRE` 0.018-0.148), which is the right comparison.

The reference context was run and is **not used**. In the B1 worlds `Q` restricts under both R
conditions by construction, so editing away `P`'s role leaves the referent identifiable, and margins
are 2-23 logits; effects are 0.01-0.1 logits and not selective. This is a consequence of the design
choice that keeps competition out of the stimuli, not a failed replication — the causal reference
evidence is S3's and stays there.

## C5 — where does the coupling live?

The depth sweep answers this directly, and the answer is not one of the three shapes anticipated.

In Llama the state decodes at 0.969 / 0.968 / 0.944 at layers 12, 16 and 20, but the causal effect
exists only at 12; at 16, with essentially the same AUC, the true-property effect **reverses sign**
(+0.0075). Decodability is broad, use is one locus.

In Gemma layer 18 produces the largest raw effects in the whole panel (-0.20 / +0.31) at an AUC of
0.532, i.e. chance, and there the shuffled direction is *larger* than the role direction
(+0.48 vs +0.31). That layer is a place where any edit disturbs the output, not a functional site.
The probe-AUC argmax rule would have hidden this; the sweep exposes it.

So the coupling is not a shared representation that later branches, and it is not entangled to the
output. It is localised: the referential-role state governs the explanatory readout at a single
depth per family (37-61%), and the same state at neighbouring depths, decodable just as well, is
causally inert.

## C6 — the same token, a second state, the opposite signature

Question:
C4 showed the referential-role state moves the explanation readout. Is that just "some relevance
signal", or is there a separate event-relevance state at the same token with a signature of its own?

Experiment:
Identical to C4 in every respect except the label: the state is estimated on
`p_relevant_to_event` instead of `p_restricts`, at the same modifier token, with the same mass-mean
estimator, the same held-out property families, the same S3 replacement edit, the same shuffled and
random controls, and the same depth sweep. Readout is unchanged: support for the fixed explanation
continuation, true property and contrasting property. Four families.

Statistic: role minus shuffled, averaged over every depth whose held-out AUC is at least 0.6. The
threshold and the averaging are fixed in advance and applied identically to both states and all
families.

Why not the probe-AUC peak: it is a bad selector and demonstrably so. Mistral's event-relevance probe
peaks at layer 10, the one depth at which that state does nothing (+0.0105 on the true property,
wrong sign), while layers 20-30 carry the effect (-0.018, -0.016, -0.016 on the contrasting
property). Its referential probe saturates at 1.000, which makes that argmax arbitrary too.

Result — the contrasting-property column separates the two states by sign in 4/4:

| model | state | dES true property | dES contrasting property |
|---|---|---|---|
| Qwen3-8B | referential | **-0.0151** | **+0.0155** |
| | event | **-0.0265** | **-0.0198** |
| Llama-3.1-8B | referential | **-0.0036** | **+0.0075** |
| | event | -0.0051 | **-0.0131** |
| Gemma-3-12B | referential | -0.0104 | **+0.0398** |
| | event | -0.0212 | **-0.0482** |
| Mistral-Small-24B | referential | -0.0026 | +0.0018 |
| | event | **+0.0043** | **-0.0109** |

Bold marks bootstrap intervals over held-out items excluding zero.

Interpretation:
Removing the referential role lets probability mass **redistribute** to the alternative property:
once the model no longer knows which property is doing the identifying, the other one gains as an
explanation. Removing event relevance instead **withdraws the explanatory warrant**, and the
alternative does not benefit — it loses too.

A single undifferentiated relevance signal predicts the alternative property to gain under both
edits. The observed signs are opposite in all four families, which rules that out. This is the
strongest result in the project: two states at one token, estimated identically, with opposite
causal fingerprints on one readout.

Mistral is the weak family throughout — its probes are the best in the panel (AUC 1.000 for the
referential state) and its causal effects the smallest. Its referential-side contrast cell is
+0.0018 and not significant, so it contributes the sign but not the interval.

---

# Raising the sample size — 48 families

Audit that forced this. The bootstrap resamples adjective-event families, and B1 had twelve of them;
the causal experiments held out six. The 13,824 reference rows were almost entirely counterbalancing
*within* those twelve, so quoting row counts as sample size was misleading. The item set was extended
to 48 families (`scripts/b1_items.py`): the 12 inherited from Davies & Richardson, kept as a labelled
core, plus 36 authored to the same template. The extension is not pre-registered, is not
frequency-controlled the way theirs is, and was not normed on humans, so every result is reported by
source.

## B1 on 48 families

| | Qwen3-8B | Llama-3.1-8B | Gemma-3-12B | Mistral-24B |
|---|---|---|---|---|
| `dRR` | +20.10* | +2.38* | +11.35* | +3.63* |
| `dRE` true property | **+0.073*** | **+0.022*** | **+0.068*** | **+0.027*** |
| `dRE` contrasting | **-0.048*** | **-0.028*** | **-0.134*** | **-0.071*** |
| `dER` | **-1.12*** | **-0.20*** | **-1.29*** | **-0.38*** |
| `dEE` true property | -0.043 | **-0.051*** | **-0.235*** | **-0.089*** |
| `dEE` contrasting | **+0.104*** | **+0.074*** | **+0.373*** | **+0.090*** |
| \|`dER`\| / `dRR` | 5.6% | 8.5% | 11.4% | 10.6% |

The R manipulation raises support for the true property and lowers it for the contrasting one; the E
manipulation does the reverse. That is a full behavioural double dissociation on one readout, and its
signs match the C6 causal signatures cell for cell.

**Two earlier readings are withdrawn.** `dEE` was called saturation on the strength of the 12-family
run; it is significant in 4/4 here, so that was an underpowered null presented as a mechanism.
`dER` was called non-significant; it is significant in 4/4. The magnitude asymmetry survives — `dER`
is 5.6-11.4% of `dRR` — so "the reverse influence is an order of magnitude weaker" stands, but as a
statement about size, not about existence.

**Provenance, stated rather than blurred.** `dRE` is significant on the inherited core and on the
extension separately, in both halves. `dEE` on the contrasting property is significant in **no**
family on the core alone and needs the extension's power; it is 4/4 on the extension and matches an
independent causal result, but it is reported as an extension-powered finding.

**One honest weakness of the extension.** Llama's `G2_E` manipulation check is +0.172 on the
inherited core and +0.034, not significant, on the authored families. Our adjective-event pairings
are weaker than D&R's human-normed ones for that model. Qwen's extension check is +0.349 and holds.

## Stimulus quality gate, and what it found

A per-item manipulation check — `G2_E` computed for each family rather than each panel — showed 7 of
48 families with a null or backwards manipulation, **all of them authored, none inherited**. The
inherited mean check is +0.313 against the authored +0.195. The items were the problem, not the
statistics, so the criteria were made explicit and executable in
`scripts/validate_b1_items.py`:

| criterion | threshold | source |
|---|---|---|
| event verb frequency | Zipf >= 3.0 | rarer verbs are not used reliably |
| verb pair matched within a quartet | \|dZipf\| <= 1.2 | **Davies & Richardson's own bar** |
| property value frequency | Zipf >= 2.4 | their `mouldy` is 2.43, which sets the floor |
| Q value frequency | Zipf >= 3.5 | must be an ordinary word |
| no lexical overlap between P and Q; values distinct within a dimension | — | construct validity |
| no verb phrase carrying its own article-bearing complement | — | it strands the object |

The gate found **26 violations, every one of them in the authored set**. `descale` and `limescaled`
have a Zipf of 0.00, so that item was testing words the models barely see; `rebind` is 1.38 and
`rewire` 2.45. Twelve quartets were mismatched by more than D&R allow — a criterion this project had
simply never applied — and eight Q values were rarer than ordinary words. Fourteen families were
revised; the authored set now passes every criterion. The three violations among the inherited twelve
are D&R's own (`feed`/`tickle` differ by 1.43 Zipf, `tinned`, `unframed`) and are printed rather than
fixed, since changing their words would end the inheritance.

**Pre-stated test of the revision.** Authored families with a null manipulation fell from 8 to 3 of
48. The twelve inherited families produced bit-identical numbers — 0 of 12 moved by any amount —
which is the check that matters, since they were untouched and therefore fix a reference point for
whether the revision leaked into the core. The authored mean rose from +0.210 to +0.273 against the
core's +0.348.

**Where the revision stops.** Three families still fail: `patched`/`punctured`, `dried`/`damp`,
`sharpened`/`blunt`. The tempting explanation is that the `+sem` verb lexically presupposes the
property, so restating it as the reason is redundant. Checking all 48 kills that story — presupposing
pairs are common in the set and most are fine (`grit`/`icy`, `air out`/`stuffy`, `fill`/`empty`). The
three are therefore left in. Continuing to edit whichever items score badly is tuning, and three
nulls in 48 dilute an effect rather than create one. The distribution is reported instead: median
`G2_E` +0.268, range -0.126 to +0.707, 3/48 non-positive.

## B1 on the cleaned 48 families, and what the ratios say

Cleaning the stimuli strengthened the *manipulation*, not the effect, which is the direction that
tells you the cleaning was real. Llama's authored-set `G2_E` went from +0.034 and not significant to
+0.071 and significant; Qwen's from +0.349 to +0.465. The inherited twelve returned bit-identical
numbers.

| all 48 families | Qwen3-8B | Llama-3.1-8B | Gemma-3-12B | Mistral-24B |
|---|---|---|---|---|
| `dRR` | +20.99* | +2.29* | +11.66* | +3.50* |
| `dRE` true property | **+0.068*** | **+0.021*** | **+0.078*** | **+0.025*** |
| `dRE` contrasting | **-0.049*** | **-0.028*** | **-0.139*** | **-0.072*** |
| `dER` | -1.37* | -0.14 | -0.85* | -0.34* |
| `dEE` true property | -0.019 | -0.025 | **-0.173*** | **-0.073*** |
| `dEE` contrasting | **+0.121*** | **+0.126*** | **+0.388*** | **+0.109*** |

The crossing is the result and it holds in 4/4 (`figures/fig_behavioural_matrix.pdf`): the
referential manipulation raises the true-property explanation and lowers the contrasting one, the
event manipulation does the reverse.

**How many sources each readout listens to.** Taking the ratio of the two manipulations' effects on
each readout turns the asymmetry into a statement about architecture rather than about leakage:

| | reference readout `|dRR|/|dER|` | explanation readout `|dEE|/|dRE|` |
|---|---|---|
| Qwen3-8B | **15.3x** | 2.5x |
| Llama-3.1-8B | **16.6x** | 4.5x |
| Gemma-3-12B | **13.8x** | 2.8x |
| Mistral-24B | **10.4x** | 1.5x |

Reference is governed by one function to within an order of magnitude. Explanation is a joint
integration of two, within a factor of a few, and they pull in opposite directions. That is a
stronger claim than "referential status leaks into explanation", and it costs no extra experiment —
it is a ratio of numbers already in the table.

**A deeper reading that was tested and rejected.** If the two functions merely re-allocated a fixed
budget of explanatory credit, the sum `ES(true) + ES(contrast)` would be invariant while the
difference moved. It is not: the sum rises significantly under the E manipulation in 3/4 families
(+0.083 to +0.292) and under the R manipulation in 2/4. Event relevance raises total explanatory
mass rather than redistributing it. Reporting only the difference, which is significant in 3/4 and
would have made the conservation story look right, would have been construction.
