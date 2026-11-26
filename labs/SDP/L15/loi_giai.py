import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
I = lambda ca, ce: ce / (ca + ce)
ic = I(kv['ca1'], kv['ce1'])
ie = I(kv['ca2'], kv['ce2'])
print(f'core_I={ic:.2f}')
print(f'edge_I={ie:.2f}')
print(f'valid_dep_dir={int(ie >= ic)}')
