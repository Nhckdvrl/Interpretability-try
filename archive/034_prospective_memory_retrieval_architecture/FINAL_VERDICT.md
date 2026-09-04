# 034 — Final Verdict

Decision: **ARCHIVE**
Date: 2026-09-04

## What the registered object was

Prospective-memory retrieval architecture: whether a future intention held across a delay is kept
under strategic monitoring, re-enters computation only through cue-triggered spontaneous
retrieval, or switches between the two with cue focality and expectancy.

## Why it does not survive

**1. The registered mechanism has no locus (S1).** The frozen cue-token transplant, at three
pre-registered relative depths in both families, produced no selective positive effect on the
second intention's action margin: Qwen -0.077 / -0.932 / +0.028, Llama +0.010 / -0.018 / -0.011,
with real-minus-shuffled never positive and no-cue injection at 0.00. 0/3 depths passed per model.

**2. The focality gate is not a stable cross-family effect (S2).** On a 2x larger, lexically
balanced item set the semantic-versus-orthographic ongoing task moved the two families in
inconsistent directions and moved the two cue types in opposite directions within Qwen
(+0.417 / +0.323 for second-intention cues, -0.151 / -0.240 for first-intention cues). The
proposed upgrade -- that routing piggybacks on the ongoing task's own category check -- was
refuted: Qwen's crossover was -0.005 [-0.099, +0.099] and Llama's was -0.281 [-0.349, -0.208],
the wrong sign.

**3. The one robust effect is an object prior work already owns (S2/S3).** What replicates is a
one-directional capture: triggers for the second listed intention are executed as the first
intention's action (Qwen 40.6-72.9%, Llama 23.4-51.0%) while the reverse error is 0.0-4.7%. S3
shows this survives neutral `ALPHA`/`BETA` naming (+0.406 Qwen, +0.234 Llama), so it is genuine
position primacy among standing instructions -- which is instruction position/priority bias, an
object owned by existing work. Under `STRICT_EXTENSION_GATE` E1, mechanism depth on an owned
behavioral object does not create a new topic.

**4. Cross-family cleanliness fails.** Only Qwen's capture is trigger-specific (1.0-2.6% no-cue
false alarms). Llama fires the first action on 11.5-50.0% of no-cue trials -- under neutral naming
more often than on genuine second-intention triggers -- so its effect is a generic first-action
bias plus ongoing-task noncompliance.

## What is worth carrying forward

The S2 probe result is the durable technical finding, and it is recorded here rather than
developed further: with category pairs counterbalanced so that every cue word appears once in each
role, the intention-role binding is decoded at the cue token at 0.500 balanced accuracy at layer 0
and 0.995-1.000 at mid depth in **every** ongoing-task condition, transfers across conditions at
0.91-0.99, and is decoded correctly on **100%** of the Qwen trials that were nonetheless misrouted.
Representation-present / use-absent dissociations of this shape converge with the late-selection
result in `038`, where referent preference is likewise constructed at the decision stage rather
than carried by the earlier state. If a future topic needs that claim, it should be registered on
its own object, not as a continuation of prospective memory.

## Not done, deliberately

No further depth or token sweeps, no narrowing to "instruction primacy in agents", and no rescue
by dropping Llama. The registered object is dead and the surviving one is owned.
