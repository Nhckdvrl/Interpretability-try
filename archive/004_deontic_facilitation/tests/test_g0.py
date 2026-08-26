from __future__ import annotations

import json
from pathlib import Path
import pytest

from deontic_g0.dataset import CARD_PERMUTATIONS, FORMS, MODALS, canonical_pair, generate_items, load_items, permute_item, write_items
from deontic_g0.prompts import CANDIDATES, TEMPLATES, build_prompt


def test_generator_is_true_matched_design() -> None:
    rows=generate_items(); assert len(rows)==64
    pair_ids=sorted({x.pair_id for x in rows}); assert len(pair_ids)==32
    for pair_id in pair_ids:
        pair=[x for x in rows if x.pair_id==pair_id]; assert {x.modal for x in pair}==set(MODALS)
        e=next(x for x in pair if x.modal=="epistemic"); d=next(x for x in pair if x.modal=="deontic")
        assert e.cards==d.cards and e.gold==d.gold and e.form==d.form and e.frame_id==d.frame_id and e.rule!=d.rule
    assert {f:len({x.pair_id for x in rows if x.form==f}) for f in FORMS}=={f:8 for f in FORMS}


def test_candidates_are_all_six_unordered_pairs() -> None:
    assert CANDIDATES==("1,2","1,3","1,4","2,3","2,4","3,4")


def test_card_rotation_preserves_gold_semantics() -> None:
    item=generate_items()[0]; seen={i:set() for i in range(1,5)}
    for perm in CARD_PERMUTATIONS:
        shown=permute_item(item,perm); assert canonical_pair(shown.gold) in CANDIDATES
        for displayed,orig_zero in enumerate(perm,start=1): seen[orig_zero+1].add(displayed)
    assert all(v=={1,2,3,4} for v in seen.values())


def test_instruction_itself_does_not_inject_deontic_cues() -> None:
    joined=" ".join(TEMPLATES).lower()
    for cue in ("violat","oblig","prohibit","permission"): assert cue not in joined


def test_instruction_defines_two_sided_card_structure() -> None:
    for template in TEMPLATES:
        text=template.lower()
        assert "condition-side" in text
        assert "outcome-side" in text
        assert "hidden" in text
        assert "turn" in text


def test_roundtrip_and_prompt(tmp_path: Path) -> None:
    path=tmp_path/"matched.jsonl"; write_items(path); rows=load_items(path,strict=True); assert len(rows)==64
    p=build_prompt(rows[0],0); assert "exactly one pair" in p.lower() and "1." in p


def test_loader_rejects_broken_pair(tmp_path: Path) -> None:
    path=tmp_path/"matched.jsonl"; write_items(path)
    objs=[json.loads(x) for x in path.read_text(encoding="utf-8").splitlines()]; objs[1]["cards"][0]="BROKEN"
    path.write_text("\n".join(json.dumps(x) for x in objs)+"\n",encoding="utf-8")
    with pytest.raises(ValueError,match="structurally matched"): load_items(path,strict=True)
