import sys
s = sys.stdin.read().strip() or "2.0 1.6 0.25"
v, a, td = map(float, s.split())
d_stop = (v * v) / (2.0 * a) + v * td
print(f"stop_dist_m={d_stop:.3f}")
