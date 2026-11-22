n = (0.0, 0.6, 0.8); l = (0.0, 0.8, 0.6)
n_dot_l = max(0.0, sum(a * b for a, b in zip(n, l)))
spec64 = 0.95 ** 64
spec128 = 0.95 ** 128
print(f"diffuse={n_dot_l:.2f} spec_s64={spec64:.4f} spec_s128={spec128:.4f}")
