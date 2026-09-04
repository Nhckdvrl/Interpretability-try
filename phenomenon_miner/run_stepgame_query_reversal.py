#!/usr/bin/env python3
"""Paired test of direct versus reversed queries for one stated relation."""

from __future__ import annotations

import argparse, concurrent.futures, json, random, re, time, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path
from typing import Any
from datasets import load_dataset

LABELS = ["upper-left", "above", "upper-right", "left", "right", "lower-left", "below", "lower-right", "overlap"]
INVERSE = {"upper-left":"lower-right", "above":"below", "upper-right":"lower-left", "left":"right",
           "right":"left", "lower-left":"upper-right", "below":"above", "lower-right":"upper-left", "overlap":"overlap"}

def ents(text: str) -> list[str]:
    return re.findall(r"\b[A-Z]\b", text)

def parse(text: str) -> str:
    t=text.casefold().replace("_","-")
    aliases=[("northwest","upper-left"),("north east","upper-right"),("northeast","upper-right"),
             ("southwest","lower-left"),("south east","lower-right"),("southeast","lower-right"),
             ("north","above"),("south","below"),("east","right"),("west","left"),("same","overlap")]
    # Prefer the first explicit label, since some models then quote the premise in an explanation.
    found=[]
    for label in LABELS:
        m=re.search(rf"(?<!\w){re.escape(label)}(?!\w)",t)
        if m: found.append((m.start(),label))
    for key,val in aliases:
        m=re.search(rf"(?<!\w){re.escape(key)}(?!\w)",t)
        if m: found.append((m.start(),val))
    return min(found)[1] if found else ""

def build(limit:int,seed:int)->list[dict[str,Any]]:
    d=[x for x in load_dataset("ZhengyanShi/StepGame",split="validation") if int(x["k_hop"])==1]
    random.Random(seed).shuffle(d); out=[]
    for i,row in enumerate(d[:limit]):
        story=row["story"][0]; se=ents(story); qe=ents(row["question"])
        if len(set(se))!=2 or len(set(qe))!=2 or set(se)!=set(qe): continue
        a,b=se[0],next(x for x in se if x!=se[0])
        original_order=(qe[0],next(x for x in qe if x!=qe[0]))
        direct_gold=row["label"] if original_order==(a,b) else INVERSE[row["label"]]
        option_order=LABELS[:]; random.Random(f"{seed}:{i}").shuffle(option_order)
        letters="ABCDEFGHI"
        for variant,(x,y),gold in [("direct",(a,b),direct_gold),("reversed",(b,a),INVERSE[direct_gold])]:
            prompt=("Read the single spatial fact and answer the question. Pay attention to the order of the two agents.\n\n"
                    f"Fact: {story}\nQuestion: What is the relation of agent {x} to agent {y}?\n"
                    "Options: "+"; ".join(f"{letters[j]}) {z}" for j,z in enumerate(option_order))+".\n"
                    "Return only the option letter.\nAnswer:")
            out.append({"item_id":i,"variant":variant,"story":story,"query_first":x,"query_second":y,
                        "direct_relation":direct_gold,"gold":gold,"gold_letter":letters[option_order.index(gold)],
                        "option_order":option_order,"prompt":prompt})
    return out

def call(url,model,prompt):
    payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":4,
             "structured_outputs":{"choice":list("ABCDEFGHI")},"chat_template_kwargs":{"enable_thinking":False}}
    req=urllib.request.Request(f"{url.rstrip('/')}/v1/chat/completions",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
    last=None
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req,timeout=180) as r: data=json.load(r)
            m=data["choices"][0]["message"]; return (m.get("content") or m.get("reasoning_content") or "").strip()
        except (urllib.error.URLError,TimeoutError) as e: last=e; time.sleep(2**attempt)
    raise RuntimeError(last)

def run(args):
    reqs=build(args.limit,args.seed)
    def ev(x):
        response=call(args.base_url,args.model,x["prompt"]); letter=response.strip().upper()[:1]
        pred=x["option_order"][ord(letter)-65] if letter in "ABCDEFGHI" else ""
        return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":letter==x["gold_letter"],
          "echoes_direct_relation":x["variant"]=="reversed" and pred==x["direct_relation"],"model":args.model}
    res=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
        fs=[p.submit(ev,x) for x in reqs]
        for n,f in enumerate(concurrent.futures.as_completed(fs),1):
            res.append(f.result())
            if n%200==0: print(f"completed {n}/{len(fs)}",flush=True)
    res.sort(key=lambda x:(x["item_id"],x["variant"])); out=Path(args.out); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf-8") as f:
        for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
    by=defaultdict(list); items=defaultdict(dict)
    for x in res: by[x["variant"]].append(x);items[x["item_id"]][x["variant"]]=x
    paired=[x for x in items.values() if len(x)==2]
    rev=by["reversed"]
    summary={"model":args.model,"n_items":len(paired),"accuracy":{v:sum(x["correct"] for x in xs)/len(xs) for v,xs in by.items()},
      "direct_correct_reversed_wrong":sum(x["direct"]["correct"] and not x["reversed"]["correct"] for x in paired),
      "direct_wrong_reversed_correct":sum(not x["direct"]["correct"] and x["reversed"]["correct"] for x in paired),
      "reversed_echoes_direct_relation":sum(x["echoes_direct_relation"] for x in rev)/len(rev),
      "echo_rate_among_reversed_errors":sum(x["echoes_direct_relation"] for x in rev)/max(1,sum(not x["correct"] for x in rev))}
    out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)

def cli():
    p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
    p.add_argument("--limit",type=int,default=300);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
