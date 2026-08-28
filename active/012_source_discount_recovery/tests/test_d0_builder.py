import importlib.util
from pathlib import Path

import pandas as pd


def _builder():
    path = Path(__file__).resolve().parents[1] / "data" / "build_natural_d0.py"
    spec = importlib.util.spec_from_file_location("build_012_d0", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def fixture():
    rows = []
    for task in range(80):
        truth = task % 2
        for worker in ("H", "L"):
            if worker == "H":
                ans = truth if task % 10 != 0 else 1 - truth
            else:
                ans = truth if task % 5 not in (0, 1) else 1 - truth
            rows.append({"task": task, "worker": worker, "truth": truth, "answer": ans, "domain": 1})
    return pd.DataFrame(rows)


def test_directional_lr_and_pair_order_survive_split():
    m = _builder()
    df = fixture()
    cal_df, val_df = m.split_by_task(df, task_col="task", seed=7)
    cal = m.worker_stats(cal_df, worker_col="worker", truth_col="truth", answer_col="answer", target_label=1, other_label=0, min_per_class=10)
    val = m.worker_stats(val_df, worker_col="worker", truth_col="truth", answer_col="answer", target_label=1, other_label=0, min_per_class=5)
    pairs = m.stable_worker_pairs(cal, val, min_low_accuracy=.55, min_accuracy_gap=.05, min_lr_margin=1.05)
    assert pairs
    low, high, lowv, highv = pairs[0]
    assert low.worker == "L" and high.worker == "H"
    assert 1 < low.target_lr < high.target_lr
    assert 0 < high.other_lr < low.other_lr < 1
    assert 1 < lowv.target_lr < highv.target_lr
    assert 0 < highv.other_lr < lowv.other_lr < 1


def test_worker_used_once():
    m = _builder()
    df = fixture()
    cal_df, val_df = m.split_by_task(df, task_col="task", seed=7)
    cal = m.worker_stats(cal_df, worker_col="worker", truth_col="truth", answer_col="answer", target_label=1, other_label=0, min_per_class=10)
    val = m.worker_stats(val_df, worker_col="worker", truth_col="truth", answer_col="answer", target_label=1, other_label=0, min_per_class=5)
    chosen = m.choose_disjoint_pairs(m.stable_worker_pairs(cal, val, min_low_accuracy=.55, min_accuracy_gap=.05, min_lr_margin=1.05), limit=5)
    workers = [w.worker for p in chosen for w in p[:2]]
    assert len(workers) == len(set(workers))
