import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: tuple(float(x) for x in s.split(','))
cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
u, v, w = p(kv['u']), p(kv['v']), p(kv['w'])
print(f'cos_sim={cos(u, v):.3f} cos_orth={cos(u, w):.1f}')
