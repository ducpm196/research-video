import hashlib, sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, e, d = 3233, 17, int(kv.get('d', '2753'))
hmod = lambda s: int(hashlib.sha256(s.encode('utf-8')).hexdigest(), 16) % n
m = hmod(kv['good']); m_bad = hmod(kv['tampered'])
sig = pow(m, d, n); chk = pow(sig, e, n)
print(f'n={n} e={e}')
print(f'sig_matches_digest={int(chk == m)}')
print(f'tamper_detected={int(chk != m_bad)}')
