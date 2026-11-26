import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
k, a = int(kv['tests']), float(kv['alpha'])
f1 = 1.0 - (1.0 - a) ** k; ab = a / k; f2 = 1.0 - (1.0 - ab) ** k
print(f'raw_fwer={f1:.3f} bonf_alpha={ab:.4f} fwer_bonf={f2:.3f}')
