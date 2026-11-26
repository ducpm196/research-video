import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
l2 = kv['l2_hit'] + kv['l2_miss'] * kv['ram']
tot = kv['l1_hit'] + kv['l1_miss'] * l2
print(f'l2_amat_ns={l2:.1f}')
print(f'total_amat_ns={tot:.2f}')
print(f'locality_speedup_vs_ram={kv["ram"] / tot:.1f}')
