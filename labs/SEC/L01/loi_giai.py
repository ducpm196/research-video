import hashlib
dk = hashlib.pbkdf2_hmac('sha256', b'pw', b'salt1', 10000).hex()
fast = (26 ** 8) / 1e10; slow_d = (26 ** 8) / (1e4 * 86400)
print(f'fast_crack_s={fast:.1f}')
print(f'slow_crack_days={round(slow_d)}')
print(f'pbkdf2_hex_len={len(dk)}')
