import math, sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p1, p2 = kv['p1'], kv['p2']; pb = (p1 + p2) / 2.0
za, zb = 1.959963984540054, 0.8416212335729143
s1 = za * math.sqrt(2 * pb * (1 - pb)); s2 = zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))
print(f'n_per_group={math.ceil(((s1 + s2) / (p2 - p1)) ** 2)}')
