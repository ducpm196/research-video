proj = lambda x, y, z, f=1.0: (round(f*x/z, 2), round(f*y/z, 2))
z0, z1, u0, u1, t = 3.0, 9.0, 0.0, 1.0, 0.5
num = (1 - t) * (u0 / z0) + t * (u1 / z1)
den = (1 - t) * (1.0 / z0) + t * (1.0 / z1)
print(f"at_z5={proj(4,2,5)} at_z10={proj(4,2,10)} persp_u={num/den:.3f}")
