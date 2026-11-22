import math
p = 0.65
maj7 = sum(
    math.comb(7, k) * (p ** k) * ((1 - p) ** (7 - k))
    for k in range(4, 8)
)
print(f"single={p:.3f} maj7_indep={maj7:.3f}")
