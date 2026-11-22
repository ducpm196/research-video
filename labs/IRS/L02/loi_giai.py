import math
docs = ['xe dap nhanh', 'xe dien ben', 'xe dien dep']
vocab = ['xe', 'dap', 'nhanh', 'dien', 'ben', 'dep']
df = {w: sum(1 for d in docs if w in d.split()) for w in vocab}
idf = {w: math.log(len(docs) / df[w]) for w in vocab}
vec = lambda s: [s.split().count(w) * idf[w] for w in vocab]
cos = lambda a, b: (
    sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
)
vq, vd2, vd3 = vec('xe dien'), vec(docs[1]), vec(docs[2])
print(f"idf_xe={idf['xe']:.1f} idf_dien={idf['dien']:.3f}",
      f"cos_d2={cos(vq, vd2):.3f} cos_d3={cos(vq, vd3):.3f}")
