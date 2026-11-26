import sys, math
s = sys.stdin.read().strip() or "0.0 1.0 -6.0 -5.0"
a00, a01, a10, a11 = map(float, s.split())
tr = a00 + a11
det = a00 * a11 - a01 * a10
disc = math.sqrt(tr * tr - 4.0 * det)
l1, l2 = (tr + disc) / 2.0, (tr - disc) / 2.0
print(f"eigs=({l1:.1f}, {l2:.1f}) stable={int(l1 < 0 and l2 < 0)}")
