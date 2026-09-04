#!/usr/bin/env python3
"""Test whether document boundaries selectively impair multi-hop composition.

The evidence sentences, their order, and their text are identical.  Only the
container label changes: one document with sections vs multiple documents.
"""
import argparse, json, re, unicodedata, urllib.request
from pathlib import Path

import pyarrow as pa
import pyarrow.ipc as ipc


def norm(s):
    s = unicodedata.normalize("NFKD", s).lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return " ".join(s.split())


def correct(text, answers):
    t = norm(text)
    return any(norm(a) and norm(a) in t for a in answers)


def call(url, model, prompt):
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0, "max_tokens": 48,
        "chat_template_kwargs": {"enable_thinking": False},
    }
    req = urllib.request.Request(url + "/v1/chat/completions",
        data=json.dumps(body).encode(), headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.load(r)["choices"][0]["message"]["content"]


def load_rows(path, n):
    with pa.memory_map(path, "r") as f:
        rows = ipc.open_stream(f).read_all().to_pylist()
    out, seen = [], set()
    for r in rows:
        if not r["answerable"] or r["id"] in seen: continue
        supp = sorted((p for p in r["paragraphs"] if p["is_supporting"]), key=lambda p:p["idx"])
        if len(supp) not in (2, 3, 4): continue
        seen.add(r["id"]); out.append((r, supp))
        if len(out) >= n: break
    return out


def context(supp, mode):
    chunks=[]
    if mode == "one_document":
        chunks.append("DOCUMENT: Evidence file")
        for i,p in enumerate(supp,1):
            chunks.append(f"Section {i}: {p['title']}\n{p['paragraph_text']}")
    elif mode == "many_documents":
        for i,p in enumerate(supp,1):
            chunks.append(f"DOCUMENT {i}: {p['title']}\n{p['paragraph_text']}")
    elif mode == "bare":
        for p in supp: chunks.append(p["paragraph_text"])
    return "\n\n".join(chunks)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--data", required=True); ap.add_argument("--url", required=True)
    ap.add_argument("--model", required=True); ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--out", required=True)
    a=ap.parse_args(); rows=load_rows(a.data,a.n)
    modes=["bare","one_document","many_documents"]
    rec=[]
    for j,(r,supp) in enumerate(rows):
        answers=[r["answer"]]+(r["answer_aliases"] or [])
        item={"id":r["id"],"hops":len(supp),"question":r["question"],"answer":r["answer"]}
        for mode in modes:
            prompt=("Answer the question using only the evidence. Give only the short answer.\n\n"
                    +context(supp,mode)+"\n\nQUESTION: "+r["question"]+"\nANSWER:")
            ans=call(a.url,a.model,prompt)
            item[mode]={"output":ans,"correct":correct(ans,answers)}
        rec.append(item)
        if (j+1)%20==0:
            rates={m:sum(x[m]["correct"] for x in rec)/len(rec) for m in modes}
            print(j+1,rates,flush=True)
    out={"model":a.model,"n":len(rec),"records":rec}
    out["accuracy"]={m:sum(x[m]["correct"] for x in rec)/len(rec) for m in modes}
    for h in (2,3,4):
        z=[x for x in rec if x["hops"]==h]
        out[f"accuracy_{h}hop"]={m:(sum(x[m]["correct"] for x in z)/len(z) if z else None) for m in modes}
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2))
    print(json.dumps({k:v for k,v in out.items() if k!="records"},indent=2))

if __name__=="__main__": main()
