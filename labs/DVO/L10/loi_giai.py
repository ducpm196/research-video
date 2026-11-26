import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
av = lambda m, r: 100 * m / (m + r)
print(f'avail_1h={av(kv["mtbf"], kv["mttr_slow"]):.3f}%')
print(f'avail_15m={av(kv["mtbf"], kv["mttr_fast"]):.3f}%')
print(f'downtime_cut_factor={kv["mttr_slow"] / kv["mttr_fast"]:.1f}x')
