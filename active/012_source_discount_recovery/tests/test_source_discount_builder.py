from __future__ import annotations

from pathlib import Path
import importlib.util
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
    return pd.DataFrame(rows)


def test_builder_uses_task_disjoint_source_histories_and_global_worker_disjointness(tmp_path: Path):
    df=_fixture(); csv=tmp_path/'fixture.csv'; df.to_csv(csv,index=False)
    rows=mod.build_from_csv(
        str(csv), dataset_name='fixture', license_name='test', source_url='https://example.org',
        domain_col='capability', task_col='taskId', worker_col='workerId', truth_col='truth', answer_col='answer',
        seed=20260829, min_per_class=20, pairs_per_domain=2,
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
    assert len(workers)==len(set(workers))
