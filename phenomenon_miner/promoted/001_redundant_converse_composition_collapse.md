# Promoted phenomenon 001: Redundant-Converse Composition Collapse

Status: `DOWNGRADED / HOLD — TOO CONSTRUCTED AND INTERFACE-SPECIFIC`
Date: 2026-08-27

> Downgrade note (2026-08-27): this candidate depends on an artificial spatial
> relation world and a direct-choice interface, and the effect did not survive
> cleanly in free generation. It is retained as a mining lesson, not as the
> recommended research phenomenon.

## One-sentence phenomenon

In direct-choice spatial QA, adding a logically redundant converse fact selectively makes larger language models fail to combine two individually intact spatial components into a diagonal relation.

```text
Fact 1: Alice is above and to the left of Bob.
Fact 2: Equivalently, Bob is below and to the right of Alice.
Question: Where is Alice relative to Bob?
```

Fact 2 adds no world information and the answer remains `upper-left`. Repeating Fact 1 does not have the same effect. The deliberately narrow name is **Redundant-Converse Composition Collapse (RCCC)**. It should not be advertised as a general free-generation failure.

## Why it clears the discovery gate

- Natural and simple: “Adding the same fact from the other viewpoint makes the model worse.”
- Strict relation: world state, query, and gold are unchanged.
- Cross-family: Qwen, Gemma, and Phi show the same direction at adequate capability.
- Scaling anomaly: the selective effect strengthens or emerges with scale.
- Dissociation: diagonal composition fails while vertical and horizontal components remain available.
- Controlled: exact repetition is harmless; generic irrelevant-fact effects are smaller in stronger models.
- Mechanistically open: it separates component representation, role binding, composition, and direct-choice readout.

## Frozen setup

- Public StepGame validation split; natural one-hop templates.
- Query entity order matches the original fact order.
- Transformation appends the exact converse, optionally introduced by `Equivalently`.
- Randomized multiple-choice labels, temperature 0, thinking disabled.
- Controls: original, exact duplicate, disconnected irrelevant fact, ordinary converse, atomic compass converse, and explicitly marked converse.

## Primary cross-model result

Diagonal subset, 74 paired items per model, explicitly marked converse:

| Model | Original | + marked converse | Change | + exact duplicate | + irrelevant fact |
|---|---:|---:|---:|---:|---:|
| Qwen3-4B | 73.0% | 62.2% | -10.8 pp | 75.7% | 59.5% |
| Qwen3-8B | 78.4% | 62.2% | -16.2 pp | 74.3% | 68.9% |
| Gemma3-4B | 47.3% | 45.9% | -1.4 pp | 56.8% | 51.4% |
| Gemma3-12B | 67.6% | 54.1% | -13.5 pp | 67.6% | 62.2% |
| Phi-4-mini | 66.2% | 50.0% | -16.2 pp | 62.2% | 56.8% |

Paired exact tests on the capable/third-family panel:

| Model | Correct→wrong | Wrong→correct | Exact p |
|---|---:|---:|---:|
| Qwen3-8B | 14 | 2 | 0.0042 |
| Gemma3-12B | 11 | 1 | 0.0063 |
| Phi-4-mini | 12 | 0 | 0.00049 |

The scaling signature is not merely weak models failing. Qwen's loss grows from 4B to 8B. Gemma moves from a capability floor at 4B to a clear converse-specific loss at 12B. Meanwhile, stronger models tolerate a disconnected irrelevant fact better than the exact converse.

## Component-intact / composition-broken dissociation

On 120 public diagonal items:

| Model | Joint original | Joint + converse | Vertical original→converse | Horizontal original→converse |
|---|---:|---:|---:|---:|
| Qwen3-8B | 86.7% | 73.3% | 90.8%→95.8% | 95.0%→95.0% |
| Gemma3-12B | 88.3% | 76.7% | 95.0%→97.5% | 92.5%→93.3% |
| Phi-4-mini | 80.0% | 55.8% | 84.2%→70.8% | 84.2%→76.7% |

Cases where both components are correct but the joint label is wrong rise:

- Qwen3-8B: 7→25 of 120.
- Gemma3-12B: 6→22 of 120.
- Phi-4-mini: 9→17 of 120, with some component degradation too.

An 80-item exact-duplicate control gives:

| Model | Original joint | + converse | + exact duplicate |
|---|---:|---:|---:|
| Qwen3-8B | 86.3% | 73.8% | 85.0% |
| Gemma3-12B | 87.5% | 73.8% | 85.0% |
| Phi-4-mini | 78.8% | 53.8% | 81.3% |

This rejects plain length and repetition accounts.

## Important boundary condition

The anomaly is mode-specific. With unconstrained free generation and permission to reason, 100 diagonal items give:

| Model | Original | + marked converse |
|---|---:|---:|
| Qwen3-8B | 87% | 85% |
| Gemma3-12B | 91% | 96% |
| Phi-4-mini | 89% | 83% |

Therefore do not claim a general destruction of spatial reasoning. Claim a **direct-choice/readout-mode composition failure**, and treat deliberative rescue as part of the phenotype. The central mechanism question is why a deliberative path recovers the relation while immediate choice/readout fails.

## Nearest mother phenomena and decisive contrast

### StepGame noise robustness

StepGame already establishes that irrelevant, disconnected, and supporting noise can hurt. It does not establish an exact one-edge converse causing a diagonal-selective component/joint dissociation, scale-emergent selectivity, and deliberative rescue.

### Inverse/converse relation failure

ConvRe and 2026's `Reversing Arrows in Large Language Models` study classifying inverse relations. RCCC leaves the directly query-aligned fact explicitly present. The anomaly is that adding its equivalent converse corrupts joint readout despite intact components.

### Premise order

Premise-order work establishes permutation sensitivity. RCCC is a monotonicity violation from redundant equivalent evidence, with component/joint and response-mode dissociations. Order is a secondary axis, not the full phenotype.

The novelty search is preliminary, not a legal priority claim. An exact-signature search remains mandatory before paper commitment.

## Mechanistic hypotheses

1. **Joint readout suppression:** vertical/horizontal features survive, but competing frames suppress the diagonal label late.
2. **Incompatible role bindings:** equivalent sentences bind the same relation through swapped subject/object slots that are not canonicalized.
3. **Fast-reader failure:** the world-model writer is adequate, but direct choice reads shallow relation/option features before stable composition.
4. **Scale-installed shortcut:** larger models form cleaner components yet causally rely more on a fast, converse-sensitive option-selection circuit.

## First mechanistic package

1. Freeze 256 diagonal items and four conditions: original, duplicate, irrelevant, marked converse.
2. Replace grammar-constrained output with teacher-forced option-letter logit scoring.
3. Probe vertical, horizontal, joint direction, entity identity, and subject/object role across layers and positions.
4. Patch original→converse at evidence entities and query subject/object tokens.
5. Patch deliberative→direct-choice at the final query position.
6. Search heads/MLPs that change joint logits without damaging component probes.
7. Test query-oriented canonicalization, explicit subject/object markers, and late joint-state patching.
8. Replicate on SpaRTUN/SpaRP and a non-spatial two-feature relation task.

## Paper go/no-go gates

Proceed only if:

- teacher-forced logits reproduce the loss without grammar constraints;
- a second prompt and spatial dataset reproduce the component/joint dissociation;
- two capable families show analogous causal loci;
- an intervention rescues joint choice without merely eliciting longer reasoning;
- exact-nearest-work review finds no prior report of the full signature.

Kill or narrow if it is entirely due to structured-output grammar, one option layout, or StepGame templates.

## Reproduction artifacts

- `run_stepgame_redundant_converse.py`
- `run_spatial_component_dissociation.py`
- `run_spatial_converse.py`
- `run_converse_freeform_validation.py`
- JSONL records and summaries in `phenomenon_miner/results/`
