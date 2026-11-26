import sys, math
s = sys.stdin.read().strip() or "1.0 0.05 20"
xs, hs, ns = s.split()
x0, h, steps = float(xs), float(hs), int(ns)
x = x0
for _ in range(steps): x += h * (-2.0 * x)
exact = x0 * math.exp(-2.0 * h * steps)
print(f"euler={x:.4f} exact={exact:.4f} err={abs(x - exact):.4f}")
