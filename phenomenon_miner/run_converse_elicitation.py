#!/usr/bin/env python3
"""Test whether models possess converse knowledge but fail to deploy it in QA."""
from __future__ import annotations
import argparse,concurrent.futures,json,random,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path

REL={"above":"above","below":"below","left":"to the left of","right":"to the right of",
 "upper-left":"above and to the left of","upper-right":"above and to the right of",
 "lower-left":"below and to the left of","lower-right":"below and to the right of"}
INV={"above":"below","below":"above","left":"right","right":"left","upper-left":"lower-right",
 "upper-right":"lower-left","lower-left":"upper-right","lower-right":"upper-left"}
LABELS=list(REL);LETTERS="ABCDEFGH";NAMES=["Alice","Bob","Carol","David","Emma","Frank","Grace","Henry"]

def build(per_relation,seed):
 rng=random.Random(seed);out=[];idx=0
 for gold in LABELS:
  for _ in range(per_relation):
   a,b=rng.sample(NAMES,2); fact=f"{b} is {REL[INV[gold]]} {a}."
   order=LABELS[:];rng.shuffle(order);gl=LETTERS[order.index(gold)]
   options="; ".join(f"{LETTERS[j]}) {r}" for j,r in enumerate(order))
   stems={
    "ordinary_qa":f"Question: What is the relation of {a} to {b}?",
    "rewrite_blank":f"Rewrite the fact without changing its meaning, beginning with {a}: '{a} is [RELATION] {b}.' Which relation fills the blank?",
    "explicit_role_swap":f"Swap the subject and object of the fact and use the converse spatial relation. What is the resulting relation of {a} to {b}?",
   }
   for variant,stem in stems.items():
    prompt=(f"Fact: {fact}\n{stem}\nOptions: {options}.\nReturn only the option letter.\nAnswer:")
    out.append({"item_id":idx,"variant":variant,"gold":gold,"gold_letter":gl,"option_order":order,"fact":fact,"a":a,"b":b,"prompt":prompt})
   idx+=1
 return out

def call(url,model,prompt):
 payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":4,
          "structured_outputs":{"choice":list(LETTERS)},"chat_template_kwargs":{"enable_thinking":False}}
 req=urllib.request.Request(f"{url.rstrip('/')}/v1/chat/completions",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"});last=None
 for n in range(5):
  try:
   with urllib.request.urlopen(req,timeout=180) as r:data=json.load(r)
   m=data["choices"][0]["message"];return (m.get("content") or m.get("reasoning_content") or "").strip()
  except (urllib.error.URLError,TimeoutError) as e:last=e;time.sleep(2**n)
 raise RuntimeError(last)
def run(args):
 reqs=build(args.per_relation,args.seed)
 def ev(x):
  response=call(args.base_url,args.model,x["prompt"]);letter=response.strip().upper()[:1]
  pred=x["option_order"][ord(letter)-65] if letter in LETTERS else ""
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":letter==x["gold_letter"],"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  fs=[p.submit(ev,x) for x in reqs]
  for n,f in enumerate(concurrent.futures.as_completed(fs),1):
   res.append(f.result())
   if n%300==0:print(f"completed {n}/{len(fs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["variant"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);br=defaultdict(list);items=defaultdict(dict)
 for x in res:by[x["variant"]].append(x["correct"]);br[(x["variant"],x["gold"])].append(x["correct"]);items[x["item_id"]][x["variant"]]=x["correct"]
 summary={"model":args.model,"n_items":len(items),"accuracy":{k:sum(v)/len(v) for k,v in by.items()},
  "cardinal_accuracy":{k:sum(x for r in ["above","below","left","right"] for x in br[(k,r)])/(4*args.per_relation) for k in by},
  "accuracy_by_relation":{k:{r:sum(br[(k,r)])/len(br[(k,r)]) for r in LABELS} for k in by},
  "qa_wrong_rewrite_correct":sum((not x["ordinary_qa"]) and x["rewrite_blank"] for x in items.values()),
  "qa_wrong_explicit_swap_correct":sum((not x["ordinary_qa"]) and x["explicit_role_swap"] for x in items.values())}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--per-relation",type=int,default=25);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
