import sys, math
s = sys.stdin.read().strip() or "7.0 2.0"
zc, R = map(float, s.split())
b, c = -2.0 * zc, zc * zc - R * R
disc = math.sqrt(b*b - 4.0*c)
t1, t2 = (-b - disc) / 2.0, (-b + disc) / 2.0
print(f"hits=({t1:.1f}, {t2:.1f}) nearest={min(t1, t2):.1f}")
