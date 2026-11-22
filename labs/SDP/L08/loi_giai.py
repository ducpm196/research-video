sing = [0]
def bump_s(): sing[0] += 1; return sing[0]
def bump_new(): c = [0]; c[0] += 1; return c[0]
sa, sb = bump_s(), bump_s()
ia, ib = bump_new(), bump_new()
print(f'singleton_a_then_b={sa},{sb}')
print(f'isolated_a_then_b={ia},{ib}')
print(f'order_leak={int(sb != ia)}')
