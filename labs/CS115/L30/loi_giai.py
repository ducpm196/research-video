import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
phi = lambda x, m: math.exp(-0.5 * (x - m) ** 2) / math.sqrt(2 * math.pi)
p1 = kv['w'] * phi(kv['x'], kv['m1']); p2 = (1.0 - kv['w']) * phi(kv['x'], kv['m2'])
r1 = p1 / (p1 + p2); r2 = 1.0 - r1
p1_b = kv['w'] * phi(kv['x2'], kv['m1']); p2_b = (1.0 - kv['w']) * phi(kv['x2'], kv['m2'])
r1_b = p1_b / (p1_b + p2_b)
mu1_new = (r1 * kv['x'] + r1_b * kv['x2']) / (r1 + r1_b)
print(f"r1={r1:.6f} r2={r2:.6f}")
print(f"sum={r1 + r2:.1f} mu1_new={mu1_new:.4f}")
