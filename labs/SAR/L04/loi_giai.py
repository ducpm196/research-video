import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
eff = lambda h: h * kv['cache_ms'] + (1.0 - h) * kv['db_ms']
l1, l2 = eff(kv['h1']), eff(kv['h2'])
print(f'lat_85pct_ms={l1:.2f}\nlat_98pct_ms={l2:.2f}\nspeedup_98={kv["db_ms"] / l2:.1f}x')
