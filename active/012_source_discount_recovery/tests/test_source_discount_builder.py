from __future__ import annotations

from pathlib import Path
import collections
import importlib.util
import re
import sys
import pandas as pd

MOD_PATH = Path(__file__).resolve().parents[1] / "data" / "build_natural_d0.py"
spec = importlib.util.spec_from_file_location("build_natural_d0", MOD_PATH)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


def _fixture() -> pd.DataFrame:
    rows=[]
    task=0
    for capability, low, high in [(1,'L1','H1'),(2,'L2','H2')]:
        for i in range(240):
            truth=i%2
            task += 1
            for worker, period in [(high,10),(low,10)]:
                if worker.startswith('H'):
                    correct = (i % 10) != 0
                else:
                    correct = (i % 10) not in (0,1,2)
                answer = truth if correct else 1-truth
                rows.append({'taskId':task,'tasksetId':100+capability,'workerId':worker,
                             'answer':answer,'completeTime':1_000_000+task,'truth':truth,'capability':capability})
            rows.append({'taskId':task,'tasksetId':100+capability,'workerId':f'F{capability}',
                         'answer':truth,'completeTime':2_000_000+task,'truth':truth,'capability':capability})
        # Administrative tasks neither focal annotator ever touched. Real crowdsourcing
        # histories always contain these, and the delay material must be drawn from them.
        for i in range(40):
            task += 1
            for filler in (f'A{capability}', f'B{capability}'):
                rows.append({'taskId':task,'tasksetId':200+capability,'workerId':filler,
                             'answer':i%2,'completeTime':3_000_000+task,'truth':i%2,'capability':capability})
    return pd.DataFrame(rows)


def test_builder_uses_task_disjoint_source_histories_and_global_worker_disjointness(tmp_path: Path):
    df=_fixture(); csv=tmp_path/'fixture.csv'; df.to_csv(csv,index=False)
    rows=mod.build_from_csv(
        str(csv), dataset_name='fixture', license_name='test', source_url='https://example.org',
        domain_col='capability', task_col='taskId', worker_col='workerId', truth_col='truth', answer_col='answer',
        seed=20260829, min_per_class=20, max_pairs_per_cell=2, lr_margin=1.05,
        taskset_col='tasksetId', time_col='completeTime',
    )
    assert len(rows)==2
    workers=[]
    for row in rows:
        workers.extend([row['low_source'],row['high_source']])
        assert 1 < row['low_target_lr'] < row['high_target_lr']
        assert 0 < row['high_other_lr'] < row['low_other_lr'] < 1
        src=row['source']
        assert 1 < src['validation_low_target_lr'] < src['validation_high_target_lr']
        assert 0 < src['validation_high_other_lr'] < src['validation_low_other_lr'] < 1
        assert 'task ' in row['short_delay_text'] and 'completion-time' in row['short_delay_text']
        assert len(row['long_delay_text']) > len(row['short_delay_text'])
        assert row['low_source'] not in row['short_delay_text'] and row['high_source'] not in row['short_delay_text']
        # Delay records must come from tasks the focal annotators never worked on, not
        # merely from other annotators' rows on the focal annotators' own tasks.
        delay_tasks = {int(t) for t in re.findall(r'task (\d+) /', row['long_delay_text'])}
        focal = df[df['workerId'].isin([row['low_source'].split()[-1], row['high_source'].split()[-1]])]
        assert not (delay_tasks & set(focal['taskId'].tolist()))
    assert len(workers)==len(set(workers))


def _multi_pair_fixture() -> pd.DataFrame:
    """Two capabilities, three low- and three high-reliability annotators each."""
    rows = []
    task = 0
    for capability in (1, 2):
        for i in range(300):
            truth = i % 2
            task += 1
            for k in range(3):
                for role, miss in (('H', 12 + k), ('L', 4 + k)):
                    worker = f'{role}{k}_{capability}'
                    answer = truth if (i % miss) != 0 else 1 - truth
                    rows.append({'taskId': task, 'tasksetId': 100 + capability, 'workerId': worker,
                                 'answer': answer, 'completeTime': 1_000_000 + task,
                                 'truth': truth, 'capability': capability})
        for i in range(60):
            task += 1
            rows.append({'taskId': task, 'tasksetId': 200 + capability, 'workerId': f'A{capability}',
                         'answer': i % 2, 'completeTime': 3_000_000 + task,
                         'truth': i % 2, 'capability': capability})
    return pd.DataFrame(rows)


def test_round_robin_caps_scenarios_per_cell_and_balances_domains(tmp_path: Path):
    df = _multi_pair_fixture(); csv = tmp_path / 'multi.csv'; df.to_csv(csv, index=False)
    kwargs = dict(dataset_name='fixture', license_name='test', source_url='https://example.org',
                  domain_col='capability', task_col='taskId', worker_col='workerId',
                  truth_col='truth', answer_col='answer', seed=20260829, min_per_class=20,
                  lr_margin=1.05, taskset_col='tasksetId', time_col='completeTime')
    two = mod.build_from_csv(str(csv), max_pairs_per_cell=2, **kwargs)
    one = mod.build_from_csv(str(csv), max_pairs_per_cell=1, **kwargs)
    # one cell per capability here, so the cap is what sets the bank size
    assert len(one) == 2 and len(two) == 4
    per_domain = collections.Counter(r['domain'] for r in two)
    assert set(per_domain.values()) == {2}, per_domain
    workers = [w for r in two for w in (r['low_source'], r['high_source'])]
    assert len(workers) == len(set(workers))
    # the first pass keeps the strongest pair of each cell ahead of any second pick
    assert [r['scenario_id'] for r in one] == [r['scenario_id'] for r in two[:2]]


def test_excluding_a_domain_drops_it_before_selection(tmp_path: Path):
    df = _multi_pair_fixture(); csv = tmp_path / 'multi.csv'; df.to_csv(csv, index=False)
    kwargs = dict(dataset_name='fixture', license_name='test', source_url='https://example.org',
                  domain_col='capability', task_col='taskId', worker_col='workerId',
                  truth_col='truth', answer_col='answer', seed=20260829, min_per_class=20,
                  lr_margin=1.05, max_pairs_per_cell=2, taskset_col='tasksetId', time_col='completeTime')
    kept = mod.build_from_csv(str(csv), exclude_domains=['1'], **kwargs)
    assert kept and all(r['domain'] == 'capability-2' for r in kept)
