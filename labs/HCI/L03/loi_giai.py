import math
t_flat = 0.18 * math.log2(24 + 1)
t_2lvl = 0.18 * math.log2(4 + 1) + 0.18 * math.log2(6 + 1)
print(f"flat_24={t_flat:.3f}s two_level={t_2lvl:.3f}s")
