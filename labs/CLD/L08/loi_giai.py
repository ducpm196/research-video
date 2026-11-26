import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n = int(kv['n']); u, s = float(kv['unavail']), float(kv['surge'])
print(f'min_ready={n - math.floor(n * u)}\nmax_total={n + math.ceil(n * s)}')
