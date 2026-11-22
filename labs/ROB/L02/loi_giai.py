import math
mm_per_tick = math.pi * 0.2 * 1000.0 / 2000.0
lat_err = 15.0 * math.sin(math.radians(2.0))
print(f"mm_per_tick={mm_per_tick:.3f} lateral_err_15m={lat_err:.3f}m")
