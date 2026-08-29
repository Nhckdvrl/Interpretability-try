# Data provenance — 014 Alias Entrainment Transfer

## D0 — frozen discovery bank

`frozen_d0.jsonl` is the historical discovery artefact and is NOT rebuilt.

```text
sha256  c744ae319600fc79e80195ca5b5774b0af6b812714371812e0f61259dae37239
items   300 (150 entities x 2 directions)
strata  opaque_strict 144 / opaque 92 / partial 62 / acronym 2
```

It was built from PopQA by `src/alias_entrainment/build_d0.py`.  The later alias
construct audit and the historical UNREL bug are documented in the project
README; preserving D0 unchanged is part of the provenance.

## D1 — r4 scope correction (canonical build)

Canonical contract: `configs/contract_d1_r4.yaml`.

The previous D1 construction accidentally narrowed the original scientific
question to a person/non-compositional/opaque/one-direction subset.  It was
caught before any D1 model outcome.  r4 restores the intended population:

- all RedirectQA entity types;
- all natural surface-relation strata (compositional / partial / opaque /
  opaque_strict) are retained as labels rather than construction filters;
- all distinct redirect surfaces are retained, not one arbitrary alias per
  entity;
- both valid ordered directions are built;
- Unicode is allowed; there is no pageview or ASCII construction filter;
- `ASSOC_ANY` is the primary strong-association control and
  `ASSOC_SAMETYPE` is a sensitivity control;
- `Typical_Errors` is retained as a diagnostic surface class but cannot by
  itself establish the referential-identity claim.

### Canonical r4 artefacts

```text
data/d1_surface_pairs_r4.json
    <- build_d1_candidates.py

data/d1_wikidata_r4.json
    <- fetch_wikidata.py

data/d1_assoc_candidates_r4.json
    <- build_d1_assoc.py

results/d1_build/cooc_r4/
    <- count_cooccurrence.py
    requires version d1-r4-cooc-v2

data/frozen_d1_r4.jsonl
    <- build_d1_bank.py
```

### Historical / DO NOT CONSUME for r4

The following tracked files were generated under the superseded narrow design
and are kept only because git history/provenance may be useful:

```text
data/d1_candidates.json
data/d1_wikidata.json
data/d1_wikidata_all.json
data/d1_assoc_candidates.json
results/d1_build/cooc/*
```

The committed `results/d1_build/cooc/*` shards were also produced before the
initials sentence-splitting fix (`P. Diddy`, `L. L. Zamenhof`, etc.) and are
therefore invalid even for the historical design.  r4 writes to a new directory
and `build_d1_bank.py` refuses any cooccurrence version other than
`d1-r4-cooc-v2`, so stale shards cannot be mixed accidentally.

The old `data/frozen_d1.jsonl` was deleted when r4 was adopted: it was not a
complete D1 bank (it hard-coded person/opaque_strict/alias->canonical metadata
and did not actually contain the advertised SEMREL/UNREL controls).  The blob is
still recoverable from git history.

### Rebuild order

```bash
python src/alias_entrainment/build_d1_candidates.py
python src/alias_entrainment/fetch_wikidata.py
python src/alias_entrainment/build_d1_assoc.py
python src/alias_entrainment/count_cooccurrence.py --workers 16
python src/alias_entrainment/build_d1_bank.py
python -m pytest tests -q
```
