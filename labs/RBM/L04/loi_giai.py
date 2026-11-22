import math
L1, L2 = 1.2, 0.8
t1, t2 = math.radians(45.0), math.radians(45.0)
x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)
y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)
dist = math.hypot(x, y)
print(f"end=({x:.3f}, {y:.3f}) dist={dist:.3f}")
