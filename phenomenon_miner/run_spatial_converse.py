#!/usr/bin/env python3
"""Balanced scan of logically equivalent converse descriptions.

For example, "Alice is above Bob" and "Bob is below Alice" describe exactly
the same state.  The query and gold answer are held fixed across conditions.
"""
from __future__ import annotations
import argparse, concurrent.futures, json, random, re, time, urllib.error, urllib.request
from collections import defaultdict
from pathlib import Path

REL={"above":"above","below":"below","left":"to the left of","right":"to the right of",
     "upper-left":"above and to the left of","upper-right":"above and to the right of",
     "lower-left":"below and to the left of","lower-right":"below and to the right of"}
INV={"above":"below","below":"above","left":"right","right":"left","upper-left":"lower-right",
     "upper-right":"lower-left","lower-left":"upper-right","lower-right":"upper-left"}
LABELS=list(REL)
NAMES=["Alice","Bob","Carol","David","Emma","Frank","Grace","Henry","Iris","James","Karen","Leo"]

def sentence(a,r,b): return f"{a} is {REL[r]} {b}."
def parse(text):
 t=text.casefold().replace("_","-"); hits=[]
 for l in LABELS:
  m=re.search(rf"(?<!\w){re.escape(l)}(?!\w)",t)
  if m:hits.append((m.start(),l))
 for key,val in [("northwest","upper-left"),("northeast","upper-right"),("southwest","lower-left"),("southeast","lower-right"),("north","above"),("south","below"),("west","left"),("east","right")]:
  m=re.search(rf"(?<!\w){key}(?!\w)",t)
  if m:hits.append((m.start(),val))
 return min(hits)[1] if hits else ""

def build(per_relation,seed):
 rng=random.Random(seed);out=[];i=0
 for gold in LABELS:
  for _ in range(per_relation):
   a,b=rng.sample(NAMES,2); direct=sentence(a,gold,b); converse=sentence(b,INV[gold],a)
   c,d=rng.sample([x for x in NAMES if x not in (a,b)],2)
   same_direction=f"Relative to {b}, {a} is {REL[gold]}."
   irrelevant=sentence(c,INV[gold],d)
   option_order=LABELS[:];rng.shuffle(option_order)
   letters="ABCDEFGH";gold_letter=letters[option_order.index(gold)]
   variants={"direct_only":[direct],"converse_only":[converse],"direct_then_converse":[direct,converse],
             "converse_then_direct":[converse,direct],"direct_duplicate":[direct,direct],
             "direct_then_same_direction":[direct,same_direction],"direct_then_irrelevant":[direct,irrelevant]}
   for variant,facts in variants.items():
    prompt=("The following spatial statements are mutually consistent. Answer about the named order in the question.\n\n"
            +"\n".join(f"Fact {j+1}: {x}" for j,x in enumerate(facts))
            +f"\n\nQuestion: What is the relation of {a} to {b}?\n"
            +"Options: "+"; ".join(f"{letters[j]}) {x}" for j,x in enumerate(option_order))+".\n"
            +"Return only the option letter.\nAnswer:")
    out.append({"item_id":i,"variant":variant,"gold":gold,"gold_letter":gold_letter,"option_order":option_order,
                "a":a,"b":b,"facts":facts,"prompt":prompt})
   i+=1
 return out

def call(url,model,prompt):
 payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":4,
          "structured_outputs":{"choice":list("ABCDEFGH")},"chat_template_kwargs":{"enable_thinking":False}}
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
  pred=x["option_order"][ord(letter)-65] if letter in "ABCDEFGH" else ""
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":letter==x["gold_letter"],"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  fs=[p.submit(ev,x) for x in reqs]
  for n,f in enumerate(concurrent.futures.as_completed(fs),1):
   res.append(f.result())
   if n%400==0:print(f"completed {n}/{len(fs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["variant"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);br=defaultdict(list);items=defaultdict(dict)
 for x in res:by[x["variant"]].append(x["correct"]);br[(x["variant"],x["gold"])].append(x["correct"]);items[x["item_id"]][x["variant"]]=x["correct"]
 summary={"model":args.model,"n_items":len(items),"accuracy":{k:sum(v)/len(v) for k,v in by.items()},
  "accuracy_by_relation":{v:{r:sum(br[(v,r)])/len(br[(v,r)]) for r in LABELS} for v in by},
  "paired_direct_correct_converse_wrong":sum(x["direct_only"] and not x["converse_only"] for x in items.values()),
  "consistent_extra_fact_hurts":{v:sum(x["direct_only"] and not x[v] for x in items.values()) for v in
    ["direct_then_converse","converse_then_direct","direct_duplicate","direct_then_same_direction","direct_then_irrelevant"]}}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--per-relation",type=int,default=40);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
