import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: [float(x) for x in s.split(',')]; q = p(kv['q'])
docs = {it.split(':')[0]: p(it.split(':')[1]) for it in kv['docs'].split(';')}
cos = lambda u, v: sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))
best = max(docs, key=lambda k: cos(q, docs[k])); r1 = float(best == kv['relevant'])
print(f'top1={best} cos={cos(q, docs[best]):.3f} recall_at_1={r1:.1f}')
