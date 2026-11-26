import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
sym = lambda a, b: a + b - a * b
wn = sym(kv['w01'], kv['w10']); wc = sym(kv['w12'], kv['w21'])
print(f"w_near_01={wn:.2f} w_cross_12={wc:.4f}")
print(f"keeps_cluster={int(wn > 10 * wc)}")
