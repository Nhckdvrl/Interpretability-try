#!/usr/bin/env python3
"""Classic Frege/opacity test: identity substitution inside vs outside belief."""
import argparse, concurrent.futures, json, random, urllib.request
from pathlib import Path

PEOPLE=["Maya","Jonah","Priya","Felix","Nora","Theo","Lina","Omar","Eva","Darius"]
ALIASES=[("the violinist","the night guard"),("Dr. Rowan","the radio host"),("the masked runner","Ms. Bell"),("Captain North","the baker"),("the poet","the chess champion")]
PROPS=["won the blue ribbon","owns the red bicycle","left the key in the library","painted the mural","sent the anonymous letter","found the missing necklace"]

def call(url,model,p):
 b={"model":model,"messages":[{"role":"user","content":p}],"temperature":0,"max_tokens":8,"chat_template_kwargs":{"enable_thinking":False}}
 q=urllib.request.Request(url+"/v1/chat/completions",data=json.dumps(b).encode(),headers={"Content-Type":"application/json"})
 with urllib.request.urlopen(q,timeout=90) as r:return json.load(r)["choices"][0]["message"]["content"]

def items(n,seed):
 rng=random.Random(seed); out=[]
 for i in range(n):
  person=rng.choice(PEOPLE); a,b=rng.choice(ALIASES); prop=rng.choice(PROPS)
  common=(f"{person} has heard of {a} and {b}, but believes they are two different people. "
          f"Unknown to {person}, {a} and {b} are actually the same person. ")
  variants={
   "opaque_unaware":(common+f"{person} believes that {a} {prop}.\n\nDoes {person} believe that {b} {prop}?",False),
   "opaque_truth_last":(f"{person} believes that {a} {prop}. {person} believes that {a} and {b} are two different people. "
                         f"In fact, {a} and {b} are the same person, but {person} does not know this.\n\n"
                         f"Does {person} believe that {b} {prop}?",False),
   "opaque_unaware_last":(f"In fact, {a} and {b} are the same person. {person} believes that {a} {prop}. "
                           f"However, {person} does not know they are the same and believes they are two different people.\n\n"
                           f"Does {person} believe that {b} {prop}?",False),
   "opaque_aware":(f"{person} knows that {a} and {b} are the same person. {person} believes that {a} {prop}.\n\nDoes {person} believe that {b} {prop}?",True),
   "extensional":(common+f"In reality, {a} {prop}.\n\nIn reality, did {b} {prop}?",True),
   "surface_control":(common+f"{person} believes that {a} {prop}.\n\nDoes {person} believe that {a} {prop}?",True),
  }
  for cond,(story,gold) in variants.items():
   out.append({"id":i,"condition":cond,"gold":gold,"prompt":story+" Answer only Yes or No."})
 return out

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--url',required=True);ap.add_argument('--model',required=True);ap.add_argument('--n',type=int,default=80);ap.add_argument('--out',required=True); a=ap.parse_args()
 its=items(a.n,17)
 def go(x):
  z=call(a.url,a.model,x['prompt']); pred=z.strip().lower().startswith('yes'); return {**x,'output':z,'correct':pred==x['gold']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=20) as ex: rec=list(ex.map(go,its))
 acc={c:sum(x['correct'] for x in rec if x['condition']==c)/a.n for c in sorted(set(x['condition'] for x in rec))}
 # Key error: correct on every matched control but substitutes inside unaware belief.
 by={i:{x['condition']:x for x in rec if x['id']==i} for i in range(a.n)}
 signature=sum((not v['opaque_truth_last']['correct']) and all(v[c]['correct'] for c in ['opaque_aware','extensional','surface_control']) for v in by.values())/a.n
 Path(a.out).write_text(json.dumps({'model':a.model,'accuracy':acc,'selective_substitution_error':signature,'records':rec},indent=2))
 print(json.dumps({'model':a.model,'accuracy':acc,'selective_substitution_error':signature},indent=2))
if __name__=='__main__':main()
