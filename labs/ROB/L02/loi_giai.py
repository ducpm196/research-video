import sys, math
s = sys.stdin.read().strip() or "0.2 2000 15.0 2.0"
ds, ts, dist_s, ang_s = s.split()
D, ticks, dist, ang = float(ds), int(ts), float(dist_s), float(ang_s)
mm_per_tick = math.pi * D * 1000.0 / ticks
lat_err = dist * math.sin(math.radians(ang))
print(f"mm_per_tick={mm_per_tick:.3f} lateral_err_15m={lat_err:.3f}m")
