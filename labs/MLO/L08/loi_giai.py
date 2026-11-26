import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
exp = [float(x) for x in kv['exp'].split(',')]; cur = [float(x) for x in kv['cur'].split(',')]
psi = sum((c - e) * math.log(c / e) for e, c in zip(exp, cur))
print(f'psi={psi:.3f} alert_moderate={int(0.1 <= psi < 0.25)}')
