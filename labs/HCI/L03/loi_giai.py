import sys, math
s = sys.stdin.read().strip() or "0.18 24 4 6"
bs, n_s, g_s, m_s = s.split()
b, n, g, m = float(bs), int(n_s), int(g_s), int(m_s)
t_flat = b * math.log2(n + 1)
t_2lvl = b * math.log2(g + 1) + b * math.log2(m + 1)
print(f"flat_24={t_flat:.3f}s two_level={t_2lvl:.3f}s")
