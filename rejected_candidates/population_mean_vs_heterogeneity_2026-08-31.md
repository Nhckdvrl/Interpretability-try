# Rejected Candidate — Population Mean ≠ Human Heterogeneity / Dispersion

Date: 2026-08-31
Status: **TERMINAL REJECTION**

## Natural question

> Can a language model recover what a human population believes or reports on average while failing to represent how much different people vary around that average?

Equivalently: are population central tendency and population heterogeneity distinct computations, or does an LLM collapse a population into a prototypical respondent?

## Why it looked good

This initially looked unusually strong under the current search philosophy:

- the distinction is natural and exists independently of LLMs;
- mean and dispersion/covariance are objectively defined statistics of the same real human population;
- human survey microdata provide direct external gold with no LLM judge and no researcher-created semantic labels;
- the phenomenon would be easy to explain to a broad audience: a model may know the `average person` while erasing the fact that real people disagree;
- a mechanistic decomposition could in principle distinguish a population-prototype estimator from mechanisms that preserve latent subgroup/individual variation.

Recent empirical work also reports strong under-dispersion and homogenization in LLM-based personas, making the phenomenon behaviorally plausible.

## Kill evidence

The title-level scientific object is already directly owned by current mother/successor work.

Most decisively, 2026 `Do participant-matched LLM personas approximate human survey data?` evaluates human-versus-persona correspondence across **construct means, dispersions, individual-level distances, and construct-wise correlations**. Across 91 psychological constructs and 177 matched participants, the paper explicitly reports that model-implied responses can approximate aggregate mean patterns while only modestly reproducing individual differences. It directly quantifies under-dispersion via persona/human SD ratios and treats central tendency and dispersion as separate evaluation objects.

This is not merely a convenient dataset that could support our distinction: the paper's stated scientific conclusion is already the distinction itself.

A second 2026 nearest neighbor, ACL Findings `Beyond Marginal Distributions: A Framework to Evaluate the Representativeness of Demographic-Aligned LLMs`, makes the same broader point at distribution-structure level: matching marginal response distributions can mask failure to reproduce human correlation structure. Thus even broadening from variance to covariance/heterogeneity does not recover title-level novelty.

Other 2025–2026 synthetic-population work explicitly targets response diversity and under-dispersion, further crowding a mechanism-only follow-up.

Therefore an MI paper asking whether hidden states separately encode `population mean` and `population heterogeneity`, or localizing where diversity collapses, would be a direct **mother behavior → mechanism** successor under the repository's N0 rule.

## Death code

`KILL-N0 / HUMAN-DISTRIBUTION-MOTHER-OWNS-MEAN-VS-HETEROGENEITY`

## Nearest-neighbor warning

Do **not** resurrect this as any of the following:

- mean vs variance;
- central tendency vs dispersion;
- average opinion vs disagreement;
- marginal distribution vs covariance/correlation structure;
- population prototype vs individual diversity;
- demographic subgroup mean vs within-group variance;
- persona homogenization / diversity collapse;
- another survey domain, country, demographic prompt, open model, temperature, or sampling method;
- probes/SAEs/patching/steering for response diversity.

These are the same occupied scientific family unless a qualitatively different natural behavioral object is independently established.

## Resurrection condition

Only reconsider if a new natural phenomenon is discovered where the scientifically important failure is **not** representativeness, persona fidelity, survey-distribution matching, under-dispersion, or population heterogeneity itself, and where mean/dispersion behavior is merely a control rather than the title-level object.

Changing the survey, model family, prompting scheme, sampling temperature, subgroup, or MI method is not a resurrection condition.
