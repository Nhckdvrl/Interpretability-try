# 026 source and target audit

Date: 2026-08-31
Verdict: `PARK-DATA / NO MODEL CALL`

## Required fields

```yaml
natural_hypotheses: partial_pass
source_provenance: pass_for_candidate_sources
plausibility_target: not_independently_available_at_required_quality
testability_target: not_independently_available_at_required_quality
no_llm_judge_as_primary_gold: fail_for_only_source_with_both_axes
cross_axis_support: not_auditable
restriction_budget: would_be_excessive
anti_narrowing_stop: triggered
```

## 1. ACL 2026 mother / MOF

*Experiments or Outcomes? Probing Scientific Feasibility in Large Language
Models* uses 615 MATTER-OF-FACT instances. The paper's structured task has one
claim-level `FEASIBLE/INFEASIBLE` gold label and optional experiments/outcomes
extracted from source papers. This supports natural hypotheses, source evidence,
and a composite feasibility target.

It does not provide independent plausibility and testability labels. Treating
the binary feasibility label as plausibility and experiment presence as
testability would define the targets from different observables and would not
yield the required 2×2.

The paper advertises `https://github.com/mohammadi-ali/scify`, but that repository
returned `Repository not found` during this audit. This access issue is
secondary: the published schema itself lacks the two target axes.

## 2. NAACL 2025 materials artifact

Repository:
`shri071/Hypothesis-Generation-for-Materials-Discovery-and-Design-Using-Goal-Driven-and-Constraint-Guided-LLM`

Frozen audit commit:
`923a842db8ffacbe7464cebea93fd1dfeba92ad8`

Artifact inventory:

- `Materials Discovery & Design Dataset.xlsx`: 51 rows; columns are Title,
  Goal Statement, Constraints, Materials, Methods, and KG Graph Data.
- `Evaluation_of_Hypotheses.xlsx`: 24 rows and six evaluation columns plus
  paper name.
- evaluation workbook SHA-256:
  `fb71355cb413116d3c0c77ccb1fc4f1702922ff4d7f14452128fceb436df50d9`.

The quality prose contains `Scientific Plausibility`, `Testability`, and
`Feasibility and Scalability` ratings in all 24 rows. However, every evaluation
column is explicitly labeled `Evaluation by o1-preview`, and the repository
README states that OpenAI o1-preview is the Evaluation Agent. These are model
judgments, not expert primary gold. The source is also materials-only and too
small to support the broad multi-domain title.

## 3. SFBench

SFBench supplies 197 de-novo materials-science claims with subject-matter-expert
five-point feasibility ratings and explanations. It passes expert provenance
for a composite feasibility label, but it exposes neither an independent
testability score nor a matched experiment-design target. Deriving testability
from explanations would require new annotation.

## 4. Clinical hypothesis-quality instrument

Jing et al. develop a clinical-hypothesis evaluation instrument containing
validity and testability among ten dimensions. Experimental evaluation 1 used
19 hypotheses; evaluation 2 sampled 30, of which 17 passed the validity screen.
Only half of the ten items reached moderate ICC in evaluation 2, and the final
brief instrument retained validity, significance, and feasibility—not
testability.

The public associated files are evaluation instruments/method summaries rather
than a broad row-level corpus with reliable independent plausibility and
testability gold. It is a small single-domain validation study, not a viable
primary bank.

## Cross-axis audit

No audited source permits a legitimate P+/P- × T+/T- count. The only artifact
with both named fields uses an LLM evaluator. The expert sources provide a
composite feasibility/validity signal without a separately reliable
testability target. Consequently, any current 2×2 would require one of the
forbidden moves:

1. have this project or another LLM invent the labels;
2. equate plausibility with feasibility and testability with experiment length
   or presence;
3. shrink the title to 24 model-scored materials hypotheses;
4. hand-select illustrative quadrants.

## Unlock condition

Reopen only when a public source (or a prospectively collected expert study)
provides:

- natural hypothesis text and source/domain provenance;
- independently worded plausibility and discriminating-testability questions;
- multiple human/SME judgments per axis with reported reliability;
- auditable support in all four cross-axis cells without outcome-conditioned
  filtering;
- at least two scientific domains, or a frozen second-domain confirmation;
- experiment descriptions sufficient to distinguish falsifiability from cost
  or ease of execution.

Until then, data do not support the title-level scientific object.

## Sources

- https://aclanthology.org/2026.acl-short.50/
- https://github.com/shri071/Hypothesis-Generation-for-Materials-Discovery-and-Design-Using-Goal-Driven-and-Constraint-Guided-LLM
- https://arxiv.org/abs/2606.29630
- https://pmc.ncbi.nlm.nih.gov/articles/PMC9882446/
