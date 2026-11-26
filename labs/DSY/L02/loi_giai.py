import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: tuple(int(x) for x in s.split(','))
def rel(u, v):
    if u == v: return 'equal'
    le = all(a <= b for a, b in zip(u, v))
    ge = all(a >= b for a, b in zip(u, v))
    if le: return 'before'
    return 'after' if ge else 'concurrent'
r1 = rel(p(kv['u1']), p(kv['v1']))
r2 = rel(p(kv['u2']), p(kv['v2']))
print(f'v100_vs_v201={r1}')
print(f'v201_vs_v120={r2}')
print(f'partial_order_ok={int(r1 in ("before", "after", "equal") and r2 == "concurrent")}')
