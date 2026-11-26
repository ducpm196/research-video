import sys
s = sys.stdin.read().strip() or "600.0 400.0 300.0 0.6 0.3 3.0"
f, cx, cy, X, Y, Z = map(float, s.split())
u = f * (X / Z) + cx; v = f * (Y / Z) + cy
print(f"pixel_u={u:.0f} pixel_v={v:.0f}")
