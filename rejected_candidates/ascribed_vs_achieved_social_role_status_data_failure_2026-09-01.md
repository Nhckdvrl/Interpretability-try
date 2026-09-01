# Rejection — Ascribed vs Achieved Social-Role Status

Date: 2026-09-01  
Verdict: **KILL-DATA / KILL-SCALE**

## Natural question

Does a language model distinguish social positions that are largely **ascribed/assigned** (for example kinship or status given by birth) from roles that are **achieved/acquired through action or appointment**?

## Semantic aliases

- ascribed vs achieved status
- assigned vs earned/acquired role
- inherited vs attained social position
- status origin

## Why it looked promising

This was a Hamdi-style omitted-axis attempt from the 2026 `Granularity Axis` mother. Ascription/achievement is a classic sociological distinction independent of micro-to-macro granularity, and no direct modern-LLM mechanistic collision was found in the first novelty search.

## Decisive kill evidence

The mother substrate does not support the proposed cross-axis cleanly. The released 75-role inventory is overwhelmingly composed of achieved/appointed occupational, organizational, institutional, and policy roles. Only a small set of micro roles are plausibly ascribed/kinship-like (`parent`, `grandparent`, `widow`, etc.). There is no balanced natural `ascribed × achieved` coverage across the five granularity levels or domains.

Therefore the project would require us to construct a new role inventory specifically to manufacture the cross-cells and then run models to discover whether the axis exists. That violates the v2.1 Route-A/Route-C anti-lottery discipline: the mother no longer supplies the measurement substrate, and the synthetic labels would become the source of the phenomenon.

## Strongest-neighbor warning

Do not revive merely by hand-authoring dozens of new roles, asking an LLM to label ascribed/achieved status, or treating the absence of a novelty collision as sufficient evidence.

## Death code

`F1 + F3 / KILL-DATA-SCALE — natural question but no legitimate mother-aligned row-level cross-cells; continuation would become synthetic-first behavior discovery.`

## Resurrection condition

Only reconsider if an independently published/open social-role dataset supplies balanced, auditable ascribed-versus-achieved labels/cross-cells together with modern open-model role behavior, without requiring the project to create the scientific axis itself.