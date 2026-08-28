from __future__ import annotations
import argparse, json
from .run import run
from .metrics import summarize

def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--data", required=True); r.add_argument("--out", required=True)
    r.add_argument("--model", required=True); r.add_argument("--family", required=True); r.add_argument("--revision")
    r.add_argument("--dtype", default="auto"); r.add_argument("--batch-size", type=int, default=64)
    s = sub.add_parser("summarize")
    s.add_argument("--data", required=True); s.add_argument("--results", required=True)
    s.add_argument("--config", required=True); s.add_argument("--out")
    args = ap.parse_args()
    if args.cmd == "run":
        run(data_path=args.data, out_path=args.out, model_name=args.model, family=args.family,
            revision=args.revision, dtype=args.dtype, sequence_batch_size=args.batch_size)
    else:
        x = summarize(data_path=args.data, results_path=args.results,
                      config_path=args.config, out_path=args.out)
        print(json.dumps({k: x[k] for k in ("model_pass", "verdict", "aggregate")},
                         ensure_ascii=False, indent=2, allow_nan=True))

if __name__ == "__main__":
    main()
