from __future__ import annotations
from dataclasses import dataclass
from typing import Sequence
import math

@dataclass(frozen=True)
class ScoreResult:
    logprobs: dict[str, float]
    probs: dict[str, float]

def softmax_dict(logprobs: dict[str, float]) -> dict[str, float]:
    if not logprobs: raise ValueError("logprobs cannot be empty")
    m=max(logprobs.values());exps={k:math.exp(v-m) for k,v in logprobs.items()};z=sum(exps.values());return {k:v/z for k,v in exps.items()}

class HFChoiceScorer:
    """Exact continuation scorer for local HF causal LMs; no LLM judge."""
    def __init__(self,model_name:str,*,revision:str|None=None,device_map:str="auto",dtype:str="auto")->None:
        import torch
        from transformers import AutoModelForCausalLM,AutoTokenizer
        self.torch=torch;self.tokenizer=AutoTokenizer.from_pretrained(model_name,revision=revision,trust_remote_code=True)
        if self.tokenizer.pad_token_id is None:self.tokenizer.pad_token=self.tokenizer.eos_token
        dtype_arg=dtype if dtype=="auto" else getattr(torch,dtype)
        self.model=AutoModelForCausalLM.from_pretrained(model_name,revision=revision,device_map=device_map,torch_dtype=dtype_arg,trust_remote_code=True);self.model.eval();self._cache={}
    def _prefix(self,user_text:str)->str:
        messages=[{"role":"user","content":user_text}]
        if getattr(self.tokenizer,"chat_template",None):
            kwargs=dict(tokenize=False,add_generation_prompt=True)
            try:return self.tokenizer.apply_chat_template(messages,enable_thinking=False,**kwargs)
            except TypeError:return self.tokenizer.apply_chat_template(messages,**kwargs)
        return f"USER: {user_text}\nASSISTANT:"
    def _encode_pair(self,prompt:str,candidate:str)->tuple[list[int],int]:
        if not candidate:raise ValueError("candidate cannot be empty")
        prefix=self._prefix(prompt);pids=self.tokenizer(prefix,add_special_tokens=False).input_ids;fids=self.tokenizer(prefix+candidate,add_special_tokens=False).input_ids
        if not pids or len(fids)<=len(pids) or fids[:len(pids)]!=pids:raise ValueError(f"candidate {candidate!r} changes the prompt tokenization boundary; do not silently add whitespace to fix this")
        return fids,len(pids)
    def score_batch(self,requests:Sequence[tuple[str,tuple[str,...]]],*,sequence_batch_size:int=64)->list[ScoreResult]:
        if sequence_batch_size<=0:raise ValueError("sequence_batch_size must be > 0")
        per=[{} for _ in requests];pending={}
        for i,(prompt,cands) in enumerate(requests):
            if len(cands)<2 or len(set(cands))!=len(cands):raise ValueError("each request needs at least two unique candidates")
            for c in cands:
                key=(prompt,c)
                if key in self._cache:per[i][c]=self._cache[key]
                else:pending.setdefault(key,[]).append((i,c))
        flat=[]
        for key,dests in pending.items():ids,pl=self._encode_pair(*key);flat.append((key,dests,ids,pl))
        device=self.model.get_input_embeddings().weight.device;torch=self.torch
        for start in range(0,len(flat),sequence_batch_size):
            chunk=flat[start:start+sequence_batch_size]
            if not chunk:continue
            ml=max(len(x[2]) for x in chunk);idsb=[];masks=[];meta=[]
            for key,dests,ids,pl in chunk:
                pad=ml-len(ids);idsb.append(ids+[self.tokenizer.pad_token_id]*pad);masks.append([1]*len(ids)+[0]*pad);meta.append((key,dests,pl,len(ids)))
            input_ids=torch.tensor(idsb,device=device);attention_mask=torch.tensor(masks,device=device)
            with torch.inference_mode():logits=self.model(input_ids=input_ids,attention_mask=attention_mask).logits
            for ri,(key,dests,pl,sl) in enumerate(meta):
                total=0.0
                for pos in range(pl,sl):total+=float(torch.log_softmax(logits[ri,pos-1].float(),dim=-1)[idsb[ri][pos]].item())
                self._cache[key]=total
                for i,c in dests:per[i][c]=total
        return [ScoreResult(s,softmax_dict(s)) for s in per]
