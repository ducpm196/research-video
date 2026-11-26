import sys, hashlib
sys.stdin.reconfigure(encoding="utf-8")
s = sys.stdin.read().strip() or "3233 17 2753|A trả B 15|A trả B 150"
ks, m1, m2 = s.split("|", 2)
n, e, d = map(int, ks.split())
h_mod = lambda t: int(hashlib.sha256(t.encode("utf-8")).hexdigest(), 16) % n
m = h_mod(m1)
sig = pow(m, d, n)
ok_orig = pow(sig, e, n) == m
ok_tampered = pow(sig, e, n) == h_mod(m2)
print(f"sig_valid={int(ok_orig)} tampered_valid={int(ok_tampered)}")
