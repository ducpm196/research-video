import hashlib
enc = lambda k, b: hashlib.sha256(k + b).digest()[:8]
msg = b'BLOCK_A_' * 2; b0, b1 = msg[:8], msg[8:]; k = b'key'
ecb0, ecb1 = enc(k, b0), enc(k, b1)
ctr0 = bytes(x ^ y for x, y in zip(b0, enc(k, b'nonce0')))
ctr1 = bytes(x ^ y for x, y in zip(b1, enc(k, b'nonce1')))
same_ecb = int(ecb0 == ecb1)
print(f'ecb_blocks_identical={same_ecb}')
print(f'ctr_blocks_identical={int(ctr0 == ctr1)}')
print(f'ecb_leaks_pattern={same_ecb}')
