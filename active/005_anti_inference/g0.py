from __future__ import annotations
import argparse,json,math,random
from dataclasses import dataclass
from pathlib import Path

PROB_CANDS=("50%","60%","70%","80%","90%","95%","99%")
DOMAINS={
"legal":[("the suspect committed the burglary","a shoeprint at the scene matches the suspect","the matching shoeprint implies the suspect committed the burglary"),("the driver crossed the red light","camera metadata shows the vehicle entered after the signal changed","entering after the signal changed implies the driver crossed the red light")],
"medical":[("the patient has condition X","marker M is present","marker M implies the patient has condition X"),("the patient has infection Y","culture pattern C is present","culture pattern C implies the patient has infection Y")],
"cyber":[("the server is compromised","indicator I is present","indicator I implies the server is compromised"),("the account was taken over","token pattern T is present","token pattern T implies the account was taken over")],
"engineering":[("the pump has bearing failure","vibration signature V is present","vibration signature V implies the pump has bearing failure"),("the circuit has a short","diagnostic pattern D is present","diagnostic pattern D implies the circuit has a short")],
}

def generate():
 rows=[];i=0
 for domain,items in DOMAINS.items():
  for rep in range(8):
   for target,evidence,rule in items:
    for reliability in (80,90,95):
     i+=1
     for cond in ('direct','inferred','inferred_explicit'):
      rows.append({'family_id':f'f{i:04d}','domain':domain,'condition':cond,'target':target,'evidence':evidence,'rule':rule,'reliability':reliability})
 return rows

def prompts(r,variant=0):
 target=r['target']; rel=r['reliability']; cond=r['condition']
 if cond=='direct':
  evidence=f"A calibrated source directly reports that {target}. The source's report about this proposition is correct {rel}% of the time."
  check=f"Does the source directly assert that {target}?"
 elif cond=='inferred':
  evidence=f"A calibrated pipeline reports that {r['evidence']}. The valid rule is: {r['rule']}. The pipeline's end-to-end conclusion about whether {target} is correct {rel}% of the time."
  check=f"According to the stated rule, if {r['evidence']}, does it follow that {target}?"
 else:
  evidence=f"A calibrated pipeline reports that {r['evidence']}. The valid rule is: {r['rule']}. Therefore, {target}. The pipeline's end-to-end conclusion about whether {target} is correct {rel}% of the time."
  check=f"According to the stated rule, if {r['evidence']}, does it follow that {target}?"
 order=list(PROB_CANDS)
 if variant==1: order=order[3:]+order[:3]
 elif variant==2: order=list(reversed(order))
 q=(f"{evidence}\nGiven only this information, what probability should you assign to the proposition that {target}? " if variant!=2 else f"{evidence}\nEstimate the probability that {target}, using only the stated calibration information. ")+"Answer exactly one of: "+', '.join(order)+"\nAnswer:"
 c=check+" Answer exactly Yes or No.\nAnswer:"
 return c,q

@dataclass
class Score: probs:dict[str,float]
class Scorer:
 def __init__(self,model_name):
  import torch
  from transformers import AutoModelForCausalLM,AutoTokenizer
  self.torch=torch;self.tok=AutoTokenizer.from_pretrained(model_name,trust_remote_code=True)
  if self.tok.pad_token_id is None:self.tok.pad_token=self.tok.eos_token
  self.model=AutoModelForCausalLM.from_pretrained(model_name,device_map='auto',torch_dtype='auto',trust_remote_code=True);self.model.eval();self.cache={}
 def prefix(self,p):
  if getattr(self.tok,'chat_template',None):return self.tok.apply_chat_template([{'role':'user','content':p}],tokenize=False,add_generation_prompt=True,enable_thinking=False)
  return p+'\n'
 def score(self,p,cands):
  torch=self.torch;pref=self.prefix(p);pre=self.tok(pref,add_special_tokens=False).input_ids;logs={};dev=next(self.model.parameters()).device
  for c in cands:
   k=(p,c)
   if k in self.cache:logs[c]=self.cache[k];continue
   ids=self.tok(pref+c,add_special_tokens=False).input_ids
   if ids[:len(pre)]!=pre:raise ValueError('continuation changed prefix tokenization')
   x=torch.tensor([ids],device=dev)
   with torch.inference_mode(): logits=self.model(x).logits[0]
   s=sum(float(torch.log_softmax(logits[pos-1].float(),-1)[ids[pos]].item()) for pos in range(len(pre),len(ids)))
   self.cache[k]=s;logs[c]=s
  m=max(logs.values());z=sum(math.exp(v-m) for v in logs.values());return Score({k:math.exp(v-m)/z for k,v in logs.items()})

def run(data,model,out,limit=None):
 rows=[json.loads(x) for x in Path(data).read_text().splitlines() if x.strip()];sc=Scorer(model);Path(out).parent.mkdir(parents=True,exist_ok=True);n=0
 with Path(out).open('w') as f:
  for r in rows:
   for v in range(3):
    cp,qp=prompts(r,v);cs=sc.score(cp,('Yes','No'));qs=sc.score(qp,PROB_CANDS)
    exp=sum(int(k[:-1])*p for k,p in qs.probs.items())
    f.write(json.dumps({'family_id':r['family_id'],'domain':r['domain'],'condition':r['condition'],'reliability':r['reliability'],'variant':v,'p_recognize':cs.probs['Yes'],'expected_probability':exp,'pred_probability':max(qs.probs,key=qs.probs.get)})+'\n');n+=1
    if limit and n>=limit:return

def bootstrap(vals,seed=0,B=5000):
 r=random.Random(seed);means=[]
 for _ in range(B):means.append(sum(r.choice(vals) for _ in vals)/len(vals))
 means.sort();return [means[int(.025*B)],means[int(.975*B)]]

def summarize(data,results,out):
 recs=[json.loads(x) for x in Path(results).read_text().splitlines() if x.strip()];g={}
 for x in recs:g.setdefault((x['family_id'],x['domain'],x['condition'],x['reliability']),[]).append(x)
 for k,v in g.items():
  if len(v)!=3 or {x['variant'] for x in v}!={0,1,2}:raise ValueError(f'incomplete/duplicate variants {k}')
 fam={}
 for (fid,dom,cond,rel),v in g.items():fam[(fid,cond)]={'domain':dom,'rel':rel,'rec':sum(x['p_recognize'] for x in v)/3,'prob':sum(x['expected_probability'] for x in v)/3}
 ids=sorted({fid for fid,_ in fam});deltas=[];bydom={};direct_cal=[];gated=0
 for fid in ids:
  need=[(fid,c) for c in ('direct','inferred','inferred_explicit')]
  if any(k not in fam for k in need):raise ValueError(f'missing condition for {fid}')
  d,i,e=(fam[k] for k in need)
  if d['rec']>=.8 and i['rec']>=.8 and abs(d['rec']-i['rec'])<=.10:
   gated+=1;delta=d['prob']-i['prob'];deltas.append(delta);bydom.setdefault(d['domain'],[]).append(delta);direct_cal.append(abs(d['prob']-d['rel']))
 if not deltas:raise ValueError('no gated families')
 ci=bootstrap(deltas);mean=sum(deltas)/len(deltas);pos=sum(x>0 for x in deltas)/len(deltas);dm={k:sum(v)/len(v) for k,v in bydom.items()};cal=sum(direct_cal)/len(direct_cal)
 summary={'gated_families':gated,'mean_discount_points':mean,'bootstrap95':ci,'positive_fraction':pos,'domain_mean':dm,'direct_mean_abs_calibration_error':cal,'pass':gated>=60 and mean>=5 and ci[0]>2 and pos>=.65 and sum(v>0 for v in dm.values())>=3 and cal<=5}
 Path(out).parent.mkdir(parents=True,exist_ok=True);Path(out).write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))

def main():
 ap=argparse.ArgumentParser();sp=ap.add_subparsers(dest='cmd',required=True)
 a=sp.add_parser('generate');a.add_argument('--out',required=True)
 a=sp.add_parser('run');a.add_argument('--model',required=True);a.add_argument('--data',required=True);a.add_argument('--out',required=True);a.add_argument('--limit',type=int)
 a=sp.add_parser('summarize');a.add_argument('--data',required=True);a.add_argument('--results',required=True);a.add_argument('--out',required=True);x=ap.parse_args()
 if x.cmd=='generate':
  rows=generate();Path(x.out).parent.mkdir(parents=True,exist_ok=True);Path(x.out).write_text('\n'.join(json.dumps(r) for r in rows)+'\n');print(len(rows))
 elif x.cmd=='run':run(x.data,x.model,x.out,x.limit)
 else:summarize(x.data,x.results,x.out)
if __name__=='__main__':main()
