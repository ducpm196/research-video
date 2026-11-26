import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
for lbl, n in ((6, kv['n1']), (12, kv['n2'])):
    print(f'n={lbl} allowed={n * (n + 1) // 2}/{n * n}')
