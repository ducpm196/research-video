import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = [float(x) for x in kv['p'].split(',')]; q = [float(x) for x in kv['q'].split(',')]
r, eta, lam = float(kv['r']), float(kv['eta']), float(kv['lam'])
err = r - sum(a * b for a, b in zip(p, q))
p0 = [round(pi + eta * err * qi, 4) for pi, qi in zip(p, q)]
pr = [round(pi + eta * (err * qi - lam * pi), 4) for pi, qi in zip(p, q)]
print(f'err={err:.1f} p_raw={p0} p_reg={pr}')
