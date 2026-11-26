import sys
s = sys.stdin.read().strip() or "142 0.05 132 20.0 30.0"
d4_s, p4_s, d5_s, v1_s, v2_s = s.split()
d4, p4, d5, v1, v2 = float(d4_s), float(p4_s), int(d5_s), float(v1_s), float(v2_s)
stop_d = lambda mph: (v := mph * 0.44704) * 0.2 + (v ** 2) / 8.0
ratio_dist = stop_d(v2) / stop_d(v1)
print(f"mi_2004={d4 * p4:.1f} mi_2005={d5} stop_ratio={ratio_dist:.2f}x")
