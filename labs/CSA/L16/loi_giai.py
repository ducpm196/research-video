import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p = kv['p']; s = 1.0 - p
sp = 1.0 / (s + p / int(kv['cores'])); lim = 1.0 / s
print(f'speedup_8cores_p85={sp:.2f}')
print(f'limit_inf={lim:.2f}')
print(f'cache_timing_ratio={kv["miss_ns"] / kv["hit_ns"]:.1f}x')
