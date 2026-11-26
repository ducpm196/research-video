import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
a, b, q = float(kv['a']), float(kv['b']), float(kv['q'])
pr = b / (a + b); pp = (b ** 0.75) / (a ** 0.75 + b ** 0.75); cr = -math.log(q)
print(f'raw_B={pr:.3f} pow075_B={pp:.3f} logq_corr={cr:.3f}')
