import math
r = 0.8
vif = 1.0 / (1.0 - r * r)
se_mult = math.sqrt(vif)
print(f"r={r:.1f} VIF={vif:.2f} se_inflation={se_mult:.2f}x")
