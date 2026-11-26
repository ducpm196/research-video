import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
h, s = kv['hist_days'], kv['speed']
print(f'naive_days={h / s:.1f}\nreal_catchup_days={h / (s - 1.0):.1f}')
