import math
stat = lambda a, b: (
    a / (a + b), math.sqrt(a * b / ((a + b) ** 2 * (a + b + 1)))
)
m1, s1 = stat(1, 1)
m2, s2 = stat(31, 471)
print(f"new_mean={m1:.2f} new_sd={s1:.3f}")
print(f"old_mean={m2:.4f} old_sd={s2:.4f}")
