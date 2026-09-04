#!/usr/bin/env python3
"""Natural path-independence probe for calendar updates, using free generation."""
from __future__ import annotations
import argparse,concurrent.futures,json,random,re,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path

DAYS=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
EVENTS=["dentist appointment","project review","tennis lesson","team lunch","piano class","budget meeting","book club",
 "doctor visit","design workshop","parent conference","yoga class","car service","research seminar","movie night",
 "language lesson","volunteer shift","hiking trip","lab meeting","flight briefing","cooking class","choir rehearsal","client call"]

def build(limit,seed,gap):
 rng=random.Random(seed);out=[]
 for i in range(limit):
  target=rng.choice(EVENTS);first,middle=rng.sample(DAYS,2)
  distractors=[]
  for j in range(2*gap):
   ev=rng.choice([x for x in EVENTS if x!=target]);d=rng.choice(DAYS)
   distractors.append(f"The {ev} is scheduled for {d}.")
  paths={
   "stable":[f"The {target} is scheduled for {first}.",f"Confirmed: the {target} remains on {first}.",f"Confirmed again: the {target} remains on {first}."],
   "restored":[f"The {target} is scheduled for {first}.",f"Update: the {target} has moved to {middle}.",f"Correction: the {target} has moved back to {first}."],
   "changed":[f"The {target} is scheduled for {first}.",f"Update: the {target} has moved to {middle}.",f"Confirmed: the {target} remains on {middle}."],
  }
  for variant,updates in paths.items():
   lines=[updates[0],*distractors[:gap],updates[1],*distractors[gap:],updates[2]]
   gold=middle if variant=="changed" else first
   prompt=("Below is a chronological calendar log. Later entries supersede earlier entries for the same event.\n\n"
    +"\n".join(f"{j+1}. {x}" for j,x in enumerate(lines))+f"\n\nQuestion: On which weekday is the {target} currently scheduled?\n"
    +"End with a separate line exactly as FINAL: <weekday>.")
   out.append({"item_id":i,"variant":variant,"target":target,"first":first,"middle":middle,"gold":gold,"gap":gap,"prompt":prompt})
 return out
def parse(text):
 finals=re.findall(r"final\s*:\s*(monday|tuesday|wednesday|thursday|friday|saturday|sunday)",text.casefold())
 return finals[-1].capitalize() if finals else ""
def call(url,model,prompt):
 payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":384,"chat_template_kwargs":{"enable_thinking":False}}
 req=urllib.request.Request(f"{url.rstrip('/')}/v1/chat/completions",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"});last=None
 for n in range(5):
  try:
   with urllib.request.urlopen(req,timeout=180) as r:data=json.load(r)
   m=data["choices"][0]["message"];return (m.get("content") or m.get("reasoning_content") or "").strip()
  except (urllib.error.URLError,TimeoutError) as e:last=e;time.sleep(2**n)
 raise RuntimeError(last)
def run(args):
 reqs=build(args.limit,args.seed,args.gap)
 def ev(x):
  response=call(args.base_url,args.model,x["prompt"]);pred=parse(response)
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":pred==x["gold"],"parse_ok":bool(pred),"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  for n,f in enumerate(concurrent.futures.as_completed([p.submit(ev,x) for x in reqs]),1):
   res.append(f.result())
   if n%100==0:print(f"completed {n}/{len(reqs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["variant"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);items=defaultdict(dict)
 for x in res:by[x["variant"]].append(x);items[x["item_id"]][x["variant"]]=x
 summary={"model":args.model,"n_items":len(items),"gap":args.gap,
  "accuracy":{k:sum(x["correct"] for x in v)/len(v) for k,v in by.items()},"parse_rate":{k:sum(x["parse_ok"] for x in v)/len(v) for k,v in by.items()},
  "stable_correct_restored_wrong":sum(x["stable"]["correct"] and not x["restored"]["correct"] for x in items.values()),
  "stable_correct_changed_wrong":sum(x["stable"]["correct"] and not x["changed"]["correct"] for x in items.values())}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--limit",type=int,default=100);p.add_argument("--gap",type=int,default=8);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
