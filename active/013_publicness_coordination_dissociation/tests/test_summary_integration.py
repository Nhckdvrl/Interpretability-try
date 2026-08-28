from __future__ import annotations

import json
from pathlib import Path

from publicness_coordination_g0.metrics import summarize
from publicness_coordination_g0.prompts import ACTION_TEMPLATES, CAPABILITY_PROBES, PARTICIPANTS, VERSIONS
from test_publicness_coordination_contract import row


def write_data(tmp: Path) -> Path:
    p=tmp/'data.jsonl'; p.write_text(json.dumps(row())+'\n'); return p


def write_cfg(tmp: Path) -> Path:
    cfg=json.loads((Path(__file__).resolve().parents[1] / 'configs' / 'frozen_g0.json').read_text())
    cfg['bootstrap_samples']=200
    cfg['model_pass'].update({
        'min_capability_gated_fraction':1.0,
        'min_action_capable_fraction':1.0,
        'min_action_capable_pairs':1,
        'min_strong_pair_fraction':1.0,
        'min_controls_robust_fraction':1.0,
        'min_positive_domains':1,
        'min_dissociation_ci_lower':0.0,
    })
    p=tmp/'cfg.json'; p.write_text(json.dumps(cfg)); return p


def values(version: str, mode: str):
    table={
        'primary': {'private':.30,'public':.33,'explicit_ck':.50},
        'paraphrase': {'private':.31,'public':.34,'explicit_ck':.50},
        'length': {'private':.29,'public':.32,'explicit_ck':.49},
    }
    if mode=='null':
        table={
            'primary': {'private':.30,'public':.49,'explicit_ck':.50},
            'paraphrase': {'private':.31,'public':.49,'explicit_ck':.50},
            'length': {'private':.29,'public':.48,'explicit_ck':.49},
        }
    return table[version]


def write_results(tmp: Path, *, mode='pass', tom_floor=False) -> Path:
    common={'model':'m','family':'Qwen','revision':None,'size_b':8.0,'requested_dtype':'auto'}
    rows=[]
    for who in PARTICIPANTS:
        for state in ('private','public'):
            for probe in CAPABILITY_PROBES:
                for order in (0,1):
                    p=.95
                    if tom_floor and who=='a' and state=='public' and probe=='knows_other_knows_self_knows_other_received': p=.40
                    rows.append({**common,'kind':'capability_probe','scenario_id':'c1','domain':'coordination','participant':who,'state':state,'probe':probe,'label_order':order,'p_correct':p})
        for version in VERSIONS:
            cell=values(version,mode)
            for state in ('private','public','explicit_ck'):
                for tid,_ in enumerate(ACTION_TEMPLATES):
                    for order in (0,1):
                        rows.append({**common,'kind':'action_readout','scenario_id':'c1','domain':'coordination','participant':who,
                                     'state':state,'version':version,'template_id':tid,'label_order':order,'p_coordinate':cell[state]})
    p=tmp/'results.jsonl'; p.write_text(''.join(json.dumps(r)+'\n' for r in rows)); return p


def test_full_matrix_can_reach_pass_to_panel(tmp_path: Path):
    out=summarize(data_path=str(write_data(tmp_path)),results_path=str(write_results(tmp_path)),config_path=str(write_cfg(tmp_path)))
    assert out['verdict']=='PASS-TO-PANEL'
    assert out['model_pass'] is True
    assert out['aggregate']['action_capable_pairs']==1


def test_full_matrix_correct_publicness_use_is_hard_null(tmp_path: Path):
    out=summarize(data_path=str(write_data(tmp_path)),results_path=str(write_results(tmp_path,mode='null')),config_path=str(write_cfg(tmp_path)))
    assert out['verdict']=='HARD-KILL-NO-PUBLICNESS-COORDINATION-DISSOCIATION'
    assert out['model_pass'] is False


def test_full_matrix_recursive_tom_floor_cannot_count(tmp_path: Path):
    out=summarize(data_path=str(write_data(tmp_path)),results_path=str(write_results(tmp_path,tom_floor=True)),config_path=str(write_cfg(tmp_path)))
    assert out['verdict']=='HARD-KILL-PUBLICNESS-TOM-CAPABILITY-FLOOR'
    assert out['model_pass'] is False
