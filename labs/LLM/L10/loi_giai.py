import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p, n = float(kv['p']), int(kv['n']); me = 1.96 * math.sqrt(p * (1 - p) / n) * 100
print(f'acc={p * 100:.1f}% margin_pp={me:.2f}')
