import sys
s = sys.stdin.read().strip() or "4 2 5 10 1.0|3.0 9.0 0.0 1.0 0.5"
p_s, i_s = s.split("|")
x, y, zA, zB, f = map(float, p_s.split())
z0, z1, u0, u1, t = map(float, i_s.split())
proj = lambda z: (round(f*x/z, 2), round(f*y/z, 2))
num = (1 - t) * (u0 / z0) + t * (u1 / z1)
den = (1 - t) * (1.0 / z0) + t * (1.0 / z1)
print(f"at_z5={proj(zA)} at_z10={proj(zB)} persp_u={num/den:.3f}")
