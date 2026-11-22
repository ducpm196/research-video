import hashlib
n, e, d = 3233, 17, 2753
h_mod = lambda s: int(hashlib.sha256(s.encode()).hexdigest(), 16) % n
m = h_mod("A trả B 15")
sig = pow(m, d, n)
ok_orig = (pow(sig, e, n) == m)
ok_tampered = (pow(sig, e, n) == h_mod("A trả B 150"))
print(f"sig_valid={int(ok_orig)} tampered_valid={int(ok_tampered)}")
