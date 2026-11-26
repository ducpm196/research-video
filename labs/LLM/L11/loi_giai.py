import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p, m = float(kv['p']), int(kv['trials']); maj = sum(math.comb(m, k) * (p ** k) * ((1 - p) ** (m - k)) for k in range(m // 2 + 1, m + 1))
print(f'single={p:.3f} maj7_indep={maj:.3f}')
