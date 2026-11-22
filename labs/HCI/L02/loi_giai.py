import math
id_fn = lambda D, W: math.log2(D / W + 1.0)
t_fn = lambda idv: 0.1 + 0.15 * idv
id1, id2 = id_fn(360, 18), id_fn(360, 72)
print(f"id_18={id1:.3f} t_18px={t_fn(id1):.3f}s id_72={id2:.3f} t_72px={t_fn(id2):.3f}s")
