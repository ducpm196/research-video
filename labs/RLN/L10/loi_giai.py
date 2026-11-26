import sys, math
s = sys.stdin.read().strip() or "1.5 3.0 0.2 0.9 0.3"
diff, r_raw, beta, pi, pref = map(float, s.split())
p = 1.0 / (1.0 + math.exp(-diff))
loss = -math.log(p)
pen_r = r_raw - beta * math.log(pi / pref)
print(f"prob={p:.3f} loss={loss:.3f} kl_adj_r={pen_r:.3f}")
