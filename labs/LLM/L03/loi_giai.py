import math
cos = lambda u, v: (
    sum(a * b for a, b in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))
)
c1 = cos((2, 1, 0), (3, 2, 1))
c2 = cos((2, 1, 0), (-1, 2, 0))
print(f"cos_sim={c1:.3f} cos_orth={c2:.1f}")
