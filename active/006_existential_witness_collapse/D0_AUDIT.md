# 006 D0 Audit — Natural Identity-Redaction Panel

Status: `D0-PASS`
Date: 2026-08-28
Items: `40`
Manual audit: `20 / 20 PASS`

## Natural source choice

D0 uses historical domestic-football Double records rather than toy FOL/staffing vignettes.

Source:
https://en.wikipedia.org/wiki/Double_(association_football)

The source defines a domestic Double as the **same club** winning a country's top-tier league and primary domestic cup in the same season, and provides historical season tables by country.

The frozen panel samples five real Double seasons from each of eight national settings:

- Albania
- Austria
- Belgium
- Croatia
- Denmark
- Finland
- Georgia
- Trinidad and Tobago

Each source record is a real historical positive Double entry. The exact source club is retained only in provenance metadata and is **not shown to the model** in the unknown condition.

## Model-visible transformation

For each real source record, the model receives two independently existentialized facts:

```text
at least one club won the league
at least one club won the cup
```

The model-visible excerpt omits champion identity. Therefore, from the excerpt alone:

```text
same club won both           = logically possible
different clubs won          = logically possible
same club established        = false
different clubs established  = false
```

The task is not to recover the historical champion from world knowledge. Prompts repeatedly ask what is justified by the **current identity-redacted record**.

## Downstream action

The action is an archive/certification operation grounded in the real sports definition:

- `collapse_action`: enter the season in a domestic-Double register as already established;
- `preserve_action`: leave the entry unresolved until champion identities are established.

This avoids risk-preference / efficiency contamination. Under the model-visible unknown record, `preserve_action` is the only justified action.

## Matched controls

Each item includes:

- `unknown`: two existential winner facts, identities absent;
- `paraphrase`: same information in a natural archival summary;
- `same_explicit`: explicitly states one club won both;
- `distinct_explicit`: explicitly states different clubs won the competitions;
- `neutral_control`: same-season contextual information with no identity relation;
- `relation_reminder`: diagnostic only.

The full-source historical fact that the sampled season really was a Double is **not** supplied in the unknown prompt.

## Gold audit

Every frozen item satisfies:

- P witness exists;
- Q witness exists;
- joint witness possible;
- distinct witnesses possible;
- premises do not identify witnesses;
- same-explicit authorizes archive entry;
- distinct-explicit blocks archive entry;
- unknown requires identity check;
- paraphrase preserves identity underdetermination;
- neutral context does not identify the champion.

## Source-memory threat

Because historical country/season labels remain visible, parametric recall is a possible alternative explanation.

Mitigations:

1. the panel deliberately uses mostly old / non-headline domestic seasons across eight countries rather than famous contemporary examples;
2. source club names are withheld in all unknown/paraphrase prompts;
3. the raw-case audit must inspect whether any effect concentrates in recognizably famous seasons/countries;
4. if collapse is driven only by source-memory-prone slices, verdict is `HOLD-SOURCE-MEMORY-ARTIFACT`, not phenotype evidence.

No threshold may be changed to rescue such a result.

## D0 decision

`PASS`

The panel contains 40 externally anchored natural records, has hard identity gold, preserves both identity worlds in the model-visible unknown condition, and provides a unique normative downstream action.

Model execution is authorized only for the frozen first-shot two-family smoke.
