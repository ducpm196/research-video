import hashlib, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
enc = lambda k, b: hashlib.sha256(k + b).digest()[:8]
b0, b1 = kv['b0'].encode(), kv['b1'].encode(); k = b'key'
ecb0, ecb1 = enc(k, b0), enc(k, b1)
ctr0 = bytes(x ^ y for x, y in zip(b0, enc(k, kv['n0'].encode())))
ctr1 = bytes(x ^ y for x, y in zip(b1, enc(k, kv['n1'].encode())))
same_ecb = int(ecb0 == ecb1)
print(f'ecb_blocks_identical={same_ecb}')
print(f'ctr_blocks_identical={int(ctr0 == ctr1)}')
print(f'ecb_leaks_pattern={same_ecb}')
