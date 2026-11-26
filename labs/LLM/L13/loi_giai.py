import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
sc = kv['n_new'] // kv['n_old']; print(f'kv_mult={sc}x attn_flops_mult={sc ** 2}x')
