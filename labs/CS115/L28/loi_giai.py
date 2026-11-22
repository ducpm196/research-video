import math
ent = lambda a, b: -sum((x / (a + b)) * math.log(x / (a + b)) for x in (a, b) if x > 0)
gini = lambda a, b: 1.0 - (a / (a + b)) ** 2 - (b / (a + b)) ** 2
h0 = ent(5, 5)
h_after = 0.5 * ent(4, 1) + 0.5 * ent(1, 4)
ig = h0 - h_after
print(f"H_root={h0:.3f} H_split={h_after:.4f}")
print(f"info_gain={ig:.4f} gini_root={gini(5, 5):.2f}")
