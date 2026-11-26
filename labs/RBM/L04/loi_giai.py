import sys, math
s = sys.stdin.read().strip() or "1.2 0.8 45.0 45.0"
L1, L2, a1, a2 = map(float, s.split())
t1, t2 = math.radians(a1), math.radians(a2)
x = L1 * math.cos(t1) + L2 * math.cos(t1 + t2)
y = L1 * math.sin(t1) + L2 * math.sin(t1 + t2)
dist = math.hypot(x, y)
print(f"end=({x:.3f}, {y:.3f}) dist={dist:.3f}")
