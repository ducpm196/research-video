import math
l = 0.0
for p in [0.75, 0.75, 0.75, 0.75, 0.35]:
    l += math.log(p / (1.0 - p))
prob = 1.0 / (1.0 + math.exp(-l))
print(f"log_odds={l:.3f} prob={prob:.3f}")
