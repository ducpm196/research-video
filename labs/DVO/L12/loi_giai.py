import hashlib
n, e, d = 3233, 17, 2753
m = int(hashlib.sha256(b'release-v1.0').hexdigest(), 16) % n
sig = pow(m, d, n); chk = pow(sig, e, n)
m_bad = int(hashlib.sha256(b'release-tampered').hexdigest(), 16) % n
print(f'n={n} e={e}')
print(f'sig_matches_digest={int(chk == m)}')
print(f'tamper_detected={int(chk != m_bad)}')
