import hashlib, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, d, e, m = int(kv['n']), int(kv['d']), int(kv['e']), int(kv['m'])
sig = pow(m, d, n); chk = pow(sig, e, n)
h = hashlib.sha256(kv['tag'].encode()).hexdigest()
print(f'sig={sig} verify={chk}')
print(f'valid={int(chk == m)}')
print(f'sha256_hex_len={len(h)}')
