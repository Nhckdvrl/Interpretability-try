#!/usr/bin/env python3
"""Frozen behavioral G0 for NTSB relevance -> causal-role selection.

No mechanistic interpretability is performed. Inputs must come from the official
NTSB manifest prepared by `prepare_g0_population.py`.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import statistics
import urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    out=[]
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip(): out.append(json.loads(line))
    return out


def append_jsonl(path: Path, row: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False)+"\n")


def post_json(url: str, payload: Dict[str, Any], timeout: int) -> Dict[str, Any]:
    req=urllib.request.Request(url, data=json.dumps(payload).encode(),
        headers={"Content-Type":"application/json","Authorization":"Bearer EMPTY"}, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode())


def strip_fence(s: str) -> str:
    s=s.strip()
    s=re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
    s=re.sub(r"\s*```$", "", s)
    return s.strip()


def display_candidates(cs: List[Dict[str,Any]]) -> str:
    return "\n".join(f"F{i+1}: {c['finding_text']}" for i,c in enumerate(cs))


def task_rows(event: Dict[str,Any], task: str) -> Optional[Tuple[str,List[Dict[str,Any]]]]:
    cs=event["candidates"]
    if task=="R":
        ys=[bool(c["gold_relevant"]) for c in cs]
        if not (any(ys) and not all(ys)): return None
        prompt=(
            "You are reviewing an aviation accident investigation.\n\n"
            f"ACCIDENT NARRATIVE:\n{event['input_narrative']}\n\n"
            f"CANDIDATE FINDINGS:\n{display_candidates(cs)}\n\n"
            "Which findings were causally relevant enough to belong in the investigation's "
            "probable-cause statement, either as a cause or as a contributing factor? "
            "Return JSON only: {\"relevant_ids\":[\"F1\",\"F3\"]}."
        )
        return prompt, cs
    rel=[c for c in cs if c.get("gold_legacy_role") in {"C","F"}]
    if not rel: return None
    extra=""
    if task=="O":
        extra=("\n\nOFFICIAL PROBABLE CAUSE NARRATIVE (oracle/interface control):\n"+
               event["hidden_probable_cause_narrative"])
    prompt=(
        "You are reviewing an aviation accident investigation. Every candidate finding below "
        "is already known to be causally relevant. Assign its causal role.\n\n"
        f"ACCIDENT NARRATIVE:\n{event['input_narrative']}\n\n"
        f"CANDIDATE FINDINGS:\n{display_candidates(rel)}{extra}\n\n"
        "For every ID, label it exactly `cause` or `contributing_factor`. "
        "Return JSON only, e.g. {\"roles\":{\"F1\":\"cause\",\"F2\":\"contributing_factor\"}}."
    )
    return prompt, rel


def parse_R(text: str, n: int) -> Tuple[Optional[List[bool]],str]:
    try:
        x=json.loads(strip_fence(text)); ids=x["relevant_ids"]
        if not isinstance(ids,list): raise ValueError
        seen=set()
        for v in ids:
            m=re.fullmatch(r"F(\d+)",str(v).strip(),re.I)
            if not m: raise ValueError
            k=int(m.group(1));
            if not 1<=k<=n: raise ValueError
            seen.add(k)
        return [i in seen for i in range(1,n+1)],"json"
    except Exception: return None,"parse_fail"


def parse_role(text: str, n: int) -> Tuple[Optional[List[str]],str]:
    try:
        x=json.loads(strip_fence(text)); mp=x["roles"]
        if not isinstance(mp,dict): raise ValueError
        out=[]
        for i in range(1,n+1):
            v=str(mp[f"F{i}"]).strip().lower().replace(" ","_").replace("-","_")
            if v not in {"cause","contributing_factor"}: raise ValueError
            out.append(v)
        return out,"json"
    except Exception: return None,"parse_fail"


def run(args: argparse.Namespace) -> None:
    events=read_jsonl(Path(args.manifest)); out=Path(args.output)
    done=set()
    if args.resume and out.exists():
        done={r["request_id"] for r in read_jsonl(out)}
    url=args.base_url.rstrip("/")+"/v1/chat/completions"
    for ev in events:
        built=task_rows(ev,args.task)
        if not built: continue
        prompt,cs=built
        rid=hashlib.sha256(f"{args.family}\0{args.model}\0{args.task}\0{ev['ev_id']}".encode()).hexdigest()[:20]
        if rid in done: continue
        payload={"model":args.model,"temperature":0,"top_p":1,"max_tokens":args.max_tokens,
                 "messages":[{"role":"user","content":prompt}]}
        row={"request_id":rid,"family":args.family,"model":args.model,"task":args.task,
             "ev_id":ev["ev_id"],"candidate_count":len(cs)}
        if args.task=="R": row["gold"]=[bool(c["gold_relevant"]) for c in cs]
        else: row["gold"]=["cause" if c["gold_legacy_role"]=="C" else "contributing_factor" for c in cs]
        try:
            raw=post_json(url,payload,args.timeout); text=raw["choices"][0]["message"]["content"]
            pred,mode=(parse_R(text,len(cs)) if args.task=="R" else parse_role(text,len(cs)))
            row.update(raw_text=text,pred=pred,parse_mode=mode,server_model=raw.get("model"),error=None)
        except Exception as e:
            row.update(raw_text=None,pred=None,parse_mode="request_error",server_model=None,error=repr(e))
        append_jsonl(out,row)


def confusion(rows: Iterable[Dict[str,Any]]) -> Tuple[int,int,int,int,int,int]:
    tp=tn=fp=fn=parsed=total=0
    for r in rows:
        total+=1
        if r.get("pred") is None: continue
        parsed+=1
        if r["task"]=="R": gold=r["gold"]; pred=r["pred"]
        else:
            gold=[x=="cause" for x in r["gold"]]; pred=[x=="cause" for x in r["pred"]]
        for g,p in zip(gold,pred):
            if g and p: tp+=1
            elif (not g) and (not p): tn+=1
            elif (not g) and p: fp+=1
            else: fn+=1
    return tp,tn,fp,fn,parsed,total


def metrics(rows: Iterable[Dict[str,Any]]) -> Dict[str,Any]:
    tp,tn,fp,fn,parsed,total=confusion(rows)
    tpr=tp/(tp+fn) if tp+fn else None; tnr=tn/(tn+fp) if tn+fp else None
    ba=(tpr+tnr)/2 if tpr is not None and tnr is not None else None
    p1=tp/(tp+fp) if tp+fp else 0; r1=tpr or 0; f1p=2*p1*r1/(p1+r1) if p1+r1 else 0
    p0=tn/(tn+fn) if tn+fn else 0; r0=tnr or 0; f1n=2*p0*r0/(p0+r0) if p0+r0 else 0
    return {"parse_coverage":parsed/total if total else 0,"balanced_accuracy":ba,"macro_f1":(f1p+f1n)/2,
            "sensitivity":tpr,"specificity":tnr,"tp":tp,"tn":tn,"fp":fp,"fn":fn,
            "parsed_events":parsed,"total_events":total}


def boot_gap(rrows: List[Dict[str,Any]], srows: List[Dict[str,Any]], seed: int, n: int) -> List[Optional[float]]:
    R={r["ev_id"]:r for r in rrows if r.get("pred") is not None}; S={r["ev_id"]:r for r in srows if r.get("pred") is not None}
    ids=sorted(set(R)&set(S)); rng=random.Random(seed); vals=[]
    if len(ids)<2: return [None,None]
    for _ in range(n):
        samp=[rng.choice(ids) for _ in ids]
        rm=metrics([R[i] for i in samp]); sm=metrics([S[i] for i in samp])
        if rm["balanced_accuracy"] is not None and sm["balanced_accuracy"] is not None:
            vals.append(rm["balanced_accuracy"]-sm["balanced_accuracy"])
    if not vals: return [None,None]
    vals.sort()
    def q(x):
        k=x*(len(vals)-1); a=int(k); b=min(a+1,len(vals)-1); w=k-a; return vals[a]*(1-w)+vals[b]*w
    return [q(.025),q(.975)]


def analyze(args: argparse.Namespace) -> None:
    byfam=defaultdict(dict)
    for spec in args.inputs:
        fam,task,path=spec.split("=",2)
        byfam[fam][task]=read_jsonl(Path(path))
    summary={"contract_date":"2026-08-31","families":{}}
    positives=0
    for fam,ts in sorted(byfam.items()):
        missing={"R","S","O"}-set(ts)
        if missing: raise SystemExit(f"{fam} missing tasks {missing}")
        rm,sm,om=metrics(ts["R"]),metrics(ts["S"]),metrics(ts["O"])
        gap=(rm["balanced_accuracy"]-sm["balanced_accuracy"] if rm["balanced_accuracy"] is not None and sm["balanced_accuracy"] is not None else None)
        ci=boot_gap(ts["R"],ts["S"],args.seed,args.bootstrap)
        pos=bool(rm["parse_coverage"]>=.95 and sm["parse_coverage"]>=.95 and om["parse_coverage"]>=.95 and
                 rm["balanced_accuracy"] is not None and rm["balanced_accuracy"]>=.80 and rm["macro_f1"]>=.75 and
                 sm["balanced_accuracy"] is not None and sm["balanced_accuracy"]<=.65 and sm["macro_f1"]<=.65 and
                 gap is not None and gap>=.15 and om["balanced_accuracy"] is not None and om["balanced_accuracy"]>=.90 and
                 ci[0] is not None and ci[0]>.05)
        positives+=int(pos)
        summary["families"][fam]={"R":rm,"S":sm,"O":om,"R_minus_S_balanced_accuracy":gap,
                                  "event_cluster_bootstrap_gap_95ci":ci,"positive":pos}
    summary["positive_families"]=positives; summary["family_count"]=len(byfam)
    summary["verdict"]=("PASS-TO-N0-N1 (STILL NOT REGISTERED)" if len(byfam)>=3 and positives>=2
                        else "KILL-S0 / NO-BROAD-RELEVANCE-GOOD-ROLE-BAD-PHENOTYPE")
    Path(args.output).write_text(json.dumps(summary,indent=2,ensure_ascii=False),encoding="utf-8")
    print(json.dumps({"positive_families":positives,"family_count":len(byfam),"verdict":summary["verdict"]},indent=2))


def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest="cmd",required=True)
    r=sub.add_parser("run"); r.add_argument("--manifest",required=True); r.add_argument("--task",choices=["R","S","O"],required=True)
    r.add_argument("--family",required=True); r.add_argument("--model",required=True); r.add_argument("--base-url",default="http://127.0.0.1:8000")
    r.add_argument("--output",required=True); r.add_argument("--max-tokens",type=int,default=512); r.add_argument("--timeout",type=int,default=180); r.add_argument("--resume",action="store_true"); r.set_defaults(func=run)
    a=sub.add_parser("analyze"); a.add_argument("--inputs",nargs="+",required=True,help="FAMILY=TASK=path.jsonl"); a.add_argument("--output",required=True); a.add_argument("--seed",type=int,default=20260831); a.add_argument("--bootstrap",type=int,default=5000); a.set_defaults(func=analyze)
    args=p.parse_args(); args.func(args)
if __name__=="__main__": main()
