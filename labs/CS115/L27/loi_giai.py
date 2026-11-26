import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: tuple(float(v) for v in s.split(','))
A, B, Q, S = p(kv['a']), p(kv['b']), p(kv['q']), p(kv['scale'])
dist = lambda u, v: math.hypot(u[0] - v[0], u[1] - v[1])
sc = lambda pt: (pt[0] / S[0], pt[1] / S[1])
print(f"raw_dQA={dist(Q, A):.1f} raw_dQB={dist(Q, B):.2f}")
print(f"norm_dQA={dist(sc(Q), sc(A)):.3f} norm_dQB={dist(sc(Q), sc(B)):.3f}")
