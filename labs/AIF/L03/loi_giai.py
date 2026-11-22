lo, hi = 1.0, 5.0
for _ in range(50):
    mid = (lo + hi) / 2.0
    val = sum(mid**k for k in range(5))
    if val < 101.0: lo = mid
    else: hi = mid
print(f"b_star={mid:.4f} sum_val={sum(mid**k for k in range(5)):.2f}")
