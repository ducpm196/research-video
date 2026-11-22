pts = [(3.0, 4.0), (5.0, 0.0), (-3.0, -4.0), (0.0, 5.0)]
u = (0.6, 0.8)
z = [x * u[0] + y * u[1] for x, y in pts]
mse = sum((x - zi * u[0]) ** 2 + (y - zi * u[1]) ** 2 for (x, y), zi in zip(pts, z)) / len(pts)
print(f"latent={[round(v, 3) for v in z]}")
print(f"recon_mse={mse:.4f}")
