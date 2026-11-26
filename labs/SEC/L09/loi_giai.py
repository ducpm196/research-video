import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
n, e, d = 33, 3, 7
h = lambda s: sum(s.encode()) % 30 + 2
ms = h(kv.get('signed', kv.get('good', '')))
mg = h(kv.get('presented', kv.get('good', '')))
mb = h(kv['bad'])
sig = pow(ms, d, n); rec = pow(sig, e, n)
print(f'legit_cert_valid={int(rec == mg)}')
print(f'forged_domain_valid={int(rec == mb)}')
print(f'chain_verified={int(rec == mg and rec != mb)}')
