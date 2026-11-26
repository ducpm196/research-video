import sys, hashlib
s = sys.stdin.read().strip() or "khoi-99 00"
prefix, target = s.split()
nonce = 0
while True:
    d = hashlib.sha256(f"{prefix}:{nonce}".encode()).hexdigest()
    if d.startswith(target): break
    nonce += 1
print(f"found_nonce={nonce} hash_prefix={d[:6]}")
