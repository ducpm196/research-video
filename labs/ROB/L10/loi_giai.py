import sys
s = sys.stdin.read().strip() or "2.5 0.75"
L, e = map(float, s.split())
curv = 2.0 * e / (L * L)
radius = 1.0 / curv
print(f"curvature={curv:.2f} radius={radius:.2f}m")
