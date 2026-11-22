import math
phi = lambda x, m: math.exp(-0.5 * (x - m) ** 2) / math.sqrt(2 * math.pi)
w1, w2 = 0.5 * phi(1.0, 0.0), 0.5 * phi(1.0, 4.0)
r1 = w1 / (w1 + w2)
r2 = 1.0 - r1
r1_b = 1.0 - r1
mu1_new = (r1 * 1.0 + r1_b * 3.0) / (r1 + r1_b)
print(f"r1={r1:.6f} r2={r2:.6f}")
print(f"sum={r1 + r2:.1f} mu1_new={mu1_new:.4f}")
