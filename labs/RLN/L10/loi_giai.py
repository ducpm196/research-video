import math
p = 1.0 / (1.0 + math.exp(-1.5))
loss = -math.log(p)
pen_r = 3.0 - 0.2 * math.log(0.9 / 0.3)
print(f"prob={p:.3f} loss={loss:.3f} kl_adj_r={pen_r:.3f}")
