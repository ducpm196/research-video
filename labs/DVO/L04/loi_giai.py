import hashlib
h = lambda b: hashlib.sha256(b).hexdigest()
h1, h2, h3 = h(b'app-v1.4.2'), h(b'app-v1.4.2'), h(b'app-v1.4.3')
print(f'same_artifact_same_hash={int(h1 == h2)}')
print(f'changed_byte_different_hash={int(h1 != h3)}')
print(f'sha256_len_hex={len(h1)}')
