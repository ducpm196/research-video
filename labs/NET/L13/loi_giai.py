p, g, a, b = 23, 5, 6, 15
A = pow(g, a, p); B = pow(g, b, p)
ka = pow(B, a, p); kb = pow(A, b, p)
print(f'A={A} B={B}')
print(f'shared_alice={ka} shared_bob={kb}')
print(f'keys_match={int(ka == kb)}')
