# Prototype vs Exemplar Categorization — Rejection Record

```yaml
question: When an LLM learns/generalizes a category, does it rely on an abstract category representation/prototype or concrete stored exemplars?
mother: category-learning / prototypicality literature
semantic_aliases:
  - prototype vs exemplar category learning in LLMs
  - abstract category representation vs concrete instance memory
  - category abstraction vs exemplar retrieval
  - prototype abstraction in language models
  - exemplar-based vs abstraction-based concept learning
what_was_reviewed: classic 5/4 and 5/5 category-learning theory; 2026 LLM prototypicality work; EACL 2026 Best Paper Humans and transformer LMs: Abstraction drives language learning; July 2026 follow-up Exemplars in Disguise
kill_class: F8
kill_evidence: EACL 2026 Best Paper Jian & Manning already asks how transformer LMs learn linguistic categories by explicitly contrasting abstract feature-based and concrete exemplar-based accounts, and concludes that abstraction plays a key role. A July 2026 follow-up, Exemplars in Disguise, directly contests whether their abstraction-first signature is diagnostic by showing pure exemplar learners can mimic it. Thus the concept-level abstraction-vs-exemplar question is already an active, explicitly owned LLM scientific debate. Recasting abstract feature representations as prototypes, moving from training trajectories to in-context category learning, or adding causal MI is not a wide enough N2 delta.
nearest_neighbor_warning: Do not revive as prototype-vs-exemplar circuits, prototype abstraction vs exemplar memory, category centroid vs instance retrieval, or ICL category learning by changing stimuli, model family, or measurement method.
resurrection_condition: A categorization question with an orthogonal scientific axis not reducible to abstraction/prototype versus exemplar accounts, and with theory-diagnostic predictions not already central to Jian & Manning and its follow-ups.
```

Key collision: Jian & Manning, EACL 2026 Best Paper, `Humans and transformer LMs: Abstraction drives language learning` (https://aclanthology.org/2026.eacl-long.32/). The abstract itself frames abstract feature-based versus concrete exemplar-based accounts. A July 2026 paper `Exemplars in Disguise: Pure Exemplar Models Mimic Abstraction-First Learning` directly reopens the same diagnostic question.
