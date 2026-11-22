from math import cos, sin, acos, atan2, degrees
L1, L2, x, y = 1.0, 1.0, 1.2, 0.9
c2 = (x*x + y*y - L1*L1 - L2*L2) / (2.0 * L1 * L2)
def solve(s):
    t2 = s * acos(c2)
    return atan2(y, x) - atan2(L2*sin(t2), L1 + L2*cos(t2)), t2
sols = [solve(1), solve(-1)]
ok = all(abs(L1*cos(a)+L2*cos(a+b)-x) < 1e-9
         and abs(L1*sin(a)+L2*sin(a+b)-y) < 1e-9 for a, b in sols)
deg = lambda a, b: (round(degrees(a), 2), round(degrees(b), 2))
print(f"down={deg(*sols[0])} up={deg(*sols[1])} fk_match={int(ok)}")
