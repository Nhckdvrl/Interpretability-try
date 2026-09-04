# 045 — Experiment Log

Object: Donnellan's referential/attributive distinction. Every world is a misdescription conflict —
the speaker's established target R does not satisfy the description F while a second person S does
— so referential use should send reference to R and attributive use to S with the description and
all world facts identical.

Readouts are deterministic single-token forced choice. `use_mode` asks which person the speaker
means; `downstream_action` asks which person the host should fetch, so the claim does not rest on
one metalinguistic question. Raw-fact denominators (`description_truth`, `speaker_target_fact`,
`entity_fact`) share each scene verbatim.

## S0 v1 — first crossover attempt

Result:
Referential accuracy 0.027 (Qwen) and 0.046 (Llama); attributive 1.000. The crossover was in the
right direction (+7.35 [+5.48, +9.33] Qwen, +1.12 [+0.80, +1.50] Llama) but never flipped a
choice. `speaker_target_fact` scored 0.397 and 0.266 — below chance.

Interpretation:
Two construction defects, not a result. The referential frame established an attended person and
then had the speaker request a description, which reads as two separate wants; Donnellan's
referential use requires the speaker to *believe the description fits their target*, which was
never stated, so the referential use was not instantiated at all. And the denominator asked one
clumsy disjunctive question ("was X watching or has X met before?") covering both establishment
families, which is why it scored below chance.

## S0 v2 — belief stated, denominator split by establishment family

Result:
The denominator fix worked for Qwen (`speaker_target_fact` 0.397 -> 0.850, description truth 0.998,
entity fact 0.995) and the crossover grew by an order of magnitude: +15.33 [+11.33, +19.67] on
`use_mode` and +14.32 [+11.85, +17.04] on `downstream_action`, consistent across both establishment
families and all four description families. Referential accuracy nonetheless stayed at 0.214 /
0.155 (Qwen), 0.145 / 0.049 (Llama), 0.004 / 0.000 (Phi); attributive stayed at 1.000 everywhere.
Denominators still failed for Llama (0.506, with an A/B position fallback: 0.16 versus 0.86 by
mapping) and Phi (0.649).

Interpretation:
Three families agree on direction, but two of three cannot reliably report who the speaker's
established target is, and none of them lets that target override the description. The target was
established descriptively ("the guest standing by the window") and had to be resolved to a name,
which is a second measurement burden rather than part of the object.

## S1 v3 — named target, paraphrased frames

Result:
Naming the target lifted Qwen's referential accuracy from 0.214 to **0.741** on `use_mode`
(0.155 -> 0.361 on `downstream_action`) with attributive still at 1.000, and it held across all
three referential paraphrases (0.833 / 0.660 / 0.729) and all three attributive paraphrases
(1.000 each). But two denominators moved the wrong way: `speaker_target_fact` 0.550 and
`entity_fact` 0.720.

Interpretation:
The breakdown is diagnostic, not broken. `speaker_target_fact` split 0.86 referential versus 0.24
attributive, because the attributive frames say "setting that aside" and the question "who did the
speaker already have in view" was read as "who does the speaker want". `entity_fact` split 0.45
referential versus 0.90-1.00 attributive, which is the serious one: the frame's bare assertion
"Ann believes Mr. Vale is the one drinking a martini" was absorbed as a world fact, so choosing the
target could be the model revising the facts rather than speaker reference overriding semantic
reference.

Naming the target is not a salience confound, because the confound control is the matched
attributive frame containing the identical clause.

## S1 v4 — common establishment sentence, belief marked false

Design:
Every frame now opens with the identical sentence `{speaker} has been watching {target} for a while
now.`, so target salience, mention count and recency are exactly equal across use modes and the
denominator question is unambiguous. Referential frames mark the belief as *false* ("mistakenly
believes", "wrongly taking", "under the false impression") so the model has no reason to revise the
world facts. Frames avoid the word the `use_mode` question asks about. Three paraphrases per mode
support held-out-paraphrase probing, and description-token states are captured at nine depths for
the use-mode direction and its amplification test.

Result:
Running on four families.

Result:
Denominators recovered in the three families that track the target: description truth 0.99/0.82/1.00,
speaker-target 0.99/1.00/0.98, entity fact 0.80/0.90/0.98 (Qwen/Phi/Gemma, referential contexts).
The crossover is real on `use_mode`: referential 0.701/0.931/0.926 against attributive 1.000
everywhere. Llama fails its denominators again (speaker-target 0.57, entity 0.70) and is out.
The v4 "representation-action gap" was an artifact of my own question. Splitting the action readout
by the actor's information state gives, for Qwen/Phi/Gemma, speaker's own action 0.803/0.743/0.812,
a fully informed assistant 0.653/0.479/0.706, and the uninformed host 0.463/0.206/0.481. The
gradient tracks the actor's access to the speaker's belief, which is the normatively correct
behaviour; there is no representation-action dissociation. The use-mode probe at the description
token is at layer-0 chance and reaches AUC 1.000 by 37.5% depth in every family, i.e. the state is
fully determined by the frame and carries no discriminating information.

## S1 v6 — is speaker reference inferred, or only followed when stated?

Question:
v5's referential frames end by stating whom the speaker is talking about, so following them needs
no inference. Removing only that clause, while keeping the same attention sentence and the same
false belief, asks whether the models compute speaker reference at all.

Result:
Qwen 0.701 -> 0.609, Phi 0.931 -> 0.519, Llama 0.127 -> 0.271 (wrong direction, denominators
already failing). Attributive stays at 1.000 in every family and every frame.
The decisive number is the paraphrase breakdown. Within a single condition, changing only the
wording moves accuracy across almost the whole range: Qwen `i1` 0.74, `i2` 0.48, `i3` 0.60 and
`r1` 0.96, `r2` 0.46, `r3` 0.69; Phi `i1` 0.92, `i2` 0.15, `i3` 0.49. That within-condition swing
is far larger than the referential/attributive effect it is supposed to support.

Interpretation:
The referential side of the object is carried by frame wording, not by the registered scientific
factor. Only the attributive side is stable, and a stable attributive reading is just descriptions
denoting. See `FINAL_VERDICT.md`.
