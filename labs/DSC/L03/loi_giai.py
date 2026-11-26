import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
orig = [float(x) for x in kv['orig'].split(',')]; k = int(kv['add'])
var = lambda xs: sum((x - sum(xs) / len(xs)) ** 2 for x in xs) / (len(xs) - 1)
mn = sum(orig) / len(orig); imp = orig + [mn] * k
print(f'orig_var={var(orig):.3f} mean_imputed_var={var(imp):.3f}')
