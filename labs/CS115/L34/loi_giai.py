import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
out_sz = (kv['n'] - kv['k'] + 2 * kv['p']) // kv['s'] + 1
params = (kv['k'] * kv['k'] * kv['cin'] + 1) * kv['cout']
dense = out_sz * out_sz * kv['cout']
print(f"out_dim={out_sz}x{out_sz}x{kv['cout']}={dense}")
print(f"conv_params={params}")
