#!/usr/bin/env python3
"""Does pretrained co-reference leak across an explicitly partitioned belief state?"""
import argparse, concurrent.futures, json, random, urllib.request
from pathlib import Path

FAMOUS=[("Clark Kent","Superman"),("Bruce Wayne","Batman"),("Peter Parker","Spider-Man"),("Diana Prince","Wonder Woman"),("Selina Kyle","Catwoman"),("Anakin Skywalker","Darth Vader"),("Tom Riddle","Lord Voldemort"),("Bruce Banner","the Hulk"),("Matt Murdock","Daredevil"),("Tony Stark","Iron Man"),("Miley Stewart","Hannah Montana"),("Barry Allen","the Flash"),("Arthur Curry","Aquaman"),("T'Challa","Black Panther"),("Kara Danvers","Supergirl")]
INVENTED=[("Dr. Rowan","the radio host"),("Ms. Bell","the masked runner"),("Mr. Vale","the violinist"),("Dr. Moss","the night guard"),("Ms. Lake","the chess champion"),("Mr. Snow","the baker"),("Dr. Finch","the poet"),("Ms. Gray","the carpenter"),("Mr. Reed","the cyclist"),("Dr. Lane","the sculptor"),("Ms. King","the pilot"),("Mr. Shaw","the gardener"),("Dr. Stone","the singer"),("Ms. North","the sailor"),("Mr. Wood","the painter")]
PEOPLE=["Maya","Jonah","Priya","Felix","Nora","Theo","Lina","Omar"]
PROPS=["owns the red bicycle","won the blue ribbon","left the key in the library","painted the town mural","sent the anonymous letter","found the missing necklace"]

def call(url,model,p):
 b={"model":model,"messages":[{"role":"user","content":p}],"temperature":0,"max_tokens":8,"chat_template_kwargs":{"enable_thinking":False}}
 q=urllib.request.Request(url+"/v1/chat/completions",data=json.dumps(b).encode(),headers={"Content-Type":"application/json"})
 with urllib.request.urlopen(q,timeout=90) as r:return json.load(r)["choices"][0]["message"]["content"]

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--url',required=True);ap.add_argument('--model',required=True);ap.add_argument('--reps',type=int,default=6);ap.add_argument('--out',required=True);a=ap.parse_args()
 rng=random.Random(123); req=[]
 for kind,pairs in [('famous',FAMOUS),('invented',INVENTED)]:
  for k,(x,y) in enumerate(pairs):
   for rep in range(a.reps):
    person=rng.choice(PEOPLE); prop=PROPS[rep%len(PROPS)]
    core=(f"{person} has encountered {x} and {y}, but {person} firmly believes they are two different people. "
          f"In reality, {x} and {y} are the same person. {person} believes that {x} {prop}. ")
    variants={
      'belief_cross':(core+f"Does {person} believe that {y} {prop}?",False),
      'belief_same':(core+f"Does {person} believe that {x} {prop}?",True),
      'reality_cross':(core+f"In reality, does {y} {prop}?",True),
    }
    for cond,(p,gold) in variants.items():req.append({'kind':kind,'pair':k,'rep':rep,'condition':cond,'gold':gold,'prompt':p+' Answer only Yes or No.'})
 def go(z):
  o=call(a.url,a.model,z['prompt']);pred=o.strip().lower().startswith('yes');return {**z,'output':o,'correct':pred==z['gold']}
 with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex: rec=list(ex.map(go,req))
 acc={}
 for kind in ['famous','invented']:
  for cond in ['belief_cross','belief_same','reality_cross']:
   z=[r for r in rec if r['kind']==kind and r['condition']==cond];acc[kind+'/'+cond]=sum(r['correct'] for r in z)/len(z)
 Path(a.out).write_text(json.dumps({'model':a.model,'accuracy':acc,'records':rec},indent=2));print(json.dumps({'model':a.model,'accuracy':acc},indent=2))
if __name__=='__main__':main()
