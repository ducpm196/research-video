import sys

parts = sys.stdin.read().split()
c = float(parts[0]) / 255.0
right_lin = float(parts[1])
wrong_lin = c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
c_out = 12.92 * right_lin if right_lin <= 0.0031308 else (1.055 * (right_lin ** (1.0 / 2.4)) - 0.055)
right_srgb = round(c_out * 255.0)
print(f"wrong_lin={wrong_lin:.3f} right_srgb={right_srgb}")
