import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p, n = kv['p'], int(kv['layers'])
print(f'indep_pct={(p ** n) * 100:.2f}% shared_pct={p * 100:.1f}%')
