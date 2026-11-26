import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
lim = kv['limit_mib'] * 1024 * 1024; mx = lim // kv['item_b']
print(f'max_embedded={mx}\nbytes_if_exceed={(mx + 1) * kv["item_b"]}')
