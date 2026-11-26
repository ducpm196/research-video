import sys
kv = {k: int(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
p = lambda n: n * (n - 1) // 2; n1, n2 = kv['n1'], kv['n2']
p1, p2 = p(n1), p(n2); red = 100 * (p2 - n2) / p2
print(f'p2p_8={p1} bus_8={n1}')
print(f'p2p_40={p2} bus_40={n2}')
print(f'reduction_40={red:.1f}%')
