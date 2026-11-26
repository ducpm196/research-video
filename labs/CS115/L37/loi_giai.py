import sys
kv = dict(t.split('=') for t in sys.stdin.read().split())
pts = [tuple(float(v) for v in p.split(':')) for p in kv['pts'].split(',')]
u = tuple(float(v) for v in kv['u'].split(','))
z = [x * u[0] + y * u[1] for x, y in pts]
mse = sum((x - zi * u[0]) ** 2 + (y - zi * u[1]) ** 2 for (x, y), zi in zip(pts, z)) / len(pts)
print(f"latent={[round(v, 3) for v in z]}")
print(f"recon_mse={mse:.4f}")
