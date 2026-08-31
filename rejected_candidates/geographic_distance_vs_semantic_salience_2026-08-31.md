# Rejected Candidate — Geographic Distance ≠ Semantic / Landmark Salience

Date: 2026-08-31
Status: **TERMINAL REJECTION**

## Natural question

> Does a language model keep real metric geography separate from semantic or cultural closeness, or do famous/co-occurring places become represented as if they were geographically nearer than they really are?

A VLM variant asked whether salient landmarks override other geographically diagnostic evidence.

## Why it looked good

- Geographic distance is deterministic from coordinates and exists independently of the model.
- Semantic/cultural salience is plausibly learned from text frequency and co-occurrence, giving a simple competing-mechanism story.
- Country/city pairs provide broad real-world coverage without hand-created labels.
- The phenomenon would be understandable as a world-model distortion rather than a benchmark artifact.

## Kill evidence

The title-level object is already directly occupied.

2025 `Evaluation of geographical distortions in language models` explicitly compares semantic distances in model representations with true geographic distances and introduces an anomaly measure between semantic and geographic distance. It reports systematic regional distortions, including places that are semantically much closer or farther than their actual geography would imply.

2026 work further expands this family: `Investigating spatial-temporal bias of LLMs` studies geographically clustered estimation errors; ACL 2026 geospatial-reasoning benchmarks explicitly disentangle memory from spatial reasoning; and `HoloGeo` directly studies landmark bias in VLM geolocation and evidence-driven mitigation.

Thus `metric distance vs semantic salience`, `real geography vs landmark prior`, and a mechanistic probe of those distortions are direct continuations of an already named geography-bias family.

## Death code

`KILL-N0/N1 / DIRECT-GEOGRAPHIC-DISTORTION-AND-LANDMARK-BIAS-FAMILY`

## Nearest-neighbor warning

Do not resurrect as:

- city distance vs semantic similarity;
- cultural closeness vs physical closeness;
- famous landmark vs metric geography;
- Western-centric geographic representation;
- another continent/city list;
- another embedding distance, VLM, map prompt, SAE, probe, patch or steering method.

## Resurrection condition

Only reconsider a new geographic phenomenon whose title-level scientific object is not geographic distortion, metric-distance representation, landmark bias, geolocation evidence selection, or generic spatial reasoning.
