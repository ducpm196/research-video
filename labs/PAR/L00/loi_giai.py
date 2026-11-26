import sys
s = sys.stdin.read().strip() or "0.80 8"
ps, ns = s.split(); p, N = float(ps), float(ns)
sN = 1.0 / ((1.0 - p) + p / N)
s_inf = 1.0 / (1.0 - p)
print(f"amdahl_8={sN:.2f}x max_limit={s_inf:.1f}x")
