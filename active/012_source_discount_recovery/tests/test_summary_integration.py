from __future__ import annotations

import json
from pathlib import Path
from statistics import mean

import pytest

from source_discount_g0.metrics import summarize
from source_discount_g0.prompts import CONDITIONS, DIRECTIONS, MEMORY_PROBES, READOUT_TEMPLATES, SOURCES, SUPPORT_PROBES
from test_source_discount_contract import row


def write_data(tmp: Path) -> Path:
    p = tmp / "data.jsonl"
    p.write_text(json.dumps(row()) + "\n")
    return p


def write_cfg(tmp: Path) -> Path:
    cfg = json.loads((Path(__file__).resolve().parents[1] / 'configs' / 'frozen_g0.json').read_text())
    cfg['bootstrap_samples'] = 200
    cfg['model_pass'].update({
        'min_support_gated_fraction': 1.0,
        'min_memory_gated_fraction': 1.0,
        'min_weighting_capable_fraction': 1.0,
        'min_weighting_capable_pairs': 1,
        'min_strong_pair_fraction': 1.0,
        'min_recovery_pair_fraction': 1.0,
        'min_reinstatement_pair_fraction': 1.0,
        'min_positive_domains': 1,
        'min_gap_shrink_ci_lower': 0.0,
        'min_primary_cell_size': 1,
        'min_primary_cells': 1,
    })
    p = tmp / 'cfg.json'; p.write_text(json.dumps(cfg)); return p


def raw_value(direction: str, condition: str, mode: str) -> float:
    base = .50
    values = {
        'no_message_immediate': base, 'no_message_short': base, 'no_message_long': base,
        'low_immediate': .58, 'high_immediate': .70,
        'low_short': .61, 'high_short': .69,
        'low_long': .64, 'high_long': .69,
        'low_long_reinstated': .58, 'high_long_reinstated': .70,
        'low_long_length': .64, 'high_long_length': .69,
    }
    if mode == 'null':
        values.update({
            'low_short': .58, 'high_short': .70,
            'low_long': .58, 'high_long': .70,
            'low_long_reinstated': .58, 'high_long_reinstated': .70,
            'low_long_length': .58, 'high_long_length': .70,
        })
    x = values[condition]
    return x if direction == 'supports_target' else 1.0 - x


def write_results(tmp: Path, *, mode: str = 'pass', memory_floor: bool = False) -> Path:
    rows = []
    common = {'model':'m','family':'Qwen','revision':None,'size_b':8.0,'requested_dtype':'auto'}
    for direction in DIRECTIONS:
        for probe in SUPPORT_PROBES:
            for order in (0,1):
                rows.append({**common,'kind':'support_probe','scenario_id':'s1','domain':'diagnostics','direction':direction,'probe':probe,'label_order':order,'p_correct':.95})
        for source in SOURCES:
            for delay in ('short','long'):
                for probe in MEMORY_PROBES:
                    for order in (0,1):
                        p=.95
                        if memory_floor and source=='low' and delay=='short' and probe=='source_identity': p=.40
                        rows.append({**common,'kind':'memory_probe','scenario_id':'s1','domain':'diagnostics','direction':direction,'source':source,'delay':delay,'probe':probe,'label_order':order,'p_correct':p})
        for tid,(kind,_) in enumerate(READOUT_TEMPLATES):
            for condition in CONDITIONS:
                for order in (0,1):
                    rows.append({**common,'kind':'readout','scenario_id':'s1','domain':'diagnostics','direction':direction,
                                 'condition':condition,'template_id':tid,'template_kind':kind,'label_order':order,
                                 'p_target':raw_value(direction,condition,mode)})
    p=tmp/'results.jsonl'; p.write_text(''.join(json.dumps(r)+'\n' for r in rows)); return p


def test_full_matrix_can_reach_pass_to_panel(tmp_path: Path):
    out = summarize(data_path=str(write_data(tmp_path)), results_path=str(write_results(tmp_path)), config_path=str(write_cfg(tmp_path)))
    assert out['verdict'] == 'PASS-TO-PANEL'
    assert out['model_pass'] is True
    assert out['aggregate']['weighting_capable_pairs'] == 1


def test_full_matrix_normal_discount_without_recovery_is_hard_kill(tmp_path: Path):
    out = summarize(data_path=str(write_data(tmp_path)), results_path=str(write_results(tmp_path, mode='null')), config_path=str(write_cfg(tmp_path)))
    assert out['verdict'] == 'HARD-KILL-NO-SOURCE-DISCOUNT-RECOVERY'
    assert out['model_pass'] is False


def test_full_matrix_memory_floor_cannot_masquerade_as_recovery(tmp_path: Path):
    out = summarize(data_path=str(write_data(tmp_path)), results_path=str(write_results(tmp_path, memory_floor=True)), config_path=str(write_cfg(tmp_path)))
    assert out['verdict'] == 'HARD-KILL-SOURCE-MEMORY-CAPABILITY-FLOOR'
    assert out['model_pass'] is False


def write_stratified(tmp: Path, spec: list[tuple[str, int, str]]) -> tuple[Path, Path]:
    """spec: (cell_id, scenario count, result mode) per cell."""
    data, results = [], []
    common = {'model': 'm', 'family': 'Qwen', 'revision': None, 'size_b': 8.0, 'requested_dtype': 'auto'}
    for cell, count, mode in spec:
        domain = cell.split(':')[0]
        for i in range(count):
            sid = f'{cell}-{i}'
            record = row()
            record.update({'scenario_id': sid, 'domain': domain, 'cell_id': cell})
            data.append(record)
            tag = {**common, 'scenario_id': sid, 'domain': domain}
            for direction in DIRECTIONS:
                for probe in SUPPORT_PROBES:
                    for order in (0, 1):
                        results.append({**tag, 'kind': 'support_probe', 'direction': direction,
                                        'probe': probe, 'label_order': order, 'p_correct': .95})
                for source in SOURCES:
                    for delay in ('short', 'long'):
                        for probe in MEMORY_PROBES:
                            for order in (0, 1):
                                results.append({**tag, 'kind': 'memory_probe', 'direction': direction,
                                                'source': source, 'delay': delay, 'probe': probe,
                                                'label_order': order, 'p_correct': .95})
                for tid, (kind, _) in enumerate(READOUT_TEMPLATES):
                    for condition in CONDITIONS:
                        for order in (0, 1):
                            results.append({**tag, 'kind': 'readout', 'direction': direction,
                                            'condition': condition, 'template_id': tid,
                                            'template_kind': kind, 'label_order': order,
                                            'p_target': raw_value(direction, condition, mode)})
    dp = tmp / 'strat_data.jsonl'; dp.write_text(''.join(json.dumps(r) + '\n' for r in data))
    rp = tmp / 'strat_results.jsonl'; rp.write_text(''.join(json.dumps(r) + '\n' for r in results))
    return dp, rp


def strat_cfg(tmp: Path) -> Path:
    cfg = json.loads(write_cfg(tmp).read_text())
    cfg['model_pass'].update({'min_primary_cell_size': 5, 'min_primary_cells': 1})
    p = tmp / 'strat_cfg.json'; p.write_text(json.dumps(cfg)); return p


def test_undersized_cells_are_secondary_only_and_cannot_move_the_verdict(tmp_path: Path):
    cfg = strat_cfg(tmp_path)
    big = ('d1:0v1', 5, 'pass')
    dp, rp = write_stratified(tmp_path, [big, ('d2:0v1', 1, 'null')])
    out = summarize(data_path=str(dp), results_path=str(rp), config_path=str(cfg))
    agg = out['aggregate']
    assert agg['primary_cells'] == ['d1:0v1']
    assert agg['secondary_cells'] == ['d2:0v1']
    assert sorted(agg['cell_means']) == ['d1:0v1']
    assert agg['primary_scenarios'] == 5 and agg['secondary_scenarios'] == 1
    assert out['verdict'] == 'PASS-TO-PANEL' and out['model_pass'] is True

    # the same primary set with the undersized cell flipped the other way is identical
    dp2, rp2 = write_stratified(tmp_path, [big, ('d2:0v1', 1, 'pass')])
    flipped = summarize(data_path=str(dp2), results_path=str(rp2), config_path=str(cfg))
    assert flipped['verdict'] == out['verdict']
    assert flipped['model_pass'] == out['model_pass']
    assert flipped['aggregate']['cell_mean_gap_shrink'] == agg['cell_mean_gap_shrink']
    assert flipped['aggregate']['gap_shrink_ci95'] == agg['gap_shrink_ci95']
    # but the descriptive full-bank fraction does move, and is reported separately
    assert flipped['aggregate']['strong_pair_fraction'] != agg['strong_pair_fraction']


def test_cells_are_equally_weighted_regardless_of_how_many_pairs_they_hold(tmp_path: Path):
    cfg = strat_cfg(tmp_path)
    dp, rp = write_stratified(tmp_path, [('d1:0v1', 15, 'pass'), ('d1:0v2', 5, 'null')])
    out = summarize(data_path=str(dp), results_path=str(rp), config_path=str(cfg))
    means = out['aggregate']['cell_means']
    assert sorted(means) == ['d1:0v1', 'd1:0v2']
    assert out['aggregate']['cell_mean_gap_shrink'] == pytest.approx(mean(means.values()))
    # a pair-level mean would have been dragged three-to-one toward the larger cell
    assert out['aggregate']['cell_mean_gap_shrink'] != pytest.approx(out['aggregate']['mean_gap_shrink'])
