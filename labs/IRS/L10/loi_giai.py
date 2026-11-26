import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
print(f'ips_rel_pos1={kv["c1"]/kv["e1"]:.3f} ips_rel_pos4={kv["c2"]/kv["e2"]:.3f}')
