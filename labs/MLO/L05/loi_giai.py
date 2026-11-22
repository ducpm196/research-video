x, std = 80.0, 10.0
z_train = (x - 55.0) / std
z_serve = (x - 65.0) / std
print(f"z_train={z_train:.1f} z_serve_skew={z_serve:.1f}")
