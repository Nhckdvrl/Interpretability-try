# Social-cue recognition != accommodation / action

Status: **TERMINAL REJECTION (2026-08-31)**

## Natural question

A model can sometimes infer an interlocutor's latent social state (e.g. power, affect, expertise) from implicit cues. Does that imply that the inferred state is actually used to select an appropriate response strategy, or can recognition succeed while accommodation/action fails?

## Why it looked good

ACL 2026 `Know Your Place: Diagnosing Implicit Social Adaptation Failures in Chinese Large Language Models` establishes a strong behavior-level anomaly (`Social Agnosia`): models substantially adapt under explicit social conditioning but produce homogenized responses to implicit power/arousal/epistemic cues. Crucially, that paper treats Social Agnosia as an observable interaction-level descriptor rather than a claim about internal mechanism, and its evaluated LLMs are tested through reply generation rather than a separate recognition-vs-action decomposition.

A natural-data path also appeared plausible: Prabhakaran et al. provide 122 real Enron email threads manually annotated for hierarchical/situational power, influence, communication control, overt displays of power, and success of power attempts; separate communication-accommodation corpora contain real conversations under high/low/neutral power roles. This initially suggested a non-synthetic S0 route.

## Kill evidence

A direct 2026 nearest neighbor already owns the title-level decomposition. `Reading the Air: Evaluating Field Intelligence of LLMs in Social Dynamics` / GroupMind explicitly evaluates a progressive social chain:

1. Subtext Deciphering,
2. Atmosphere Recognition,
3. Social Appropriateness.

The paper explicitly reports a **cognition-action gap**: models can possess the capacity to perceive social signals yet fail to respond appropriately, and states that the bottleneck can lie beyond parsing the social cue itself. This is the same scientific object as `recognize implicit power/social state but fail to accommodate`, only broader across social dynamics.

Therefore an MI project that localizes a `social-state reader -> accommodation/action gate`, even on Enron or another natural corpus, would be a direct mechanism successor to an already named 2026 behavior object rather than a new ACL/EMNLP/NAACL-level scientific object.

## Death code

`KILL-N1 / DIRECT-SOCIAL-COGNITION-ACTION-GAP-COLLISION`

## Nearest-neighbor warning

Do not resurrect as any of the following without genuinely new phenomenon-level evidence:

- `social perception vs response`,
- `recognition vs accommodation`,
- `power reader vs politeness/style writer`,
- `implicit cue detected but not used`,
- `social-state representation vs strategy selection`,
- switching C-ISA to Enron/Wikipedia/speed-networking,
- another language/culture/model family,
- adding probes, SAE, activation patching, steering, or a reader/writer vocabulary.

These are all the same occupied object unless a new behavior cannot be represented as the GroupMind cognition -> social-action gap.

## Resurrection condition

Only reopen if a distinct natural social phenomenon is found whose failure cannot be expressed as `social cue/subtext/atmosphere is recognized but downstream socially appropriate action is not selected`, and which has independent current-open-model existence evidence plus a non-overlapping mechanism story.
