x, y, z = -3.0, 7.0, -5.0
q = x + y
f = q * z
dx, dy, dz = z, z, q
h = 1e-5
num_x = (((x + h) + y) * z - ((x - h) + y) * z) / (2 * h)
print(f"f={f:.1f} dx={dx:.1f} dy={dy:.1f} dz={dz:.1f}")
print(f"dx={dx:.1f} num_x={num_x:.6f}")
print(f"diff={abs(dx - num_x):.2e}")
