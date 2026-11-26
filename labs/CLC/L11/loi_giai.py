import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
daz, az_av = int(kv['db_az']), float(kv['az_av'])
mn, mx = int(kv['min_app']), int(kv['max_app'])
av = 1.0 - (1.0 - az_av) ** daz; ok = int(daz >= 2 and mn >= 2)
print(f'multi_az_avail={100 * av:.6f}%\napp_bounds={mn},{mx}\nspof_cleared={ok}\npillars=6')
