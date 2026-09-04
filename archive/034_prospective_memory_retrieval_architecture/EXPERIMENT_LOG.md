# Experiment Log

## S0-1 — native released-cell audit

Question:
Is there a non-floor/non-ceiling behavioral substrate across visible event, time, and hidden
state-channel intentions, and do the released scaffolds already distinguish monitoring from
cue-triggered retrieval?

Experiment:
Inventory every deterministic v9 task by type/regularity/visibility and extract the exact
Qwen/Llama/Mistral baseline and heartbeat metrics from the released 64-run report.

Prediction:
The behavioral denominator passes if all prespecified open families are imperfect but above
floor. However, heartbeat gains alone cannot identify native monitoring because heartbeat
text re-presents intention information and changes the current forward pass.

Result:
The v9 scenario contains 83 intentions: 42 visible events, 26 time targets and 15 hidden-channel
events. Released single-baseline micro Set-F1 is 0.420 (Qwen3-8B), 0.526 (Mistral Small 24B)
and 0.644 (Llama-3.3-70B), so all three families are non-floor/non-ceiling. Heartbeat effects
are heterogeneous: Qwen3-8B rises to 0.719 under proactive heartbeat, Llama rises modestly to
0.681, and Mistral remains about 0.53; fixed heartbeats can reduce performance.

The scorer's independently defined monitoring-demand partition reveals a large baseline
difficulty gap in every family. Hit rates for no-monitoring-required versus
monitoring-required intentions were 54.8%/28.2% for Qwen, 85.7%/30.8% for Llama, and
64.3%/23.1% for Mistral. Proactive heartbeat improved both Qwen cells to 90.5%/66.7%, but
changed the monitoring-required cell only to 35.9% for Llama and 20.5% for Mistral. Thus the
released effect is not a family-general signature of one retrieval strategy.

Interpretation:
Behavior is established and is rich enough for a retrieval-architecture experiment. The
released scaffolds do not adjudicate H1/H2/H3: proactive heartbeat changes the input and may
act as a retrieval cue, while fixed heartbeat also changes false-positive pressure. The next
uncertainty is the focality/context interaction under matched intention and cue semantics.
The descriptive monitoring-demand gap cannot substitute for this manipulation because the
released partition also changes cue channel and observability.

Next:
Construct the frozen focal-visible/nonfocal × expected/unexpected clone and validate cue
comprehension before any activation patching. The released heartbeat contrast is context for
experimental design, not a mechanism result.

## S0-2 — matched-cue focality x target-context expectancy

Question:
Does a controlled prospective-memory action vary with cue focality and target-context
expectancy when the critical cue sentence, intention, and action are held fixed?

Experiment:
Use 16 semantic cue/action families. Focal trials require the ongoing classification task to
process the cue's semantic category; nonfocal trials classify an unrelated approval property.
Expected versus unexpected blocks change the preceding activity context. The final cue or
matched same-category no-cue sentence is otherwise byte-identical across these conditions.
All six mappings of REMINDER/YES/NO to A/B/C are scored and aggregated back to semantic
answers. No-cue trials jointly test ongoing-task comprehension and false reminders.

Prediction:
A measurable focality or focality-by-expectancy contrast shared across model families licenses
the frozen timing intervention. Pure sustained monitoring predicts pre-cue causal availability
across cells; cue-triggered retrieval predicts a cue-time transition, especially in focal
cells; dynamic control predicts pre-cue influence concentrated in expected/nonfocal cells.
Behavior alone cannot select among these mechanisms.

Result:
A discarded execution reused a two-option system formatter despite the three-option design;
it was invalidated before interpretation. The only repair changed that formatter to explicitly
allow A/B/C. No stimulus, item, gate, or analysis rule changed.

On the corrected run, Qwen retrieved the intention on every cue trial, but failed the focal
no-cue comprehension control: accuracy was 6.25% in both expectancy cells, versus 100% in
the nonfocal no-cue cells. Its reminder margin was actually *lower* for focal than nonfocal
cues by 4.19 logits in expected context (95% paired-item bootstrap CI [-5.17, -3.20]) and
4.15 in unexpected context ([-4.95, -3.36]); the interaction was approximately zero.

Llama passed the no-cue controls (81.25% focal, 93.75% nonfocal) and cue accuracy was
93.75--100%. Its continuous reminder margin went in the opposite direction: focal exceeded
nonfocal by 1.00 logits in expected context ([0.65, 1.37]) and 0.75 in unexpected context
([0.35, 1.19]); the small margin interaction was 0.24 ([0.05, 0.49]). Raw label-map
predictions were unstable for many Llama cue cells, although the complete six-map semantic
aggregate was fixed in advance. The two-family panel gate failed.

Interpretation:
This microscope does not supply a clean shared behavioral interaction. Qwen's focal-task
category control fails, cue execution is at ceiling, and the two model families have opposite
continuous focality effects. Consequently a timing-patching result would confound retrieval
architecture with ongoing-task interpretation and model-specific label behavior. This does
not erase PMBench's established prospective-memory phenomenon; it means the current
controlled clone cannot adjudicate monitoring versus spontaneous retrieval.

Next:
Stop activation patching for this clone. A future restart must first establish a non-ceiling,
cross-family focality/expectancy behavior while keeping the critical cue identical and must
prespecify the cue-comprehension control; it may not repair these 16 items after seeing the
model outcomes or reinterpret external heartbeat prompts as native monitoring.

## S0-3 — delayed two-intention validation with word-count ongoing task

Question:
Can a longer delay and a competing future intention yield a non-ceiling focality signature
while preserving ongoing-task behavior?

Experiment:
Place two future intentions before eight neutral filler sentences and then present a matched
target cue or no-cue sentence. Cross semantic-category focal processing with a nonfocal
six-word-count task and expected/unexpected block context. Aggregate all four Latin-square
mappings of TARGET_ACTION, OTHER_ACTION, YES, and NO on both primary model families.

Prediction:
Both no-cue ongoing tasks must work, cue retrieval must not saturate, and the focality effect
must have a common sign before any internal timing claim is licensed.

Result:
The experiment was invalid at its ongoing-task control. Both Qwen and Llama scored 0% in the
nonfocal no-cue cells: they answered NO to every exactly-six-word sentence rather than doing
the word-count task. Target-cue accuracy was 100% in every cell. Continuous focal-minus-
nonfocal target margins were negative in both families (Qwen -15.85/-14.23 logits by
expectancy; Llama -0.52/-0.29), but this contrast is inseparable from ignoring the nonfocal
task.

Interpretation:
This is a task-capability and ceiling failure, not evidence against prospective-memory
retrieval architecture. The design also never presented the second intention's cue, so it did
not establish that both intentions were live. A final principled repair is warranted because
the failures correspond to two explicit construction mistakes rather than an unfavorable
scientific result.

Next:
Replace word counting with a trivial orthographic task that has the same ongoing response,
remove exact cue words from the intention examples, and include target-cue, other-cue, and
no-cue trials. Do not alter the resulting panel after observing it.

## S0-4 — two live intentions without exact cue repetition

Question:
When both intentions can actually trigger, do semantic processing depth and cue expectancy
change which intention re-enters computation?

Experiment:
Use unseen category members as target and other cues after the same eight-sentence delay.
The focal task requires semantic category classification; the nonfocal task only checks
whether the sentence begins with `The`, eliminating the observed counting floor. Present
target, other, and neither cues under likely/unlikely cue expectancy, with the same four
response mappings and two frozen model families.

Prediction:
Strategic maintenance predicts relatively robust retrieval across semantic processing depth;
cue-triggered retrieval predicts a larger cost when the ongoing task need not process cue
meaning; dynamic switching predicts modulation by expectancy and focality. With two live
intentions, a systematic substitution of the higher-priority TARGET_ACTION for OTHER_ACTION
would additionally expose competition after cue detection.

Result:
No-cue controls were largely restored: Qwen scored 0.94--1.00 and Llama 0.75--1.00. For the
target cue, Qwen was perfect when a cue was expected but only 0.31--0.38 when unexpected;
Llama remained at ceiling. For the other-intention cue, semantic processing yielded
0.88/0.63 (Qwen expected/unexpected) and 0.88/0.94 (Llama), whereas the orthographic task
fell to 0.06/0.06 and 0.56/0.56. Errors often became TARGET_ACTION rather than a generic
failure: cross-intention confusion was 0.148 for Qwen and 0.102 for Llama. Target-cue
focal-minus-nonfocal margins were negative in both families (Qwen -5.20 expected and -0.53
unexpected; Llama -0.48 and -0.56). Qwen, but not Llama, showed a large expectancy effect.
The original symmetric panel gate failed because Llama target retrieval was saturated and
other-cue nonfocal retrieval was weak.

Interpretation:
The gate failure is scientifically informative rather than a dead denominator. Across model
families, a cue for the lower-priority second intention is retrieved far more often when the
ongoing task requires semantic processing; when it does not, the model frequently emits the
first intention's action. Qwen additionally switches strongly with explicit cue expectancy.
This pattern fits a dynamic multiprocess account better than uniform strategic maintenance or
fully automatic spontaneous retrieval, while exposing an intention-competition component.
Behavior alone cannot locate whether nonfocal failure is missed cue detection or post-
retrieval action arbitration.

Next:
KEEP 034. At the critical noun, measure the layer trajectory of target-specific versus
other-specific intention information in focal/nonfocal conditions, then patch a focal OTHER-
cue state into matched nonfocal recipients. A selective rescue of OTHER_ACTION, without
changing no-cue ongoing answers, would distinguish retrieval gating from generic instruction
compliance. If that state exists, predict behaviorally that increasing intention set size will
selectively impair lower-priority nonfocal cues while sparing focal cues.

## S1 — focal cue-token state transplant (frozen depths)

Question:
Does the cue token carry a transportable retrieval state that, moved from a focal donor into a
matched nonfocal recipient, selectively restores the lower-priority intention's action?

Experiment:
Three pre-registered relative depths (25/50/75% of blocks; Llama blocks 7/15/23, Qwen 8/17/26),
same-item focal donor state versus a cross-item focal delta and a matched-norm random vector,
scored on OTHER_ACTION margin over 32 other-cue items with 32 no-cue items as an injection
control, four response mappings averaged, both frozen families.

Result:
No selective positive effect at any depth in either family. Qwen: real focal state -0.077 /
-0.932 / +0.028 across depths, with the shuffled control moving the same way (-0.050 / -1.083 /
+0.030) and real-minus-shuffled never positive with a lower bound above zero. Llama: +0.010 /
-0.018 / -0.011, real-minus-shuffled -0.001 / -0.014 / -0.009. No-cue OTHER_ACTION intrusion
stayed at 0.00 under patching in both families, so nothing was injected. Panel gate failed with
0/3 positive depths per model.

Interpretation:
The cue token holds no single transportable switch for the second intention. This rules out the
registered retrieval-gating locus rather than the behavior, and forces the question of whether
the binding is missing at the cue or present and unused later.

Next:
Decode at the same token instead of transplanting: a coarse cue-detection target and a fine
intention-role target, with role lexically neutralised by counterbalanced category pairs.

## S2 — cue-role binding probe with a three-level ongoing task

Question:
Is the intention-role binding encoded at the cue token, and is cue-to-intention routing
controlled by the ongoing task's own category check rather than by generic semantic depth?

Experiment:
32 role-counterbalanced items from 16 category pairs, three cue words per category, so every cue
word appears once as intention 1 and once as intention 2 and ROLE is lexically balanced by
construction. Ongoing task at three levels: orthographic, semantic keyed to intention 1's
category, semantic keyed to intention 2's category. Mass-mean and PCA-logistic probes with whole
category pairs held out, nine relative depths, two response mappings, both frozen families.

Result:
The monitoring-piggyback prediction failed. Qwen's crossover was -0.005 [-0.099, +0.099]; Llama's
was -0.281 [-0.349, -0.208], the wrong sign, and for Llama the semantic task keyed to intention 2
*hurt* intention-2 cues (-0.141 [-0.188, -0.099] versus orthographic). The focality effect was
sign-inconsistent: Qwen's semantic tasks raised second-intention accuracy (+0.417, +0.323) while
lowering first-intention accuracy (-0.151, -0.240).
What did replicate is a one-directional priority asymmetry. Second-intention cues were executed as
the first intention's action on 22.4-72.9% of Qwen trials and 38.5-55.7% of Llama trials, while
first-intention cues became the second intention's action on 0.0-0.5% of trials in both families.
The probes then dissociate representation from use: ROLE balanced accuracy is 0.500 at layer 0 (the
counterbalancing control) and reaches 0.995-1.000 at mid depth in every ongoing-task condition,
including the orthographic one, transferring across conditions at 0.91-0.99; DETECT is 0.92-0.99
everywhere. On the Qwen nonfocal second-intention trials that were actually misrouted (n=49), ROLE
was decoded correctly on 100% of trials at 37.5-62.5% depth.

Interpretation:
The model encodes, essentially perfectly and at the cue itself, which standing intention a trigger
belongs to, and then executes the other intention anyway. That explains the S1 null: there is
nothing missing at the cue token to transplant. The registered prospective-memory retrieval-
architecture object does not survive -- focality is not a stable cross-family gate and the
ongoing-task category check is not the router. What survives is a priority asymmetry, still
confounded because intention 1 was always listed first and always named TARGET_ACTION.

Next:
Cross listing order with action naming (neutral ALPHA/BETA, semantic forward, semantic reversed)
to decide whether the asymmetry follows position or label, then KEEP or ARCHIVE on that result.

## S3 — priority deconfound: listing position vs action-name salience

Question:
Is the one-directional capture of second-intention triggers driven by listing position, by the
`TARGET_ACTION` label, or by both -- and is it cue-specific?

Experiment:
Same 32 role-counterbalanced items and orthographic ongoing task, crossing listing order with three
naming schemes: neutral (`ALPHA_ACTION`/`BETA_ACTION`), semantic_forward (first-listed is
`TARGET_ACTION`, as in S2) and semantic_reversed (first-listed is `OTHER_ACTION`). No-cue control
words in every cell measure generic action firing. Two response mappings, both frozen families.

Result:
Position primacy is real and survives neutral naming: the second-cue-minus-first-cue misroute
asymmetry is +0.406 [+0.354, +0.458] for Qwen and +0.234 [+0.182, +0.281] for Llama, and the
reverse error is 0.000 in five of six model x scheme cells. The label adds on top and the two
families weight it differently: the name-flip effect (forward minus reversed) is +0.109
[+0.052, +0.161] for Qwen but +0.427 [+0.370, +0.490] for Llama, whose asymmetry nearly collapses
to +0.083 when `TARGET_ACTION` is listed second.
Cue specificity separates the families. Qwen's no-cue control fires an intention on 1.0-2.6% of
trials against 40.6-72.9% second-cue capture, so the capture is trigger-specific. Llama's no-cue
control fires the first action on 11.5-50.0% of trials -- under neutral naming its false-alarm
rate (0.500) is higher than its second-cue misroute rate (0.234) -- so its apparent capture is
largely a generic first-action bias plus ongoing-task noncompliance, not routing.

Interpretation:
The surviving effect is an asymmetric, one-directional capture of a second standing instruction's
trigger by the first-listed instruction, clean and trigger-specific in Qwen, contaminated in Llama.
Its behavioral object is instruction position/priority bias, which prior work already owns; the
S2 dissociation (binding decoded near-perfectly at the trigger, including on misrouted trials)
would be mechanism depth on an owned object, which the strict extension gate rules insufficient.

Next:
None. 034 is archived; see `FINAL_VERDICT.md`.
