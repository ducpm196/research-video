import math
ucb = lambda w, n, N: (w / n) + math.sqrt(2.0 * math.log(N) / n)
ua, ub = ucb(9, 12, 16), ucb(2, 4, 16)
print(f"ucb_A={ua:.4f} ucb_B={ub:.4f}")
print(f"pick={'B' if ub > ua else 'A'}")
