# Rejected Candidates — Memory Interference

**Domain:** proactive/retroactive interference, serial-position effects, working-memory competition, updating and retrieval.  
**Search date:** 2026-08-27.

## Domain rule

Memory is a natural phenomenon, but generic “LLMs forget old/new context” is far too broad. A viable topic needs a sharp cognitive contrast, substantial modern open-model behavior, and a mechanism question not already answered by lost-in-the-middle / superposition work.

---

## 1. Generic working-memory interference / recency

**Natural question:** Why do multiple active memories interfere with one another, and why are some positions easier to retrieve than others?

**Why it initially looked good:** Load- and position-dependent memory failure is large, easy to score, and maps naturally to encoding-vs-retrieval mechanisms.

**Kill evidence:** `In-context superposition: human-like working memory interference in large language models` (2026) already provides a mechanistic arc: competing items occupy overlapping internal representations, layerwise separation predicts retrieval success, and suppressing competing information improves performance. Generic recency / interference would therefore repeat the phenomenon→mechanism→intervention story.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** lost-in-the-middle, generic recency, working-memory load, overlapping item representations, and “which layer remembers?” are not fresh topics.

**Resurrection condition:** Require a qualitatively different interference asymmetry whose decisive contrast is not predicted by generic representation overlap.

**Reference:** https://arxiv.org/abs/2604.09670

---

## 2. Generic proactive interference alone

**Natural question:** Why do old key–value bindings intrude when the same key is repeatedly updated with new values?

**Why it initially looked good:** The phenomenon is robust and dramatic. `Unable to Forget` evaluates many model families and explicitly includes Qwen3-8B/14B/32B; accuracy deteriorates sharply as overwrite count grows.

**Kill evidence:** PI by itself is already a named, benchmarked failure with several follow-ups and mitigation directions. `Compress and Forget` (2026) further studies quantization effects on PI. A paper whose headline is merely “why do LLMs show proactive interference?” would be too close to an established behavior line and generic stale-memory mitigation.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** stale key-value memory, overwrite failure, latest-value retrieval, update-count scaling, and quantized PI are the same broad family.

**Resurrection condition:** A stronger dissociation must compare PI against another interference process and imply different computations/repairs.

**References:** https://openreview.net/pdf?id=YUHksmL8aw ; https://arxiv.org/abs/2608.18578

---

## Survivor under audit — PI ≫ RI inversion

**Natural question:** When old and new memories conflict, why should old memories disrupt new learning more strongly than new memories disrupt old learning?

`Transformers Remember First, Forget Last` (2026) adapts classical proactive interference (PI) and retroactive interference (RI) paradigms across 39 LLMs. Every model shows PI > RI, with Cohen's d = 1.73 (p < .0001), opposite the usual human immediate paired-associate pattern. RI and PI are nearly uncorrelated (R² = .044); model size predicts RI resistance (R² = .49) but not PI resistance (R² = .06); RI errors are mainly passive retrieval failures whereas PI errors are mainly active primacy intrusions.

This sharper **interference inversion** is not killed by the generic superposition result because it explicitly predicts two separable processes and an opposite-to-human asymmetry. Current audit found behavioral explanations such as “primacy bias,” but no causal activation-patching account that distinguishes encoding failure, retrieval selection, and late readout intrusion in modern open models.

**Status:** `PRE-CANDIDATE / SURVIVOR`.

**Reference:** https://arxiv.org/abs/2603.00270
