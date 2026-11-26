import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
nv = (kv['ma'] + kv['mb']) / 2.0; wt = (kv['na'] * kv['ma'] + kv['nb'] * kv['mb']) / (kv['na'] + kv['nb'])
print(f'naive={nv:.2f} weighted={wt:.2f}')
