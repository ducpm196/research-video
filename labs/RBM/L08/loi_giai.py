import sys, math
s = sys.stdin.read().strip() or "1.0 0.2 5"
xs, hs, ns = s.split()
x0, h, steps = float(xs), float(hs), int(ns)
x_e, x_r = x0, x0
for _ in range(steps):
    x_e += h * (-x_e)
    k1 = -x_r; k2 = -(x_r + 0.5*h*k1); k3 = -(x_r + 0.5*h*k2); k4 = -(x_r + h*k3)
    x_r += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
exact = x0 * math.exp(-h * steps)
e_e, e_r = abs(x_e - exact), abs(x_r - exact)
print(f"err_euler={e_e:.4f} err_rk4={e_r:.2e} gain={e_e/e_r:.0f}x")
