import sys
s = sys.stdin.read().strip() or "8.0 0.30 0.05 10"
ls, hds, hcs, ns = s.split()
lam, hd, hc, steps = float(ls), float(hds), float(hcs), int(ns)
run = lambda h: (1.0 - lam * h) ** steps
print(f"g_030={1.0 - lam*hd:.2f} x10_div={run(hd):.2f} x10_conv={run(hc):.5f}")
