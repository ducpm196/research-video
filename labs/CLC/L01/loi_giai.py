import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
p = float(kv['p_fail']); z1, z2 = int(kv['z1']), int(kv['z2'])
a1, a2 = 1.0 - p ** z1, 1.0 - p ** z2; dt = (1.0 - a1) * 525600
print(f'az2_avail_pct={100 * a1:.4f}%\naz3_avail_pct={100 * a2:.4f}%\naz2_downtime_min_year={dt:.1f}')
