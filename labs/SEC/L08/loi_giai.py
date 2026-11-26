import hashlib, hmac, sys
lines = [ln.strip() for ln in sys.stdin.read().splitlines() if ln.strip()]
kv = dict(ln.split('=', 1) for ln in lines)
k = kv['key'].encode(); alg = kv['alg']
tag = hmac.new(k, kv['msg'].encode(), alg).hexdigest()
t2 = hmac.new(k, kv['tampered'].encode(), alg).hexdigest()
print(f'mac_len_hex={len(tag)}')
print(f'orig_valid={int(hmac.compare_digest(tag, tag))}')
print(f'tampered_valid={int(hmac.compare_digest(tag, t2))}')
