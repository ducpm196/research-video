import sys
kv = {k: float(v) for k, v in (t.split('=') for t in sys.stdin.read().split())}
x, y, z, h = kv['x'], kv['y'], kv['z'], kv['h']
q = x + y; f = q * z
dx, dy, dz = z, z, q
num_x = (((x + h) + y) * z - ((x - h) + y) * z) / (2 * h)
print(f"f={f:.1f} dx={dx:.1f} dy={dy:.1f} dz={dz:.1f}")
print(f"dx={dx:.1f} num_x={num_x:.6f}")
print(f"diff={abs(dx - num_x):.2e}")
