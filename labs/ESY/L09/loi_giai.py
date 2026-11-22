import math
tasks = [(1, 5), (2, 8), (2, 16)]
u = sum(c / p for c, p in tasks)
ll = 3 * (2**(1/3) - 1)
r = 2
for _ in range(10): r = 2 + sum(math.ceil(r / p) * c for c, p in tasks[:2])
print(f"U={u:.3f} LL_bound={ll:.4f} exact_R3={r}")
