import hashlib, hmac
k = b'secret'
tag = hmac.new(k, b'chuyen 100', hashlib.sha256).hexdigest()
t2 = hmac.new(k, b'chuyen 900', hashlib.sha256).hexdigest()
print(f'mac_len_hex={len(tag)}')
print(f'orig_valid={int(hmac.compare_digest(tag, tag))}')
print(f'tampered_valid={int(hmac.compare_digest(tag, t2))}')
