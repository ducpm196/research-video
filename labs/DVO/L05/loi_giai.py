decl = lambda cur, target=5: target
imp = lambda cur, delta=2: cur + delta
d1 = decl(decl(3)); i2 = imp(imp(3))
print(f'decl_after_2_runs={d1}')
print(f'imp_after_2_runs={i2}')
print(f'decl_is_idempotent={int(decl(d1) == d1)}')
