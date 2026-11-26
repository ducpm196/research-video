import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p, g, a, b = kv['p'], kv['g'], kv['a'], kv['b']
A = pow(g, a, p); B = pow(g, b, p)
ka = pow(B, a, p); kb = pow(A, b, p)
print(f'A={A} B={B}')
print(f'shared_alice={ka} shared_bob={kb}')
print(f'keys_match={int(ka == kb)}')
