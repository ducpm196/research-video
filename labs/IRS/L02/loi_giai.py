import math, sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(ln.split('=', 1) for ln in lines)
docs = [kv['d1'], kv['d2'], kv['d3']]
vocab = sorted({w for d in docs for w in d.split()} | set(kv['q'].split()))
df = {w: sum(1 for d in docs if w in d.split()) for w in vocab}
idf = {w: (math.log(len(docs) / df[w]) if df[w] else 0.0) for w in vocab}
vec = lambda s: [s.split().count(w) * idf[w] for w in vocab]
cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
vq, v2, v3 = vec(kv['q']), vec(docs[1]), vec(docs[2])
print(f'idf_xe={idf[kv["w1"]]:.1f} idf_dien={idf[kv["w2"]]:.3f} cos_d2={cos(vq, v2):.3f} cos_d3={cos(vq, v3):.3f}')
