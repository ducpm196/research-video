import hashlib
exp_sha = hashlib.sha256(b'fw-v2-clean').hexdigest()
b_sha = hashlib.sha256(b'fw-v2').hexdigest()
b_hash_ok = (b_sha == exp_sha)
slot = 'B' if (b_hash_ok and True and True) else 'A'
print(f"b_hash_ok={int(b_hash_ok)} boot_slot={slot}")
