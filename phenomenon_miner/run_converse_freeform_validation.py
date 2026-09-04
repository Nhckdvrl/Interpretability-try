#!/usr/bin/env python3
"""Free-generation validation of redundant-converse diagonal collapse."""
from __future__ import annotations
import argparse,concurrent.futures,json,random,re,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path
from datasets import load_dataset

REL={"upper-left":"above and to the left of","upper-right":"above and to the right of",
     "lower-left":"below and to the left of","lower-right":"below and to the right of"}
INV={"upper-left":"lower-right","upper-right":"lower-left","lower-left":"upper-right","lower-right":"upper-left"}
LABELS=list(REL)
def ue(text):
 out=[]
 for x in re.findall(r"\b[A-Z]\b",text):
  if x not in out:out.append(x)
 return out
def build(limit,seed):
 rows=[x for x in load_dataset("ZhengyanShi/StepGame",split="validation") if int(x["k_hop"])==1 and x["label"] in LABELS]
 random.Random(seed).shuffle(rows);out=[];idx=0
 for row in rows:
  se=ue(row["story"][0]);qe=ue(row["question"])
  if len(se)!=2 or qe!=se:continue
  a,b=qe;conv=f"Equivalently, {b} is {REL[INV[row['label']]]} {a}."
  for variant,facts in [("original",[row["story"][0]]),("plus_marked_converse",[row["story"][0],conv])]:
   prompt=("Use the spatial fact(s) to answer the question.\n\n"+"\n".join(f"Fact {j+1}: {x}" for j,x in enumerate(facts))
    +f"\n\nQuestion: {row['question']}\nValid labels: "+", ".join(LABELS)+".\n"
    +"You may reason briefly, but end with a separate line exactly in the form FINAL: <label>.")
   out.append({"item_id":idx,"variant":variant,"gold":row["label"],"facts":facts,"question":row["question"],"prompt":prompt})
  idx+=1
  if idx>=limit:break
 return out
def parse(text):
 t=text.casefold().replace("_","-")
 finals=re.findall(r"final\s*:\s*\**\s*(upper-left|upper-right|lower-left|lower-right)",t)
 if finals:return finals[-1],True
 hits=[]
 for label in LABELS:
  hits.extend((m.start(),label) for m in re.finditer(rf"(?<!\w){label}(?!\w)",t))
 return (max(hits)[1] if hits else ""),False
def call(url,model,prompt):
 payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":160,
          "chat_template_kwargs":{"enable_thinking":False}}
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
  response=call(args.base_url,args.model,x["prompt"]);pred,anchored=parse(response)
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"parse_anchored":anchored,"correct":pred==x["gold"],"model":args.model}
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
 summary={"model":args.model,"n_items":len(items),"accuracy":{k:sum(x["correct"] for x in v)/len(v) for k,v in by.items()},
  "anchored_parse_rate":{k:sum(x["parse_anchored"] for x in v)/len(v) for k,v in by.items()},
  "original_correct_then_hurt":sum(x["original"]["correct"] and not x["plus_marked_converse"]["correct"] for x in items.values()),
  "original_wrong_then_help":sum(not x["original"]["correct"] and x["plus_marked_converse"]["correct"] for x in items.values())}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--limit",type=int,default=100);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
