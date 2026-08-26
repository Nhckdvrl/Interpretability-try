# Rejected Candidates — Cognitive Flexibility / Set Effects

**Domain:** Einstellung effect, confirmation bias, fixation, belief-consistent search, failure to abandon a familiar strategy.  
**Search date:** 2026-08-27.

---

## 1. Einstellung effect / diagnostic fixation

**Natural question:** Why can a familiar successful strategy prevent a reasoner from using new decisive evidence that demands a different solution?

**Why it initially looked excellent:** Einstellung is a classic cognitive-flexibility phenomenon. ACL 2026 `MedEinst` provides 5,383 counterfactual clinical pairs where a small discriminative-evidence change flips the correct diagnosis, and reports severe bias-trap rates on modern models including Qwen3 and MedGemma. The failure is large, paired, and programmatically scorable.

**Kill evidence:** The same paper already closes much of the practical method loop with ECR-Agent: Dynamic Causal Inference plus evidence audit and evolving graph memory explicitly force reasoning around patient-specific evidence rather than the familiar disease pattern. This repair does not require knowing whether the internal failure is representation, retrieval, or arbitration. Under README P3, a generic white-box mechanism paper risks becoming optional explanation after an already effective external evidence-audit solution.

**Death code:** `METHOD_COLLISION`

**Nearest-neighbor warning:** medical fixation, premature closure, familiar-pattern bias, atypical-case failure, or swapping medicine for another expert domain is not enough if the repair remains “audit decisive evidence / causal graph before committing.”

**Resurrection condition:** A representation–behavior dissociation where the model already encodes and causally retains the decisive counterevidence yet a specific internal fixation pathway overrides it, and the resulting repair is qualitatively different from external evidence audit.

**References:** https://aclanthology.org/2026.acl-long.1847/ ; https://github.com/zhui711/MedEinst

---

## 2. Generic confirmation bias / biased-hypothesis persistence

**Natural question:** Why does an initial favored hypothesis make a reasoner preferentially interpret later evidence as supporting it?

**Why it initially looked good:** Confirmation bias is natural, broad, and easy to create with matched leading-vs-neutral hypotheses.

**Kill evidence:** ICLR 2026 work on `MoLaCE` already frames leading-prompt behavior as latent confirmation bias, identifies a bias-associated latent direction, constructs activation-strength experts around it, and uses gating to reduce the effect. That directly occupies the “latent confirmation-bias state → intervention” narrative.

**Death code:** `DIRECT_MECHANISM_COLLISION`

**Nearest-neighbor warning:** leading instructions, pro/con priors, biased diagnosis hypotheses, single-agent confirmation, or multi-agent majority dominance are all too close unless the natural phenomenon is materially different.

**Resurrection condition:** A distinct confirmation phenomenon with a different causal signature from latent-concept prior skew.

**Reference:** https://openreview.net/pdf?id=MtdNbFQp5O
