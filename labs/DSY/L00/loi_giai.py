import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
loc = kv['calls'] * kv['local_ms']
wan = kv['calls'] * kv['wan_ms']
print(f'local_20_rpcs_ms={loc:.1f}')
print(f'cross_continent_20_rpcs_ms={wan:.1f}')
print(f'slowdown_factor={round(wan / loc)}x')
