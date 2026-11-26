import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
t, m = kv['total'], kv['ml']; g = t - m
print(f'ml_pct={m/t*100:.1f}% glue_lines={g} glue_pct={g/t*100:.1f}%')
