import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, base, step = int(kv['n']), float(kv['base']), float(kv['step'])
d = [base + (i % 5 - 2) * step for i in range(n)]
m = sum(d) / n
sd = math.sqrt(sum((x - m) ** 2 for x in d) / (n - 1))
se = sd / math.sqrt(n)
hw = 2.045 * se
print(f'n={n} mean={m:.2f}')
print(f'sd={sd:.3f} se={se:.3f}')
print(f'ci95={m - hw:.2f},{m + hw:.2f}')
