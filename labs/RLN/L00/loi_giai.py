import sys
s = sys.stdin.read().strip() or "0.8|0,5,10"
gs, rs = s.split("|")
g = float(gs); rewards = [float(x) for x in rs.split(",")]
g_inf = 1.0 / (1.0 - g)
g_fin = sum((g ** t) * r for t, r in enumerate(rewards))
print(f"G_inf={g_inf:.1f} G_0_5_10={g_fin:.1f}")
