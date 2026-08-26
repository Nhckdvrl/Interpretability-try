import importlib.util
from pathlib import Path

P=Path(__file__).with_name('g0.py')
spec=importlib.util.spec_from_file_location('g0',P); g0=importlib.util.module_from_spec(spec); spec.loader.exec_module(g0)

def test_generate_size_and_pairing():
    rows=g0.generate(); assert len(rows)==128
    ids={r['item_id'] for r in rows}; assert len(ids)==64
    for iid in ids:
        pair=[r for r in rows if r['item_id']==iid]
        assert {r['framing'] for r in pair}=={'descriptive','deontic'}
        assert pair[0]['cards']==pair[1]['cards']
        assert pair[0]['gold_semantic']==pair[1]['gold_semantic']==[0,3]

def test_all_permutations_preserve_gold():
    r=g0.generate()[0]
    seen=set()
    from itertools import permutations
    for p in permutations(range(4)):
        _,gold=g0.render(r,p,0); seen.add(gold)
        assert gold in g0.CANDIDATES
    assert len(seen)==6

def test_prompt_diff_is_rule_only_for_matched_item():
    a,b=g0.generate()[0:2]
    assert a['item_id']==b['item_id'] and a['cards']==b['cards']
    pa,_=g0.render(a,(0,1,2,3),0); pb,_=g0.render(b,(0,1,2,3),0)
    assert pa!=pb
    assert a['rule'] in pa and b['rule'] in pb

def test_bootstrap_constant():
    assert g0.bootstrap([0.2]*10)==[0.2,0.2]

def test_candidates_cover_all_pairs():
    assert set(g0.CANDIDATES)=={'1,2','1,3','1,4','2,3','2,4','3,4'}
