# Rejected Candidates — Physical / Object Cognition

**Domain:** physical transformation, conservation, object permanence, trajectory tracking, amodal completion.  
**Search date:** 2026-08-27.

## Domain rule

“VLM 物理推理差”不是一个研究问题。这里优先寻找删除 VLM 术语后仍然成立的认知/物理现象，并要求 conserving/non-conserving 等成对设计能够区分感知失败、状态更新失败和不变量判断失败。

---

## 1. Generic physical reasoning

**Natural question:** Why do agents fail to predict how physical scenes evolve under ordinary interventions?

**Why it initially looked good:** Physical reasoning is natural, visually grounded, and has large current-model gaps.

**Kill evidence:** The generic space is already benchmark- and method-heavy. `CausalPhys` explicitly decomposes physical reasoning through causal graphs and proposes causal-reasoning fine-tuning; `MASS` and related 2026 work also target broad physical/spatial reasoning failures. A generic “locate the physical-reasoning circuit” story would be too broad, and the practical method is already externalized into causal/structured supervision.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** falling objects, collisions, containment, support, object motion, or another simulator are not separate mother questions.

**Resurrection condition:** A sharper natural invariant or dissociation whose matched contrast cannot be reduced to generic physical prediction.

---

## 2. Generic object permanence / shell-game tracking

**Natural question:** Why should an object remain represented as the same object when it becomes hidden and later reappears?

**Why it initially looked good:** Object permanence is a classic cognitive phenomenon; shell-game style tasks produce large failures on modern VLMs, including Qwen3-VL.

**Kill evidence:** Existing shell-game work already shows that explicit trajectory/identity tracking is an effective repair direction (e.g. SGCoT-style supervision). If our mechanism merely says “the model loses track of the hidden object trajectory,” the method is predetermined and does not require a white-box causal account.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** cup swaps, hidden-object tracking, occlusion, identity persistence, and shell games are the same family unless a representation–behavior dissociation survives explicit trajectory tracking.

**Resurrection condition:** Show that object identity and trajectory are correctly represented internally throughout occlusion but a later selection/readout process systematically chooses the wrong container; that would imply a qualitatively different repair.

---

## 3. Generic amodal-completion deficit

**Natural question:** Why can a perceiver infer the hidden continuation of a partly occluded object?

**Why it initially looked good:** Amodal completion is a classical perceptual phenomenon with clean visible/occluded manipulations.

**Kill evidence:** Current LVLM evidence does not support a broad, large failure across capable models. Recent evaluations find many models roughly human-comparable overall, with deficits concentrated in particular categories/languages. Using a narrow weak slice to manufacture a large effect would violate the repository’s behavior-first rule.

**Death code:** `NO_NATURAL_BEHAVIOR`

**Nearest-neighbor warning:** another occlusion dataset or weaker checkpoint should not be used to resurrect a generic amodal-completion claim.

**Resurrection condition:** A current open-family benchmark must show a large, stable, paired failure under ordinary prompts on at least two relevant model families.

---

## Survivor under audit — Conservation under physical transformation

**Natural question:** When an object or collection changes appearance—coins spread apart, clay reshaped, liquid poured into a differently shaped container—what properties should remain invariant, and why can a reasoner confuse appearance change with quantity change?

This is the classical Piagetian conservation problem, not a VLM-native construct.

`Vision Language Models Cannot Reason About Physical Transformation` / `ConservationBench` (2026) evaluates 112 VLMs on paired conservation and non-conservation videos. Humans achieve about 98.35% overall performance; under the strict paired criterion, 82/112 models score below 10%. Qwen3-VL-8B-Instruct is about 53.12% on conservation and 31.52% on non-conservation, but only 8.59% on the strict paired criterion; Qwen3-VL-8B-Thinking is 7.42% strict. The paper also reports that adding visual evidence can make balanced conservation/non-conservation judgment worse rather than better.

**Why it survives:** The decisive question is narrower than generic physical reasoning: does the model (A) misperceive endpoint quantities, (B) encode endpoints but fail to track the transformation/invariant, or (C) retain the correct visual state yet let an appearance-based/textual prior dominate the final judgment? Current audit found behavioral analysis and prompting controls, but no causal activation-patching account that adjudicates these explanations on the paired conservation/non-conservation contrast.

**Method branches:**

- endpoint-state encoding failure → improve/align quantitative visual state representations;
- transformation/invariant tracking failure → train or route an explicit invariant-state update computation;
- late prior/readout override → suppress or gate the appearance/default pathway while preserving perception.

**Status:** `PRE-CANDIDATE / SURVIVOR`.

**Reference:** https://arxiv.org/abs/2603.07109
