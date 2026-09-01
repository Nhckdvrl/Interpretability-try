# Rejection — Descriptive vs Prescriptive Normality

Date: 2026-09-01  
Verdict: **KILL-NOVELTY**

## Natural question

Does a language model distinguish **what is statistically common or average** from **what is ideal, desirable, or socially acceptable**, or does it blend both into a single notion of what is “normal”?

## Semantic aliases

- descriptive vs prescriptive norm
- common vs acceptable
- average vs ideal
- statistical normality vs normative normality
- descriptive stereotype vs prescriptive stereotype

## Why it looked promising

The distinction is extremely natural and supports clean cross-cells: a behavior can be common but disapproved of, or rare but strongly valued. Human cognitive work shows that judgments of normality combine descriptive and prescriptive information.

## Decisive kill evidence

ACL 2025 Best Paper `A Theory of LLM Sampling: Part Descriptive and Part Prescriptive` directly makes this distinction the central LLM scientific object. It proposes and experimentally tests that LLM sampling is jointly driven by a descriptive component (statistical norm) and a prescriptive component (implicit ideal), across diverse domains. It further studies concept prototypes and argues that LLM prototypes contain a prescriptive component analogous to human normality judgments.

Therefore the exact `statistical/common versus ideal/prescriptive` axis is already explicitly owned at paper scale. A hidden-state probe, steering direction, or causal patch would mainly replace the method while retaining the same scientific interpretation.

## Strongest-neighbor warning

Do not revive as common-vs-normal, typical-vs-ideal, descriptive-vs-injunctive, stereotype-vs-prescription, or normality steering.

## Death code

`F2 / N0-N2 — direct ACL Best Paper ownership of descriptive/prescriptive decomposition in LLMs.`

## Resurrection condition

Only a norm-related property that is conceptually independent of descriptive-versus-prescriptive normality could reopen this area.