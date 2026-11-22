import math
kl = lambda P, Q: sum(p * math.log(p / q) for p, q in zip(P, Q))
P, Q = [0.7, 0.3], [0.4, 0.6]
d1, d2 = kl(P, Q), kl(Q, P)
print(f"KL_PQ={d1:.6f} KL_QP={d2:.6f}")
print(f"asymmetric={int(abs(d1 - d2) > 1e-3)} nonneg={int(d1 >= 0)}")
