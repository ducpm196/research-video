p = lambda n: n * (n - 1) // 2
p8, p40 = p(8), p(40)
red = 100 * (p40 - 40) / p40
print(f'p2p_8={p8} bus_8=8')
print(f'p2p_40={p40} bus_40=40')
print(f'reduction_40={red:.1f}%')
