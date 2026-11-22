import hashlib
nonce = 0
while True:
    d = hashlib.sha256(f"khoi-99:{nonce}".encode()).hexdigest()
    if d.startswith("00"): break
    nonce += 1
print(f"found_nonce={nonce} hash_prefix={d[:6]}")
