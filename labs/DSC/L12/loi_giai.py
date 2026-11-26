import math, sys
r = float(sys.stdin.read().split('=')[1])
vif = 1.0 / (1.0 - r * r); se = math.sqrt(vif)
print(f'r={r:.1f} VIF={vif:.2f} se_inflation={se:.2f}x')
