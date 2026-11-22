import math
x, h = 1.0, 0.05
for _ in range(20): x += h * (-2.0 * x)
exact = math.exp(-2.0)
print(f"euler={x:.4f} exact={exact:.4f} err={abs(x - exact):.4f}")
