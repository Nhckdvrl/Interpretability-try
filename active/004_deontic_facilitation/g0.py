from __future__ import annotations
import argparse, json, math, random, urllib.request
from dataclasses import dataclass
from itertools import permutations
from pathlib import Path

CANDIDATES=("1,2","1,3","1,4","2,3","2,4","3,4")
DOMAINS={
"access":{
 "states":[("badge is red","badge is blue"),("gate light is green","gate light is amber"),("door sign says restricted","door sign says public"),("alarm is active","alarm is inactive")],
 "actions":[("visitor enters the archive","visitor must enter the archive","visitor waits outside"),("technician opens the console","technician must open the console","technician keeps the console closed"),("guard checks the permit","guard must check the permit","guard ignores the permit"),("operator locks the cabinet","operator must lock the cabinet","operator leaves the cabinet unlocked")]},
"school":{
 "states":[("card says senior","card says junior"),("exam flag is blue","exam flag is white"),("lab light is on","lab light is off"),("form is marked complete","form is marked incomplete")],
 "actions":[("student enters the lab","student must enter the lab","student waits in the hall"),("student submits the booklet","student must submit the booklet","student keeps the booklet"),("assistant wears gloves","assistant must wear gloves","assistant works without gloves"),("teacher signs the sheet","teacher must sign the sheet","teacher leaves the sheet unsigned")]},
"work":{
 "states":[("shift board says night","shift board says day"),("panel shows hazard","panel shows normal"),("pressure lamp is red","pressure lamp is green"),("job code is urgent","job code is routine")],
 "actions":[("operator wears the visor","operator must wear the visor","operator works without the visor"),("engineer stops the machine","engineer must stop the machine","engineer keeps the machine running"),("inspector records the reading","inspector must record the reading","inspector skips the reading"),("supervisor calls maintenance","supervisor must call maintenance","supervisor does not call maintenance")]},
"travel":{
 "states":[("ticket is international","ticket is domestic"),("lane sign is express","lane sign is local"),("boarding card is priority","boarding card is standard"),("route marker is orange","route marker is gray")],
 "actions":[("passenger shows a passport","passenger must show a passport","passenger does not show a passport"),("driver uses the transponder","driver must use the transponder","driver does not use the transponder"),("traveler uses gate A","traveler must use gate A","traveler uses gate B"),("pilot contacts the tower","pilot must contact the tower","pilot does not contact the tower")]}}

def generate():
 rows=[]; i=0
 for domain,cfg in DOMAINS.items():
  for p,not_p in cfg["states"]:
   for desc,deon,not_q in cfg["actions"]:
    i+=1; cards=[p.capitalize(),not_p.capitalize(),desc.capitalize(),not_q.capitalize()]
    for framing,rule in (("descriptive",f"If the {p}, then the {desc}."),("deontic",f"If the {p}, then the {deon}.")):
     rows.append({"item_id":f"m{i:03d}","domain":domain,"framing":framing,"rule":rule,"cards":cards,"gold_semantic":[0,3]})
 return rows

def render(row,perm,template):
 shown=[row["cards"][j] for j in perm]; gold=','.join(map(str,sorted(perm.index(j)+1 for j in row["gold_semantic"])))
 stem=("Turn exactly the cards that must be checked to determine whether the conditional rule is violated. Do not turn unnecessary cards." if template==0 else "Select exactly the two cards required to test the rule. A violation is a case where the antecedent is true and the consequent is false.")
 prompt=f"{stem}\nRule: {row['rule']}\n"+'\n'.join(f"{k+1}. {x}" for k,x in enumerate(shown))+"\nAnswer with exactly one pair from: "+', '.join(CANDIDATES)+"\nAnswer:"
 return prompt,gold

@dataclass
class Score: probs:dict[str,float]
class Scorer:
 def __init__(self,model_name):
  import torch
  from transformers import AutoModelForCausalLM,AutoTokenizer
  self.torch=torch; self.tok=AutoTokenizer.from_pretrained(model_name,trust_remote_code=True)
  if self.tok.pad_token_id is None:self.tok.pad_token=self.tok.eos_token
  self.model=AutoModelForCausalLM.from_pretrained(model_name,device_map="auto",torch_dtype="auto",trust_remote_code=True); self.model.eval(); self.cache={}
 def prefix(self,p):
  if getattr(self.tok,"chat_template",None):return self.tok.apply_chat_template([{"role":"user","content":p}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
  return p+"\n"
 def score(self,p,cands):
  torch=self.torch; pref=self.prefix(p); pre=self.tok(pref,add_special_tokens=False).input_ids; logs={}; dev=next(self.model.parameters()).device
  for c in cands:
   key=(p,c)
   if key in self.cache: logs[c]=self.cache[key]; continue
   ids=self.tok(pref+c,add_special_tokens=False).input_ids
   if ids[:len(pre)]!=pre: raise ValueError("continuation changed prefix tokenization")
   x=torch.tensor([ids],device=dev)
   with torch.inference_mode(): logits=self.model(x).logits[0]
   s=sum(float(torch.log_softmax(logits[pos-1].float(),-1)[ids[pos]].item()) for pos in range(len(pre),len(ids)))
   self.cache[key]=s; logs[c]=s
  m=max(logs.values()); z=sum(math.exp(v-m) for v in logs.values()); return Score({k:math.exp(v-m)/z for k,v in logs.items()})

def run(data,model,out,limit=None):
 rows=[json.loads(x) for x in Path(data).read_text().splitlines() if x.strip()]; scorer=Scorer(model); Path(out).parent.mkdir(parents=True,exist_ok=True); n=0
 with Path(out).open('w') as f:
  for row in rows:
   for perm in permutations(range(4)):
    for t in (0,1):
     p,g=render(row,perm,t); s=scorer.score(p,CANDIDATES); f.write(json.dumps({"item_id":row["item_id"],"domain":row["domain"],"framing":row["framing"],"perm":perm,"template":t,"gold":g,"p_correct":s.probs[g],"pred":max(s.probs,key=s.probs.get)})+'\n'); n+=1
     if limit and n>=limit:return

def bootstrap(vals,seed=0,B=5000):
 r=random.Random(seed); means=[]
 for _ in range(B):means.append(sum(r.choice(vals) for _ in vals)/len(vals))
 means.sort(); return [means[int(.025*B)],means[int(.975*B)]]

def summarize(data,results,out):
 recs=[json.loads(x) for x in Path(results).read_text().splitlines() if x.strip()]; groups={}
 for r in recs:groups.setdefault((r["item_id"],r["domain"],r["framing"]),[]).append(r)
 for k,v in groups.items():
  keys={(tuple(x["perm"]),x["template"]) for x in v}
  if len(v)!=48 or len(keys)!=48:raise ValueError(f"incomplete/duplicate variants for {k}: {len(v)} rows, {len(keys)} unique")
 item={(iid,fr):{"domain":dom,"p":sum(x["p_correct"] for x in v)/48} for (iid,dom,fr),v in groups.items()}
 ids=sorted({iid for iid,_ in item}); deltas=[]; bydom={}
 for iid in ids:
  if (iid,"deontic") not in item or (iid,"descriptive") not in item:raise ValueError(f"missing matched framing for {iid}")
  d=item[(iid,"deontic")]["p"]-item[(iid,"descriptive")]["p"]; deltas.append(d); bydom.setdefault(item[(iid,"deontic")]["domain"],[]).append(d)
 ci=bootstrap(deltas); mean=sum(deltas)/len(deltas); pos=sum(d>0 for d in deltas)/len(deltas); dmean={k:sum(v)/len(v) for k,v in bydom.items()}
 summary={"n_items":len(deltas),"mean_facilitation_delta":mean,"bootstrap95":ci,"positive_fraction":pos,"domain_mean":dmean,"pass":mean>=.08 and ci[0]>0 and pos>=.65 and sum(v>0 for v in dmean.values())>=3}
 Path(out).parent.mkdir(parents=True,exist_ok=True); Path(out).write_text(json.dumps(summary,indent=2)); print(json.dumps(summary,indent=2))

def fetch_neubaroco(out):
 Path(out).parent.mkdir(parents=True,exist_ok=True); urllib.request.urlretrieve("https://raw.githubusercontent.com/kmineshima/NeuBAROCO/main/eacl2026/wason.tsv",out)

def main():
 ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest='cmd',required=True)
 a=sp.add_parser('generate');a.add_argument('--out',required=True)
 a=sp.add_parser('run');a.add_argument('--model',required=True);a.add_argument('--data',required=True);a.add_argument('--out',required=True);a.add_argument('--limit',type=int)
 a=sp.add_parser('summarize');a.add_argument('--data',required=True);a.add_argument('--results',required=True);a.add_argument('--out',required=True)
 a=sp.add_parser('fetch-neubaroco');a.add_argument('--out',required=True); x=ap.parse_args()
 if x.cmd=='generate':
  rows=generate();Path(x.out).parent.mkdir(parents=True,exist_ok=True);Path(x.out).write_text('\n'.join(json.dumps(r) for r in rows)+'\n');print(len(rows))
 elif x.cmd=='run':run(x.data,x.model,x.out,x.limit)
 elif x.cmd=='summarize':summarize(x.data,x.results,x.out)
 else:fetch_neubaroco(x.out)
if __name__=='__main__':main()
