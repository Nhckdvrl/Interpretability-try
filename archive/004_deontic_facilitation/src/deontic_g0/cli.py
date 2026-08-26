from __future__ import annotations

import argparse

from .dataset import write_items
from .metrics import summarize
from .run import run_g0


def generate_main() -> None:
    p=argparse.ArgumentParser(description="Generate the frozen matched deontic-facilitation G0 bank")
    p.add_argument("--out",default="data/matched_wason.jsonl"); args=p.parse_args()
    rows=write_items(args.out); print(f"wrote {len(rows)} rows ({len(rows)//2} matched pairs) to {args.out}")


def run_main() -> None:
    p=argparse.ArgumentParser(description="Run frozen matched deontic-facilitation G0")
    p.add_argument("--model",required=True); p.add_argument("--data",default="data/matched_wason.jsonl"); p.add_argument("--out",required=True); p.add_argument("--limit",type=int); p.add_argument("--sequence-batch-size",type=int,default=96); p.add_argument("--dtype",default="auto"); args=p.parse_args()
    run_g0(model_name=args.model,data_path=args.data,out_path=args.out,limit=args.limit,sequence_batch_size=args.sequence_batch_size,dtype=args.dtype)


def summarize_main() -> None:
    p=argparse.ArgumentParser(description="Summarize frozen matched deontic-facilitation G0")
    p.add_argument("--data",default="data/matched_wason.jsonl"); p.add_argument("--results",required=True); p.add_argument("--config",default="configs/g0.json"); p.add_argument("--out",required=True); args=p.parse_args()
    s=summarize(data_path=args.data,results_path=args.results,config_path=args.config,out_path=args.out); a=s["paired"]
    print(f"model_pass={s['model_pass']} delta_acc={a['mean_delta_accuracy']:.4f} delta_p={a['mean_delta_p_gold']:.4f} strong={a['strong_pairs']}")
