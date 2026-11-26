import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
l1, l0 = (int(v) for v in kv['left'].split(','))
r1, r0 = (int(v) for v in kv['right'].split(','))
ent = lambda a, b: (-sum((x / (a + b)) * math.log(x / (a + b)) for x in (a, b) if x > 0)) + 0.0
gini = lambda a, b: 1.0 - (a / (a + b)) ** 2 - (b / (a + b)) ** 2
tot = l1 + l0 + r1 + r0
h0 = ent(l1 + r1, l0 + r0)
h_after = ((l1 + l0) / tot) * ent(l1, l0) + ((r1 + r0) / tot) * ent(r1, r0)
print(f"H_root={h0:.3f} H_split={h_after:.4f}")
print(f"info_gain={h0 - h_after:.4f} gini_root={gini(l1 + r1, l0 + r0):.2f}")
