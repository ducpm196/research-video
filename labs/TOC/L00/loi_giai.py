from itertools import product
chains = [''.join(p) for k in range(5) for p in product('01', repeat=k)]
nonempty = [s for s in chains if len(s) > 0]
print(f"count_le4={len(chains)} nonempty={len(nonempty)}")
