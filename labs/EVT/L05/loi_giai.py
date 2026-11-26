import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
w, p, t = kv['w'], kv['p'], kv['secs']
bl = (w - p) * t
print(f'backlog={bl}\ndata_lag_s={bl / w:.1f}\ndrain_with_2_s={bl / (2 * p - w):.1f}')
