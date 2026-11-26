import sys, math
s = sys.stdin.read().strip() or "0.1 0.15 360 18 72"
a, b, D, W1, W2 = map(float, s.split())
id_fn = lambda W: math.log2(D / W + 1.0)
t_fn = lambda idv: a + b * idv
id1, id2 = id_fn(W1), id_fn(W2)
print(f"id_18={id1:.3f} t_18px={t_fn(id1):.3f}s id_72={id2:.3f} t_72px={t_fn(id2):.3f}s")
