# 041 — paper skeleton

Working title:

> **Same Content, Different Jobs: Referential and Explanatory Function Are Distinct Causal States
> in Language Models**

Title width check: "restrictive adjectives" would be too narrow, "discourse understanding" too
broad. The object is one modifier and two of its jobs, which is the width of the EMNLP 2025
Outstanding filler-gap paper (one construction family, one abstraction question).

## Abstract (draft)

A modifier can be true of its referent and still be doing different jobs: helping identify which
entity is meant, or bearing on why the described event happened. We ask whether language models
represent those jobs separately from the content itself. Starting from Davies and Richardson's (2021)
human factorization of referential and semantic relevance, we build four-entity worlds in which the
same true adjective either does or does not narrow the live referent set, crossed with whether it
bears on the matrix event; gold is computed from denotations and the design was frozen before any
model was run. Behaviourally, referential status reshapes what the same content is taken to explain —
support for the true property rises and support for the contrasting property falls — in all four
model families, while the reverse influence is an order of magnitude weaker. Causally, editing the
modifier's referential-role state at a single token reproduces that redistribution. Editing an
event-relevance state at the same token, estimated identically, produces the *opposite* signature:
the contrasting property loses rather than gains. A single undifferentiated relevance signal cannot
produce opposite signs, so the two discourse functions are distinct causal states. The coupling is
also localised: in one family the state decodes equally well at three depths but is causally
effective at only one.

## Section map, and which number lands where

| section | content | evidence |
|---|---|---|
| 1 Introduction | the same true property, two jobs; what is known and what is not | — |
| 2 Background | restrictive vs non-restrictive modification (Leffel et al. 2014); restriction and coherence are not exclusive (Hoek et al. 2020); referential x semantic relevance in humans (Davies & Richardson 2021); what LM work already owns: incremental reference resolution, overmodification, REG | — |
| 3 Setup | four-entity worlds, denotational gold, the two readouts, the four families, the pre-analysis freeze | `B1_PREANALYSIS_FREEZE.md` |
| 4 Human effect in an LM | semantic relevance replicates in the NP window in 4/4 and the interaction is null, as in humans; referential *licensing* does not transfer at all | **B0** |
| 5 The selectivity matrix | `dRR` +2.1 to +23.5; `dRE` on the contrasting property −0.03 to −0.15 in 4/4 with the true property moving the other way; `dER` 3.6-17% of `dRR` | **B1** |
| 6 The role state carries it | role minus shuffled, correct sign 4/4 on both halves, significant 3/4 on each | **C4** |
| 7 Two states, opposite signatures | referential edit raises the contrasting property, event-relevance edit lowers it; rules out one relevance signal | **C6** |
| 8 Where it lives | one causal depth per family while decodability is broad; in Llama layers 12/16/20 all decode at 0.94-0.97 and only 12 is effective | **C4/C5** depth sweep |
| 9 Discussion | what this says about restrictiveness as a *function* rather than a lexical class; feedback to the linguistic account | — |
| Limitations | `dER` has behavioural evidence only; B0's variance is 12 items with no participant dimension; the reference readout is insensitive inside the B1 worlds by construction | — |

Prior 041 results are reused, not re-run: **S1** (restriction is separable from uniqueness, AUC
0.997-1.000, cross-uniqueness transfer 0.867-0.929) and **S3** (causal specificity 4/4 with property
truth preserved) become section 3's established starting point. **S0** is a capability denominator
and is one sentence. **S4** is superseded by B0. **S6** and **S8** are dropped. **S7** goes to the
appendix unless the graded story is needed.

## Figures

1. **Design and result in one panel.** Left: one world, the two manipulations (live-entity clause,
   matrix verb), the two readouts. Right: the signature dissociation — two states at the same token,
   opposite effects on the contrasting property.
2. B0: two windows x four families, referential vs semantic.
3. B1: the 2x2 selectivity matrix per family, with the contrasting-property row that carries the
   specificity.
4. **Key figure.** C4 vs C6: role-minus-shuffled on the true and contrasting property, both states,
   four families.
5. Depth profile: probe AUC and causal effect against relative depth, four families.

## Scope discipline

Four families, 8B-24B, one apparatus. No scaling series, no extra families, no mitigation section.
Calibration: EMNLP 2025 Outstanding filler-gap uses three pythia sizes; ACL 2025 Outstanding
*Llama See, Llama Do* uses four Llama checkpoints with the mechanism on one; NAACL 2025
*Racing Thoughts* is primarily one Gemma model.
