import hashlib, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
h = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
h1, h2, h3 = h(kv['b1']), h(kv['b2']), h(kv['b3'])
print(f'same_artifact_same_hash={int(h1 == h2)}')
print(f'changed_byte_different_hash={int(h1 != h3)}')
print(f'sha256_len_hex={len(h1)}')
