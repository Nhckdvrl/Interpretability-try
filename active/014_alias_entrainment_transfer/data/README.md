# D0 — frozen item bank

`frozen_d0.jsonl` is force-tracked past the repository root `.gitignore` (`data/`),
because it is the provenance artefact whose sha256 the audit registry records:

```text
sha256  c744ae319600fc79e80195ca5b5774b0af6b812714371812e0f61259dae37239
items   300 (150 entities x 2 directions)
strata  opaque_strict 144 / opaque 92 / partial 62 / acronym 2
```

It is built entirely from one public artefact — [PopQA](https://huggingface.co/datasets/akariasai/PopQA),
which ships the Wikidata aliases (CC0) and Wikipedia pageview popularity for every
entity it uses — by `src/alias_entrainment/build_d0.py`. Nothing in it is synthetic
except the two semantically bleached insertion frames, which are the minimal causal
contrast and carry no effect size.

Rebuild and verify:

```bash
python src/alias_entrainment/build_d0.py --out data/frozen_d0.jsonl
sha256sum data/frozen_d0.jsonl
python -m pytest tests -q      # 9 invariants, incl. target-string-absent in ALIAS
```
