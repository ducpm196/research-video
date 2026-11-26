import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
decl = lambda cur, target=kv['target']: target
imp = lambda cur, delta=kv['delta']: cur + delta
d1 = decl(decl(kv['init']))
i2 = imp(imp(kv['init']))
print(f'decl_after_2_runs={d1}')
print(f'imp_after_2_runs={i2}')
print(f'decl_is_idempotent={int(decl(d1) == d1)}')
