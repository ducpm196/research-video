import sys, hashlib
s = sys.stdin.read().strip() or "fw-v2-clean|fw-v2|1"
exp_txt, got_txt, sig_s = s.split("|", 2)
b_hash_ok = hashlib.sha256(got_txt.encode()).hexdigest() == hashlib.sha256(exp_txt.encode()).hexdigest()
slot = "B" if (b_hash_ok and int(sig_s) == 1) else "A"
print(f"b_hash_ok={int(b_hash_ok)} boot_slot={slot}")
