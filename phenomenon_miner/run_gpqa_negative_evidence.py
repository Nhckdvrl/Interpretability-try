#!/usr/bin/env python3
"""Monotonicity test: adding verified eliminations of wrong options can only help."""
import argparse, concurrent.futures, csv, json, random, re, urllib.request
from pathlib import Path

def normalized(text):
 return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def call_chat(url, model, prompt):
 body={"model":model,"messages":[{"role":"user","content":prompt}],"temperature":0,"max_tokens":64,"chat_template_kwargs":{"enable_thinking":False}}
 req=urllib.request.Request(url.rstrip('/')+'/v1/chat/completions',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=240) as response:return json.load(response)['choices'][0]['message']['content']

GPQA=Path('/home/xiang/.cache/huggingface/hub/datasets--Idavidrein--gpqa/snapshots/633f5ee89ab8ad4522a9f850766b73f62147ffdd/gpqa_diamond.csv')

def requests(seed, n=198):
 with GPQA.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f))
 out=[]
 for i,r in enumerate(rows[:n]):
  gold=r['Correct Answer'].strip();opts=[gold]+[r[f'Incorrect Answer {j}'].strip() for j in range(1,4)]
  random.Random(f'{seed}:{i}').shuffle(opts); labels='ABCD'; g=labels[opts.index(gold)]
  wrong=[x for x in labels if x!=g];random.Random(f'w:{seed}:{i}').shuffle(wrong)
  variants=[('baseline','')]
  for k in (1,2,3):
   eliminated=wrong[:k];remaining=[x for x in labels if x not in eliminated]
   variants += [
    (f'negative_{k}',f"Verified hint: {'Options' if k>1 else 'Option'} {', '.join(eliminated)} {'are' if k>1 else 'is'} incorrect."),
    (f'remaining_{k}',f"Verified hint: The correct answer is one of these options: {', '.join(remaining)}."),
   ]
  option_text='\n'.join(f'{lab}. {val}' for lab,val in zip(labels,opts))
  for cond,hint in variants:
   p=(f"Question: {r['Question'].strip()}\n\nCandidate answers:\n{option_text}\n\n"
      +(hint+'\n\n' if hint else '')+"Give only the exact text of the correct candidate answer.")
   out.append({'id':i,'condition':cond,'gold':gold,'gold_label':g,'eliminated':wrong[:int(cond[-1])] if cond!='baseline' else [],'prompt':p})
 return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--base-url',required=True);ap.add_argument('--model',required=True);ap.add_argument('--out',required=True);ap.add_argument('--workers',type=int,default=24);ap.add_argument('--seed',type=int,default=27);ap.add_argument('--n',type=int,default=40);a=ap.parse_args();req=requests(a.seed,a.n)
 def go(x):
  o=call_chat(a.base_url,a.model,x['prompt'])
  lead=o.strip().upper()
  ok=lead.startswith(x['gold_label']+'.') or lead.startswith(x['gold_label']+')') or normalized(x['gold']) in normalized(o)
  return {k:v for k,v in x.items() if k!='prompt'}|{'output':o,'correct':ok}
 with concurrent.futures.ThreadPoolExecutor(max_workers=a.workers) as ex:rec=list(ex.map(go,req))
 conds=['baseline']+[f'{t}_{k}' for k in (1,2,3) for t in ('negative','remaining')]
 acc={c:sum(x['correct'] for x in rec if x['condition']==c)/len([x for x in rec if x['condition']==c]) for c in conds}
 by={i:{x['condition']:x for x in rec if x['id']==i} for i in sorted({x['id'] for x in rec})}
 flips={c:{'hurt':sum(v['baseline']['correct'] and not v[c]['correct'] for v in by.values()),'help':sum(not v['baseline']['correct'] and v[c]['correct'] for v in by.values())} for c in conds[1:]}
 Path(a.out).write_text(json.dumps({'model':a.model,'accuracy':acc,'flips':flips,'records':rec},indent=2));print(json.dumps({'model':a.model,'accuracy':acc,'flips':flips},indent=2))
if __name__=='__main__':main()
