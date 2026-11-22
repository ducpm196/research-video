f, cx, cy = 600.0, 400.0, 300.0
X, Y, Z = 0.6, 0.3, 3.0
u = f * (X / Z) + cx
v = f * (Y / Z) + cy
print(f"pixel_u={u:.0f} pixel_v={v:.0f}")
