# Rejected Candidates — Spatial Perspective Taking / Frame of Reference

**Domain:** spatial reasoning under viewpoint changes, especially egocentric vs allocentric frame transformations in VLMs.  
**Search date:** 2026-08-26.

## Domain goal

The attractive scientific structure is:

```text
same scene + same objects
only observer/viewpoint changes
→ spatial relations must be transformed
```

A strong mechanism paper would distinguish scene encoding, observer/viewpoint representation, mental transformation, and final spatial readout.

---

# 1. Generic “VLMs are egocentrically biased”

**Natural question:** Why do VLMs answer from the camera’s viewpoint when explicitly asked to reason from someone else’s viewpoint?

**Why it initially looked good:**

- extremely natural spatial-cognition problem;
- multiple 2025–2026 benchmarks show large human–model gaps;
- errors are structured rather than random.

**Kill evidence:**

The generic behavior is now densely established:

- ICLR 2026 `SpinBench` evaluates 43 VLMs and reports systematic egocentric bias, poor rotation understanding, and reformulation inconsistencies; humans reach 91.2%.  
  https://proceedings.iclr.cc/paper_files/paper/2026/hash/724be4472168f31ba1c9ac630f15dec8-Abstract-Conference.html
- EMNLP 2025 `FoREST` directly evaluates frame-of-reference comprehension and proposes Spatial-Guided prompting.  
  https://aclanthology.org/2025.emnlp-main.1772/
- ACL 2026 `SCOPE` evaluates egocentric/allocentric consistency across viewpoints on 20.1K spatial VQA pairs.  
  https://aclanthology.org/2026.acl-long.1514/
- ACL 2026 `MirrorQA` reports a large gap on subject-centered left/right mirror reasoning: best model 65.40% vs human 99.28%.  
  https://aclanthology.org/2026.acl-long.1879/

“Why perspective taking is hard” is therefore too broad.

**Death code:** `NARRATIVE_COLLISION`

**Nearest-neighbor warning:** egocentric bias, allocentric failure, left/right mirror confusion, camera-frame bias, and generic frame-of-reference weakness are one family unless a sharper dissociation is supplied.

**Resurrection condition:** a controlled prerequisite dissociation showing that all component abilities are individually present but integration fails in a specific, reproducible way.

---

# 2. Component-ability composition failure in Level-2 visual perspective taking

**Natural question:** If a model understands that another agent sees the scene differently and can perform mental rotation separately, why can it still fail catastrophically when it must combine those abilities?

**Why it initially looked exceptionally good:**

`Egocentric Bias in Vision-Language Models` (FlipSet, 2026) evaluates 103 VLMs. The vast majority perform below chance; roughly three-quarters of errors reproduce the camera viewpoint. Crucially, prerequisite controls reveal a compositional dissociation: models can perform theory-of-mind and mental-rotation components substantially better than the combined Level-2 VPT task.  
https://arxiv.org/abs/2602.15892

This directly supports clean competing explanations:

```text
A. viewpoint state is missing/corrupted;
B. rotation operation is missing/corrupted;
C. both exist, but viewpoint does not condition the rotation computation;
D. computation succeeds, but late readout restores the camera frame.
```

**Why it is not promoted yet:**

The method space is uncomfortably close to existing work.

- `Cognitively-Inspired Tokens Overcome Egocentric Bias in Multimodal Models` (2026) introduces perspective tokens encoding orientation/mental rotation, improves VPT across synthetic and naturalistic benchmarks, and reports representational evidence that latent orientation sensitivity already exists in the base model but lacks appropriate internal structure.  
  https://arxiv.org/abs/2601.16378
- ICCV 2025 `Perspective-Aware Reasoning ... via Mental Imagery Simulation` explicitly constructs scene abstractions and viewpoint transformations to repair perspective reasoning.  
  https://openaccess.thecvf.com/content/ICCV2025/html/Lee_Perspective-Aware_Reasoning_in_Vision-Language_Models_via_Mental_Imagery_Simulation_ICCV_2025_paper.html
- A 2026 viewpoint-aware self-correction paper likewise adds explicit frame-of-reference signals and reasoning traces.  
  https://doi.org/10.1007/s44267-026-00126-0

If our mechanism result is simply “orientation/viewpoint information is present but is not structurally integrated,” then the natural repair—inject or condition on perspective/orientation structure—has already been demonstrated.

**Death code:** `METHOD_COLLISION` (currently HOLD-like; may be resurrected)

**Nearest-neighbor warning:** “ToM + mental rotation composition”, “binding social awareness to spatial operation”, “viewpoint routing”, and “perspective token” are extremely close. Do not revive merely by adding activation patching.

**Resurrection condition:** a causal result that changes the repair qualitatively. Example: show that viewpoint and transformed spatial relation are both computed correctly and causally available, but a *late camera-frame restoration/readout process* overwrites the allocentric answer. That would imply suppressing a late default-frame pathway rather than adding perspective representations.

---

# 3. Generic mirror left/right reasoning

**Natural question:** Why are models much worse than humans at deciding left/right from the reflected or subject-centered viewpoint?

**Why it initially looked good:**

- `MirrorQA` provides 5,549 manually verified samples and a huge human–model gap;
- left/right errors are easy to score and explain.

**Kill evidence:**

Mirror reasoning sits inside the already crowded perspective/frame-transformation family. The current behavior literature already attributes broad failures to egocentric/camera-aligned viewpoints, while explicit orientation/perspective representations are an existing repair direction. Without a distinct behavioral dissociation, the likely mechanism story is predictable.

**Death code:** `LOW_SURPRISE`

**Nearest-neighbor warning:** mirror reversal, 180-degree rotation, subject-centered left/right, and camera-to-agent coordinate conversion should not be split into separate mechanism papers solely by stimulus type.

**Resurrection condition:** a surprising asymmetry such as correct internal transformed coordinates paired with systematically inverted verbal left/right readout, robust across visual and text-only coordinate tasks.

---

# Domain verdict

This domain has excellent natural behavior and unusually strong public artifacts, but the obvious mechanism-derived fix—make viewpoint/orientation information explicit and condition spatial computation on it—is already occupied. The FlipSet composition failure remains scientifically attractive but is **not currently promoted** because the most likely mechanism story would not naturally yield a novel method.

**Current status: no final-pool candidate; component-composition failure retained as HOLD with a strict resurrection condition.**