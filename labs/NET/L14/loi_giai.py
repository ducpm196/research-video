import hashlib
n, d, e, m = 33, 7, 3, 4
sig = pow(m, d, n); chk = pow(sig, e, n)
h = hashlib.sha256(b'TLS').hexdigest()
print(f'sig={sig} verify={chk}')
print(f'valid={int(chk == m)}')
print(f'sha256_hex_len={len(h)}')
