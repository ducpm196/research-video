import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: tuple(float(v) for v in s.split(':'))
base = [p(s) for s in kv['pts'].split(',')]; out = p(kv['out'])
def corr(ps):
    mx = sum(x for x, _ in ps) / len(ps); my = sum(y for _, y in ps) / len(ps)
    return sum((x - mx) * (y - my) for x, y in ps) / math.sqrt(sum((x - mx) ** 2 for x, _ in ps) * sum((y - my) ** 2 for _, y in ps))
print(f'r_clean={corr(base):.3f} r_outlier={corr(base + [out]):.3f}')
