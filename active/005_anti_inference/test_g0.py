import importlib.util
from pathlib import Path
P=Path(__file__).with_name('g0.py');spec=importlib.util.spec_from_file_location('g0',P);g0=importlib.util.module_from_spec(spec);spec.loader.exec_module(g0)

def test_generate_complete_triplets():
    rows=g0.generate(); assert len(rows)==576
    ids={r['family_id'] for r in rows}; assert len(ids)==192
    for fid in list(ids)[:20]:
        x=[r for r in rows if r['family_id']==fid]
        assert {r['condition'] for r in x}=={'direct','inferred','inferred_explicit'}
        assert len({r['target'] for r in x})==1 and len({r['reliability'] for r in x})==1

def test_prompt_has_matched_reliability():
    rows=g0.generate(); fid=rows[0]['family_id']; x=[r for r in rows if r['family_id']==fid]
    for r in x:
        c,q=g0.prompts(r,0)
        assert f"{r['reliability']}%" in q
        assert r['target'] in q and r['target'] in c

def test_probability_candidates_fixed():
    assert tuple(g0.PROB_CANDS)==('50%','60%','70%','80%','90%','95%','99%')

def test_variants_change_order_not_candidate_set():
    r=g0.generate()[0]
    qs=[g0.prompts(r,v)[1] for v in range(3)]
    assert len(set(qs))==3
    for q in qs:
        for c in g0.PROB_CANDS: assert c in q

def test_bootstrap_constant():
    assert g0.bootstrap([5.0]*12)==[5.0,5.0]
