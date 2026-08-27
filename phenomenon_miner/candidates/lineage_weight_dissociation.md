# Lineage–Weight Dissociation: models know reports share a source, but still count them as separate evidence

## One-sentence phenomenon

**The model can correctly say that ten articles all copy one witness, yet still reasons as if it heard ten witnesses.**

This is not a generic failure to parse provenance. It is a dissociation between:

1. recovering the dependency graph among reports; and
2. using that graph when assigning evidential weight.

## Current status

Promising primary candidate, but **not safe to claim as a new mother phenomenon**. A very recent paper (Lin et al., arXiv:2608.19701, submitted 2026-08-20) independently names the system-level mother failure *Memory Correlation Bias* and proposes CAMA for multi-agent memory arbitration. GroupQA (Findings ACL 2026) also establishes that paraphrased repetition can outweigh distinct evidence, while explicitly omitting source metadata.

The potentially novel object here is narrower and mechanistically sharper: **the same base model represents source dependence correctly under a matched probe, but that available representation fails to control its final belief**. Neither adjacent paper performs this representation–utilization dissociation or a white-box causal analysis of it.

## Pilot design

Twenty mundane domains were used (warehouse entry, hiking trail, harbor, gate, package room, road, field, platform, and so on). In the key pair:

- clean tie: one equally reliable firsthand observer supports each alternative;
- echoed tie: the same two firsthand observations remain, but two extra reports explicitly state that they merely relay one of those observations;
- explicit-tally variants append the identical sentence: “there is exactly one independent firsthand observation for each conclusion.”

Answer-option order and report order are randomized. Decision probes use unconstrained greedy generation because vLLM constrained-choice decoding introduced a strong label-A artifact. Count probes are auxiliary only.

## Pilot results

Accuracy means choosing “the available evidence does not favor either conclusion.” N=20 per condition and model.

| Model | Clean tie | Clean tie + explicit tally | Echoed tie | Echoed tie + same explicit tally | Matched tally drop |
|---|---:|---:|---:|---:|---:|
| Qwen3-8B | 25% | 40% | 0% | 15% | 25 pp |
| Gemma3-12B | 50% | 60% | 10% | 40% | 20 pp |
| Qwen3-32B | 50% | 80% | 0% | 5% | 75 pp |
| Phi-4-mini | 70% | 65% | 15% | 5% | 60 pp |

Additional size replications on the matched explicit-tally pair:

| Model | Clean tie + tally | Echoed tie + tally | Drop |
|---|---:|---:|---:|
| Qwen3-4B | 75% | 25% | 50 pp |
| Qwen3-8B | 40% | 15% | 25 pp |
| Qwen3-32B | 85% | 5% | 80 pp |
| Gemma3-4B | 70% | 45% | 25 pp |
| Gemma3-12B | 60% | 40% | 20 pp |

The effect therefore survives all tested sizes in two separate families; it is not monotonic, but it is largest in Qwen3-32B rather than disappearing with scale.

### Natural human-paradigm replication

We also implemented the published election-poll version of the human *illusion of consensus* paradigm: news outlets are secondary sources and named polling companies are primary sources. This removes the explicit tally sentence and the warehouse-style templates. N=10 name/order/label rotations per condition.

| Model | Clean 1-vs-1 decision | Recognizes repeated posts share one poll | Correct dependent-consensus decision | True 4-vs-1 independent decision |
|---|---:|---:|---:|---:|
| Qwen3-4B | 100% | 0% | 50% | 90% |
| Qwen3-8B | 100% | 60% | 10% | 90% |
| Gemma3-12B | 100% | 70% | 0% | 100% |
| Qwen3-32B | 100% | 100% | 0% | 100% |
| Phi-4-mini | 100% | 90% | 0% | 100% |
| Gemma3-4B | 60% | 70% | 10% | 100% |

This is the cleanest current evidence for the proposed dissociation. In particular, Qwen3-32B identifies the dependency relation on every item but never lets it determine the answer. Qwen also shows a surprising scale split: 4B does not recognize the shared poll (0%) and is only moderately biased (50% correct), whereas 8B/32B increasingly recognize lineage (60%/100%) while their correct decisions fall to 10%/0%. Scaling improves provenance perception without improving—and apparently while worsening—provenance use. Gemma exhibits the dissociation at both 4B and 12B. The count probe is harder and should not be conflated with the binary relation probe; several models count reports rather than distinct polls even while correctly classifying SAME versus DIFFERENT.

Additional controls:

- Qwen3-32B recovers the independent-source count at 95% in echoed cases but selects the warranted tie at 0% without the explicit tally.
- All four models perform well when three genuinely independent observers support one side (75–100% decision accuracy).
- The Qwen within-family effect increases sharply from 8B to 32B rather than vanishing with scale.
- Reversing which substantive conclusion is echoed preserves the effect: correct tie rates are 0% for Qwen3-8B/32B and 40--45% for Gemma3-4B/12B. Phi-4-mini shows a weaker but still negative reverse-side effect (40% versus a 65% clean-tie control).
- A chain-of-thought repair probe on Qwen3-32B produced ten parseable final answers out of twenty; all ten were correct. This suggests an available but normally bypassed computation, not absence of the concept. The remaining ten exceeded the 512-token budget and are not scored.
- Mistral-Small-24B is an important boundary case: it solves the echoed tie (95%) but incorrectly treats genuine 3-vs-1 independent consensus as a tie (20% correct). It should be reported as a distinct conservative aggregation strategy, not hidden or used as the universal-behavior claim.

## Why it is natural

The underlying problem is ordinary testimony, not a bespoke symbolic game: syndicated news, press-release rewrites, copied citations, agent memories derived from a shared tool result, and multiple doctors relying on the same lab test all instantiate it. The normative relation is old and domain-independent: duplicating a report without adding an independent observation should not increase its evidential force.

The human-reasoning literature supplies a principled source distribution and validated manipulations, including *Getting to the Source of the Illusion of Consensus* and *Reasoning about (In)Dependent Evidence: A Mismatch between Perceiving and Incorporating Dependencies?* Public RAG datasets such as GroupQA can supply natural claims and evidence; real syndication/provenance graphs should replace templated pilot reports in the main experiment.

## Mechanistic opening

The matched probes make a direct white-box program possible:

1. localize a decodable source-dependency representation across layers;
2. compare it with the frequency/stance representation that controls the answer;
3. use activation patching from the successful count or clean-tie run into the echoed-decision run;
4. test whether provenance is represented but routed too late, or whether a document-frequency pathway overwrites it;
5. sweep the number of derivative reports to look for a cliff or winner-take-all transition;
6. test whether steering the dependency subspace restores calibration without changing stance recognition.

The strongest publishable result would be causal: patching a small set of components restores source-aware weighting while preserving document comprehension and ordinary majority aggregation.

## Required next gates

- Reproduce on at least one 70B-class model; treat Mistral-Small-24B as a preregistered boundary condition rather than an exclusion.
- Use log-probability scoring over semantically rotated labels, not only generated labels.
- Reverse which side is echoed and balance every report position.
- Replace templated pilots with stimuli from published human illusion-of-consensus materials and natural web/news provenance graphs.
- Compare exact-copy, paraphrase, explicit citation, URL-only, and multi-hop syndication.
- Audit arXiv:2608.19701 in detail; if it already contains the perception–incorporation dissociation, reject this candidate.
- Run white-box feasibility on Qwen3-8B and Gemma3-12B before promoting.

## Honest novelty statement

Do **not** claim: “We discover that correlated evidence creates a false majority.” That claim is occupied.

Potentially defensible claim: “Across model families and scales, LLMs often encode the correct evidential dependency structure but fail to use it in belief formation; we identify and causally intervene on the internal routing failure that separates provenance recognition from evidential weighting.”
