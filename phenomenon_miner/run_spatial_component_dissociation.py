#!/usr/bin/env python3
"""Test whether converse-induced diagonal failures preserve both components."""
from __future__ import annotations
import argparse,concurrent.futures,json,random,re,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path
from datasets import load_dataset

REL={"upper-left":"above and to the left of","upper-right":"above and to the right of",
     "lower-left":"below and to the left of","lower-right":"below and to the right of"}
INV={"upper-left":"lower-right","upper-right":"lower-left","lower-left":"upper-right","lower-right":"upper-left"}
JOINT=list(REL);VERT={"upper-left":"above","upper-right":"above","lower-left":"below","lower-right":"below"}
HORIZ={"upper-left":"left","lower-left":"left","upper-right":"right","lower-right":"right"}

def ue(text):
 out=[]
 for x in re.findall(r"\b[A-Z]\b",text):
  if x not in out:out.append(x)
 return out
def build(limit,seed):
 rows=[x for x in load_dataset("ZhengyanShi/StepGame",split="validation") if int(x["k_hop"])==1 and x["label"] in JOINT]
 random.Random(seed).shuffle(rows);out=[];idx=0
 for row in rows:
  se=ue(row["story"][0]);qe=ue(row["question"])
  if len(se)!=2 or qe!=se:continue
  a,b=qe;g=row["label"];conv=f"{b} is {REL[INV[g]]} {a}."
  for evidence,facts in [("original",[row["story"][0]]),("plus_converse",[row["story"][0],conv]),
                         ("plus_duplicate",[row["story"][0],row["story"][0]])]:
   tasks=[("joint",f"What is the full relation of {a} to {b}?",JOINT,g),
          ("vertical",f"Is {a} above or below {b}?",["above","below"],VERT[g]),
          ("horizontal",f"Is {a} left or right of {b}?",["left","right"],HORIZ[g])]
   for task,q,opts,gold in tasks:
    order=opts[:];random.Random(f"{seed}:{idx}:{task}").shuffle(order);letters="ABCD"[:len(order)];gl=letters[order.index(gold)]
    prompt=("Use the spatial fact(s) to answer.\n\n"+"\n".join(f"Fact {j+1}: {x}" for j,x in enumerate(facts))
            +f"\n\nQuestion: {q}\nOptions: "+"; ".join(f"{letters[j]}) {x}" for j,x in enumerate(order))
            +".\nReturn only the option letter.\nAnswer:")
    out.append({"item_id":idx,"evidence":evidence,"task":task,"gold":gold,"gold_letter":gl,"option_order":order,"facts":facts,"prompt":prompt})
  idx+=1
  if idx>=limit:break
 return out
def call(url,model,prompt,nopts):
 choices=list("ABCD"[:nopts]);payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":4,
  "structured_outputs":{"choice":choices},"chat_template_kwargs":{"enable_thinking":False}}
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
  response=call(args.base_url,args.model,x["prompt"],len(x["option_order"]));letter=response.strip().upper()[:1]
  pred=x["option_order"][ord(letter)-65] if letter and ord(letter)-65<len(x["option_order"]) else ""
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"pred":pred,"correct":letter==x["gold_letter"],"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  for n,f in enumerate(concurrent.futures.as_completed([p.submit(ev,x) for x in reqs]),1):
   res.append(f.result())
   if n%300==0:print(f"completed {n}/{len(reqs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["evidence"],x["task"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);items=defaultdict(dict)
 for x in res:by[(x["evidence"],x["task"])].append(x["correct"]);items[x["item_id"]][(x["evidence"],x["task"])]=x["correct"]
 acc={e:{t:sum(by[(e,t)])/len(by[(e,t)]) for t in ["joint","vertical","horizontal"]} for e in ["original","plus_converse","plus_duplicate"]}
 summary={"model":args.model,"n_items":len(items),"accuracy":acc,
  "converse_components_both_correct_joint_wrong":sum(x[("plus_converse","vertical")] and x[("plus_converse","horizontal")] and not x[("plus_converse","joint")] for x in items.values()),
  "original_components_both_correct_joint_wrong":sum(x[("original","vertical")] and x[("original","horizontal")] and not x[("original","joint")] for x in items.values())}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--limit",type=int,default=120);p.add_argument("--seed",type=int,default=20260827);p.add_argument("--workers",type=int,default=24);return p.parse_args()
if __name__=="__main__":run(cli())
