import math, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = lambda s: [float(x) for x in s.split(',')]
u, v, w = p(kv['u']), p(kv['v']), p(kv['w'])
cos = lambda a, b: sum(x * y for x, y in zip(a, b)) / (math.hypot(*a) * math.hypot(*b))
c1, c2 = cos(u, v), cos(u, w); pred = (c1 * v[2] + c2 * w[2]) / (c1 + c2)
print(f'cosUV={c1:.3f} cosUW={c2:.3f} pred_u3={pred:.2f}')
