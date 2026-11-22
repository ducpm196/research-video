n, e, d = 33, 3, 7
m_good = sum(b'bank.vn') % 30 + 2; m_bad = sum(b'evil.vn') % 30 + 2
sig = pow(m_good, d, n); rec = pow(sig, e, n)
print(f'legit_cert_valid={int(rec == m_good)}')
print(f'forged_domain_valid={int(rec == m_bad)}')
print(f'chain_verified={int(rec == m_good and rec != m_bad)}')
