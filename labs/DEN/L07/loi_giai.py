import math, sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
docs = {}
for ln in lines[:-1]:
    i_s, txt = ln.split(':', 1); docs[int(i_s)] = txt
kv = dict(t.split('=') for t in lines[-1].split())
q, tid = kv['query'], int(kv['target'])
post = sorted(i for i, t in docs.items() if q in t.split())
avgdl = sum(len(t.split()) for t in docs.values()) / len(docs)
N, df, dl = len(docs), len(post), len(docs[tid].split())
idf = math.log((N - df + 0.5) / (df + 0.5) + 1.0)
tf = docs[tid].split().count(q)
score = idf * (tf * 2.2) / (tf + 1.2 * (1 - 0.75 + 0.75 * dl / avgdl))
print(f'docs_with_nhanh={post}\nbm25_doc1={score:.4f}')
