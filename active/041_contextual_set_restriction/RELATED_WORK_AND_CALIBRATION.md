# 041 — neighbours and venue calibration, checked against each round

Purpose: a standing list to re-read before every new experiment, so that (a) we do not drift into a
claim a neighbour already owns, and (b) we do not inflate scope past what the venues actually
require. All numbers below were read out of the papers themselves, not from memory.

## A. Venue calibration — measured, not remembered

| paper | venue | model scope | claim structure |
|---|---|---|---|
| *Causal Interventions Reveal Shared Structure Across English Filler-Gap Constructions* | **EMNLP 2025 Outstanding** | pythia **1.4B / 2.8B / 6.9B** only, one family; main analysis at 1.4B; the larger sizes run on *smaller* eval sets (96 sentences) in the appendix | one apparatus (DAS interchange interventions) yields 1 headline (mechanisms transfer across constructions) + 4 graded secondary claims, one of which is a **negative** (no transfer across clause boundaries) |
| *Llama See, Llama Do* | **ACL 2025 Outstanding** | 4 checkpoints, **all Llama** (3.1-8B, 3.1-8B-Instruct, 2-7B, 2-13B); the mechanism is only on Llama-3.1-8B | monotone strengthening on one axis: phenomenon exists -> holds for random tokens (so mechanistic) -> modulated by semantics -> carried by identifiable heads -> ablating them removes it |
| *Racing Thoughts* | **NAACL 2025** | primarily **gemma-2-9b-it**, plus gemma-2-2b-it; Llama-2 replication in the appendix | one algorithmic hypothesis -> correlational evidence -> causal evidence -> inference-time intervention |
| *Discursive Circuits* | **EMNLP 2025 Main** | **GPT-2 medium** primary, GPT-2 large as a scale check; Llama-3.1-8B only as a preliminary appendix trial | circuits recover the behaviour -> generalise to unseen frameworks (RST, SDRT) -> layer-wise feature analysis |

**Standing conclusion.** Model count and scale are *not* the bar: 1-4 checkpoints, often one family,
GPT-2-medium to 13B. The bar is one clean apparatus producing ~1 headline plus 3-5 progressively
strengthening secondary claims, negatives included. 041 already runs four families at 8B-24B plus a
Qwen scaling series; **adding models or scale cannot raise this paper and will not be done.**

## B. Topic neighbours — what they own, and the line we must stay on

### Human substrate (ours to build on, not to re-discover)

- **Davies & Richardson (2021)**, *J. Pragmatics* 178:258-269. The 2x2 we inherit: referential
  relevance (1 vs 2 referents) x semantic relevance of the adjective to the event (`fed` vs
  `tickled the hungry rabbit`), fully crossed, within-participants and within-items, 12 vignettes,
  N=31, self-paced reading. **Result: two main effects, no interaction**, and a time-course split —
  semantic relevance only in the noun-phrase window, referential relevance persisting into wrap-up.
  - *We may not claim*: that the same content can be relevant for reference, for the event, or both,
    or that these jointly affect processing. That is theirs.
  - *What their null leaves open*: a non-significant interaction cannot distinguish one
    undifferentiated relevance signal from two independent computations. That gap is where 041 starts.
- **Leffel et al. (2014)**, MEG. Restriction is context-dependent with the answer's lexical material
  fixed; non-restrictive modifiers usually still need a discourse relation, typically explanation.
- **Hoek et al. (2020)**. Restrictive material can simultaneously enter causal/concessive coherence
  relations, so restriction and coherence are not mutually exclusive - the theoretical licence for
  our `R+E+` cell.
- **Rohde et al.** Coherence expectations act in real time. **Explicitly not used for the E axis**:
  implicit-causality verbs move referential salience by themselves and would make the E -> reference
  off-diagonal uninterpretable.

### Computational neighbours (owned ground)

- **Schlangen et al. (SIGDIAL 2009)** and later situated reference models: words incrementally
  narrow a candidate set. *041 may not claim that adjectives eliminate distractors.*
- **Monroe et al. (TACL 2017)**, **Fang et al. (CogSci 2022)**: neural pragmatic reference,
  overmodification, redundancy. *041 may not claim that redundant adjectives incur cost.*
- **Mosbach et al. (COLING 2020)**: restrictiveness metadata for relative clauses, largely tied to
  punctuation. *041 may not use comma/no-comma relative clauses as primary evidence.*
- **COLM 2025**, VLM referring-expression pragmatics; **INLG 2025**, *Analysing Reference Production
  of LLMs*. Behavioural neighbours on whether generated descriptions identify a referent.
- **Discursive Circuits (EMNLP 2025 Main)**: sparse circuits for PDTB discourse relations in GPT-2
  medium; lower layers carry lexical semantics and coreference, upper layers discourse abstractions.
  - *Closest to our C5 depth sweep.* They ask **which components process a labelled discourse
    relation**; we ask **whether the referential status of one modifier reshapes what the same
    content is taken to explain**. Their layer story is a useful external anchor for C5's ordering
    account, and we must cite it rather than present "upper layers are more discourse-like" as new.

### The line 041 stands on

> The same true modifier, in a world where nothing about it changes except which alternatives are
> live, is read differently as an explanation — and the referential-role state is what causally
> carries that. No neighbour owns the *direction* of influence between a referential function and an
> explanatory one.

## C. Per-round checklist

Run this before adding any experiment:

1. Does the new result belong to a neighbour in section B? If yes, it is a denominator, not a claim.
2. Is its direction predictable before running? If yes, it is a gate, not a claim.
3. Does it distinguish two readings that are both currently alive? If not, it is a defensive control
   and should not be run.
4. Does it add models or scale? If yes, section A says it cannot help; do not run it.
5. Does it make the topic less natural, or the sentence stating it more contorted? If yes, drop it.
