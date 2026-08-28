from __future__ import annotations
import argparse,json
from pathlib import Path
from .data import load_scenarios
from .metrics import summarize
from .panel import evaluate_panel
from .run import run

def main()->None:
    ap=argparse.ArgumentParser();sub=ap.add_subparsers(dest="cmd",required=True)
    v=sub.add_parser("validate-data");v.add_argument("--data",required=True)
    r=sub.add_parser("run");r.add_argument("--data",required=True);r.add_argument("--out",required=True);r.add_argument("--config",required=True);r.add_argument("--model",required=True);r.add_argument("--family",required=True);r.add_argument("--revision");r.add_argument("--dtype",default="auto");r.add_argument("--size-b",type=float,required=True);r.add_argument("--batch-size",type=int,default=64)
    s=sub.add_parser("summarize");s.add_argument("--data",required=True);s.add_argument("--results",required=True);s.add_argument("--config",required=True);s.add_argument("--out")
    p=sub.add_parser("panel");p.add_argument("--summary",nargs="+",required=True);p.add_argument("--config",required=True);p.add_argument("--out")
    args=ap.parse_args()
    if args.cmd=="validate-data":print(json.dumps({"validated_scenarios":len(load_scenarios(args.data,require_external_source=True))},indent=2))
    elif args.cmd=="run":run(data_path=args.data,out_path=args.out,config_path=args.config,model_name=args.model,family=args.family,revision=args.revision,dtype=args.dtype,size_b=args.size_b,sequence_batch_size=args.batch_size)
    elif args.cmd=="summarize":
        result=summarize(data_path=args.data,results_path=args.results,config_path=args.config,out_path=args.out);print(json.dumps({k:result[k] for k in ("model_pass","verdict","aggregate")},indent=2,allow_nan=True))
    else:
        cfg=json.loads(Path(args.config).read_text(encoding="utf-8"))["panel_pass"];result=evaluate_panel(args.summary,smoke_min_families=cfg["smoke_min_independent_families"],generality_min_families=cfg["generality_min_independent_families"],generality_panel_size=cfg["generality_panel_size"],required_distinct_sizes_in_one_family=cfg["required_distinct_sizes_in_one_family"])
        if args.out:Path(args.out).write_text(json.dumps(result,indent=2),encoding="utf-8")
        print(json.dumps(result,indent=2))
if __name__=="__main__":main()
