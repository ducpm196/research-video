import math
fitts = lambda D, W: 0.1 + 0.15 * math.log2(D / W + 1.0)
ratio = (48 * 48) / (28 * 28)
print(f"area_ratio={ratio:.2f}x t_28px={fitts(300, 28):.3f}s t_48px={fitts(300, 48):.3f}s")
