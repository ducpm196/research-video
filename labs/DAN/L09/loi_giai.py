import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
xs = sorted(float(x) for x in kv['xs'].split(',')); tgt = float(kv['target']); n = len(xs)
med_fn = lambda arr: arr[len(arr)//2] if len(arr)%2 else (arr[len(arr)//2-1]+arr[len(arr)//2])/2.0
mn = sum(xs) / n; sd = math.sqrt(sum((x - mn) ** 2 for x in xs) / n)
med = med_fn(xs); mad = med_fn(sorted(abs(x - med) for x in xs)); nm = 1.4826 * mad
print(f'z_classical={(tgt - mn) / sd:.2f} z_robust={(tgt - med) / nm:.1f}')
