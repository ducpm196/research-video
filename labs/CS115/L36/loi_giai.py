import math
eps = 0.2
alpha = 0.5 * math.log((1.0 - eps) / eps)
y, f, lr = 10.0, 0.0, 0.5
for _ in range(2):
    f += lr * (y - f)
print(f"adaboost_alpha={alpha:.4f}")
print(f"gbdt_f2={f:.2f} rem={y - f:.2f}")
