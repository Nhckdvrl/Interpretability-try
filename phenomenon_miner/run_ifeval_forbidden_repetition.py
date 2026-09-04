#!/usr/bin/env python3
"""Test whether repeating a forbidden token undermines the same prohibition."""
from __future__ import annotations
import argparse,concurrent.futures,json,re,time,urllib.error,urllib.request
from collections import defaultdict
from pathlib import Path
from datasets import load_dataset

def build(limit):
 out=[]
 for row in load_dataset("google/IFEval",split="train"):
  if "keywords:forbidden_words" not in row["instruction_id_list"] or "combination:repeat_prompt" in row["instruction_id_list"]:continue
  j=row["instruction_id_list"].index("keywords:forbidden_words");words=row["kwargs"][j]["forbidden_words"]
  if not words:continue
  quoted=", ".join(f'"{x}"' for x in words)
  suffixes={"baseline":"","abstract_reminder":"\n\nImportant: all exclusions listed above remain in force.",
   "explicit_repeat_x1":f"\n\nImportant reminder: do not use any of these words: {quoted}.",
   "explicit_repeat_x3":"\n\n"+" ".join([f"Do not use: {quoted}." for _ in range(3)])}
  item=len({x['item_id'] for x in out})
  for variant,suffix in suffixes.items():out.append({"item_id":item,"key":row["key"],"variant":variant,"forbidden":words,"prompt":row["prompt"]+suffix})
  if item+1>=limit:break
 return out
def call(url,model,prompt):
 payload={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":512,"chat_template_kwargs":{"enable_thinking":False}}
 req=urllib.request.Request(f"{url.rstrip('/')}/v1/chat/completions",data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"});last=None
 for n in range(5):
  try:
   with urllib.request.urlopen(req,timeout=240) as r:data=json.load(r)
   m=data["choices"][0]["message"];return (m.get("content") or m.get("reasoning_content") or "").strip()
  except (urllib.error.URLError,TimeoutError) as e:last=e;time.sleep(2**n)
 raise RuntimeError(last)
def mentions(text,word):return re.search(rf"(?<!\w){re.escape(word.casefold())}(?!\w)",text.casefold()) is not None
def run(args):
 reqs=build(args.limit)
 def ev(x):
  response=call(args.base_url,args.model,x["prompt"]);viol=[w for w in x["forbidden"] if mentions(response,w)]
  return {k:v for k,v in x.items() if k!="prompt"}|{"response":response,"violated_words":viol,"complies":not viol,"model":args.model}
 res=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as p:
  for n,f in enumerate(concurrent.futures.as_completed([p.submit(ev,x) for x in reqs]),1):
   res.append(f.result())
   if n%50==0:print(f"completed {n}/{len(reqs)}",flush=True)
 res.sort(key=lambda x:(x["item_id"],x["variant"]));out=Path(args.out);out.parent.mkdir(parents=True,exist_ok=True)
 with out.open("w",encoding="utf-8") as f:
  for x in res:f.write(json.dumps(x,ensure_ascii=False)+"\n")
 by=defaultdict(list);items=defaultdict(dict)
 for x in res:by[x["variant"]].append(x["complies"]);items[x["item_id"]][x["variant"]]=x["complies"]
 summary={"model":args.model,"n_items":len(items),"compliance":{k:sum(v)/len(v) for k,v in by.items()},
  "baseline_complies_then_violates":{v:sum(x["baseline"] and not x[v] for x in items.values()) for v in ["abstract_reminder","explicit_repeat_x1","explicit_repeat_x3"]}}
 out.with_suffix(".summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8");print(json.dumps(summary,indent=2),flush=True)
def cli():
 p=argparse.ArgumentParser();p.add_argument("--base-url",required=True);p.add_argument("--model",required=True);p.add_argument("--out",required=True)
 p.add_argument("--limit",type=int,default=40);p.add_argument("--workers",type=int,default=12);return p.parse_args()
if __name__=="__main__":run(cli())
