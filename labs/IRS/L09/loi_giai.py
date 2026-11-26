import math, sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
st = lambda a, b: (a / (a + b), math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1))))
m1, s1 = st(kv['a1'], kv['b1']); m2, s2 = st(kv['a2'], kv['b2'])
print(f'new_mean={m1:.2f} new_sd={s1:.3f}\nold_mean={m2:.4f} old_sd={s2:.4f}')
