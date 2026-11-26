import hashlib, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
dk = hashlib.pbkdf2_hmac('sha256', kv['pw'].encode(), kv['salt'].encode(), int(kv['iter'])).hex()
space = int(kv['alpha']) ** int(kv['length'])
fast = space / float(kv['fast']); slow_d = space / (float(kv['slow']) * 86400)
print(f'fast_crack_s={fast:.1f}')
print(f'slow_crack_days={round(slow_d)}')
print(f'pbkdf2_hex_len={len(dk)}')
