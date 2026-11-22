c = 160.0 / 255.0
lin_wrong = c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
right_lin = 0.25
right_srgb = round((1.055 * (right_lin ** (1.0 / 2.4)) - 0.055) * 255.0)
print(f"wrong_lin={lin_wrong:.3f} right_srgb={right_srgb}")
