import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
mx = kv['total'] - kv['min_h']
print(f'max_removable={mx} req={kv["req"]} blocked={int(kv["req"] > mx)}')
