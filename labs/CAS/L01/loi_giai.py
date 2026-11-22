scale = 1 << 23
err_tick = 0.1 - int(0.1 * scale) / scale
d50 = err_tick * (50 * 3600 * 10)
d100 = err_tick * (100 * 3600 * 10)
print(f"drift_50h={d50:.4f} drift_100h={d100:.4f}")
