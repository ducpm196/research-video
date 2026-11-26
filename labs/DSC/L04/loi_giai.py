import sys
xs = sorted(float(x) for x in sys.stdin.read().strip().split('=', 1)[1].split(','))
n = len(xs); mn = sum(xs) / n
med_f = lambda a: a[len(a)//2] if len(a)%2 else (a[len(a)//2-1]+a[len(a)//2])/2.0
med = med_f(xs); lo, hi = xs[:n // 2], xs[(n + 1) // 2:]
q1, q3 = med_f(lo), med_f(hi); fence = q3 + 1.5 * (q3 - q1)
print(f'mean={mn:.1f} median={med:.1f} fence={fence:.1f} outlier={int(max(xs) > fence)}')
