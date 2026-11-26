import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
P = [float(v) for v in kv['p'].split(',')]
Q = [float(v) for v in kv['q'].split(',')]
kl = lambda A, B: sum(a * math.log(a / b) for a, b in zip(A, B) if a > 0)
d1, d2 = kl(P, Q), kl(Q, P)
print(f"KL_PQ={d1:.6f} KL_QP={d2:.6f}")
print(f"asymmetric={int(abs(d1 - d2) > 1e-6)} nonneg={int(d1 >= 0 and d2 >= 0)}")
