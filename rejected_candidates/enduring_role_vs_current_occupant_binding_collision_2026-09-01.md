# Rejection Record — Enduring Role vs Current Occupant

**Date:** 2026-09-01  
**Verdict:** `KILL-NOVELTY`

## Natural question

Does a language model distinguish an enduring social/institutional role from the particular person who occupies that role at a given time?

Example: the office/role `President of the United States` persists across administrations, while the incumbent changes.

## Semantic aliases

- role vs occupant
- office vs officeholder
- position vs incumbent
- enduring role identity vs time-varying filler
- social-role slot vs person binding

## Why it looked promising

- The distinction is simple and independent of any benchmark.
- It is a genuine ontological/knowledge-representation distinction: roles are repeatable relational positions, while occupants are time-indexed entities filling them.
- Existing public temporal datasets provide natural windows with presidents, university presidents, CEOs, chairpersons, heads of government, and `position held` relations.
- It looked like a clean bridge between social-role representation and temporal knowledge without inventing synthetic behavior.

## Decisive kill evidence

The exact experimental substrate is already central to temporal knowledge work:

- **TempLAMA / Time-Aware Language Models as Temporal Knowledge Bases** explicitly uses time-varying relations including `position held`, `chairperson`, and `head of government`.
- **EvolveBench (ACL 2025 Main)** explicitly contains Country→President, University→President, Company→CEO, and other evolving officeholder properties.
- **When Facts Change: Temporal Knowledge Conflict Resolution in LLMs (Findings ACL 2026)** includes both `position held`, `chairperson`, `officeholder`, `replaces`, and `subject has role` among its stable/updated Wikidata relations.

More importantly, the proposed internal novelty is already crowded by generic mechanistic binding / factual-retrieval work:

- **Functional Abstraction of Knowledge Recall in Large Language Models (2025)** models relation activations as a mapping function from subject to object and validates components with activation patching.
- **Representational Analysis of Binding in Language Models / Binding-ID work** establishes causal low-dimensional entity–attribute binding.
- **Mixing Mechanisms: How Language Models Retrieve Bound Entities In-Context (ICLR 2025)** studies multiple causal binding mechanisms.
- **Cell-Based Representation of Relational Binding in Language Models (2026)** explicitly represents discourse-level bindings as entity × relation cells causally bound to attributes.
- **Factual Retrieval in LLMs Is a Redundant, Distributed and Non-Contiguous Process (ACL 2026 Main)** studies entity→attribute computation paths in Llama-3.1 and Qwen3.

Given these neighbors, a project showing a `role/officeholder slot` and time-varying occupant binding would most naturally be interpreted as applying already-established relation/entity binding machinery to a particularly intuitive temporal relation. The remaining delta is too close to `existing temporal fact object + existing generic binding mechanism -> special-case mechanization`.

## Strongest-neighbor warning

Do not revive as:

- presidency vs president hidden states;
- role-slot / filler steering;
- officeholder binding circuit;
- incumbent replacement patching;
- time-indexed role cells;
- social-role vs named-person binding.

Changing the relation, model family, time period, or intervention method does not widen N2.

## Death code

`F2 / N2 — temporal officeholder object already established; generic relation/entity binding is already mechanistically occupied.`

## Resurrection condition

Only reconsider if a distinct scientific question is found that cannot be reduced to time-varying relation binding—for example, a separately motivated cognitive property of role concepts with natural cross-cells and predictions beyond retrieving the correct occupant.
