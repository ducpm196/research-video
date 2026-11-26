import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
mps = round(kv['daily'] / 86400); bs = kv['msgs'] // kv['batch']
print(f'msgs_per_sec={mps}\nbatches={bs}\nrpc_cut={kv["msgs"] // bs}x')
