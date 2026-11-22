import math
p = 1.0 / (1.0 + math.exp(-1.5))
loss = -math.log(p)
print(f"bt_prob={p:.3f} bt_loss={loss:.3f}")
