import sys
from math import cos, sin, acos, atan2, degrees
s = sys.stdin.read().strip() or "1.0 1.0 1.2 0.9"
L1, L2, x, y = map(float, s.split())
raw_c2 = (x*x + y*y - L1*L1 - L2*L2) / (2.0 * L1 * L2)
c2 = max(-1.0, min(1.0, raw_c2))
def solve(sgn):
    t2 = sgn * acos(c2)
    return atan2(y, x) - atan2(L2*sin(t2), L1 + L2*cos(t2)), t2
sols = [solve(1), solve(-1)]
ok = abs(raw_c2) <= 1.0 + 1e-9 and all(abs(L1*cos(a)+L2*cos(a+b)-x) < 1e-9 and abs(L1*sin(a)+L2*sin(a+b)-y) < 1e-9 for a, b in sols)
deg = lambda a, b: (round(degrees(a), 2), round(degrees(b), 2))
print(f"down={deg(*sols[0])} up={deg(*sols[1])} fk_match={int(ok)}")
