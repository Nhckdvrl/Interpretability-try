#!/usr/bin/env python3
"""Add a redundant converse to naturally varied one-hop StepGame facts."""
from __future__ import annotations
import argparse,concurrent.futures,json,random,re,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path
from datasets import load_dataset

REL={"above":"above","below":"below","left":"to the left of","right":"to the right of",
 "upper-left":"above and to the left of","upper-right":"above and to the right of",
 "lower-left":"below and to the left of","lower-right":"below and to the right of"}
INV={"above":"below","below":"above","left":"right","right":"left","upper-left":"lower-right",
 "upper-right":"lower-left","lower-left":"upper-right","lower-right":"upper-left","overlap":"overlap"}
LABELS=["upper-left","above","upper-right","left","right","lower-left","below","lower-right","overlap"]
LETTERS="ABCDEFGHI"
ATOMIC={"above":"north of","below":"south of","left":"west of","right":"east of",
        "upper-left":"northwest of","upper-right":"northeast of","lower-left":"southwest of","lower-right":"southeast of"}

def unique_entities(text):
 out=[]
 for x in re.findall(r"\b[A-Z]\b",text):
  if x not in out:out.append(x)
 return out
def build(limit,seed):
 rows=[x for x in load_dataset("ZhengyanShi/StepGame",split="validation") if int(x["k_hop"])==1 and x["label"]!="overlap"]
 random.Random(seed).shuffle(rows);out=[];idx=0
 for row in rows:
  se=unique_entities(row["story"][0]);qe=unique_entities(row["question"])
  if len(se)!=2 or len(qe)!=2 or qe!=se:continue
  a,b=qe;gold=row["label"];converse=f"{b} is {REL[INV[gold]]} {a}."
  atomic_converse=f"{b} is {ATOMIC[INV[gold]]} {a}."
  # Same length class and relation vocabulary, but disconnected from the queried pair.
  c,d=random.Random(f"{seed}:{idx}").sample([x for x in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if x not in (a,b)],2)
  irrelevant=f"{c} is {REL[INV[gold]]} {d}."
  order=LABELS[:];random.Random(f"opts:{seed}:{idx}").shuffle(order);gl=LETTERS[order.index(gold)]
  variants={"original":[row["story"][0]],"plus_converse":[row["story"][0],converse],
            "plus_atomic_converse":[row["story"][0],atomic_converse],
            "plus_marked_converse":[row["story"][0],"Equivalently, "+converse],
            "plus_duplicate":[row["story"][0],row["story"][0]],"plus_irrelevant":[row["story"][0],irrelevant]}
  for variant,facts in variants.items():
   prompt=("Use the spatial facts to answer the question.\n\n"+"\n".join(f"Fact {j+1}: {x}" for j,x in enumerate(facts))
           +f"\n\nQuestion: {row['question']}\nOptions: "+"; ".join(f"{LETTERS[j]}) {x}" for j,x in enumerate(order))
           +".\nReturn only the option letter.\nAnswer:")
   out.append({"item_id":idx,"variant":variant,"gold":gold,"gold_letter":gl,"option_order":order,"facts":facts,"question":row["question"],"prompt":prompt})
  idx+=1
  if idx>=limit:break
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
 reqs=build(args.limit,args.seed)
 def ev(x):
  response=call(args.base_url,args.model,x["prompt"]);letter=response.strip().upper()[:1]
  pred=x["option_order"][ord(letter)-65] if letter in LETTERS else ""
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":letter==x["gold_letter"],"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  for n,f in enumerate(concurrent.futures.as_completed([p.submit(ev,x) for x in reqs]),1):
   res.append(f.result())
   if n%300==0:print(f"completed {n}/{len(reqs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["variant"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);items=defaultdict(dict);br=defaultdict(list)
 for x in res:by[x["variant"]].append(x["correct"]);items[x["item_id"]][x["variant"]]=x["correct"];br[(x["variant"],x["gold"])].append(x["correct"])
 summary={"model":args.model,"n_items":len(items),"accuracy":{k:sum(v)/len(v) for k,v in by.items()},
  "accuracy_by_relation":{v:{r:sum(z)/len(z) for r in LABELS if (z:=br[(v,r)])} for v in by},
  "baseline_correct_then_hurt":{v:sum(x["original"] and not x[v] for x in items.values()) for v in
    ["plus_converse","plus_atomic_converse","plus_marked_converse","plus_duplicate","plus_irrelevant"]}}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--limit",type=int,default=200);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
